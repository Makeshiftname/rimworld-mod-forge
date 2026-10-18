# Mod 开发流程

本文是生产 mod 的总流程。具体技术细节继续查阅 Atlas：

- 骨架与日志：[project-templates.md](https://github.com/Makeshiftname/rimworld-mod-atlas/blob/ae09d37/docs/knowledge/guides/project-templates.md)
- XML/Defs：[xml-defs-and-patches.md](https://github.com/Makeshiftname/rimworld-mod-atlas/blob/ae09d37/docs/knowledge/guides/xml-defs-and-patches.md)
- Harmony 补丁：[harmony-patching.md](https://github.com/Makeshiftname/rimworld-mod-atlas/blob/ae09d37/docs/knowledge/guides/harmony-patching.md)
- 跨版本结构：[cross-version-structure.md](https://github.com/Makeshiftname/rimworld-mod-atlas/blob/ae09d37/docs/knowledge/guides/cross-version-structure.md)
- 测试：[testing-and-validation.md](https://github.com/Makeshiftname/rimworld-mod-atlas/blob/ae09d37/docs/knowledge/guides/testing-and-validation.md)
- 发布与许可：[publishing-and-release.md](https://github.com/Makeshiftname/rimworld-mod-atlas/blob/ae09d37/docs/knowledge/guides/publishing-and-release.md)

## 1. 先选择模式

| 模式 | 使用场景 | 放置位置 |
|---|---|---|
| 原创 mod | 新功能、新内容、独立发布 | `mods/owned/<stable-id>/` |
| 补丁/兼容 mod | 不复制目标源码，只改运行时行为或 XML | `mods/patches/<stable-id>/` |
| fork/源码改版 | 复制并修改第三方源码/资源 | 独立的 `rimworld-mod-forks` 仓库 |
| 一次性本地实验 | 不发布、不进入长期产品线 | 仓库外临时目录 |

如果目标 mod 的代码需要被复制进仓库，默认按 fork 处理，而不是补丁。

## 2. 开工前

1. 确认目标游戏版本：目前正式门禁是 1.6；1.7 只有在程序集、构建和运行时测试都通过后才登记。
2. 确认稳定 ID 和 `packageId`：
   - 原创：`Makeshiftname.<ModName>`
   - 补丁：`Makeshiftname.<ModName>Patch`
3. 检查依赖、目标 mod 的 `packageId` 和许可证。
4. 确认素材来源；第三方贴图、音频、代码不能因为放在本仓库就自动变成 MIT。
5. 写一份设计简报，至少包含：
   - 要解决的问题；
   - 不做什么；
   - 目标版本；
   - 依赖和加载顺序；
   - 玩家可见行为；
   - 验收场景；
   - 需要的素材和许可。

设计简报没有通过前，不开始批量写代码。

## 3. 建立骨架

从 `templates/owned-mod/` 或 `templates/patch-mod/` 复制，并完成以下内容：

- `About/About.xml`：`packageId`、名称、作者、描述、支持版本、依赖。
- `Common/`：跨版本共享的 Defs、Patches、Languages。
- `1.6/`：1.6 特有源码、程序集和资源。
- `1.7/`：只有实际验证后才创建。
- `README.md`：功能、安装、依赖、构建与兼容性。
- `AGENTS.md`：本 mod 的路径、命令、边界和验收。
- `Tests/whitebox/`：至少一个静态测试。

纯 XML mod 不强行创建 C# 工程。需要 C# 时，csproj 的输出路径和游戏引用都必须跟随 `$(GameVersion)`。

## 4. 实现顺序

1. 先实现一个可运行的最小垂直切片。
2. 在游戏内确认它能加载、能触发、不会刷错误日志。
3. 再补设置、翻译、兼容性和边界条件。
4. 每增加一个功能，补一个静态检查或明确的测试步骤。
5. 发现目标 mod 版本变化时，先更新分析，再改代码；不要把未验证推断写成事实。

## 5. 构建与测试

### 构建

```powershell
powershell -File shared/build/build_mod.ps1 -ModPath mods/owned/<id> -GameVersion 1.6
```

发布 tag 必须覆盖所有 `supportedVersions`。声明 1.6 和 1.7，就必须分别有对应的 1.6/1.7 产物和测试记录。

### 静态检查

```powershell
python shared/tests/check_mod.py mods/owned/<id>
python -m unittest discover -s mods/owned/<id>/Tests -v
```

至少检查：

- `About.xml` 可解析；
- `packageId` 非空、无占位符、符合 `Makeshiftname.*`；
- `packageId` 在仓库内不重复；
- `supportedVersions` 与实际版本目录一致；
- `modDependencies` / `loadAfter` 的 packageId 大小写正确；
- 所有 XML 可解析；
- 翻译 key 与 Def 的 defName 对应；
- 没有硬编码本机绝对路径；
- 发布物不含 `obj/`、`bin/`、日志和本地配置。

### 游戏内测试

至少覆盖：

- 新存档；
- 已有存档；
- 目标依赖存在；
- 目标依赖缺失（补丁 mod）；
- 不同加载顺序；
- 设置修改后重载；
- 多版本切换。

## 6. 发布

1. 更新 `About.xml` 的版本和描述。
2. 更新 `README.md` / changelog。
3. 重新构建并提交对应 `Assemblies/*.dll`。
4. 运行完整静态检查。
5. 创建 release tag。
6. 检查 `_PublisherPlus.xml` 的排除项。
7. 确认许可证、素材来源和依赖链接。
8. 记录 Atlas 回写链接和 commit。

## 7. Atlas 回写

- 生产代码留在本仓库，Atlas 只登记稳定 ID、`packageId` 和外部代码位置。
- 可复用分析写入 `rimworld-mod-atlas/records/<stable-id>/`。
- 只有审核过的跨 mod 结论才进入 `docs/knowledge/`。
- 跨仓库引用固定到 commit，避免 Atlas 文档变化让旧结论失去上下文。

## 8. 完成定义

一个 mod 只有同时满足以下条件才算完成：

- [ ] 设计和验收标准已记录；
- [ ] `packageId` 和稳定 ID 已固定；
- [ ] 目标版本构建通过；
- [ ] 静态测试通过；
- [ ] 游戏内冒烟测试通过；
- [ ] 依赖和加载顺序正确；
- [ ] 许可证和素材来源明确；
- [ ] README、`About.xml`、版本号和发布 tag 一致；
- [ ] 发布 DLL 已提交；
- [ ] Atlas 回写或明确记录“无可复用结论”。

## 9. 交接回报

Agent 完成任务后必须报告：

1. 模式（原创/补丁/fork）和稳定 ID；
2. 改了哪些文件；
3. 构建和测试命令及结果；
4. 游戏内验证覆盖了哪些场景；
5. 仍然未验证的内容；
6. 是否需要 Atlas 回写。
