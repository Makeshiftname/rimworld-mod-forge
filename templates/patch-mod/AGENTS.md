# AGENTS.md — Example Patch

- 稳定 ID：`example-patch`
- packageId：`Makeshiftname.ExamplePatch`
- 目标 packageId：`author.targetmod`
- 目标版本：待填写

## 边界

- 不复制、不修改目标 mod 的源码、Defs、贴图和程序集。
- 硬依赖写入 `modDependencies`；只影响顺序才写 `loadAfter`。
- 目标缺失或版本不匹配时必须有明确日志或安全降级。
