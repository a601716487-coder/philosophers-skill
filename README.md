# Philosophers · 哲学家工作法

把哲学家的**问题意识与方法**变成可执行的工作流程：诊断、决策、批判、概念澄清、复盘。

> A skill that turns the *questions and methods* of philosophers — Kant, Hegel, Nietzsche, Aristotle, Wittgenstein, Marx, Foucault, Heidegger — into runnable workflows for real work: decisions, critiques, concept clarification, reviews. Not personas, not name-dropping.

<p align="center">
  <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg">
  <img alt="Python 3.9+" src="https://img.shields.io/badge/Python-3.9%2B-blue">
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent_Skill-SKILL.md-8b5cf6">
  <img alt="Dependencies: none" src="https://img.shields.io/badge/Dependencies-none-brightgreen">
</p>

---

## 这是什么

一个 **Agent Skill**（遵循 Agent Skills 约定，`SKILL.md` 为入口），外加一组可独立运行的脚本。它让 agent 在接到工作类任务时，不靠“哲学口吻”，而是按某位哲学家的分析步骤去**操作**一个问题，最后落到判断与行动。

- 8 位哲学家 = 8 个“透镜”，每个透镜给出：核心问题、可操作工具、重述句式、输出模板、边界与误用。
- 7 个工作流 = 把常见工作形态（决策、批判、概念澄清……）映射成带步骤、输入、产出、质量门的可执行流程。
- 独立 CLI：`scripts/council.py` 可把任意任务 + 透镜打包成一个自包含提示词，供任何 LLM/agent 使用，不依赖本仓库之外的任何东西。

## 不是什么

- **不是哲学史百科**：不回答“康德生于哪年”这类知识题。
- **不是人格扮演**：默认用理论分析，不模仿文风；除非你明确要求“用某人的口吻写”。
- **不是权威背书**：哲学家只提供问题与检验，不提供事实；现实决策以事实、数据、法律、专业意见为准。

## 特性

- 每个透镜自带“重述句式”，把问题翻译成哲学家真正会问的问题。
- 内置“法庭模式”：2–3 个透镜各自独立判断，再合成，冲突如实呈现，不和稀泥。
- 纪律明确：不伪造引文、不堆术语、不回避哲学家的历史局限（如海德格尔的纳粹问题）。
- 可扩展：加一位哲学家 = 复制模板填一张文件；加一个工作流 = 复制改步骤。

## 安装

这是标准 Agent Skill 布局，仓库根目录就是技能包（`SKILL.md` 在根）。安装到各工具：

**Claude Code / 兼容 Agent Skills 的工具**

```bash
git clone <repo-url> .claude/skills/philosophers
# 或 ~/.claude/skills/philosophers
```

**DeepSeek Harness**

```bash
git clone <repo-url> ~/.dsh/skills/philosophers
# 或放到项目根的 .dsh/skills/philosophers
```

之后在对话里直接说“用康德的视角分析……”，或输入 `/philosophers`。

## 快速开始

不需要记命令：

- “用尼采的视角看：我们要不要为了增长做下沉市场？”
- “黑格尔式地分析一下：为什么这个团队改革推不动？”
- “这个概念我们吵了半天，用维特根斯坦的方法澄清一下。”
- “帮我用哲学家工作流复盘一下这个项目。”

也可以独立跑 CLI：

```bash
python3 scripts/council.py --list
python3 scripts/council.py --task "要不要上线默认勾选续订" --workflow decision
python3 scripts/council.py --task "分析这个方案" --lenses kant,marx,foucault --format json
```

### English quick start

Tell your agent things like: *"Review this decision through the Kant lens"*, *"Critique this strategy the way Hegel would"*, or *"Clarify this term using Wittgenstein"*. The `philosophers` skill routes the task to a workflow and lens automatically. Or run the standalone CLI:

```bash
python3 scripts/council.py --task "Should we ship dark patterns?" --workflow critique
```

## 八位哲学家透镜

| 透镜 | 一句话 | 文件 |
|---|---|---|
| 康德 | 先问“这凭什么可能、凭什么正当”，再问怎么做 | `references/kant.md` |
| 黑格尔 | 别急着选边，先看各方抓住了什么真理，再推到反面 | `references/hegel.md` |
| 尼采 | 先问价值从哪来、为谁服务，失效后还剩什么 | `references/nietzsche.md` |
| 亚里士多德 | 先问“为了什么”，再问情境里的恰当 | `references/aristotle.md` |
| 维特根斯坦 | 把问题带回语言的实际用法 | `references/wittgenstein.md` |
| 马克思 | 先看物质关系、谁受益、谁买单 | `references/marx.md` |
| 福柯 | 先问它凭什么成为真理、让谁被当正常 | `references/foucault.md` |
| 海德格尔 | 先看已在的实践整体，工具把世界揭示成了什么 | `references/heidegger.md` |

## 七个工作流

| 任务形态 | 工作流 | 默认透镜 | 产出 |
|---|---|---|---|
| 要不要做 / 选哪个 | `workflows/decision.md` | 康德 + 亚里士多德 + 黑格尔 | `templates/decision-memo.md` |
| 方案 / 战略行不行 | `workflows/critique.md` | 黑格尔 + 马克思 + 福柯 | `templates/critique-memo.md` |
| 定义 / 术语打架 | `workflows/concept.md` | 维特根斯坦 + 康德 | `templates/concept-note.md` |
| 动力 / 激励 / 文化 | `workflows/value-audit.md` | 尼采 + 马克思 + 亚里士多德 | `templates/council-report.md` |
| 变革推不动 / 谁说了算 | `workflows/power-map.md` | 福柯 + 马克思 + 黑格尔 | `templates/council-report.md` |
| 复盘 | `workflows/postmortem.md` | 黑格尔 + 亚里士多德 + 维特根斯坦 | `templates/council-report.md` |
| 文本 / 论证 | `workflows/writing.md` | 亚里士多德 + 维特根斯坦 + 尼采 | `templates/critique-memo.md` |

路由入口在 `workflows/operating-manual.md`。完整示例见 `examples/`。

## 目录结构

```
.
├── SKILL.md                 # 入口：选透镜 + 选工作流 + 纪律
├── references/              # 8 个哲学家透镜 + 模板
├── workflows/               # 7 个可执行工作流 + 操作手册
├── templates/               # 4 个产出模板
├── examples/                # 完整跑通示例
├── scripts/
│   ├── council.py           # 提示词生成器（stdlib only）
│   └── validate.py          # 结构校验（CI 使用）
└── .github/workflows/       # 自动校验
```

## 设计原则

1. **先事实后理论**：每个工作流第一步都是摆事实，禁止一上来套概念。
2. **理论是脚手架，不是结论**：产出永远落到可执行动作与验证方式。
3. **冲突优先于“综合”**：透镜意见相左时如实呈现，比强行统一更有价值。
4. **按需加载**：入口只做路由，透镜文件用到才读，不把八套理论全塞进上下文。
5. **引文纪律**：不伪造书名页码，不确定就标“大意”。

## 如何扩展

- **加一位哲学家**：复制 `references/_template.md` 为 `<name>.md`，填好，在 `SKILL.md` 选透镜表加一行，并在 `scripts/council.py` 的 `LENSES` 里注册。
- **加一个工作流**：复制任意 `workflows/*.md` 改步骤，在 `SKILL.md` 与 `workflows/operating-manual.md` 映射表加一行，并在 `scripts/council.py` 的 `WORKFLOWS` 里注册。

改动后跑 `python3 scripts/validate.py` 检查一致性。

## FAQ

**为什么不是 8 个独立技能？** 独立技能会让目录多 8 条摘要、上下文更贵；单一入口按需加载更省，也支持跨哲学家的“法庭模式”。想要 `/nietzsche` 这样的独立入口，可以再拆。

**它能替我做决定吗？** 不能。它给出框架、检验与行动建议，决策权在你自己；涉及法律、医疗、财务以专业人士为准。

**会被误用吗？** 会。每个透镜文件都写了“边界与误用”，纪律也要求不伪造引文、不把哲学家当权威。

**和提示词库有什么区别？** 提示词库给模板；这里给的是“问题意识 + 可操作步骤 + 质量门”，并有校验脚本和 CI 保证结构一致。

## 贡献

欢迎 Issue 与 PR。改动后请跑 `python3 scripts/validate.py` 确保结构一致；新增透镜或工作流按上面“如何扩展”的步骤注册。提交前自查，不要把 `__pycache__`、`dist/` 等生成物提交进来。

## 局限

- 哲学不替代事实、数据、法律、医疗、财务专业意见。
- 某些哲学家的文本存在争议与历史局限（如《权力意志》为遗稿编排、海德格尔的政治污点），透镜文件里已标注，使用时保持批判距离。
- 术语的中文译名不唯一；透镜文件采用通行译名并在关键处附原文。

## License

MIT，见 [LICENSE](LICENSE)。
