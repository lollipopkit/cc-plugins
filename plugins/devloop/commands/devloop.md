---
name: devloop
description: 启动或恢复 devloop 工作流（创建分支 → 修复 → 提交 → PR → 等待 AI 审查 → 应用评论 → 重复）。
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "AskUserQuestion", "TodoWrite", "Task", "Skill"]
argument-hint: "--issue <github-url|number|feishu/lark-url|text|file> [--base main]"
---

使用本插件中的插件组件运行 devloop 工作流。此命令通过重复循环，将任务推进到可以合并的 pull request。
