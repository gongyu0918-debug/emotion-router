# 情绪路由 / Emotion Router

[English](./README.md) · [GitHub](https://github.com/gongyu0918-debug/emotion-skill-qingxu-skill) · `clawhub install emotion-skill`

面向 Coding Agent 的 Markdown-first 轻量情绪路由 skill。触发边界只看当前用户 prompt 和当前 context window：急迫、愤怒/挫败、困惑。

Agent 没有真实情绪。本 skill 读取的是用户侧压力信号，并把它转成 agent 下一步回复、工作顺序和验证方式。

## 为什么值得装

用户负面情绪和时间压力容易让模型进入不稳定工作流：防御、解释过度、猜测、跑偏或扩大范围。

情绪路由只保留三条路线：

- **急迫**：最快最小路径满足 prompt，再做最快最小验证。
- **愤怒/挫败**：先止损，找出失败点，给最小修复路径。
- **困惑**：说明现在正在做什么、当前卡点是什么、下一步是什么，用通俗语言恢复工作节奏。

## 结构

ClawHub 发布包：

- `SKILL.md`：触发边界、优先级和路由选择
- `agents/openai.yaml`：界面元数据和默认调用提示
- `references/emotion-routes.md`：三路由的信号、prompt 引导、禁止行为和示例开句

GitHub 仓库额外保留：

- `scripts/`：发布检查、审计和 legacy runtime 回归测试
- `references/`：旧设计说明和不进入安装包的验证参考
- `assets/`、`demo/`、`reports/`：校准材料、本地样例和测试证据

## 使用方式

在支持 skills 的 agent 中：

```text
Use $emotion-skill when the current user prompt or visible context shows urgency,
anger/frustration, or confusion. Pick one route and apply the matching prompt
pattern. Do not run a Python classifier.
```

Agent 应先读 `SKILL.md`，再加载 `references/emotion-routes.md` 中匹配的 route。信号词只是例子，不是硬关键词触发。

## 验证

仓库验证：

```bash
python scripts/markdown_skill_audit.py
python scripts/bundle_manifest_check.py
python scripts/marketplace_tag_audit.py
python scripts/smoke_test.py --strict
git diff --check
```

Subagent forward test 是真实行为检查，覆盖急迫、愤怒/挫败、困惑，以及急迫+愤怒冲突。

## 边界

这是 skill，不是 plugin 或 runtime classifier。它不检查 AGENTS.md、长记忆、用户画像、隐藏历史或旧校准状态，只处理当前 prompt 和当前 context window。

## License

MIT. See the [GitHub repository license](https://github.com/gongyu0918-debug/emotion-skill-qingxu-skill/blob/main/LICENSE).
