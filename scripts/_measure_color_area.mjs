// 量化原参考图四色（红/紫/粉/绿）占全图的像素比例，作为风格生成时的占比基准。
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import jpeg from 'jpeg-js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dir = '/Users/tychowu/Desktop/封面';
const files = fs.readdirSync(dir).filter(f => /Screenshot_2026-09-07/.test(f));

// 四色 hex（与原风格 JSON 一致）
const TARGETS = {
  red:   [0xAA, 0x25, 0x16],
  purple:[0x7D, 0x6C, 0xC8],
  pink:  [0xDD, 0x83, 0x9D],
  green: [0x11, 0xAC, 0x42],
};

function near(r, g, b, [tr, tg, tb], tol = 48) {
  return Math.abs(r - tr) <= tol && Math.abs(g - tg) <= tol && Math.abs(b - tb) <= tol;
}

for (const f of files) {
  const buf = fs.readFileSync(path.join(dir, f));
  const { data, width, height } = jpeg.decode(buf, { useTArray: true });
  const total = width * height;
  const counts = { red: 0, purple: 0, pink: 0, green: 0 };
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i], g = data[i + 1], b = data[i + 2];
    for (const k in TARGETS) {
      if (near(r, g, b, TARGETS[k])) { counts[k]++; break; }
    }
  }
  const pct = k => ((counts[k] / total) * 100).toFixed(2) + '%';
  console.log(`${f}`);
  console.log(`  尺寸 ${width}x${height} | 红 ${pct('red')} | 紫 ${pct('purple')} | 粉 ${pct('pink')} | 绿 ${pct('green')} | 合计 ${((Object.values(counts).reduce((a,c)=>a+c,0)/total)*100).toFixed(2)}%`);
}
