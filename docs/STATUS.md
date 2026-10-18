# 仓库状态

## 当前阶段

- `rimworld-mod-forge` 已初始化，作为原创和补丁 mod 的生产 monorepo。
- 当前只有一个原创草稿：`mods/owned/rimtalk-persona-traits/`。
- 该 mod 只声明并验证 1.6；1.7 待实际构建和游戏内测试。
- 还没有补丁 mod 试点，也没有正式 release。

## 当前 mod

| 稳定 ID | 类型 | packageId | 版本 | 状态 |
|---|---|---|---|---|
| `rimtalk-persona-traits` | 原创 XML | `Makeshiftname.RimTalkPersonaTraits` | 1.6 | 草稿 |

## 门禁

```powershell
python shared/tests/check_all.py
```

该命令会扫描 `mods/owned/` 和 `mods/patches/`，运行静态检查和每个 mod 的单元测试。

## 待办

1. 在真实 RimWorld 1.6 环境做游戏内冒烟测试：
   - 新档和旧档；
   - 特质随机出现；
   - RimTalk 提示词包含 trait 描述。
2. 拿到 1.7 程序集后，完成构建和游戏内测试，再把 1.7 写入
   `supportedVersions`。
3. 增加一个实际补丁 mod 试点，验证 `modDependencies` / `loadAfter` 和目标缺失行为。
4. 发布前执行 [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md)。
5. 不把 fork 放进本仓库；fork 使用本地 `rimworld-mod-forks`。
