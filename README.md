# RimWorld Mod Forge

Makeshiftname 的 RimWorld 生产仓库，保存可发布的原创 mod 和补丁 mod。

- 研究、分析记录和通用知识在 [`rimworld-mod-atlas`](https://github.com/Makeshiftname/rimworld-mod-atlas)。
- 本仓库只保存生产代码、构建配置、测试和发布物。
- fork 或源码改版放在独立的 [`rimworld-mod-forks`](https://github.com/Makeshiftname/rimworld-mod-forks) 仓库。

## 目录

```text
mods/owned/       原创 mod
mods/patches/     面向第三方 mod 的补丁/兼容 mod
shared/build/     共享构建脚本
shared/tests/     共享静态检查
templates/        新 mod 模板
docs/             开发、发布和决策文档
```

## 当前 mod

| 稳定 ID | packageId | 版本 | 状态 |
|---|---|---|---|
| `rimtalk-persona-traits` | `Makeshiftname.RimTalkPersonaTraits` | 1.6 | 草稿，1.7 待验证 |

## 开始

1. 读 [`AGENTS.md`](AGENTS.md)。
2. 读 [`docs/MOD_DEVELOPMENT.md`](docs/MOD_DEVELOPMENT.md)。
3. 按任务进入 `mods/owned/<id>/AGENTS.md` 或 `mods/patches/<id>/AGENTS.md`。

## 验证

```powershell
python shared/tests/check_mod.py mods/owned/rimtalk-persona-traits
python -m unittest discover -s mods/owned/rimtalk-persona-traits/Tests -v
```

## 许可

本仓库中的原创代码使用 [MIT 许可](LICENSE)。第三方 mod 的代码、贴图和其它资源不因本仓库的 MIT 许可而改变其原有许可；补丁和 fork 必须单独核对上游许可。
