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
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_ROOT = REPO_ROOT / "agents"
FACTORY_VERSION = "0.0"

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
    text = Path(spec_path).read_text()
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
    (agent_dst / "MODE").write_text(f"{mode}\n")

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


def render_business_readme(name, agents):
    agent_list = "\n".join(f"- `{a['id']}/` (mode: {a['mode']})" for a in agents)
    return (
        f"# {name}\n\n"
        f"Factory-built business instance. Factory version: {FACTORY_VERSION}.\n\n"
        f"## What's in here\n\n"
        f"- `OFFER.md` — the offer (paragraph + price + promise)\n"
        f"- `manifest.json` — what got built from what spec\n"
        f"{agent_list}\n\n"
        f"## How to run\n\n"
        f"Open this directory in Claude Code. The agents live in their own subdirs and inherit "
        f"the verifiable-autonomy MODE-contract discipline.\n\n"
        f"## Mode\n\n"
        f"Agents default to `step` (operator-supervised). Flip per-agent `MODE` file to `auto` "
        f"only per the MODE-CONTRACT in the parent V-A repo.\n"
    )


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
        (business_dir / "OFFER.md").write_text(render_offer(name, offer))
        manifest["offer_fields_present"] = {
            k: bool(offer.get(k)) for k in ("paragraph", "price", "promise")
        }

    (business_dir / "README.md").write_text(render_business_readme(name, manifest["agents"]))
    (business_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

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
