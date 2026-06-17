# Wonderverse Docs 🦋

> *Turn an idea into a finished story, video, or campaign — generated end-to-end in a single click.*

Wonderverse 用户手册的源代码与静态站点。中 / 日 / 英三语版本。

## 目录结构

```
.
├── wonderverse-docs-zh.md    中文版源（29 章 Markdown）
├── wonderverse-docs-ja.md    日文版源
├── wonderverse-docs-en.md    英文版源
└── wonderverse-site/         静态站点输出
    ├── index.html            中文版入口
    ├── ja/index.html         日文版入口
    ├── en/index.html         英文版入口
    └── assets/               logo 等静态资源
```

## 站点特性

- 🎨 深色 + Playfair Display + 思源黑体的极简高级设计
- 📐 14+ 张内嵌 SVG 图示（流程图、决策树、节点解剖图等）
- 🌍 严格单语原则，三个版本互不混杂
- 🔀 顶栏中 / 日 / EN 真切换，跨语言保持当前章节
- 📱 响应式，移动端可读

## 部署

Vercel 自动部署。push 到 `main` 分支即触发。

- **生产环境根目录**：`wonderverse-site/`
- **构建命令**：无（已预 build）
- **输出目录**：`./`

## 本地开发

修改 Markdown 源后重建静态站点：

```bash
python3 /tmp/wv_build3.py
```

本地预览：

```bash
cd wonderverse-site && python3 -m http.server 9527
```

打开 [http://localhost:9527/](http://localhost:9527/)。

---

© 2026 Wonderverse
