# 原创 mod · RimTalk Persona Traits

> 本 mod 已从 Atlas 草稿迁入 forge，作为 `Makeshiftname` 的原创 mod 维护。
> 第三方 mod 的源码、分析记录和参考资料保留在 Atlas，不在本仓库复制。

## 开发状态

- 稳定 ID：`rimtalk-persona-traits`
- packageId：`Makeshiftname.RimTalkPersonaTraits`
- 当前只声明并验证 1.6；1.7 待实际构建和游戏内测试后再加入 `supportedVersions`。
- 这是从 Atlas 草稿迁入 forge 的第一个试点 mod。

## 一句话定位

轻量级**角色扮演向特质包**：10 个「对话人设」特质（性格/说话风格/嗜好），
**0 数值改动、纯描述、纯 XML（无 C#）**，每个特质的描述专为 **RimTalk 提示词注入**优化。

## 为什么做这个（RimTalk 提示词优化）

RimTalk（[Atlas 分析库](https://github.com/Makeshiftname/rimworld-mod-atlas)）在 `Full` 信息级别下，会把小人每个特质的
`degreeDatas/li/label` + `description` 拼进提示词：

```text
Traits: gossip:{PAWN_nameDef} is always the first to hear...
        dramatic:Everything is a performance for {PAWN_nameDef}...
```

- 描述里的 `{PAWN_nameDef}` / `{PAWN_pronoun}` / `{PAWN_possessive}` / `{PAWN_objective}`
  会被 RimTalk 自动解析成真实小人信息（对应 `CommonUtil.Sanitize` → `Formatted(pawn.Named("PAWN"))`）。
- 富文本标签会被剥离、换行会被去掉 —— 所以描述一律**不用** `<b>`/`<color>` 等标签。
- 因此「喂给 LLM 的提示词质量」≈ **特质描述文字本身**：本包的描述聚焦
  **怎么说话、聊什么**，给 LLM 明确的角色扮演钩子。

本包纯 XML 即可达成上述目标，无需 C#。

## 特质清单（10 个，初始定稿，可细调）

| defName / label                         | 中文名     | 类型     | 对话钩子                   |
| --------------------------------------- | ---------- | -------- | -------------------------- |
| `RB_Gossip` / gossip                  | 八卦精     | 性格     | 爱打听、主动聊他人近况     |
| `RB_Dramatic` / dramatic              | 戏精       | 性格     | 戏剧化独白、夸张措辞       |
| `RB_Raconteur` / raconteur            | 说书人     | 说话风格 | 长篇叙事、把日常讲成传奇   |
| `RB_Taciturn` / taciturn              | 寡言       | 说话风格 | 极简短句、开口即点睛       |
| `RB_Pedant` / pedant                  | 字面人     | 说话风格 | 抠定义、纠正措辞、字面理解 |
| `RB_TeaConnoisseur` / tea connoisseur | 茶道爱好者 | 嗜好     | 以茶会友、品评生活细节     |
| `RB_Angler` / angler                  | 钓鱼佬     | 嗜好     | 「跑掉的那条鱼」式吹牛     |
| `RB_Stargazer` / stargazer            | 观星者     | 嗜好     | 星空哲思、深夜有感         |
| `RB_Daydreamer` / daydreamer          | 白日梦者   | 性格     | 幻想跑偏、话题神游         |
| `RB_Curmudgeon` / curmudgeon          | 老牢骚     | 性格     | 刀子嘴豆腐心、毒舌吐槽     |

- 多数 `commonality` = 1.0；`Stargazer` / `Daydreamer` 为 0.8。全部 degree 0、**无数值/thought/mentalState**。
- 内部冲突：`Taciturn` 与 `Gossip` / `Raconteur` / `Dramatic` 互斥（说话风格矛盾）。

## 目录结构

```
mods/owned/rimtalk-persona-traits/
├── About/About.xml                                  # packageId Makeshiftname.RimTalkPersonaTraits, 1.6
├── 1.6/Defs/Traits.xml                              # 10 个 TraitDef（纯 XML）
├── Languages/ChineseSimplified/DefInjected/TraitDef/Traits.xml   # 中文 label + description
└── README.md
```

## 构建 / 验证

纯 XML mod，无编译步骤。验证：

```bash
python shared/tests/check_mod.py mods/owned/rimtalk-persona-traits
python -m unittest discover -s mods/owned/rimtalk-persona-traits/Tests -v
```

游戏内验证（可选，需 RimWorld 环境）：软链到 `Mods/` → 开档观察特质随机出现 →
RimTalk 对话（Full 信息级别）确认 `Traits:` 行包含本包特质描述。

## 待细调（后调项）

- `conflictingTraits`：若安装了 Vanilla Traits Expanded 等特质 mod，同名特质
  （Angler / Gossip / Stargazer 等）需按实际安装补写 `MayRequire` 冲突。
- `commonality`：按实际出现频率微调。
- 特质清单：随时增删，改时同步本表、中文翻译和测试中的数量/键检查。

## 相关参考

- [RimTalk 提示词注入机制](https://github.com/Makeshiftname/rimworld-mod-atlas/blob/ae09d37/%E6%94%B6%E9%9B%86/80-standalone-RimTalk/Source/Service/ContextBuilder.cs)（`GetTraitsContext`）
- [TraitDef 结构参考](https://github.com/Makeshiftname/rimworld-mod-atlas/blob/ae09d37/%E6%94%B6%E9%9B%86/82-patch-HautsAddedTraits/1.6/Defs/Traits.xml)
- [Atlas 知识库](https://github.com/Makeshiftname/rimworld-mod-atlas)
