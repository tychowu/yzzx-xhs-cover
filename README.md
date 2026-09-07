# 言直在线专属视频封面生成 Skill

机器名称：`YZZX-cover`

言直在线的专属视频封面生成skill。适用于ip直接根据图像套用模板生成封面图，或根据文案内容自行生成封面。默认输出 4 套真正不同的方案，并在支持图片生成时一次交付 4 张独立封面供比较。

## 文件结构

```text
YZZX-cover/
├── SKILL.md
├── README.md
├── references/
│   ├── cover-design-sop.md
│   └── output-template.md
└── tests/
    └── test-cases.md
```

## 最简单的调用方式

```text
请使用 YZZX-cover Skill，为这期“手把手制作小红书封面 Skill”的视频生成封面。
```

也可以直接描述需求：

```text
为这篇小红书笔记设计封面，先给我 4 套不同方向的方案。
```

## 安装位置

### WorkBuddy：用户级

把整个文件夹复制到：

```text
~/.workbuddy/skills/YZZX-cover/
```

### WorkBuddy：项目级

把整个文件夹复制到项目中的：

```text
.workbuddy/skills/YZZX-cover/
```

安装后可直接用自然语言描述需要制作、优化小红书封面的任务，让 WorkBuddy 自动匹配；或在对话中通过 Skill 工具调用 `YZZX-cover`。

## 版本 1.0 的设计重点

- 输入、输出、执行步骤和验收标准完整。
- 默认生成 4 套真正不同的方向。
- 不伪造官方背书或数据。
- 强制保持一个视觉中心。
- 支持把真实使用中的反馈抽象成新规则。
