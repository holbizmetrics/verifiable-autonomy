#!/usr/bin/env python3
"""verifiable business factory v0.0.

Compile a business-spec file into a runnable per-business directory.
Each output business is a scaffolded Claude-Code project: per-agent dirs
wired from the agents/ templates, configured to the spec's ICP + offer,
mode defaulting to step, ready to be opened in Claude Code.

Usage:
    python factory/factory.py build factory/specs/verifiable-autonomy.json

Output:
    businesses/<name>/
        OFFER.md
        manifest.json
        README.md
        <agent_id>/
            README.md           (from agent template)
            falsifier.md        (from agent template)
            MODE                (from spec; default: step)
            icp.md              (copied from spec.icp_source)
            prospects.md        (from prospects-template.md; operator fills)
            interview-log.jsonl (empty)
            drafts/             (empty)
            replies/            (empty)
"""

import argparse
import html
import json
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_ROOT = REPO_ROOT / "agents"
TEMPLATES_ROOT = REPO_ROOT / "factory" / "templates"
LOOP_TEMPLATE = TEMPLATES_ROOT / "loop"
FACTORY_VERSION = "0.1"

# Factory-emitted text is always utf-8. Default encoding on Windows is cp1252,
# which mojibakes the templates' non-ASCII (em-dashes etc.) on both read and
# write; pin utf-8 everywhere so a build is byte-identical across platforms.
ENC = "utf-8"

LOOP_RENDER_EXTS = {".md", ".html"}
LOOP_SKIP_NAMES = {"render.py", "config.env.example", "deploy-pages.yml.tmpl"}

PER_INSTANCE_SKIP = {
    "icp.md",
    "prospects.md",
    "interview-log.jsonl",
    "drafts",
    "replies",
    "test-fixtures",
    "test-fixtures-v0.2-paraphrase-exception",
    "OPEN-WORK-paraphrase-exception.md",
    "AMENDMENT-v0.3-DRAFT-falsifier-spec-tightening.md",
    "flip-history.jsonl",
    "MODE",
}


def load_spec(spec_path):
    text = Path(spec_path).read_text(encoding=ENC)
    return json.loads(text)


def scaffold_agent(agent_id, agent_dst, spec):
    template_dir = AGENTS_ROOT / agent_id
    if not template_dir.exists():
        sys.exit(f"REFUSING: agent template not found: {template_dir}")

    agent_dst.mkdir()

    for item in template_dir.iterdir():
        if item.name in PER_INSTANCE_SKIP:
            continue
        if item.is_file():
            shutil.copy2(item, agent_dst / item.name)

    (agent_dst / "drafts").mkdir()
    (agent_dst / "replies").mkdir()
    (agent_dst / "interview-log.jsonl").touch()
    (agent_dst / "flip-history.jsonl").touch()

    mode = spec.get("mode", "step")
    (agent_dst / "MODE").write_text(f"{mode}\n", encoding=ENC)

    icp_source = spec.get("icp_source")
    if icp_source:
        src = REPO_ROOT / icp_source
        if src.exists():
            shutil.copy2(src, agent_dst / "icp.md")
        else:
            print(f"WARN: icp_source not found ({src}); falling back to icp-template.md",
                  file=sys.stderr)
            tmpl = template_dir / "icp-template.md"
            if tmpl.exists():
                shutil.copy2(tmpl, agent_dst / "icp.md")
    else:
        tmpl = template_dir / "icp-template.md"
        if tmpl.exists():
            shutil.copy2(tmpl, agent_dst / "icp.md")

    tmpl = template_dir / "prospects-template.md"
    if tmpl.exists():
        shutil.copy2(tmpl, agent_dst / "prospects.md")

    return {
        "id": agent_id,
        "mode": mode,
        "icp_source": icp_source,
    }


def render_offer(name, offer):
    return (
        f"# Offer — {name}\n\n"
        f"## What it is\n\n{offer.get('paragraph', '[TODO]')}\n\n"
        f"## Price\n\n{offer.get('price', '[TODO]')}\n\n"
        f"## Falsifiable promise\n\n{offer.get('promise', '[TODO]')}\n\n"
        f"---\n\n*Factory-built from spec. Edit in place; do not regenerate over operator edits.*\n"
    )


def render_business_readme(name, agents, has_loop=False):
    agent_list = "\n".join(f"- `{a['id']}/` (mode: {a['mode']})" for a in agents)
    storefront_what = (
        "- `storefront/` — the value->capture loop (landing page, intake, render "
        "script, deploy guide)\n"
        if has_loop
        else ""
    )
    storefront_run = (
        "\n## Deploy the storefront\n\n"
        "The value->capture loop lives in `storefront/`. Business content is baked "
        "in; operator secrets (your email, Stripe) are filled at deploy time by "
        "`storefront/render.py`. See `storefront/OPERATOR-ACTIONS.md` for the deploy "
        "steps (local verify, GitHub Pages, or Cloudflare).\n"
        if has_loop
        else ""
    )
    return (
        f"# {name}\n\n"
        f"Factory-built business instance. Factory version: {FACTORY_VERSION}.\n\n"
        f"## What's in here\n\n"
        f"- `OFFER.md` — the offer (paragraph + price + promise)\n"
        f"- `manifest.json` — what got built from what spec\n"
        f"{storefront_what}"
        f"{agent_list}\n\n"
        f"## How to run\n\n"
        f"Open this directory in Claude Code. The agents live in their own subdirs and inherit "
        f"the verifiable-autonomy MODE-contract discipline.\n"
        f"{storefront_run}\n"
        f"## Mode\n\n"
        f"Agents default to `step` (operator-supervised). Flip per-agent `MODE` file to `auto` "
        f"only per the MODE-CONTRACT in the parent V-A repo.\n"
    )


def _html_list(items):
    """List of strings -> indented <li> lines for a landing-page <ul>."""
    return "\n".join(f"  <li>{html.escape(str(item))}</li>" for item in items)


def _intake_md(loop):
    """Render the intake body.

    Prefers structured loop['intake_fields'] = [{heading, items:[...]}, ...];
    falls back to a flat bullet list from loop['what_you_send'].
    """
    fields = loop.get("intake_fields")
    if fields:
        blocks = []
        for i, field in enumerate(fields, start=1):
            heading = field.get("heading", f"Item {i}")
            items = field.get("items", [])
            bullets = "\n".join(f"- {it}" for it in items)
            blocks.append(f"## {i}. {heading}\n{bullets}".rstrip())
        return "\n\n".join(blocks)
    return "\n".join(f"- {it}" for it in loop.get("what_you_send", []))


def _spec_subs(spec):
    """Build-time {{SPEC:KEY}} substitutions for the loop templates."""
    offer = spec.get("offer", {})
    loop = spec.get("loop", {})
    title = loop.get("title") or spec["name"]
    cta_subject = loop.get("cta_subject") or f"{title} - Request"
    return {
        "BUSINESS_TITLE": title,
        "HEADLINE": loop.get("headline", title),
        "PITCH": loop.get("pitch") or offer.get("paragraph", ""),
        "PRICE": offer.get("price", ""),
        "PROMISE": offer.get("promise", ""),
        "CTA_LABEL": loop.get("cta_label", "Request"),
        "CTA_SUBJECT": quote(cta_subject),
        "WHAT_YOU_SEND_HTML": _html_list(loop.get("what_you_send", [])),
        "WHAT_YOU_GET_HTML": _html_list(loop.get("what_you_get", [])),
        "TURNAROUND": loop.get("turnaround", ""),
        "FOOTER": loop.get("footer", "Delivered async (written, no call)."),
        "REPO_URL": spec.get(
            "repo_url", "https://github.com/holbizmetrics/verifiable-autonomy"
        ),
        "INTAKE_FIELDS_MD": _intake_md(loop),
    }


def _apply_spec_subs(text, subs):
    for key, val in subs.items():
        text = text.replace("{{SPEC:" + key + "}}", val)
    return text


def emit_loop(business_dir, spec):
    """Emit the value->capture storefront (landing + intake + render + deploy
    guide) into business_dir/storefront/, with business content baked in and
    operator secrets ({{OPERATOR_EMAIL}}) left for the storefront's own
    render.py to fill at deploy time."""
    if not LOOP_TEMPLATE.exists():
        sys.exit(f"REFUSING: loop template not found: {LOOP_TEMPLATE}")

    subs = _spec_subs(spec)
    storefront = business_dir / "storefront"
    storefront.mkdir()

    rendered = 0
    copied = 0
    for src in LOOP_TEMPLATE.rglob("*"):
        rel = src.relative_to(LOOP_TEMPLATE)
        if src.is_dir():
            continue
        dst = storefront / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.name not in LOOP_SKIP_NAMES and src.suffix in LOOP_RENDER_EXTS:
            dst.write_text(_apply_spec_subs(src.read_text(encoding=ENC), subs), encoding=ENC)
            rendered += 1
        else:
            shutil.copy2(src, dst)
            copied += 1

    # Surface any unfilled build-time placeholder so a malformed spec is loud,
    # not silently shipped with a {{SPEC:...}} hole in the customer's face.
    holes = []
    for src in storefront.rglob("*"):
        if src.is_file() and src.suffix in LOOP_RENDER_EXTS:
            if "{{SPEC:" in src.read_text(encoding=ENC):
                holes.append(str(src.relative_to(business_dir)))
    if holes:
        print(
            f"WARN: unfilled {{{{SPEC:...}}}} placeholders remain in: {', '.join(holes)}",
            file=sys.stderr,
        )

    return {
        "type": spec.get("loop", {}).get("type", "email-intake"),
        "storefront_files_rendered": rendered,
        "storefront_files_copied": copied,
        "unfilled_placeholders": holes,
    }


def build(spec, output_root):
    name = spec["name"]
    business_dir = Path(output_root) / name

    if business_dir.exists():
        sys.exit(
            f"REFUSING: {business_dir} already exists. Remove or use a different name."
        )

    business_dir.mkdir(parents=True)

    manifest = {
        "factory_version": FACTORY_VERSION,
        "name": name,
        "spec_source": spec.get("_spec_source", ""),
        "agents": [],
    }

    for agent_id in spec.get("agents", []):
        agent_dst = business_dir / agent_id
        manifest["agents"].append(scaffold_agent(agent_id, agent_dst, spec))

    offer = spec.get("offer", {})
    if offer:
        (business_dir / "OFFER.md").write_text(render_offer(name, offer), encoding=ENC)
        manifest["offer_fields_present"] = {
            k: bool(offer.get(k)) for k in ("paragraph", "price", "promise")
        }

    if spec.get("loop"):
        manifest["loop"] = emit_loop(business_dir, spec)

    (business_dir / "README.md").write_text(
        render_business_readme(name, manifest["agents"], has_loop="loop" in manifest),
        encoding=ENC,
    )
    (business_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding=ENC
    )

    print(f"Built: {business_dir}")
    return business_dir


def main():
    parser = argparse.ArgumentParser(description="verifiable business factory v0.0")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build", help="Scaffold a business instance from a spec")
    p_build.add_argument("spec", help="Path to spec file (JSON)")
    p_build.add_argument(
        "--output-root",
        default=str(REPO_ROOT / "businesses"),
        help="Where to write the business dir (default: businesses/ at repo root)",
    )

    args = parser.parse_args()

    if args.cmd == "build":
        spec = load_spec(args.spec)
        spec["_spec_source"] = args.spec
        build(spec, args.output_root)


if __name__ == "__main__":
    main()
