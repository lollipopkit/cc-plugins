[English](README.md) | 简体中文

# Claude Code 插件

## 插件列表

- `rlm`: 模拟递归语言模型 - 通过 Self-Refine、Reflexion、Tree of Thoughts 实现多轮推理。
- `dev-loop`: 对一个 issue 进行迭代，直到准备好合并：创建分支、修复、提交、打开 PR、等待 AI 审查、应用反馈、重复。

各插件的具体文档位于各自的插件文件夹中。

## 使用方法

在Claude Code 中

```bash
# 将此仓库添加为 marketplace
/plugin marketplace add lollipopkit/cc-plugins
# 从此 marketplace 安装插件
/plugin install <plugin-name>@lk-ccp # 替换 <plugin-name> 为具体插件名
```

## 许可证

MIT
