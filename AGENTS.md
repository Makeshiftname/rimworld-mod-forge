# AGENTS.md — RimWorld Mod Forge

本仓库是生产 mod 仓库。开始任何任务前先读
[`docs/MOD_DEVELOPMENT.md`](docs/MOD_DEVELOPMENT.md) 和目标 mod 自己的 `AGENTS.md`。

## 目录边界

- `mods/owned/`：Makeshiftname 原创 mod，可以修改、构建和发布。
- `mods/patches/`：面向第三方 mod 的补丁/兼容 mod；只能写自己的代码和 XML，不能修改目标 mod 本体。
- `templates/`：新 mod 模板，不直接发布。
- `shared/`：跨 mod 的构建和检查工具。
- `docs/`：长期流程、发布清单和决策记录。

fork 或源码改版不放本仓库，放在独立的 `rimworld-mod-forks` 仓库。

## 身份约定

- 新原创 mod 的 `packageId` 使用 `Makeshiftname.<ModName>`。
- 新补丁 mod 的 `packageId` 使用 `Makeshiftname.<ModName>Patch`。
- 稳定 ID 使用小写 ASCII slug；目录名、`packageId` 和显示名是三件不同的事。
- 第三方 mod 的 packageId 原样引用，不得改写或冒充。
- `packageId` 一旦发布不再更改；改名要作为新包处理，并把旧值登记为迁移别名。

## 开发规则

1. 先写设计简报和验收标准，再写实现。
2. 先做可运行的最小垂直切片，再扩展功能。
3. 只支持已经实际构建和测试过的游戏版本；1.7 未验证前不要写进 `supportedVersions`。
4. 第三方 mod 只通过 `modDependencies` / `loadAfter` 和运行时补丁关联，不复制目标源码。
5. 不硬编码本机路径；游戏目录通过环境变量或本地配置提供。
6. 发布版本的 `Assemblies/*.dll` 必须随源码提交；`obj/`、`bin/`、PDB 和本地临时文件不入库。

## 常用命令

```powershell
python shared/tests/check_all.py
powershell -File shared/build/build_mod.ps1 -ModPath mods/owned/<id> -GameVersion 1.6
```

补丁 mod 同时验证目标存在和目标缺失两种情况。
当前阶段见 [`docs/STATUS.md`](docs/STATUS.md)。

## Atlas 回写

- Atlas 是知识库，不是生产代码仓库。
- 需要回写分析时，在 Atlas 的 `records/<stable-id>/` 建立记录，并链接回本仓库的具体 commit。
- 只有 `deep + analyzed` 且经过审核的通用结论才能进入 `docs/knowledge/`。
- 不运行 Atlas 的 `migrate_mods.py --apply` 来搬运生产代码；跨仓库关系通过 registry 的外部代码字段登记。
