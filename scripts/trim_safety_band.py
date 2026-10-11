#!/usr/bin/env python3
"""裁掉底部黑色安全边，避开 WorkBuddy 宿主的右下角角标水印。

背景
----
WorkBuddy 的 ImageGen 会在成图**右下角**叠加「AI生成 WORKBUDDY」宿主角标，
生成时无法关闭，事后擦除又容易连主副标题一起抹掉（`erase` 不可用）。
本技能改用**避让**而不擦除：

1. 请求画布高度 = 目标高度 + 底部安全边（默认 1440 + 70 = 1510），
   并在 prompt 末尾要求底部一条纯黑实心横条作为安全边；
2. 宿主角标固定落在右下角（实测距底约 10–70 像素），必然压在安全边内；
3. 生图后调用本脚本：补宽到目标宽度 → 裁掉整条安全边 → 校正到精确目标尺寸。

结果：3:4 精确成图，右下角角标随安全边一并被裁掉，无需任何事后修补。

实测底座（ImageGen）
-------------------
- 请求 1080×1510 → 实际返回 1072×1504（宽 −8、高 −6，按比例缩放）。
- 模型对「底部 70 像素」常画宽：实测安全边高度 117–165 像素，故裁切量
  必须按实测黑边高度取，不能写死 70。
- 安全边是纯黑且与画面边界清晰（相邻行亮度从 200+ 突降到 0），
  可用「整行像素 R、G、B 均 < 10」稳定识别；但边界行常有抗锯齿/渐变过渡，
  判到纯黑后仍要多裁几行（`--extra`，默认 4），否则成图最底会留 1–2 行暗行。
- 裁掉安全边后内容高度通常略小于 1440（安全边 165 时裁后 1339），
  脚本等比放大 1.03–1.08× 后居中裁宽到精确 1080×1440。

用法
----
  python trim_safety_band.py --image IN.png --out OUT.png
  python trim_safety_band.py --image IN.png --out OUT.png --band 70 \\
      --target 1080x1440 --canvas-height 1510

参数
----
  --image          输入图（宿主刚生成的带安全边原图）
  --out            输出图（默认覆盖输入）
  --band           安全边最小高度，默认 70；实测黑边不足该值时按其处理
  --target         目标尺寸，默认 1080x1440
  --canvas-height  期望的画布高度，默认 1510（仅用于提示与日志）
  --black-threshold 判定纯黑的通道上限，默认 10
  --no-upscale     高度不足目标时只裁不放大（输出会小于目标，不推荐）

依赖 pillow（隔离 venv：/Users/tychowu/.workbuddy/binaries/python/envs/default）。
"""

from __future__ import annotations

import argparse
import sys


def parse_size(text: str) -> tuple[int, int]:
    w, _, h = text.lower().partition("x")
    return int(w), int(h)


def find_band_height(img, threshold: int, max_scan_ratio: float = 0.35, extra: int = 2) -> int:
    """从底部向上数「整行近纯黑」的连续行数。

    只采样左侧 60% 宽度：宿主角标压在右下角，若把它算进来，
    水印所在的整行会被判成「非黑」而提前中断（实测会把 117 像素的黑边
    误判成 4 像素）。安全边本身贯通左右，左侧采样足以判定。
    """
    px = img.load()
    w, h = img.size
    x_end = max(1, int(w * 0.6))
    step = max(1, x_end // 100)
    max_scan = max(1, int(h * max_scan_ratio))
    band = 0
    for offset in range(max_scan):
        y = h - 1 - offset
        row_is_black = True
        for x in range(0, x_end, step):
            r, g, b = px[x, y][:3]
            if r > threshold or g > threshold or b > threshold:
                row_is_black = False
                break
        if not row_is_black:
            break
        band += 1
    # 多裁几行吃掉黑条与画面之间的抗锯齿过渡行；实测过渡行比纯黑行更亮，
    # 不会被「整行纯黑」判到，漏裁会在成图最底留下 1–2 行偏暗的残行。
    if band:
        band += extra
    return band


def main() -> int:
    ap = argparse.ArgumentParser(description="裁掉底部黑色安全边（避开宿主水印）")
    ap.add_argument("--image", required=True)
    ap.add_argument("--out")
    ap.add_argument("--band", type=int, default=70)
    ap.add_argument("--target", default="1080x1440")
    ap.add_argument("--canvas-height", type=int, default=1510)
    ap.add_argument("--black-threshold", type=int, default=10)
    ap.add_argument("--extra", type=int, default=4, help="额外多裁几行，吃掉黑条与画面间的抗锯齿/渐变过渡行")
    ap.add_argument("--no-upscale", action="store_true")
    args = ap.parse_args()

    try:
        from PIL import Image
    except ImportError:
        print("需要 pillow：/Users/tychowu/.workbuddy/binaries/python/envs/default/bin/pip install pillow")
        return 2

    out = args.out or args.image
    tw, th = parse_size(args.target)

    img = Image.open(args.image).convert("RGB")
    src_w, src_h = img.size

    # 1) 补宽到目标宽度（边缘复制，不缩放）
    if img.width < tw:
        pad = tw - img.width
        left = pad // 2
        right = pad - left
        canvas = Image.new("RGB", (tw, img.height))
        canvas.paste(img, (left, 0))
        if left:
            canvas.paste(img.crop((0, 0, 1, img.height)).resize((left, img.height)), (0, 0))
        if right:
            canvas.paste(img.crop((img.width - 1, 0, img.width, img.height)).resize((right, img.height)), (left + img.width, 0))
        img = canvas
    elif img.width > tw:
        left = (img.width - tw) // 2
        img = img.crop((left, 0, left + tw, img.height))

    # 2) 裁掉底部安全边
    measured = find_band_height(img, args.black_threshold, extra=args.extra)
    band = max(measured, args.band)
    if band >= img.height:
        print(f"错误：安全边判定高度 {band} 不小于图像高度 {img.height}，请检查输入图")
        return 3
    img = img.crop((0, 0, tw, img.height - band))

    # 3) 校正到精确目标尺寸（保顶部：标题在顶部，裁切从底部进行）
    scale_note = "无需缩放"
    if img.height < th:
        scale = th / img.height
        new_w = max(tw, round(img.width * scale))
        img = img.resize((new_w, th), Image.LANCZOS)
        left = (img.width - tw) // 2
        img = img.crop((left, 0, left + tw, th))
        scale_note = f"等比放大 {scale:.3f}× 后居中裁宽到 {tw}"
    elif img.height > th:
        img = img.crop((0, 0, tw, th))
        scale_note = "裁掉多余底部内容"

    img.save(out)

    print(f"输入      {src_w}×{src_h}")
    print(f"安全边实测 {measured} 像素（阈值 <{args.black_threshold}），采用 {band} 像素")
    print(f"裁后校正   {scale_note}")
    print(f"输出      {img.size[0]}×{img.size[1]}  {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
