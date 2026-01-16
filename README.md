English | [简体中文](README.zh-CN.md)

# Claude Code Plugins

## Plugins

- `rlm`: Simulate Recursive Language Model - multi-pass reasoning with Self-Refine, Reflexion, Tree of Thoughts.
- `issue-loop`: Iterate on an issue until it is ready to merge: fix, commit, open PR, wait for AI review, apply feedback, repeat.

Plugin-specific docs live in each plugin folder.

## Usage

In Claude Code

```bash
# Add this repo as a marketplace
/plugin marketplace add lollipopkit/cc-plugins
# Install plugins from this marketplace
/plugin install <plugin-name>@lk-ccp # replace <plugin-name> with the specific plugin name
```

## License

MIT
