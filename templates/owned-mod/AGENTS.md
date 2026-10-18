# AGENTS.md — Example Mod

- 稳定 ID：`example-mod`
- packageId：`Makeshiftname.ExampleMod`
- 目标版本：1.6（1.7 未验证）
- 构建：`powershell -File shared/build/build_mod.ps1 -ModPath mods/owned/example-mod -GameVersion 1.6`
- 静态检查：`python shared/tests/check_mod.py mods/owned/example-mod`
- 测试：`python -m unittest discover -s mods/owned/example-mod/Tests -v`

## 边界

- 不修改 `mods/patches/` 或第三方 mod 本体。
- 不硬编码本机游戏路径。
- 发布前更新 `About.xml`、README 和 changelog。
