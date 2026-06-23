#!/usr/bin/env python3
"""Render this storefront's templates with operator config (deploy-time).

Factory-emitted. The factory already substituted the business-content
({{SPEC:...}}) placeholders at build time; this script fills the remaining
operator-secret placeholders ({{OPERATOR_EMAIL}}, {{STRIPE_CHECKOUT_URL}})
at deploy time, from env vars (preferred) or .local/config.env.

Real values never enter git: .local/ is gitignored; placeholders without
values are left untouched (warning printed) so you can render incrementally
(e.g. email set, Stripe URL added later).

Usage:
    python3 render.py
    OPERATOR_EMAIL=... STRIPE_CHECKOUT_URL=... python3 render.py
"""

import os
import shutil
import sys
from pathlib import Path

STOREFRONT_DIR = Path(__file__).resolve().parent
DIST_DIR = STOREFRONT_DIR / ".local" / "dist"
CONFIG_FILE = STOREFRONT_DIR / ".local" / "config.env"

KEYS = ["OPERATOR_EMAIL", "STRIPE_CHECKOUT_URL"]
RENDER_EXTS = {".md", ".html"}
SKIP_DIRS = {".local", ".git"}
SKIP_FILES = {"render.py", "config.env.example"}


def load_config():
    cfg = {}
    if CONFIG_FILE.exists():
        for line in CONFIG_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            cfg[k.strip()] = v.strip().strip('"').strip("'")
    for k in KEYS:
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    missing = [k for k in KEYS if not cfg.get(k)]
    if missing:
        print(
            f"WARN: missing config: {', '.join(missing)} - placeholders left untouched",
            file=sys.stderr,
        )
    return cfg


def render_text(text, cfg):
    for k in KEYS:
        if cfg.get(k):
            text = text.replace("{{" + k + "}}", cfg[k])
    return text


def main():
    cfg = load_config()
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    rendered = 0
    copied = 0
    for src in STOREFRONT_DIR.rglob("*"):
        rel = src.relative_to(STOREFRONT_DIR)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if src.name in SKIP_FILES:
            continue
        if src.is_dir():
            continue
        dst = DIST_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in RENDER_EXTS:
            dst.write_text(render_text(src.read_text(), cfg))
            rendered += 1
        else:
            shutil.copy2(src, dst)
            copied += 1

    print(f"Rendered {rendered} templated + copied {copied} files to {DIST_DIR}")


if __name__ == "__main__":
    main()
