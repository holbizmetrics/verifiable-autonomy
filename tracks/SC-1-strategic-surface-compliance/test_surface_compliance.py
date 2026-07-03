#!/usr/bin/env python3
"""End-to-end tests for SC-1. Builds fixture transcripts, feeds the hook real Stop
payloads on stdin, asserts the block/allow verdict. Run: python3 test_surface_compliance.py
(also pytest-compatible). Exits non-zero if any case fails."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vulcan-surface-compliance.py")


def _msg(role: str, blocks: list[dict]) -> str:
    return json.dumps({"type": role, "message": {"role": role, "content": blocks}})


def _transcript(user_text: str, tool_uses: list[dict], assistant_text: str) -> str:
    """Write a JSONL transcript: one user turn, an assistant turn with tool_uses + text,
    then (if any tool carries a "result") a tool_result-only user message — mirroring how
    Claude Code delivers tool outputs. A tool dict may set "result": "ok" | "fail" to emit
    a tool_result with is_error accordingly; omit it to leave the result UNKNOWN."""
    content: list[dict] = []
    result_blocks: list[dict] = []
    for i, t in enumerate(tool_uses):
        tid = f"t{i}"
        content.append({"type": "tool_use", "name": t["name"], "input": t.get("input", {}), "id": tid})
        if "result" in t:
            result_blocks.append({
                "type": "tool_result", "tool_use_id": tid,
                "is_error": t["result"] == "fail",
                "content": "Exit code 1" if t["result"] == "fail" else "ok",
            })
    content.append({"type": "text", "text": assistant_text})
    lines = [
        _msg("user", [{"type": "text", "text": user_text}]),
        _msg("assistant", content),
    ]
    if result_blocks:
        lines.append(_msg("user", result_blocks))
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def run_hook(payload: dict, audit: str) -> str:
    env = dict(os.environ, VULCAN_SC_AUDIT=audit)
    p = subprocess.run(["python3", HOOK], input=json.dumps(payload),
                       capture_output=True, text=True, env=env)
    assert p.returncode == 0, f"hook must always exit 0; got {p.returncode}, stderr={p.stderr}"
    return p.stdout.strip()


def _verdict(stdout: str) -> str:
    if not stdout:
        return "allow"
    try:
        return json.loads(stdout).get("decision", "allow")
    except Exception:
        return "allow"


# --- cases: (name, tool_uses, assistant_text, expected_verdict) ----------------------
EDIT = {"name": "Edit", "input": {"file_path": "x.py"}}
WRITE = {"name": "Write", "input": {"file_path": "x.py"}}
WRITE_DOC = {"name": "Write", "input": {"file_path": "NOTES.md"}}
PYTEST = {"name": "Bash", "input": {"command": "python3 -m pytest -q"}}          # result UNKNOWN
PYTEST_OK = {"name": "Bash", "input": {"command": "python3 -m pytest -q"}, "result": "ok"}
PYTEST_FAIL = {"name": "Bash", "input": {"command": "python3 -m pytest -q"}, "result": "fail"}
READ = {"name": "Read", "input": {"file_path": "x.py"}}
READ_OTHER = {"name": "Read", "input": {"file_path": "other.py"}}

CASES = [
    ("mutation+success+noverify -> block", [EDIT], "Done. It works now.", "block"),
    # F2: a verify command backs the claim only if its result is present AND passed.
    ("mutation+success+pytest PASSED -> allow", [EDIT, PYTEST_OK], "Done, all tests pass.", "allow"),
    ("F2: verify RAN but FAILED, no readback -> block", [EDIT, PYTEST_FAIL], "Done, tests green.", "block"),
    ("F2: verify result UNKNOWN, no readback -> block", [EDIT, PYTEST], "Done, tests green.", "block"),
    ("F2: verify UNKNOWN but readback present -> allow", [EDIT, PYTEST, READ], "Fixed.", "allow"),
    ("mutation+success+readback -> allow", [WRITE, READ], "Fixed and verified.", "allow"),
    # F3 fix: a "done" after writing a doc/note has nothing to test -> requiring a verify
    # command there is the fatal false positive. Code-only scoping makes this allow.
    ("doc mutation + success + noverify -> allow", [WRITE_DOC], "Done, drafted the notes.", "allow"),
    ("derivation+noread -> block", [], "I read config.py and it sets DEBUG=true.", "block"),
    # F1: the read must touch the file the claim NAMES.
    ("derivation+read of named file -> allow", [READ], "I read x.py; DEBUG=true.", "allow"),
    ("F1: derivation + read of UNRELATED file -> block", [READ_OTHER], "I read config.py; DEBUG=true.", "block"),
    ("conversational done, no mutation -> allow", [], "Done — what do you want next?", "allow"),
    ("negated success + mutation -> allow", [EDIT], "Not done yet, still need to verify.", "allow"),
    ("success inside a question -> allow", [EDIT], "Is it done? Let me check.", "allow"),
]


def _check(name, tools, text, expected) -> None:
    audit = tempfile.mkstemp(suffix=".jsonl")[1]
    tpath = _transcript("go", tools, text)
    out = run_hook({"transcript_path": tpath, "session_id": "test"}, audit)
    got = _verdict(out)
    os.unlink(tpath)
    assert got == expected, f"[{name}] expected {expected}, got {got} (stdout={out!r})"


def test_cases() -> None:
    for name, tools, text, expected in CASES:
        _check(name, tools, text, expected)


def test_loop_guard() -> None:
    audit = tempfile.mkstemp(suffix=".jsonl")[1]
    tpath = _transcript("go", [EDIT], "Done, it works.", )
    out = run_hook({"transcript_path": tpath, "session_id": "t", "stop_hook_active": True}, audit)
    os.unlink(tpath)
    assert _verdict(out) == "allow", "stop_hook_active must always allow (loop guard)"


def test_fail_open_bad_payload() -> None:
    audit = tempfile.mkstemp(suffix=".jsonl")[1]
    out = run_hook({"transcript_path": "/nonexistent/path.jsonl"}, audit)
    assert _verdict(out) == "allow", "missing transcript must fail open"


def test_audit_record_written() -> None:
    audit = tempfile.mkstemp(suffix=".jsonl")[1]
    tpath = _transcript("go", [EDIT], "Done, it works.", )
    run_hook({"transcript_path": tpath, "session_id": "auditcheck"}, audit)
    os.unlink(tpath)
    with open(audit) as fh:
        rec = json.loads(fh.readline())
    assert rec["verdict"] == "block" and rec["reason_code"] == "mutation_success_unverified", rec


def main() -> int:
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} test functions passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
