# WorkBuddy 环境适配说明（与 Codex 并存，不修改 Codex 流程）

本文件说明 YZZX-cover 在 **WorkBuddy** 宿主下运行时的差异与调整。Codex 原有的所有规则与流程**保持不变**；此处仅在 WorkBuddy 环境给出替代分支。

判断依据：WorkBuddy 提供**宿主内置 ImageGen 图片生成工具**、**内置浏览器预览面板**（`present_files` 工具）、以及当前对话**非多模态**（内联图片会被过滤，但 `Read` 本地图片文件可正常查看）。

---

## 0. 调用方式（必读）

- WorkBuddy 中按**小写**名称调用：`@skill:yzzx-cover`（对应 `SKILL.md` frontmatter 的 `name: yzzx-cover`）。用大写目录名 `YZZX-cover` 调用会失败（`Can not find skill`）。
- 若 Skill 工具按名称解析失败，直接按路径读取 `SKILL.md` 并严格遵循其流程（本仓库即如此处理）。

## 0.5 触发即开流程（极简响应）

- 每次独立调用第一步、收集素材之前执行 [版本检查与更新确认](version-check.md)：全局和项目均对比官方 main，列出差异后询问更新；已最新直接继续本次流程，后续生图前不再检查，不自动更新全局。目录不明、本地修改或检查失败时按流程处理。
- 用户说「生成一张封面 / 做一张封面 / 出图」等，**立即开始一次新流程**，不要长篇铺垫、不复述技能说明、不回顾无关上文。
- 回复 1–2 句：材料已齐则直接进入标题确认；缺文案或人物照则只简短询问这两项（不默认沿用上期）。
- WorkBuddy 下尤其避免「思考很多有的没的」——触发后先落地行动，缺失信息一次只问最关键的一件。
- 完整规则见 SKILL.md「快速开始：触发即进入制作流程」与核心原则第 7 条。

## 1. 打开风格展示站（A1 — 你实际踩到的痛点）

- **Codex**：`mcp__codex_app__open_in_codex` 打开 URL 的浏览器面板。
- **WorkBuddy：调用 `present_files`，传入 `https://yzzxref.diwu-pru.vip`，会在右侧内置浏览器面板直接打开，无需跳转外部浏览器。**
- 退路：若当前会话无内置预览能力，再调用 `agent-browser` 技能打开该 URL，并如实说明「已在浏览器中打开」。
- ❌ 禁止只回一句「链接在这 / 点开查看」——必须真正在右侧面板打开。

## 2. 生图画布尺寸实测（A2）

- **现象**：ImageGen 请求 `1080x1440` 实际可能返回非精确尺寸（实测返回 **1072×1440**，比例 0.744，而非严格 0.75）。
- **处理**：生图后必须用工具实测像素——
  - macOS：`sips -g pixelWidth -g pixelHeight <file>`
  - Linux：`identify <file>`
- 若实测不等于精确 **1080×1440**，先以填充/裁剪校正到精确 1080×1440，**再做**交付前验收；非 3:4 一律判不过（见 SKILL.md 通用生图规则·画布尺寸实测）。

## 3. 环境依赖（A3）

- WorkBuddy 推荐走**宿主内置 ImageGen**，根本不需要 PyYAML / OpenAI SDK / Node。此时 `bootstrap.py` 的 PyYAML 强依赖应降级为 warning，不因缺依赖而 `ready=false` 卡死出图。
- 运行 Python 脚本一律用**托管 Python 3.13**：`/Users/tychowu/.workbuddy/binaries/python/versions/3.13.12/bin/python3`（系统 3.9.6 有 venv/ensurepip 风险）。`output_paths.py` 零依赖，可直接成功。
- 仅当真要用 `generate.mjs` 提示词脚本时才需 Node 18+（可用托管 Node 22）。

## 4. 人物分析与成图验收看图（A5）

- **现状**：WorkBuddy 当前对话**内联图被过滤**（`current model does not support images`），但 `Read` 工具读取本地图片文件正常。
- **处理**：人物参考图与成图一律用 `Read` 读本地文件做身份锁定与逐项验收，例如：
  - 参考图：`~/.workbuddy/clipboard-images/*.jpg`
  - 成图：`~/Pictures/Yzzx Cover/covers/<主题>/*.png`
- ⚠️ 会话非多模态时，**必须声明「未做视觉验收，不可谎报通过」**；若无法读取成图，明确告知用户「本次未完成视觉验收」，不要凭 prompt 声称合格。

## 5. 水印处理

### 5.1 prompt 侧：避免模型自绘平台水印

- 生成 prompt **不要**直接写「小红书」等具体平台名称（易触发模型绘制平台水印）；如确需说明版式用途，用「竖版封面」泛指。
- 每张 prompt 末尾强制追加禁止水印句（详见 SKILL.md 通用生图规则·禁止平台水印）。

### 5.2 宿主角标：不擦除，用底部安全边裁切避让

- **事实**：WorkBuddy 的 ImageGen **必然**在成图右下角叠加「AI生成 WORKBUDDY」宿主角标，生成时无法关闭（无 LogoAdd 开关；`footnote` 设空也无效）。
- **不要用 `erase`**：`buddy-image-processing` 的 `erase` 实为「移除所有文字」，实测会连封面标题、副标题一起抹掉，对以文字为主的封面不可用。
- **做法（三步）**：
  1. 请求尺寸用 `1080x1510`（= 目标 1080×1440 + 底部 70 像素安全边），prompt 末尾追加：「画面最底部约 70 像素（不大于画面高度 5%）为贯通左右、纯黑 #000000 的实心横条安全边，横条内不得出现任何文字、图案、人物或元素。」
  2. 生成后运行：
     ```bash
     /Users/tychowu/.workbuddy/binaries/python/envs/default/bin/python \
       scripts/trim_safety_band.py --image "<原图>" --out "<成图>"
     ```
     脚本先左右补宽到 1080（边缘复制、不缩放），再实测并裁掉整条安全边，最后校正到精确 1080×1440。
  3. 角标随安全边一并被裁掉，成图右下角无残留，无需任何事后修补。
- **实测底座**：
  - 请求 1080×1510 → 实际返回 **1072×1504**（宽 −8、高 −6，按比例缩放）。
  - 模型对「底部 70 像素」**常画宽**：多次实测安全边为 **117 / 118 / 133 / 156 / 165** 像素，故裁切量必须按实测取值、不能写死 70；脚本内置 70 像素下限。
  - 角标固定在右下角、距底约 10–70 像素、宽约 150 像素，必然落在安全边内。
  - 安全边为纯黑且与画面分界清晰（相邻行亮度 200+ → 0 突降）；脚本按「整行纯黑」识别，**只采样左侧 60% 宽度**——若把右下角角标一并采样，水印所在行会被判成非黑，实测会把 117 像素的黑边误判成 4 像素。
  - **边界行有抗锯齿/渐变过渡**：只按纯黑行裁会在成图最底留 1–2 行暗行（实测最底行均值 37–45），脚本默认 `--extra 4` 多裁几行吃掉它。
  - 裁掉安全边后内容高度通常略小于 1440（安全边 117 时裁后 1387），脚本等比放大 1.03–1.08× 后居中裁宽到精确 1080×1440，不拉伸、不损人脸与文字；代价是画面整体略放大、上下内容更贴边，故 prompt 里须写明内容不压黑条。
- 依赖 pillow（隔离 venv，`/Users/tychowu/.workbuddy/binaries/python/envs/default`）；未装时先 `pip install pillow`。

## 6. 输出目录与交付

- 沿用 `scripts/output_paths.py` 创建的外置目录：`~/Pictures/Yzzx Cover/covers/<主题>/`。
- 成图验收通过后，用 `present_files` 同时交付：本地 png（外置目录绝对路径）+ 预览。
- ❌ 不要用仓库内 `output/`（仓库不跟踪生成图，且已取消跟踪）。

## 7. 与 Codex 的差异速查

| 项 | Codex | WorkBuddy |
| --- | --- | --- |
| 打开风格站 | `mcp__codex_app__open_in_codex` | `present_files(URL)` → 右侧内置面板 |
| 图片生成 | 宿主内置 ImageGen | 宿主内置 ImageGen（相同） |
| 人物/成图查看 | 内联多模态 | `Read` 本地文件 |
| 宿主角标（右下角水印） | — | 请求 `1080x1510` 留底部安全边，生成后 `trim_safety_band.py` 裁掉 |
| 环境依赖 | `bootstrap.py` + PyYAML | 托管 Python 3.13，可免 PyYAML |
| 画布 | 按 3:4 | 实测像素并校正到精确 1080×1440 |
| 调用名 | `yzzx-cover` | 小写 `yzzx-cover`（大写目录名会失败） |

---

> 本文件为 WorkBuddy 专属补充，不改动任何 Codex 段落；Codex 用户忽略即可。
