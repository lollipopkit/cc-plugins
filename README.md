English | [简体中文](README.zh-CN.md)

# Claude Code Plugins

Claude 5.5 Opus is recommended for the best experience.

## Plugins

- `peer-model`: Run any Anthropic-compatible model (DeepSeek, GLM, ...) as a peer Claude Code session, optionally inheriting the current conversation context, with two-way messaging via `SendMessage`. Profiles are configured in `~/.config/cc-peer-model/config.toml`.

## Usage

### Remote Marketplace

In Claude Code:

```bash
# Add this repo as a marketplace
/plugin marketplace add lollipopkit/cc-plugins
# Install plugins from this marketplace
/plugin install <plugin-name>@lk-ccp # replace <plugin-name> with the specific plugin name
```

### Local Development

If you want to use the local version of this repo:

```bash
# Add local folder as a marketplace
/plugin marketplace add .
# Install plugins from the local marketplace
/plugin install <plugin-name>@lk-ccp
```

## License

MIT
