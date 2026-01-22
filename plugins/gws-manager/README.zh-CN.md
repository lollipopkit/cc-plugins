[English](README.md) | 简体中文

# gws-manager

一个 Claude Code 插件，用于通过 [gws](https://github.com/lollipopkit/gws) CLI 工具管理并行开发工作区 (git worktree) 和建议锁 (advisory locks)。

## 安装

```bash
/plugin marketplace add lollipopkit/cc-plugins
/plugin install gws-manager@lk-ccp
```

## 特性

- **工作区隔离**：使用 git worktree 轻松创建、列出和删除并行开发工作区。
- **建议锁**：使用建议锁与其他代理或团队成员协调，防止冲突更改。
- **自动建议**：当检测到重大更改时（通过 PreToolUse 钩子），建议创建一个新的工作区。
- **环境检查**：在会话开始时检查 `gws` CLI 的可用性和工作区健康状况。

## 命令

- `/gws:new` – 创建一个新的并行开发工作区。
- `/gws:list` – 列出所有当前工作区。
- `/gws:rm` – 删除一个工作区。
- `/gws:prune` – 清理过时的工作区。
- `/gws:lock` – 对资源获取建议锁。
- `/gws:unlock` – 释放建议锁。
- `/gws:locks` – 列出所有活动的建议锁。
- `/gws:doctor` – 运行 gws 环境健康检查。
- `/gws:integrate` – 在当前项目中安装/更新 gws 集成。

## 组件

- **代理 (Agent)**: `agents/workspace-agent.md` – 用于工作区和锁管理的专门代理。
- **技能 (Skill)**: `skills/workspace-management/SKILL.md` – 复杂工作区操作的核心逻辑。
- **钩子 (Hook)**: `hooks/hooks.json` – 会话开始健康检查和工作区创建建议。
