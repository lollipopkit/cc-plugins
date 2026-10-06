[English](README.md) | 简体中文

# Claude Code 插件

建议使用 Claude 5.5 Opus 获得最佳体验。

## 插件列表

- `peer-model`: 以 peer session 方式运行任意 Anthropic 兼容模型（DeepSeek、GLM 等），可继承当前对话上下文，并通过 `SendMessage` 双向通信。profile 配置在 `~/.config/cc-peer-model/config.toml`。

## 使用方法

### 远程 Marketplace

在 Claude Code 中：

```bash
# 将此仓库添加为 marketplace
/plugin marketplace add lollipopkit/cc-plugins
# 从此 marketplace 安装插件
/plugin install <plugin-name>@lk-ccp # 替换 <plugin-name> 为具体插件名
```

### 本地开发

如果你想使用此仓库的本地版本：

```bash
# 将本地文件夹添加为 marketplace
/plugin marketplace add .
# 从本地 marketplace 安装插件
/plugin install <plugin-name>@lk-ccp
```

## 许可证

MIT
