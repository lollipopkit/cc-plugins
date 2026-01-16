[English](README.md) | 简体中文

# dev-loop

一个 Claude Code 插件，用于把一个 issue/任务以“循环迭代”的方式推进到可合并的 PR：

1. **创建分支**：始终根据 issue/任务内容创建一个新的描述性分支。
2. **实现修复**：研究并实现最小正确修复。
3. **提交 commit**：创建清晰的提交消息。
4. **Pull Request**：打开 PR 进行审查。
5. **等待审查**：轮询 review 评论。
6. **应用反馈**：根据 review 评论应用更改，并再次提交/推送。
7. **重复**：迭代执行 review 和反馈循环，直到 PR 被批准或合并。

## 安装

```bash
/plugin marketplace add lollipopkit/cc-plugins
/plugin install dev-loop@lk-ccp
```

## 组件

- Skill：`skills/dev-loop/SKILL.md`
- Agent：`agents/dev-loop-runner.md`
- Commands：
  - `/dev-loop`：启动或继续该工作流
  - `/dev-loop-enable`：创建/更新 `.claude/dev-loop.local.md`
- Hook：
  - `hooks/hooks.json`：Stop hook，可通过用户提供的命令模板发送 IM 通知

## 配置

在你的项目根目录创建 `.claude/dev-loop.local.md`。

最小模板：

```markdown
---
enabled: true
base_branch: "main"

# Review behavior
review_mode: "github"   # github|local-agent|custom
max_review_polls: 40
review_poll_seconds: 60

# External non-interactive LLM (optional)
llm_shell: "auto"       # auto|bash|fish
llm_command_template: "" # e.g. llm_script.sh "$DEV_LOOP_PROMPT"  OR  ccpxy "$DEV_LOOP_PROMPT"

# Notifications (optional)
notify_enabled: false
notify_shell: "auto"            # auto|bash|fish
notify_on_stop: true
notify_command_template: ""      # executed with selected shell; can reference env vars below
---

这里可以写给 dev-loop 的额外说明。
```

### 模板与环境变量

`llm_command_template`：

- 期望执行一个非交互式的 LLM 工具。
- runner 会在执行前导出 `DEV_LOOP_PROMPT`。
- 命令应输出一个 Markdown checklist，以便稳定解析。

期望输出格式：

```markdown
## Review Checklist
- [ ] path/to/file.ts:123 - 描述需要做的具体修改
- [ ] path/to/file.ts - 描述修改（行号可选）
- [ ] (general) 非文件级建议（尽量少用）
```

解析脚本：`python3 "$CLAUDE_PLUGIN_ROOT/scripts/parse-review-checklist.py"`（开发时也可用 `python3 dev-loop/scripts/parse-review-checklist.py`）。

示例：

- `llm_script.sh "$DEV_LOOP_PROMPT"`
- `ccpxy gpt -- -p "$DEV_LOOP_PROMPT"`（如果 `ccpxy` 只在 fish 下可用，设置 `llm_shell: "fish"`）

关于 `ccpxy`：在 fish 配置里，`ccpxy` 会把第一个非 option 参数当作 profile 名（例如 `gpt`/`g3p`/`g3f`/`gc`/`glm`/`c`）。不要把 `llm_command_template` 设成 `ccpxy "$DEV_LOOP_PROMPT"`，因为 prompt 会被当成 profile。

关于 `claude` CLI：非交互模式是 `-p/--print`，因此模板通常需要包含 `-p` 并把 prompt 放到最后。

`notify_command_template`：

- 由 Stop hook 脚本 `scripts/dev-loop-notify.sh` 执行。
- hook 会导出：
  - `DEV_LOOP_MESSAGE`（短消息）
  - `DEV_LOOP_PROJECT_DIR`
  - `DEV_LOOP_EVENT_NAME`
  - `DEV_LOOP_REASON`
  - `DEV_LOOP_TRANSCRIPT_PATH`
  - `DEV_LOOP_EVENT_JSON_B64`（base64 编码的 hook 输入 JSON）
