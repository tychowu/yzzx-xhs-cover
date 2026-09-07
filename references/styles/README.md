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

> 共 4 个。使用「风格学习工作流」上传参考图后，会自动在此登记。

| 风格中文名 | 风格 ID（文件名） | 参考图片 | prompt 摘要 |
| --- | --- | --- | --- |
| 蓝衫知识 | blue-shirt-knowledge | [绿](blue-shirt-knowledge.jpg) · [红](blue-shirt-knowledge-02.jpg) · [紫](blue-shirt-knowledge-03.jpg) · [粉](blue-shirt-knowledge-04.jpg) | 知识型 IP 现场拆解风：人物服装跟随素材，仅在冲突或主体不突出时兜底替换为 #3B6BC3；四个版式各自只使用一种原图取样强调色，并复刻面积比例——绿 #11AC42 / 16.87%，红 #AA2516 / 13.02%，紫 #7D6CC8 / 13.60%，粉 #DD839D / 21.56%；含上下信息板、对角线杂志、户外手写、深色编辑批注四个分支。 |
| 硬核财经 | hardcore-finance | [外卖监管](hardcore-finance.jpg) · [保险](hardcore-finance-02.jpg) · [内存](hardcore-finance-03.jpg) · [日元](hardcore-finance-04.jpg) · [药价](hardcore-finance-05.jpg) | 深色财经新闻海报：上半区超大立体白字、下半区人物与 1–3 个证据型素材；以黑/深蓝黑为基底，根据内容选择金白、黑红、蓝灰或酒红强调；可用数据线、烟雾和笔刷增强冲突，禁止伪英文与水印。 |
| 奶油巨字 | cream-giant-type | [财经事件](cream-giant-type.jpg) · [谈判](cream-giant-type-02.jpg) · [个人故事](cream-giant-type-03.jpg) | 人物观点口播海报：暖黑/墨绿真实室内背景，固定四个奶油米白 #FFF5D6 巨字，每字带黑色软阴影；人物至少占画面 1/3，与标题形成可读的前后遮挡；必要时仅在上下标题中间加入一条同色系深色半透明信息条或亮色小字总结。 |
| 金棕解读 | golden-brown-expert | [变盘预警](golden-brown-expert.jpg) · [配置判断](golden-brown-expert-02.jpg) · [人物事件](golden-brown-expert-03.jpg) · [窗口策略](golden-brown-expert-04.jpg) | 高信任财经口播截图：暖深色或暖米白真实办公背景，左文右人；4–7 字金白/黑棕双行大标题，配细金线、切角或轻阴影；8–16 字小标题固定左中下，以黑色细描边主卡或低明度蓝结论条承载。人物需呈自然说话、桌边解释或交流手势。 |

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
