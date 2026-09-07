# YZZX-cover 风格库

本目录存放「风格学习工作流」从参考图提取出的可复用封面风格模板。

## 文件约定

- 每个风格由一对文件组成，均用英文命名（与风格库 JSON 格式一致）：
  - `<style-id>.json`：风格定义，含 `name`（中文名）与 `prompt`（图片生成提示词）。
  - `<style-id>.jpg` / `.png` / `.webp`：用户选中的一张参考图，用风格英文名命名。
- 文件名示例：`warm-orange-motivation.json` + `warm-orange-motivation.jpg`。
- 通用出图约定（适用于本库所有风格）：画布比例强制 3:4（像素 1152×1536，禁止 1024×1536 等 2:3 拉长比例）；强调色面积占比须与原参考图一致（单色约 13%–22%、合计约 18%–23%）；字体按内容自动推荐、保留手写/变体风格；系列标签位置不与同色大块重叠、尺寸同原图小标签、文案需先询问用户并注明「推荐 ip 名称」；去水印优先用本库 `scripts/hunyuan_img_no_logo.py`（请求体固定 `LogoAdd=0`，复用内置 TC3 签名与轮询，需运行态 `BUDDY_CLOUD_TOKEN`），ImageGen 工具参数未暴露 LogoAdd 仅作降级（可能仍含水印）。

## 已收录风格

> 共 1 个。使用「风格学习工作流」上传参考图后，会自动在此登记。

| 风格中文名 | 风格 ID（文件名） | 参考图片 | prompt 摘要 |
| --- | --- | --- | --- |
| 蓝衫知识 IP | blue-shirt-knowledge-ip | [blue-shirt-knowledge-ip.jpg](blue-shirt-knowledge-ip.jpg) | 知识型 IP 设计教程拆解风：IP 手持样稿居中、超大主标题（字体按内容混合手写/变体/黑体，不千篇一律黑体）；强调色固定四选一且与原参考图一致（红 #AA2516 / 蓝紫 #7D6CC8 / 粉 #DD839D / 绿 #11AC42），面积占比单色 13%–22%、合计 18%–23%；标志元素「与强调色同色的实色大块承载文字」；人物服装色跟随素材，仅冲突或不够突出才兜底 #3B6BC3 蓝；系列标签不与同色块重叠、尺寸同原图小标签、文案需先问用户并注「推荐 ip 名称」；强制 3:4（1152×1536）；出去水印用 scripts/hunyuan_img_no_logo.py（LogoAdd=0） |

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
