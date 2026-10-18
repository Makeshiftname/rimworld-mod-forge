# mods

生产 mod 按所有权和修改方式分开：

- `owned/`：Makeshiftname 原创 mod。
- `patches/`：面向第三方 mod 的补丁/兼容 mod，不复制目标源码。

每个 mod 目录都必须能独立打包，拥有自己的 `About/About.xml`、版本目录、README、AGENTS 和测试。目录名使用稳定 ID，不使用 `NN-功能-名称` 排序。

补丁 mod 的 `About.xml` 必须明确写出目标 mod 的 `packageId` 和兼容版本。硬依赖进入 `modDependencies`，只影响加载顺序才使用 `loadAfter`。

fork 不放在这里，放到独立的 `rimworld-mod-forks` 仓库。
