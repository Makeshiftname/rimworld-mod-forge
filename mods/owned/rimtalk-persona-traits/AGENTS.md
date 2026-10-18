# AGENTS.md — RimTalk Persona Traits

- 稳定 ID：`rimtalk-persona-traits`
- packageId：`Makeshiftname.RimTalkPersonaTraits`
- 当前支持版本：1.6
- 1.7：未验证，不要提前写入 `supportedVersions`
- 类型：纯 XML，无 C# 程序集

## 修改边界

- 只修改本目录内的 About、Defs、Languages、README 和测试。
- 不修改 Atlas 的 `收集/` 内容，也不把第三方 mod 的源码或资源复制进来。
- 特质描述必须保留 `{PAWN_...}` 占位符；不要加入富文本标签。
- 修改 `defName` 时同步更新中文翻译和测试中的数量/冲突检查。

## 验证

```powershell
python shared/tests/check_mod.py mods/owned/rimtalk-persona-traits
python -m unittest discover -s mods/owned/rimtalk-persona-traits/Tests -v
```

游戏内验证：软链到 `Mods/`，开新档确认 10 个特质可被随机分配；启用 RimTalk 后确认特质描述出现在提示词中。
