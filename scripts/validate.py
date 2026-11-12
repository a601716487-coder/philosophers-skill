#!/usr/bin/env python3
"""Validate the philosophers skill bundle structure and cross-references.

Exit code 0 when the bundle is consistent, 1 otherwise. Used by CI and locally:
  python3 scripts/validate.py
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

LENSES = ["kant", "hegel", "nietzsche", "aristotle", "wittgenstein", "marx", "foucault", "heidegger"]
WORKFLOWS = ["decision", "critique", "concept", "value-audit", "power-map", "postmortem", "writing", "operating-manual"]
TEMPLATES = ["decision-memo", "critique-memo", "concept-note", "council-report"]
LENS_SECTIONS = ["一句话", "核心问题", "可操作工具", "重述句式", "输出模板", "边界与误用"]

errors: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        errors.append(msg)


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    fields: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields


def main() -> int:
    # 1. SKILL.md
    skill = ROOT / "SKILL.md"
    check(skill.exists(), "SKILL.md missing")
    if skill.exists():
        text = read(skill)
        fm = parse_frontmatter(text)
        name = fm.get("name", "")
        check(bool(name), "SKILL.md frontmatter missing 'name'")
        if name:
            check(bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name)), f"skill name '{name}' is not kebab-case")
        check(bool(fm.get("description")), "SKILL.md frontmatter missing 'description'")
        size = len(text.encode("utf-8"))
        check(size < 8192, f"SKILL.md is {size} bytes (>= 8192); tool-result pruning may trim it")

    # 2. references
    for name in LENSES:
        p = ROOT / "references" / f"{name}.md"
        check(p.exists(), f"references/{name}.md missing")
        if p.exists():
            content = read(p)
            for sec in LENS_SECTIONS:
                check(f"## {sec}" in content, f"references/{name}.md missing section '## {sec}'")
    check((ROOT / "references" / "_template.md").exists(), "references/_template.md missing")

    # 3. workflows + templates
    for name in WORKFLOWS:
        check((ROOT / "workflows" / f"{name}.md").exists(), f"workflows/{name}.md missing")
    for name in TEMPLATES:
        check((ROOT / "templates" / f"{name}.md").exists(), f"templates/{name}.md missing")

    # 4. cross-references (references/, templates/, workflows/, examples/)
    link_re = re.compile(r"`(references|templates|workflows|examples)/[^`\s]+\.md`")
    for md in list((ROOT / "references").glob("*.md")) + \
              list((ROOT / "workflows").glob("*.md")) + \
              [ROOT / "SKILL.md"]:
        if md.name == "_template.md":
            continue
        for target in link_re.findall(read(md)):
            if target.startswith("../"):
                # normalise: workflows use ../references/x.md
                resolved = (md.parent / target).resolve()
            else:
                resolved = (ROOT / target).resolve()
            check(resolved.exists(), f"{md.relative_to(ROOT)} links to missing '{target}'")

    # 5. report
    if errors:
        print(f"FAILED: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(
        f"OK: {len(LENSES)} lenses, {len(WORKFLOWS)} workflows, "
        f"{len(TEMPLATES)} templates, SKILL.md valid"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
