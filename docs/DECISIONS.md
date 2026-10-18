# 仓库决策

## 2026-10-18：仓库分层

- `rimworld-mod-atlas` 只做知识库、分析记录、稳定 ID 和外部代码元数据。
- `rimworld-mod-forge` 是生产 monorepo，保存原创 mod 和补丁 mod。
- `rimworld-mod-forks` 独立保存 fork/源码改版。

## 2026-10-18：packageId

- 新原创 mod：`Makeshiftname.<ModName>`。
- 新补丁 mod：`Makeshiftname.<ModName>Patch`。
- `RunningBugs.*` 属于原仓库主，不再用于新作品。
- 稳定 ID 使用小写 slug，和 `packageId` 分离。

## 2026-10-18：版本

- 目标版本为 1.6 和 1.7，逐步转向 1.7。
- 只有实际构建、加载和测试通过的版本才写入 `supportedVersions`。
- 1.7 未验证前保持预览状态。

## 2026-10-18：发布物

- 发布 tag 对应版本的 `Assemblies/*.dll` 随源码提交。
- `obj/`、`bin/`、PDB 和本地临时文件不入库。

## 2026-10-18：Atlas 外部代码

- Atlas registry 使用 `code.kind: external` 登记本仓库代码。
- 外部代码记录 `repo`、`path` 和固定 `commit`。
- Atlas 不 clone、不扫描外部仓库，只校验元数据。
