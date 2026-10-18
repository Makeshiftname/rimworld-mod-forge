# 发布检查清单

## 身份

- [ ] 稳定 ID、`packageId`、显示名一致。
- [ ] `packageId` 使用 `Makeshiftname.*`，没有沿用 `RunningBugs.*`。
- [ ] 补丁 mod 的目标 `packageId` 大小写完全正确。
- [ ] 没有和仓库内其它 mod 重复的 `packageId`。

## 构建

- [ ] `supportedVersions` 中的每个版本都实际构建过。
- [ ] csproj 的输出路径跟随 `$(GameVersion)`。
- [ ] 游戏程序集和第三方 DLL 引用没有写死本机路径。
- [ ] 发布版本的 `Assemblies/*.dll` 已提交。
- [ ] `obj/`、`bin/`、PDB、日志和本地配置没有进入发布物。

## 行为

- [ ] 新存档可加载。
- [ ] 已有存档可加载。
- [ ] 依赖存在时功能正常。
- [ ] 依赖缺失时补丁 mod 不崩溃、不静默破坏。
- [ ] 加载顺序变化不会导致静默失效。
- [ ] 设置修改后能持久化。
- [ ] 多版本切换没有引用错 DLL。

## 文档与许可

- [ ] `About.xml` 描述与 README 一致。
- [ ] 依赖、工坊链接和安装顺序已写明。
- [ ] 第三方代码/贴图/音频有明确许可。
- [ ] fork 保留原 LICENSE、作者和来源。
- [ ] 版本号在 `About.xml`、README、changelog、tag 中一致。

## 仓库

- [ ] `python shared/tests/check_mod.py <mod>` 通过。
- [ ] `python -m unittest discover -s <mod>/Tests -v` 通过。
- [ ] 没有修改 `mods/patches/` 目标 mod 的本体。
- [ ] Atlas 外部代码登记和回写链接已更新。
- [ ] 变更已提交，tag 已创建。
