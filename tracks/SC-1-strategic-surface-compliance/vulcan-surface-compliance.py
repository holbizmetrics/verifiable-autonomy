#!/usr/bin/env python3
"""SC-1 — Strategic Surface-Compliance Gate (verifiable-autonomy track).

A Claude Code `Stop` hook that refuses to let a turn close while it asserts work the
turn's own tool calls did not back. Strategic-layer analogue of the execution-layer gate
that "refuses to emit a record with zero artifact reads behind it."

DESIGN (inverted): the leaky part of the naive design is detecting "a claim" in free text.
So the gate does NOT fire on every "done". It fires on the high-precision triad:

    mutation (Edit/Write/NotebookEdit)  AND  success-claim  AND  no verification this turn

plus a secondary derivation check (asserts "I read X" with no Read/Grep/Glob this turn).

ASYMMETRIC LOSS: a false positive traps a turn -> the operator disables the gate (fatal).
A false negative is backstopped by the next-boot Mirror (tolerable). Therefore: maximize
precision, accept low recall, FAIL OPEN in every branch, and loop-guard so a block can
never trap a turn.

Emits one append-only JSONL audit record per turn checked (discipline #3 shape), so the
verdict is `tail | jq`-able without trusting the agent's narrative.

Env overrides (test/lab only): VULCAN_SC_AUDIT (audit log path).
"""
from __future__ import annotations

import json
import os
import re
import sys
from typing import Any

# --- High-precision pattern sets (assertion form; kept deliberately narrow) ---------

# Success assertions. Word-boundary anchored; matched against the assistant turn text.
SUCCESS = re.compile(
    r"\b(it works|works now|tests? pass(?:ing|ed|es)?|all green|now green|"
    r"verified|confirmed working|done|fixed|complete(?:d)?|shipped|"
    r"ready to (?:ship|go)|good to go)\b",
    re.IGNORECASE,
)

# Derivation assertions ("I read X / per the file / according to ...").
DERIVATION = re.compile(
    r"\b(i read|i've read|i checked|i inspected|per the (?:file|code|source)|"
    r"according to the (?:file|code)|the file says|as the code shows)\b",
    re.IGNORECASE,
)

# Negation / hedge tokens that, near a match, disqualify it (avoid false positives on
# "not done", "isn't fixed", "almost done", and questions).
NEGATION = re.compile(
    r"\b(not|n't|isn't|aren't|wasn't|haven't|hasn't|no longer|almost|nearly|"
    r"once|after|when|if|until|need to|still need|not yet|todo|to do)\b",
    re.IGNORECASE,
)

MUTATION_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
READ_TOOLS = {"Read", "Grep", "Glob"}

# A success claim only demands verification when CODE changed. A "done" after writing a
# doc/note/config has nothing to test/build, so requiring a verify-command there is a false
# positive -- and a false positive (which traps a turn) is the fatal loss this gate is tuned
# against. So the success rule fires only on mutations to code-like files.
CODE_EXTS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs", ".java", ".kt",
    ".kts", ".c", ".cc", ".cpp", ".h", ".hpp", ".rb", ".php", ".swift", ".scala", ".cs",
    ".m", ".mm", ".sql", ".sh", ".bash", ".zsh",
}

# Bash commands that count as verification (test/build/lint/typecheck).
# F2: matching the command is necessary but not sufficient — the command's tool_result
# must also be explicitly present with is_error False (see _passed_verify).
VERIFY_CMD = re.compile(
    r"\b(pytest|unittest|npm (?:run )?test|yarn test|jest|vitest|cargo (?:test|build|check)|"
    r"go test|go build|make(?:\s|$)|tsc|mypy|ruff|eslint|flake8|gradle|mvn|"
    r"npm run build|next build|vite build|cmake|ctest|bats)\b",
    re.IGNORECASE,
)

# F1: extensions that make a token in assistant text look like a referenced file.
REF_EXTS = CODE_EXTS | {
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".xml", ".html", ".css", ".csv", ".lock", ".env", ".ipynb",
}

# Filename-looking tokens in prose ("config.py", "settings.json"). Extension is then
# checked against REF_EXTS so "e.g" / "v2.0" style tokens never enter the relevant set
# (a spurious referenced-file would tighten F1 into a false-positive source).
FILENAME = re.compile(r"\b[\w.-]+\.[A-Za-z]\w*\b")


def allow() -> None:
    sys.exit(0)


def block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def _text_of(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def _tool_uses(content: Any) -> list[dict[str, Any]]:
    if not isinstance(content, list):
        return []
    return [
        {"name": b.get("name", ""), "input": b.get("input", {}) or {}, "id": b.get("id", "")}
        for b in content
        if isinstance(b, dict) and b.get("type") == "tool_use"
    ]


def _is_real_user_message(ev: dict[str, Any]) -> bool:
    """A genuine user turn (text), not a tool_result echoed back as a user message."""
    if ev.get("type") not in ("user", None) and ev.get("role") != "user":
        return False
    if ev.get("type") == "user" or ev.get("role") == "user":
        msg = ev.get("message", ev)
        content = msg.get("content") if isinstance(msg, dict) else None
        if isinstance(content, list):
            # tool_result blocks are not a real user turn boundary
            if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
                return False
            return any(isinstance(b, dict) and b.get("type") == "text" for b in content)
        return bool(isinstance(content, str) and content.strip())
    return False


def _tool_results(content: Any) -> dict[str, bool]:
    """Map tool_use_id -> failed?, read from tool_result blocks. failed = is_error truthy.
    These blocks ride in the tool-result-only user messages within the turn window."""
    out: dict[str, bool] = {}
    if not isinstance(content, list):
        return out
    for b in content:
        if isinstance(b, dict) and b.get("type") == "tool_result":
            tuid = b.get("tool_use_id", "")
            if tuid:
                out[tuid] = bool(b.get("is_error"))
    return out


def parse_last_turn(transcript_path: str) -> tuple[str, list[dict[str, Any]], dict[str, bool]]:
    """Return (assistant_text, tool_uses, results) for the turn since the last real user
    message. `results` maps tool_use_id -> failed_bool (True iff the result carried
    is_error); a tool with no captured result is simply absent (= unknown)."""
    events: list[dict[str, Any]] = []
    with open(transcript_path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except Exception:
                continue
    # Find the last real user message; the turn is everything after it.
    start = 0
    for i in range(len(events) - 1, -1, -1):
        if _is_real_user_message(events[i]):
            start = i + 1
            break
    text_parts: list[str] = []
    tools: list[dict[str, Any]] = []
    results: dict[str, bool] = {}
    for ev in events[start:]:
        msg = ev.get("message", ev)
        content = msg.get("content") if isinstance(msg, dict) else None
        if ev.get("type") == "assistant" or ev.get("role") == "assistant":
            text_parts.append(_text_of(content))
            tools.extend(_tool_uses(content))
        try:
            results.update(_tool_results(content))
        except Exception:
            pass  # fail open: an unreadable result just leaves that tool unknown
    return " ".join(p for p in text_parts if p), tools, results


def _matches_unnegated(pattern: re.Pattern[str], text: str) -> bool:
    """True iff `pattern` matches a span with no negation/hedge in its local window and
    the containing sentence is not a question. Conservative: precision over recall."""
    for m in pattern.finditer(text):
        lo = max(0, m.start() - 45)
        window = text[lo:m.end() + 5]
        if NEGATION.search(window):
            continue
        # crude sentence end: nearest '.', '!' or '?' after the match
        tail = text[m.end():m.end() + 120]
        nxt_q = tail.find("?")
        nxt_dot = min([p for p in (tail.find("."), tail.find("!")) if p != -1] or [10**9])
        if nxt_q != -1 and nxt_q < nxt_dot:
            continue  # the assertion is inside a question
        return True
    return False


def _mutated_code(tools: list[dict[str, Any]]) -> bool:
    """True iff this turn edited at least one code-like file (by extension)."""
    for t in tools:
        if t["name"] in MUTATION_TOOLS:
            path = t["input"].get("file_path") or t["input"].get("notebook_path") or ""
            _, ext = os.path.splitext(str(path))
            if ext.lower() in CODE_EXTS:
                return True
    return False


def _passed_verify(tools: list[dict[str, Any]], results: dict[str, bool]) -> bool:
    """True iff a verify command (test/build/lint) RAN and explicitly did NOT error.

    F2: a verify command counts only when its result is present with is_error False.
    A missing/unknown result contributes NOTHING — it is never inferred as passed (that
    would re-open the 'ran = verified' hole) nor as failed (that could trap a turn whose
    result has not landed). Fail-open: uncertainty falls through to read_back."""
    for t in tools:
        if t["name"] == "Bash" and VERIFY_CMD.search(str(t["input"].get("command", ""))):
            if results.get(t.get("id", "")) is False:  # ran AND explicitly did not error
                return True
    return False


# A filename-like token in prose (config.py, NOTES.md). Extension is 2-8 letters, which
# excludes prose false hits like "e.g"/"i.e" (1-char) and version numbers ("3.11").
_FILE_TOKEN = re.compile(r"\b[\w./-]+\.[A-Za-z]{2,8}\b")


def _read_backs_derivation(assistant_text: str, tools: list[dict[str, Any]]) -> bool:
    """F1: a read backs an 'I read X' claim only if it plausibly touches the file the
    claim NAMES. A path-less (repo-wide) search counts, and if the claim names no file
    we fall back to 'any read counts' — F1 is a recall gap, never a false-positive source,
    so every uncertain case resolves toward backing (no block)."""
    reads = [t for t in tools if t["name"] in READ_TOOLS]
    if not reads:
        return False
    read_bases: set[str] = set()
    for t in reads:
        rp = t["input"].get("file_path") or t["input"].get("path") or ""
        if not rp:
            return True  # repo-wide grep/glob: plausibly covers the named file
        read_bases.add(os.path.basename(str(rp)))
    # A read whose filename STEM is named in the prose (e.g. "the config" + a Read of
    # config.py) backs the claim even if an extensioned token elsewhere differs. Without
    # this, a loosely-named referent ("the config") plus a name-dropped file ("README.md")
    # would false-block a turn that really did read the right file. Stem >= 3 chars to avoid
    # spurious 1-2 char hits (that only costs recall, never a false block).
    for base in read_bases:
        stem = os.path.splitext(base)[0]
        if len(stem) >= 3 and re.search(r"\b" + re.escape(stem) + r"\b", assistant_text, re.IGNORECASE):
            return True
    referenced = {os.path.basename(m) for m in _FILE_TOKEN.findall(assistant_text)}
    if not referenced:
        return True  # claim names no specific file -> any read counts (prior behavior)
    return bool(referenced & read_bases)


def evaluate(
    assistant_text: str,
    tools: list[dict[str, Any]],
    results: dict[str, bool] | None = None,
) -> tuple[str, str]:
    """Return (verdict, reason_code). verdict in {'pass','block'}."""
    results = results or {}
    names = [t["name"] for t in tools]
    mutated = _mutated_code(tools)
    read_back = any(n in READ_TOOLS for n in names)
    # F2: a verify command backs a success claim only if it PASSED (result seen, no error);
    # read_back remains the softer fallback (avoids false positives on grep-the-call-sites).
    verified = _passed_verify(tools, results) or read_back

    success_claim = _matches_unnegated(SUCCESS, assistant_text)
    derivation_claim = _matches_unnegated(DERIVATION, assistant_text)

    # Primary inverted rule: changed something, claimed success, ran no verification.
    if mutated and success_claim and not verified:
        return "block", "mutation_success_unverified"
    # Secondary: asserted a read, but no read this turn touches the file the claim names.
    if derivation_claim and not _read_backs_derivation(assistant_text, tools):
        return "block", "derivation_unread"
    return "pass", "clean"


def write_audit(record: dict[str, Any]) -> None:
    path = os.environ.get(
        "VULCAN_SC_AUDIT",
        os.path.join(os.path.expanduser("~"), ".claude", "vulcan-surface-compliance.jsonl"),
    )
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as fh:
            fh.write(json.dumps(record) + "\n")
    except Exception:
        pass  # audit failure must never block or crash the turn


REASONS = {
    "mutation_success_unverified": (
        "SC-1 (surface-compliance): this turn edited files and asserts success, but ran no "
        "test/build/lint and no read-back. You are cleared to verify now — the turn stays "
        "open for it. Run the real check, OR downgrade the claim to its true scope "
        "(e.g. 'edited, NOT yet verified'). Then close."
    ),
    "derivation_unread": (
        "SC-1 (surface-compliance): this turn asserts 'I read / per the file' but ran no "
        "Read/Grep/Glob. Read the artifact now (the turn stays open), or downgrade the "
        "claim to what you actually checked. Then close."
    ),
}


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict):
            allow()
    except Exception:
        allow()

    if data.get("stop_hook_active"):
        allow()  # loop guard: a block can never trap a turn

    tpath = os.path.expanduser(data.get("transcript_path", "") or "")
    if not tpath or not os.path.exists(tpath):
        allow()

    try:
        assistant_text, tools, results = parse_last_turn(tpath)
    except Exception:
        allow()  # fail open

    verdict, reason_code = evaluate(assistant_text, tools, results)
    write_audit(
        {
            "session": data.get("session_id", ""),
            "tool_calls_this_turn": [t["name"] for t in tools],
            "verdict": verdict,
            "reason_code": reason_code,
            "text_excerpt": assistant_text[:160],
        }
    )

    if verdict == "block":
        block(REASONS.get(reason_code, "SC-1: unbacked claim; verify or downgrade."))
    allow()


if __name__ == "__main__":
    main()
