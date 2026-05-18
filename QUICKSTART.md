# Quickstart

> **5-minute path from clone to first agent invocation.** For early-access testers and eventually for public users. Honest about current scope.

## Prerequisites

1. **Claude Code installed.** [docs](https://docs.claude.com/en/docs/claude-code). The terminal CLI, not the web app.
2. **Anthropic API key set.** `export ANTHROPIC_API_KEY=sk-ant-...` in your shell.
3. **gh CLI installed.** Optional but recommended for cloning private repos.

Verify both:

```bash
claude --version       # should print a version
echo $ANTHROPIC_API_KEY # should not be empty
```

## Step 1: Clone

```bash
gh repo clone holbizmetrics/verifiable-autonomy
cd verifiable-autonomy
```

(Or `git clone` with HTTPS if you have repo access without `gh`.)

## Step 2: Pick an agent

Currently shipped: **B-1 customer-interviewer**. That is the only agent ready for outside use. A-track agents (closeout-auto, phase-transition-auto) live in the research lab `prometheus-crystal-lab-auto`, not here.

```bash
cd agents/b1-customer-interviewer/
ls
```

You should see `README.md`, `icp-template.md`, `prospects-template.md`, `falsifier.md`, plus the agent's runtime directories (drafts/, replies/, test-fixtures/).

## Step 3: Fill in your ICP and prospects

```bash
cp icp-template.md icp.md
cp prospects-template.md prospects.md
```

Edit both. Replace every `[fill this in]` placeholder with real substrate from your own customer-discovery work. The agent's draft quality is upper-bounded by these two files; vague inputs produce generic drafts the agent will refuse to emit.

Em-dash hygiene matters: see the note at `icp-template.md` L33. Phrases B-1 cites verbatim should not contain em-dashes (AI-text tell in outgoing mail).

## Step 4: Invoke B-1

From the repo root, launch Claude Code:

```bash
cd ../..
claude
```

Then in the Claude Code session, ask the B-1 subagent to draft:

```
/agents b1-customer-interviewer draft 5
```

(Or invoke from a parent conversation via the Task tool with `subagent_type: "b1-customer-interviewer"` and prompt `"draft 5"`.)

B-1 will read `icp.md` + `prospects.md`, draft 5 personalized outreach emails to `drafts/<prospect_id>.md`, and append records to `interview-log.jsonl`. If a prospect row lacks a verbatim substrate snippet, B-1 will skip with `PROSPECT_THIN` rather than fabricate.

## Step 5: Review and send manually

Read each draft. Verify the cited phrases. Send from your own email client. B-1 does not send.

Full flow including reply classification: `agents/b1-customer-interviewer/README.md`.

## What you should and should not expect

**Will work:**
- Drafts that cite your real ICP phrases verbatim and your prospect's real substrate verbatim.
- Append-only audit log you can `tail -f` or `jq` to verify every action.
- Surface-Compliance refusal on thin substrate (skip with code, not fabricate).

**Will not work yet:**
- No SMTP integration. No auto-send. No cron.
- No multi-campaign UI.
- No hosted version. Runs only in your local Claude Code.
- No A-track autonomy. Those are private to the research lab until the manifesto's 2-track-flip gate clears.

## If something breaks

- Open an issue on the repo (early-access testers: DM the operator who invited you).
- Include the relevant `interview-log.jsonl` entries if the failure was inside B-1.
- Do not paste real prospect data into a public issue.

---

*Quickstart v1, S55 (2026-05-18). Updates when invocation flow changes or new agents ship.*
