#!/usr/bin/env python3
"""philosophers council — build a self-contained prompt for any LLM/agent.

No dependencies beyond the standard library. Run from anywhere; paths are
resolved relative to this script's location.

Examples:
  python3 scripts/council.py --list
  python3 scripts/council.py --task "要不要上线默认勾选续订" --workflow decision
  python3 scripts/council.py --task "分析这个方案" --lenses kant,marx,foucault --format json
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

LENSES = {
    "kant": "康德：可能性条件、可普遍化、目的公式",
    "hegel": "黑格尔：内在矛盾、扬弃、承认",
    "nietzsche": "尼采：价值考古、谱系、永恒轮回",
    "aristotle": "亚里士多德：四因、目的、中道、实践智慧",
    "wittgenstein": "维特根斯坦：用法、语言游戏、伪问题",
    "marx": "马克思：结构、利益成本、异化",
    "foucault": "福柯：问题化、话语、规训",
    "heidegger": "海德格尔：上手/在手、常人、技术座架",
}

WORKFLOWS = {
    "decision": ("kant,aristotle,hegel", "decision-memo"),
    "critique": ("hegel,marx,foucault", "critique-memo"),
    "concept": ("wittgenstein,kant", "concept-note"),
    "value-audit": ("nietzsche,marx,aristotle", "council-report"),
    "power-map": ("foucault,marx,hegel", "council-report"),
    "postmortem": ("hegel,aristotle,wittgenstein", "council-report"),
    "writing": ("aristotle,wittgenstein,nietzsche", "critique-memo"),
}

DISCIPLINE = """\
纪律（必须遵守）：
- 术语第一次出现时用一句人话解释；不堆砌名词。
- 不伪造引文、书名、页码；不确定就写“大意是”，并说明这是转述。
- 哲学家不是权威；理论只提供问题和检验，不提供事实。
- 透镜冲突时，呈现冲突比编造“综合”更有价值。
- 现实决策中，事实、数据、法律与专业意见优先；哲学不替代它们。
- 用用户的语言回答。
"""


def read(name: str) -> str:
    p = ROOT / name
    if not p.exists():
        raise FileNotFoundError(f"missing file: {name}")
    return p.read_text(encoding="utf-8")


def load_lens(name: str) -> str:
    if name not in LENSES:
        raise ValueError(f"unknown lens '{name}'. available: {', '.join(LENSES)}")
    return read(f"references/{name}.md")


def load_workflow(name: str) -> str:
    if name not in WORKFLOWS:
        raise ValueError(f"unknown workflow '{name}'. available: {', '.join(WORKFLOWS)}")
    return read(f"workflows/{name}.md")


def build_markdown(task: str, lenses: list[str], workflow: str | None, template: str | None) -> str:
    parts: list[str] = []
    parts.append("# 哲学家工作法：任务\n")
    parts.append(f"## 任务\n\n{task}\n")

    if workflow:
        parts.append("\n## 工作流\n")
        parts.append(load_workflow(workflow))

    for name in lenses:
        parts.append(f"\n## 透镜：{LENSES[name]}\n")
        parts.append(load_lens(name))

    if template:
        parts.append(f"\n## 产出模板：{template}\n")
        parts.append(read(f"templates/{template}.md"))

    parts.append("\n## 执行要求\n")
    parts.append(DISCIPLINE.rstrip())
    parts.append(
        "\n\n请按工作流步骤执行，逐透镜独立给出判断，最后合成并填充产出模板，"
        "给出可执行行动与验证方式。"
    )
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task", help="the task/question to run through the council")
    parser.add_argument("--workflow", choices=list(WORKFLOWS), help="pick a workflow (sets default lenses + template)")
    parser.add_argument("--lenses", help="comma-separated lens names, e.g. kant,marx")
    parser.add_argument("--template", choices=["decision-memo", "critique-memo", "concept-note", "council-report"],
                        help="output template to append")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--out", help="write output to this file instead of stdout")
    parser.add_argument("--list", action="store_true", help="list available lenses and workflows")
    args = parser.parse_args(argv)

    if args.list:
        print("Lenses:")
        for k, v in LENSES.items():
            print(f"  {k:14} {v}")
        print("\nWorkflows:")
        for k, (lenses, tmpl) in WORKFLOWS.items():
            print(f"  {k:14} lenses={lenses}  template={tmpl}")
        return 0

    if not args.task:
        parser.error("--task is required (or use --list)")

    lenses: list[str] = []
    if args.lenses:
        lenses = [s.strip() for s in args.lenses.split(",") if s.strip()]
    elif args.workflow:
        lenses = [s.strip() for s in WORKFLOWS[args.workflow][0].split(",") if s.strip()]
    else:
        lenses = ["kant"]

    template = args.template
    if args.workflow and not template:
        template = WORKFLOWS[args.workflow][1]

    try:
        for name in lenses:
            load_lens(name)  # validate early
        if args.workflow:
            load_workflow(args.workflow)
        if template:
            read(f"templates/{template}.md")
    except (ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    md = build_markdown(args.task, lenses, args.workflow, template)

    if args.format == "json":
        payload = {
            "task": args.task,
            "workflow": args.workflow,
            "lenses": lenses,
            "template": template,
            "prompt": md,
        }
        text = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        text = md

    if args.out:
        pathlib.Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {len(text)} chars -> {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
