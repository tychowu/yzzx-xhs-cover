#!/usr/bin/env node
// YZZX-cover 风格测试生成脚本
// 用法见 SKILL.md「风格学习工作流 / Phase 3」
// 设计：读取 references/styles/<style>.json 中的 prompt，组合标题与禁止事项，
// 调用可配置的图像生成后端。未配置后端时直接输出最终 prompt，便于在 WorkBuddy 中用 ImageGen 生成。

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = resolve(__dirname, '..');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const val = argv[i + 1];
      if (val === undefined || val.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = val;
        i++;
      }
    }
  }
  return args;
}

const args = parseArgs(process.argv);
const image = args.image;
const style = args.style;
const title = args.title || '5 个让生活变好的小习惯';
const aspectRatio = args['aspect-ratio'] || '3:4';
const label = args.label || '{{系列标签文案}}';
const outputDir = args['output-dir'] || join(process.cwd(), 'output', 'style-tests', style || 'unclassified');

if (!style) {
  console.error('❌ 缺少 --style 参数（风格 ID，即 references/styles/ 下 .json 文件名去掉后缀）');
  process.exit(1);
}

const styleFile = join(SKILL_DIR, 'references', 'styles', `${style}.json`);
if (!existsSync(styleFile)) {
  console.error(`❌ 风格文件不存在：${styleFile}`);
  process.exit(1);
}

let styleDef;
try {
  styleDef = JSON.parse(readFileSync(styleFile, 'utf8'));
} catch (e) {
  console.error('❌ 风格 JSON 解析失败：', e.message);
  process.exit(1);
}

const prompt = [
  styleDef.prompt,
  `标题文案：${title}`,
  `画布比例：${aspectRatio}`,
  `系列标签文案：${label}（若用户未指定，需先询问用户具体内容，不要用固定文字写死）`,
  image ? `参考人物 / 产品图：${image}（保留原人物，仅套用上述风格，禁止修改人脸）` : '',
  '禁止事项：禁止生成多余文字、禁止修改人脸与人物特征、禁止添加文案之外的信息',
].filter(Boolean).join('\n');

console.log('🎨 组装后的生图 Prompt：\n' + prompt + '\n');

const provider = process.env.IMAGE_PROVIDER;
if (!provider) {
  console.log(
    'ℹ️  未设置 IMAGE_PROVIDER，已输出最终 prompt。\n' +
    '   方式一：在 WorkBuddy 中直接调用 ImageGen 工具，粘贴上述 prompt 生成。\n' +
    '   方式二：设置 IMAGE_PROVIDER=openai 并配置 OPENAI_API_KEY 后重跑本脚本实际出图。'
  );
  process.exit(0);
}

async function generateWithOpenAI() {
  const key = process.env.OPENAI_API_KEY;
  if (!key) {
    console.error('❌ 未设置 OPENAI_API_KEY');
    process.exit(1);
  }
  const size =
    aspectRatio === '3:4' ? '1152x1536' :
    aspectRatio === '16:9' ? '1536x1024' : '1024x1024';
  const resp = await fetch('https://api.openai.com/v1/images/generations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${key}` },
    body: JSON.stringify({ model: 'gpt-image-1', prompt, size, n: 1 }),
  });
  const data = await resp.json();
  if (!resp.ok) {
    console.error('❌ 生图失败：', JSON.stringify(data).slice(0, 500));
    process.exit(1);
  }
  const b64 = data.data?.[0]?.b64_json;
  if (!b64) {
    console.error('❌ 返回中无图片数据');
    process.exit(1);
  }
  mkdirSync(outputDir, { recursive: true });
  const out = join(outputDir, `${style}-${Date.now()}.png`);
  writeFileSync(out, Buffer.from(b64, 'base64'));
  console.log('✅ 已生成：', out);
}

if (provider === 'openai') {
  await generateWithOpenAI();
} else {
  console.error('❌ 不支持的 IMAGE_PROVIDER：', provider, '（当前仅支持 openai）');
  process.exit(1);
}
