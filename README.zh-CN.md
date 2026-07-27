# 情绪路由 / Emotion Router

[English](./README.md) · [GitHub](https://github.com/gongyu0918-debug/emotion-router) · `clawhub install emotion-skill` · `skillhub install emotion-skill`

面向 Coding Agent 的轻量 Markdown 软路由，只处理当前工作中明确出现的急迫、强烈愤怒/挫败和工作流困惑。

## 作用

压力容易让 Agent 辩解、解释过度、猜测、跑偏或扩大范围。情绪路由只把当前压力转成三种简短工作策略：

- **急迫**：以最小可用路径先完成用户点名的任务。
- **愤怒/挫败**：停止失败路径，定位问题并给出最小修复。
- **困惑**：用白话说明当前步骤、卡点和下一步。

如果用户质疑权限或未授权改动，必须先停手，再考虑速度。

## 边界

只读取当前 prompt 和可见 context，不分析用户画像、不读取长记忆，也不做情绪分类。引用文字、字段名、研究主题、中性命令和普通技术解释本身不会触发路由。

触发词只是辅助 Agent 做语义判断的例子，不是完整关键词表或脏话库。

## 安装包

运行时包只包含 `SKILL.md`、`agents/openai.yaml` 和三个 route reference。ClawHub 额外包含 `LICENSE`；SkillHub 因平台文件类型限制不包含该文件。仓库里的脚本、报告、素材和旧设计文档只供维护，不是运行时指令。

维护边界和验证命令见 [AGENTS.md](./AGENTS.md)。

## License

MIT，见 [LICENSE](./LICENSE)。
