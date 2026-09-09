# YZZX-cover 风格库

本目录存放「风格学习工作流」从参考图提取出的可复用封面风格模板。

## 文件约定

- 每个风格至少包含一份 JSON 和一张主参考图，均用英文命名（与风格库 JSON 格式一致）：
  - `<style-id>.json`：风格定义，含 `name`（中文名）与 `prompt`（图片生成提示词）。
  - `<style-id>.jpg` / `.png` / `.webp`：主参考图，用风格英文名命名。
  - `<style-id>-02.jpg` 等：同一风格的补充参考图（可选），用于保留不同版式分支。
- 文件名示例：`warm-orange-motivation.json` + `warm-orange-motivation.jpg`。
- 通用出图约定（适用于本库所有风格）：画布比例强制 3:4（像素 1080×1440，禁止 1024×1536 等 2:3 拉长比例）；强调色面积占比须与原参考图一致（单色约 13%–22%、合计约 18%–23%）；字体按内容自动推荐、保留手写/变体风格；系列标签位置不与同色大块重叠、尺寸同原图小标签、文案需先询问用户并注明「推荐 ip 名称」；去水印优先用本库 `scripts/hunyuan_img_no_logo.py`（请求体固定 `LogoAdd=0`，复用内置 TC3 签名与轮询，需运行态 `BUDDY_CLOUD_TOKEN`），ImageGen 工具参数未暴露 LogoAdd 仅作降级（可能仍含水印）。

## 已收录风格

> 共 12 个。上传的学习参考图保存在 \`source-references/\`；经用户确认的测试示意图保存在 \`approved-examples/\`，两者不得混放。

| 风格中文名 | 风格 ID（文件名） | 参考图片 | prompt 摘要 |
| --- | --- | --- | --- |
| 潮色动势 | dynamic-color-motion | [活动餐饮](source-references/dynamic-color-motion/Camera_1040g0k0320sf21r2746g5ng2muh08u4nhpvbq28.jpg) · [城市行动](source-references/dynamic-color-motion/Camera_1040g34o31nve2c2j504g5o59tda08dvq6f3mi1o.jpg) · [通勤体验](source-references/dynamic-color-motion/Camera_1040g0k0320sf21r2740g5ng2muh08u4nnpcr24g.jpg) · [产品现场](source-references/dynamic-color-motion/Camera_1040g34o31nve2c2j507g5o59tda08dvqlj47a9o.jpg) · [骑行体验](source-references/dynamic-color-motion/Camera_1040g34o31nve2c2j50605o59tda08dvqcekge00.jpg) · [已确认示意图](approved-examples/潮色动势.png) | 真实都市行动照片 + 超粗潮色标题：人物、产品和关键动作必须使用薄荷青或玫红的较粗彩色描边，1–2 条同色轨迹线沿动作方向穿过画面，点缀少量季节/场景相关扁平图形。 |
| 撕纸漫游 | torn-paper-wander | [人物故事](source-references/torn-paper-wander/Camera_XHS_17888093281421040g0083205uclf52i105ne0p8ig8efgfltjqto.jpg) · [反差叙事](source-references/torn-paper-wander/Camera_XHS_17888091333871040g2sg31fk6a25e00cg49unr6g0u3m6cf3m45g.jpg) · [户外徒步](source-references/torn-paper-wander/Camera_XHS_17888091388431040g2sg31fk6a25e00c049unr6g0u3m6ibgoseg.jpg) · [生活片段](source-references/torn-paper-wander/Camera_XHS_17888091350581040g2sg31fk6a25e00b049unr6g0u3m6tor07oo.jpg) · [旅行记录](source-references/torn-paper-wander/Camera_XHS_17888091369481040g2sg31fk6a25e00bg49unr6g0u3m69kidcng.jpg) · [已确认示意图](approved-examples/撕纸漫游.png) | 真实现场底图 + 米白撕纸相框：一色超大干刷标题跨越纸框，主角与场景互动并穿出相框，1–3 张同一事件的拍立得小图补足叙事，少量图钉、红心、星星或对话气泡收尾。 |
| 随性手绘 | casual-hand-drawn | [雨林徒步](source-references/casual-hand-drawn/Camera_1040g34o31rjnt2t9i8g05ng2muh08u4nc8vrg50.jpg) · [创意随拍](source-references/casual-hand-drawn/Camera_1040g34o322usfmiln2b05pn06mr3cik9qi6is6o.jpg) · [南京邀请](source-references/casual-hand-drawn/Camera_1040g34o31rjnt2t9i8f05ng2muh08u4nb3p3g80.jpg) · [场景教程](source-references/casual-hand-drawn/Camera_1040g34o322usfmiln2a05pn06mr3cik9nnbl0tg.jpg) · [叙事记录](source-references/casual-hand-drawn/IMG_20260908_035705.jpg) · [已确认示意图](approved-examples/随性手绘.png) | 真实现场照片上的随性手写视频笔记：上半区粗粝白色手绘大标题，奶黄为主的低密度高亮，人物在走路、记录或与环境互动；用 REC、取景框、日期、路线和箭头串起同一个正在发生的故事。 |
| 黑黄贴纸 | black-yellow-sticker | [AI 周报](source-references/black-yellow-sticker/AI产品经理周报本周玩了哪些好玩的Skill_AI产品经理周报本周玩了哪些好玩的Skill_准备把这.png.jpg) · [开发者大会](source-references/black-yellow-sticker/Google_IO_开发者大会AI如何改善生活_Google_IO_开发者大会AI如何改善生活_前两.png.jpg) · [个人网站](source-references/black-yellow-sticker/关于Vivi我在AI时代的个人网站和作品集_关于Vivi我在AI时代的个人网站和作品集_因为有了_A.png.jpg) · [英语绘本](source-references/black-yellow-sticker/挖到了可以定制主角的宝藏英语绘本Skill_挖到了可以定制主角的宝藏英语绘本_挖到了一个免.png.jpg) · [技能测评](source-references/black-yellow-sticker/测评10个让图片变好看的Skill还能定制IP_测评10个让图片变好看的Skill还能定制IP_最近.png.jpg) · [已确认示意图](approved-examples/黑黄贴纸.png) | 真人讲解 + 黄黑撕纸贴纸海报：顶部黑字黄底超宽标题每行铺满约 88%–96%，人物带白描边与黄色手绘轮廓，3–7 个主题相关对话气泡/照片贴片以箭头串联。 |
| 蓝衫知识 | blue-shirt-knowledge | [绿](source-references/blue-shirt-knowledge/blue-shirt-knowledge.jpg) · [红](source-references/blue-shirt-knowledge/blue-shirt-knowledge-02.jpg) · [紫](source-references/blue-shirt-knowledge/blue-shirt-knowledge-03.jpg) · [粉](source-references/blue-shirt-knowledge/blue-shirt-knowledge-04.jpg) · [已确认示意图](approved-examples/蓝衫知识.png) | 知识型 IP 现场拆解风：人物服装跟随素材，仅在冲突或主体不突出时兜底替换为 #3B6BC3；四个版式各自只使用一种原图取样强调色，并复刻面积比例——绿 #11AC42 / 16.87%，红 #AA2516 / 13.02%，紫 #7D6CC8 / 13.60%，粉 #DD839D / 21.56%；含上下信息板、对角线杂志、户外手写、深色编辑批注四个分支。 |
| 硬核财经 | hardcore-finance | [外卖监管](source-references/hardcore-finance/hardcore-finance.jpg) · [保险](source-references/hardcore-finance/hardcore-finance-02.jpg) · [内存](source-references/hardcore-finance/hardcore-finance-03.jpg) · [日元](source-references/hardcore-finance/hardcore-finance-04.jpg) · [药价](source-references/hardcore-finance/hardcore-finance-05.jpg) · [已确认示意图](approved-examples/硬核财经.png) | 深色财经新闻海报：上半区超大立体白字、下半区人物与 1–3 个证据型素材；以黑/深蓝黑为基底，根据内容选择金白、黑红、蓝灰或酒红强调；可用数据线、烟雾和笔刷增强冲突，禁止伪英文与水印。 |
| 奶油巨字 | cream-giant-type | [财经事件](source-references/cream-giant-type/cream-giant-type.jpg) · [谈判](source-references/cream-giant-type/cream-giant-type-02.jpg) · [个人故事](source-references/cream-giant-type/cream-giant-type-03.jpg) · [已确认示意图](approved-examples/奶油巨字.png) | 人物观点口播海报：暖黑/墨绿真实室内背景，固定四个奶油米白 #FFF5D6 巨字，每字带黑色软阴影；人物至少占画面 1/3，与标题形成可读的前后遮挡；必要时仅在上下标题中间加入一条同色系深色半透明信息条或亮色小字总结。 |
| 金棕解读 | golden-brown-expert | [变盘预警](source-references/golden-brown-expert/golden-brown-expert.jpg) · [配置判断](source-references/golden-brown-expert/golden-brown-expert-02.jpg) · [人物事件](source-references/golden-brown-expert/golden-brown-expert-03.jpg) · [窗口策略](source-references/golden-brown-expert/golden-brown-expert-04.jpg) · [已确认示意图](approved-examples/金棕解读.png) | 高信任财经口播截图：暖深色或暖米白真实办公背景，左文右人；4–7 字金白/黑棕双行大标题，配细金线、切角或轻阴影；8–16 字小标题固定左中下，以黑色细描边主卡或低明度蓝结论条承载。人物需呈自然说话、桌边解释或交流手势。 |
| 高能科技 | high-energy-tech | [拼贴实验](source-references/high-energy-tech/high-energy-tech.jpg) · [导演工作台](source-references/high-energy-tech/high-energy-tech-02.jpg) · [人物对撞](source-references/high-energy-tech/high-energy-tech-03.jpg) · [Agent 界面](source-references/high-energy-tech/high-energy-tech-04.jpg) · [已确认示意图](approved-examples/高能科技.png) | 黑/深蓝黑科技杂志海报：顶部超大冷白硬朗标题，固定以 #FECE02 关键词块占 10%–20%；人物表情须与叙事对应、具备高信息密度，下半区由人物双手参与的具体实验场景或产品工作流填满，避免泛用光效与孤立道具。 |
| 复古小财 | retro-little-finance | [留白侧脸](source-references/retro-little-finance/retro-little-finance.jpg) · [环绕消费](source-references/retro-little-finance/retro-little-finance-02.jpg) · [钱的轨迹](source-references/retro-little-finance/retro-little-finance-03.jpg) · [观点海报](source-references/retro-little-finance/retro-little-finance-04.jpg) · [穷忙](source-references/retro-little-finance/retro-little-finance-05.jpg) · [已确认示意图](approved-examples/复古小财.png) | 低饱和纸纹财经专栏：暖米、草绿、雾青或淡黄单色留白底，宋体/衬线大标题，人物与 3–7 个主题相关剪贴物构成轻叙事；可用大裁切侧脸、仰望人物或真实脸部 + 线稿服装，禁止赛博光效与随机英文。 |
| 荧光讲解 | fluorescent-explainer | [荧光变现](source-references/fluorescent-explainer/fluorescent-explainer.jpg) · [职场洞察](source-references/fluorescent-explainer/fluorescent-explainer-02.jpg) · [白捡 MVP](source-references/fluorescent-explainer/fluorescent-explainer-03.jpg) · [AI 视频](source-references/fluorescent-explainer/fluorescent-explainer-04.jpg) · [理财选题](source-references/fluorescent-explainer/fluorescent-explainer-05.jpg) · [已确认示意图](approved-examples/荧光讲解.png) | 真人讲解截图海报：蓝紫或浅蓝真实室内底，荧光黄绿/玫红/钴蓝巨字与 3–5 个手绘贴纸；人物占 40%–60%，以竖拇指、指向或近景食指和标题对话，按主题可加入报告图表与箭头，禁止荧光滥用和伪数据。 |
| 暗域科技 | skill-blast | [自动化分镜](source-references/skill-blast/skill-blast.jpg) · [技能清单](source-references/skill-blast/skill-blast-02.jpg) · [内容工厂](source-references/skill-blast/skill-blast-03.jpg) · [AI 求职](source-references/skill-blast/skill-blast-04.jpg) · [爆款技能](source-references/skill-blast/skill-blast-05.jpg) · [已确认示意图](approved-examples/暗域科技.png) | 暗色高能故事海报：近黑海军蓝到酒红底、纯白横向超大标题；人物动作、配景、配角与可选卡片均从文案事件提取，突出具体场景与成果，不默认强调工作流；标题可被人物前景局部遮挡超过 10% 但必须完整可读。 |

## 如何在生成时使用

测试生成（Phase 3，优先去水印脚本）：

```bash
# 1) 组装 prompt（仅输出文本，不出图）
node ${SKILL_DIR}/scripts/generate.mjs \
  --style "风格ID（去掉 .json）" \
  --title "标题" \
  --output-dir "/tmp/xhs-style-test"

# 2) 用去水印脚本生图（请求体固定 LogoAdd=0，需运行态 BUDDY_CLOUD_TOKEN）
BUDDY_CLOUD_TOKEN=<token> python3 ${SKILL_DIR}/scripts/hunyuan_img_no_logo.py \
  image "组装好的提示词" --resolution 1152:1536 --output-dir /tmp/xhs-style-test
```

新增风格后由工作流自动更新本表。
