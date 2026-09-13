#!/usr/bin/env python3
"""移除角标水印（WorkBuddy ImageGen 平台水印定点修补）。

背景：WorkBuddy 的 ImageGen 生成图**必然**带右下角「AI生成 WORKBUDDY」平台水印，
生成时无法关闭；而内置 buddy-image-processing 的 erase 是「移除所有文字」，
会把封面正文（标题/副标题）一并抹掉，**不适合以文字为主的封面**。

本脚本改用「克隆邻近纹理覆盖水印」的定点修补：从水印旁取一块同排纹理，
羽化接缝后覆盖水印，保留全部文字与画面。仅适用于角落小水印。

依赖：pillow（装在隔离 venv，例如
  /Users/tychowu/.workbuddy/binaries/python/envs/default/bin/python）。

用法：
  python remove_corner_watermark.py --image IN.png --out OUT.png
  # 默认：右下角 (W-152, H-74)-(W, H)，从左侧同排克隆 155px
可选：
  --corner br|bl|tr|tl   角（默认 br）
  --x0 --y0 --x1 --y1    自定义水印外框（像素）
  --off 155              克隆偏移（默认 155）
  --feather 10           接缝羽化宽度（贴图边缘贴齐图像侧不羽化）
  --blur 1.5             克隆块与遮罩的高斯模糊
"""
import argparse


def build_mask(w, h, feather, blur, corner):
    from PIL import Image, ImageDraw, ImageFilter
    mask = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(mask)
    f = max(0, feather)

    def ramp(horizontal, reverse=False):
        for i in range(f):
            a = int(255 * i / f)
            if reverse:
                a = 255 - a
            if horizontal:
                d.line([(0, i), (w, i)], fill=a)
            else:
                d.line([(i, 0), (i, h)], fill=a)

    # 与水印所在角「相对」的两条边做羽化，贴齐图像边缘的两条边保持不透明
    if corner == "br":      # 贴右+下 → 羽化 上、左
        ramp(True); ramp(False)
    elif corner == "bl":    # 贴左+下 → 羽化 上、右
        ramp(True)
        for i in range(f):
            d.line([(w - 1 - i, 0), (w - 1 - i, h)], fill=int(255 * i / f))
    elif corner == "tr":    # 贴右+上 → 羽化 下、左
        for i in range(f):
            d.line([(0, h - 1 - i), (w, h - 1 - i)], fill=int(255 * i / f))
        ramp(False)
    else:                   # tl 贴左+上 → 羽化 下、右
        for i in range(f):
            d.line([(0, h - 1 - i), (w, h - 1 - i)], fill=int(255 * i / f))
        for i in range(f):
            d.line([(w - 1 - i, 0), (w - 1 - i, h)], fill=int(255 * i / f))

    if blur > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(blur))
    return mask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--corner", default="br", choices=["br", "bl", "tr", "tl"])
    ap.add_argument("--x0", type=int)
    ap.add_argument("--y0", type=int)
    ap.add_argument("--x1", type=int)
    ap.add_argument("--y1", type=int)
    ap.add_argument("--off", type=int, default=155)
    ap.add_argument("--feather", type=int, default=10)
    ap.add_argument("--blur", type=float, default=1.5)
    a = ap.parse_args()

    from PIL import Image, ImageFilter
    im = Image.open(a.image).convert("RGB")
    W, H = im.size

    x0 = a.x0 if a.x0 is not None else W - 152
    y0 = a.y0 if a.y0 is not None else H - 74
    x1 = a.x1 if a.x1 is not None else W
    y1 = a.y1 if a.y1 is not None else H
    w, h = x1 - x0, y1 - y0

    patch = im.crop((x0 - a.off, y0, x1 - a.off, y1))
    if a.blur > 0:
        patch = patch.filter(ImageFilter.GaussianBlur(a.blur))
    mask = build_mask(w, h, a.feather, a.blur, a.corner)
    im.paste(patch, (x0, y0), mask)
    im.save(a.out)
    print(f"saved {a.out} {im.size}")


if __name__ == "__main__":
    main()
