#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Wonderverse docs static site — 三语版本（中 / 日 / 英）."""
import re, os, json, hashlib
from markdown_it import MarkdownIt

ROOT = '/Users/bella/WorkBuddy/20260616115607'
OUT_DIR = f'{ROOT}/wonderverse-site'
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(f'{OUT_DIR}/ja', exist_ok=True)
os.makedirs(f'{OUT_DIR}/en', exist_ok=True)

# 暂时禁用的章节（规则未定，灰显示 + 不可点击 + 加 🚧 标签）
# 4 = 团队与权限, 18 = 营销视频, 27 = FAQ, 28 = 计费与发票, 29 = 联系我们
DISABLED_CHAPTERS = {4, 18, 27, 28, 29}

# 资源版本戳
def asset_hash(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()[:8]
    except FileNotFoundError:
        return 'na'
LOGO_PNG_V = asset_hash(os.path.join(OUT_DIR, 'assets/logo-butterfly.png'))

# 三种语言的配置
LANGS = {
    'zh': {
        'src': f'{ROOT}/wonderverse-docs-zh.md',
        'out_path': f'{OUT_DIR}/index.html',
        'logo_href': '/assets/logo-butterfly.png',
        'home_url': '/',
        'urls': {'zh': '/', 'ja': '/ja/', 'en': '/en/'},
        'lang_attr': 'zh-CN',
        'title': 'Wonderverse · 用户手册',
        'brand_tag': '用户手册 · v0.1',
        'topbar_pill': '手册',
        'topbar_sub': '用户手册',
        'menu_label': '目录',
        'chapter_word': lambda n: f'第 {n:02d} 章',
        'prev_label': '上一章',
        'next_label': '下一章',
        'separator': '·',
        'og_locale': 'zh_CN',
        'og_image': '/assets/og-zh.png',
        'og_description': '一键全流程生成，轻松将创意转化为完整故事、成片视频或营销活动方案。',
        'groups': [
            ('🚀', '开始使用', list(range(1, 5))),
            ('🧰', 'AI 工具', list(range(5, 14))),
            ('🎯', '场景方案', list(range(14, 19))),
            ('🎨', '无限画布', list(range(19, 24))),
            ('💡', '最佳实践', list(range(24, 27))),
            ('📚', '帮助', list(range(27, 30))),
        ],
    },
    'ja': {
        'src': f'{ROOT}/wonderverse-docs-ja.md',
        'out_path': f'{OUT_DIR}/ja/index.html',
        'logo_href': '/assets/logo-butterfly.png',
        'home_url': '/ja/',
        'urls': {'zh': '/', 'ja': '/ja/', 'en': '/en/'},
        'lang_attr': 'ja-JP',
        'title': 'Wonderverse · ユーザーマニュアル',
        'brand_tag': 'ユーザーマニュアル · v0.1',
        'topbar_pill': 'マニュアル',
        'topbar_sub': 'ユーザーマニュアル',
        'menu_label': '目次',
        'chapter_word': lambda n: f'第 {n:02d} 章',
        'prev_label': '前の章',
        'next_label': '次の章',
        'separator': '·',
        'og_locale': 'ja_JP',
        'og_image': '/assets/og-ja.png',
        'og_description': 'ワンクリックで、アイデアを物語・映像・キャンペーンへ。',
        'groups': [
            ('🚀', 'はじめに', list(range(1, 5))),
            ('🧰', 'AI ツール', list(range(5, 14))),
            ('🎯', 'シナリオ', list(range(14, 19))),
            ('🎨', '無限キャンバス', list(range(19, 24))),
            ('💡', 'ベストプラクティス', list(range(24, 27))),
            ('📚', 'ヘルプ', list(range(27, 30))),
        ],
    },
    'en': {
        'src': f'{ROOT}/wonderverse-docs-en.md',
        'out_path': f'{OUT_DIR}/en/index.html',
        'logo_href': '/assets/logo-butterfly.png',
        'home_url': '/en/',
        'urls': {'zh': '/', 'ja': '/ja/', 'en': '/en/'},
        'lang_attr': 'en-US',
        'title': 'Wonderverse · User Manual',
        'brand_tag': 'User Manual · v0.1',
        'topbar_pill': 'Docs',
        'topbar_sub': 'User Manual',
        'menu_label': 'Menu',
        'chapter_word': lambda n: f'Chapter {n:02d}',
        'prev_label': 'Previous',
        'next_label': 'Next',
        'separator': '·',
        'og_locale': 'en_US',
        'og_image': '/assets/og-en.png',
        'og_description': 'Turn an idea into a finished story, video, or campaign — generated end-to-end in a single click.',
        'groups': [
            ('🚀', 'Getting Started', list(range(1, 5))),
            ('🧰', 'AI Tools', list(range(5, 14))),
            ('🎯', 'Scenarios', list(range(14, 19))),
            ('🎨', 'Studio', list(range(19, 24))),
            ('💡', 'Best Practices', list(range(24, 27))),
            ('📚', 'Help', list(range(27, 30))),
        ],
    },
}

md = MarkdownIt('commonmark', {'html': True, 'linkify': True, 'typographer': True}).enable('table').enable('strikethrough')

FIGURE_RE = re.compile(r'<figure[^>]*>.*?</figure>', re.DOTALL)

def render_with_figures(body_md):
    figures = []
    def stash(m):
        figures.append(m.group(0))
        return f'\n\n@@FIG_{len(figures)-1}@@\n\n'
    stashed = FIGURE_RE.sub(stash, body_md)
    html = md.render(stashed)
    for i, fig in enumerate(figures):
        html = html.replace(f'<p>@@FIG_{i}@@</p>', fig)
        html = html.replace(f'@@FIG_{i}@@', fig)
    return html

def add_future_class(html):
    html = re.sub(r'<li>(\s*🚧[^<]*)', r'<li class="future-tag">\1', html)
    html = re.sub(r'<li>(\s*[^<]*🚧)', r'<li class="future-tag">\1', html)
    html = re.sub(r'<h3>(\s*🚧[^<]*)</h3>', r'<h3 class="future-tag">\1</h3>', html)
    html = re.sub(r'<h4>(\s*🚧[^<]*)</h4>', r'<h4 class="future-tag">\1</h4>', html)
    html = re.sub(r'<blockquote>\s*<p>🚧', r'<blockquote class="future-tag"><p>🚧', html)
    return html

TEMPLATE = '''<!DOCTYPE html>
<html lang="__LANG__">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__OG_DESCRIPTION__">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wonderverse">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__OG_DESCRIPTION__">
<meta property="og:image" content="https://wonderverse-docs.vercel.app__OG_IMAGE__">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://wonderverse-docs.vercel.app__HOME_URL__">
<meta property="og:locale" content="__OG_LOCALE__">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="__TITLE__">
<meta name="twitter:description" content="__OG_DESCRIPTION__">
<meta name="twitter:image" content="https://wonderverse-docs.vercel.app__OG_IMAGE__">

<link rel="icon" type="image/png" href="/assets/logo-butterfly.png?v=__LOGO_PNG_V__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,900&family=Inter:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;700;900&family=Noto+Sans+JP:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#0a0a0a;
  --bg-card:#141414;
  --bg-card-hover:#1a1a1a;
  --bg-side:#0d0d0d;
  --text:#e8e8e8;
  --text-dim:#9a9a9a;
  --text-muted:#666;
  --border:#1f1f1f;
  --border-hover:#2a2a2a;
  --accent:#8b8bff;
  --accent-soft:#6e6eff22;
  --green:#7ee787;
  --serif:'Playfair Display','Noto Sans SC',Georgia,serif;
  --sans:'Inter','Noto Sans SC','Noto Sans JP',-apple-system,BlinkMacSystemFont,sans-serif;
}
html,body{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:var(--sans);font-size:15px;line-height:1.7;-webkit-font-smoothing:antialiased}
body{display:flex;min-height:100vh}

.sidebar{width:280px;flex-shrink:0;background:var(--bg-side);border-right:1px solid var(--border);padding:32px 0;position:fixed;top:0;left:0;bottom:0;overflow-y:auto;z-index:10}
.brand{padding:0 28px 28px;border-bottom:1px solid var(--border);margin-bottom:18px;text-decoration:none;color:inherit;display:block}
.brand,.brand:hover,.brand:visited,.brand:active{text-decoration:none}
.brand-logo{display:flex;align-items:center;gap:10px;margin-bottom:6px;cursor:pointer;text-decoration:none}
.brand-logo-icon{width:32px;height:32px;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}
.brand-logo-icon img{width:100%;height:100%;object-fit:contain}
.brand-name{font-family:'Playfair Display',serif;font-style:italic;font-weight:900;font-size:26px;letter-spacing:.3px;color:var(--text)}
.brand-tag{font-size:11px;color:var(--text-muted);letter-spacing:1.5px;margin-top:4px}
.nav-group{padding:14px 18px}
.nav-group-title{font-size:12px;color:var(--text-muted);margin:0 10px 10px;font-weight:600;display:flex;align-items:center;gap:8px;letter-spacing:.5px}
.nav-emoji{font-size:14px}
.nav-list{list-style:none;padding:0;margin:0}
.nav-list li{margin:0}
.nav-list a{display:block;padding:8px 12px;color:var(--text-dim);text-decoration:none;border-radius:6px;font-size:13.5px;transition:all .15s}
.nav-list a:hover{background:var(--bg-card);color:var(--text)}
.nav-list a.active{background:var(--accent-soft);color:var(--accent);font-weight:500}
.nav-list li.disabled span{display:block;padding:8px 12px;color:#555;font-size:13.5px;cursor:not-allowed;border-radius:6px;user-select:none}
.nav-list li.disabled span:hover{background:transparent}

.main{flex:1;margin-left:280px;padding:80px 0 120px;min-height:100vh}
.page{max-width:760px;margin:0 auto;padding:0 64px}
.crumb{font-size:12px;color:var(--text-muted);letter-spacing:1px;margin-bottom:16px;font-weight:500;font-feature-settings:"lnum" 1,"tnum" 1}
.page-title{font-family:'Inter','Noto Sans SC',sans-serif;font-size:64px;font-weight:800;line-height:1.1;letter-spacing:-2px;margin:0 0 28px;font-feature-settings:"lnum" 1,"tnum" 0}
@media(max-width:900px){.page-title{font-size:48px}}

.content{font-size:15.5px;line-height:1.75}
.content p{margin:0 0 18px}
.content h2{font-family:'Inter','Noto Sans SC',sans-serif;font-size:32px;font-weight:700;letter-spacing:-.5px;margin:48px 0 18px;color:var(--text);border-top:1px solid var(--border);padding-top:36px;font-feature-settings:"lnum" 1,"tnum" 0}
.content h2:first-child{border-top:none;padding-top:0;margin-top:32px}
.content h3{font-size:18px;font-weight:600;margin:32px 0 12px;color:var(--text)}
.content h4{font-size:14.5px;font-weight:600;margin:24px 0 10px;color:var(--text-dim);letter-spacing:.3px}
.content ul,.content ol{padding-left:24px;margin:0 0 18px}
.content li{margin:6px 0}
.content blockquote{border-left:2px solid var(--accent);background:var(--accent-soft);margin:18px 0;padding:14px 20px;color:var(--text-dim);border-radius:0 6px 6px 0;font-size:14.5px}
.content blockquote p{margin:0}
.content blockquote p + p{margin-top:8px}
.content blockquote em,.content blockquote i{font-family:'Playfair Display','Noto Sans SC',serif;font-style:italic;font-size:14.5px;color:var(--text);font-weight:500;letter-spacing:.2px}
.content code{background:var(--bg-card);padding:2px 8px;border-radius:4px;font-family:'SF Mono',Menlo,monospace;font-size:12.5px;color:var(--accent)}
.content pre{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:16px 18px;overflow-x:auto;font-size:12.5px;line-height:1.55;margin:18px 0}
.content pre code{background:none;padding:0;color:var(--text);font-size:12.5px}
.content a{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent;transition:border-color .15s}
.content a:hover{border-color:var(--accent)}
.content strong{color:var(--text);font-weight:600}
.content hr{border:none;border-top:1px solid var(--border);margin:36px 0}

.content table{width:100%;border-collapse:collapse;margin:18px 0;font-size:14px;background:var(--bg-card);border-radius:8px;overflow:hidden;table-layout:auto}
.content th,.content td{padding:14px 18px;text-align:left;border-bottom:1px solid var(--border);vertical-align:top;line-height:1.6}
.content th{background:var(--bg-card-hover);font-weight:600;color:var(--text);font-size:13px;letter-spacing:.3px;white-space:nowrap}
.content td{color:var(--text-dim)}
.content tr:last-child td{border-bottom:none}
.content td:first-child{white-space:nowrap;color:var(--text);font-weight:500}
.content td:last-child{white-space:normal}
.content table.two-col td{width:50%}

.content em,.content i{color:var(--text-dim);font-style:italic}

/* Figure & SVG diagrams */
.content figure{margin:32px 0;padding:0}
.content figure.diagram{display:flex;justify-content:center;background:transparent}
.content figure svg{width:100%;max-width:720px;height:auto;display:block}
.content figcaption{text-align:center;color:var(--text-muted);font-size:12.5px;margin-top:10px;letter-spacing:.5px}
.wv-svg .wv-card{transition:transform .25s ease, filter .25s ease}
.wv-svg .wv-card:hover{transform:translateY(-2px);filter:drop-shadow(0 4px 12px rgba(139,139,255,0.25))}
.wv-svg .wv-card rect{transition:stroke .25s ease}
.wv-svg .wv-card:hover rect{stroke:#8b8bff !important}

/* 🚧 即将上线 标签 */
.future-tag{opacity:.78;color:var(--text-dim) !important}
.future-tag strong{color:var(--text-dim) !important}
.future-tag a{color:var(--text-dim) !important}

.pager{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:80px;padding-top:32px;border-top:1px solid var(--border)}
.pager a{display:block;padding:18px 22px;background:var(--bg-card);border:1px solid var(--border);border-radius:10px;text-decoration:none;transition:all .2s}
.pager a:hover{background:var(--bg-card-hover);border-color:var(--border-hover);transform:translateY(-2px)}
.pager-dir{font-size:11px;color:var(--text-muted);letter-spacing:.5px;margin-bottom:6px}
.pager-title{color:var(--text);font-size:15px;font-weight:500}
.pager-prev{text-align:left}
.pager-next{text-align:right}
.pager-empty{visibility:hidden}

.topbar{position:fixed;top:0;left:280px;right:0;height:56px;background:rgba(10,10,10,.88);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;padding:0 64px;z-index:9}
.topbar-left{display:flex;align-items:center;gap:12px}
.menu-btn{display:none;align-items:center;gap:7px;background:var(--bg-card);border:1px solid var(--border);color:var(--text);padding:7px 13px 7px 11px;border-radius:8px;font-family:inherit;font-size:13px;font-weight:500;cursor:pointer;transition:all .15s}
.menu-btn:hover{border-color:var(--border-hover);background:var(--bg-card-hover)}
.menu-btn:active{transform:scale(.97)}
.menu-btn svg{display:block;flex-shrink:0}
.topbar-pill{font-size:11px;color:var(--green);letter-spacing:.5px;background:#7ee78711;border:1px solid #7ee78733;padding:3px 12px;border-radius:99px;display:flex;align-items:center;gap:6px}
.topbar-pill::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--green)}
.topbar-sub{font-size:13px;color:var(--text-muted)}
.topbar-right{display:flex;gap:8px;align-items:center}
.lang-switcher{display:flex;background:var(--bg-card);border:1px solid var(--border);border-radius:8px;overflow:hidden}
.lang-switcher a{background:none;border:none;color:var(--text-dim);padding:6px 14px;font-size:12px;cursor:pointer;font-family:inherit;letter-spacing:.5px;text-decoration:none;display:inline-block}
.lang-switcher a.active{background:var(--accent-soft);color:var(--accent)}
.lang-switcher a:hover:not(.active){color:var(--text)}

::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#222;border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:#333}

/* ==================== 移动端抽屉边缘热区 + Mask ==================== */
.edge-trigger{position:fixed;top:0;left:0;width:18px;height:100vh;z-index:8;display:none;background:linear-gradient(to right,rgba(139,139,255,.08),transparent);cursor:e-resize}
.edge-trigger::after{content:'';position:absolute;top:50%;left:4px;width:3px;height:48px;border-radius:2px;background:var(--border-hover);transform:translateY(-50%)}
.sidebar-mask{position:fixed;inset:0;background:rgba(0,0,0,.5);backdrop-filter:blur(2px);z-index:19;opacity:0;pointer-events:none;transition:opacity .25s ease}
body.drawer-open .sidebar-mask{opacity:1;pointer-events:auto}

/* ==================== 移动端响应式 ≤900px ==================== */
@media(max-width:900px){
  /* 侧栏：默认隐藏，从左边缘滑入 */
  .sidebar{transform:translateX(-100%);transition:transform .28s cubic-bezier(.4,0,.2,1);width:84vw;max-width:320px;z-index:20;box-shadow:0 0 30px rgba(0,0,0,.6)}
  body.drawer-open .sidebar{transform:translateX(0)}
  .edge-trigger{display:block}

  /* 主内容区：全宽 */
  .main{margin-left:0;padding:64px 0 80px}
  .topbar{left:0;padding:0 16px;height:52px;gap:8px}
  .topbar-sub{display:none}
  .topbar-pill{display:none}
  .menu-btn{display:inline-flex}
  .lang-switcher a{padding:5px 10px;font-size:11px}
  .page{padding:0 22px;max-width:100%}

  /* 字号缩小 */
  .page-title{font-size:38px;letter-spacing:-1px;line-height:1.15;margin-bottom:20px}
  .crumb{font-size:11px;margin-bottom:12px}
  .content{font-size:15px;line-height:1.7}
  .content h2{font-size:24px;margin:36px 0 14px;padding-top:28px}
  .content h2:first-child{margin-top:24px}
  .content h3{font-size:16.5px;margin:24px 0 10px}
  .content h4{font-size:13.5px;margin:18px 0 8px}
  .content blockquote{padding:12px 16px;font-size:14px}
  .content blockquote em,.content blockquote i{font-size:13.5px}
  .content ul,.content ol{padding-left:20px}
  .content pre{padding:12px 14px;font-size:11.5px}
  .content code{font-size:12px;padding:1.5px 6px}

  /* 表格：横向滚动，不再 nowrap 第一列 */
  .content table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;font-size:13px;border-radius:8px}
  .content th,.content td{padding:10px 12px}
  .content td:first-child{white-space:nowrap}

  /* SVG 图：保持比例，可横向滚动兜底 */
  .content figure.diagram{margin:24px -8px;overflow-x:auto;-webkit-overflow-scrolling:touch}
  .content figure svg{min-width:520px}

  /* 翻页改成上下排列 */
  .pager{grid-template-columns:1fr;gap:10px;margin-top:56px;padding-top:24px}
  .pager a{padding:14px 18px}
  .pager-next{text-align:left}
}
@media(max-width:480px){
  .page-title{font-size:32px}
  .content h2{font-size:21px}
}

</style>
</head>
<body>

<div class="edge-trigger" id="edgeTrigger" aria-label="打开导航"></div>
<div class="sidebar-mask" id="sidebarMask"></div>

<aside class="sidebar">
  <a class="brand" href="__HOME_URL__">
    <div class="brand-logo">
      <span class="brand-logo-icon">
        <img src="/assets/logo-butterfly.png?v=__LOGO_PNG_V__" alt="Wonderverse">
      </span>
      <span class="brand-name">Wonderverse</span>
    </div>
    <div class="brand-tag">__BRAND_TAG__</div>
  </a>
  __SIDEBAR__
</aside>

<header class="topbar">
  <div class="topbar-left">
    <button class="menu-btn" id="menuBtn" aria-label="__MENU_LABEL__">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
      <span>__MENU_LABEL__</span>
    </button>
    <span class="topbar-pill">__TOPBAR_PILL__</span>
    <span class="topbar-sub">__TOPBAR_SUB__</span>
  </div>
  <div class="topbar-right">
    <div class="lang-switcher">
      <a href="__URL_ZH__" class="__ACTIVE_ZH__">中</a>
      <a href="__URL_JA__" class="__ACTIVE_JA__">日</a>
      <a href="__URL_EN__" class="__ACTIVE_EN__">EN</a>
    </div>
  </div>
</header>

<main class="main">
  <article class="page" id="page">
    <div class="crumb" id="crumb"></div>
    <h1 class="page-title" id="title"></h1>
    <div class="content" id="content"></div>
    <nav class="pager" id="pager"></nav>
  </article>
</main>

<script>
const CHAPTERS = __CHAPTERS_JSON__;
const GROUPS = __GROUPS_JSON__;
const SEP = '__SEP__';
const PREV_LABEL = '__PREV_LABEL__';
const NEXT_LABEL = '__NEXT_LABEL__';
const CHAPTER_FORMAT = (n) => __CHAPTER_FORMAT__;

function chapterCrumb(num){
  for(const g of GROUPS){
    if(g.nums.includes(num)){
      return g.label;
    }
  }
  return '';
}

function escapeHtml(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function titleHtml(t){return escapeHtml(t).split('|||').join('<br>');}
function titleText(t){return String(t).split('|||').join(' ');}

const DISABLED = __DISABLED_JSON__;
function isDisabled(n){return DISABLED.indexOf(n) !== -1;}
function nextEnabled(n, dir){
  let i = n + dir;
  while(i >= 1 && i <= CHAPTERS.length){
    if(!isDisabled(i)) return CHAPTERS[i-1];
    i += dir;
  }
  return null;
}

function goto(num){
  // 禁用章节 → 跳到第 1 章
  if(isDisabled(num)){ num = 1; }
  const c = CHAPTERS[num-1];
  if(!c) return;
  const group = chapterCrumb(num);
  document.getElementById('crumb').textContent = group + ' ' + SEP + ' ' + CHAPTER_FORMAT(num);
  document.getElementById('title').innerHTML = titleHtml(c.title);
  document.getElementById('content').innerHTML = c.html;
  const pager = document.getElementById('pager');
  const prev = nextEnabled(num, -1);
  const next = nextEnabled(num, +1);
  pager.innerHTML = `
    ${prev ? `<a class="pager-prev" href="javascript:void(0)" onclick="goto(${prev.num})">
       <div class="pager-dir">← ${PREV_LABEL}</div>
       <div class="pager-title">${escapeHtml(titleText(prev.title))}</div>
     </a>` : '<div class="pager-empty"></div>'}
    ${next ? `<a class="pager-next" href="javascript:void(0)" onclick="goto(${next.num})">
       <div class="pager-dir">${NEXT_LABEL} →</div>
       <div class="pager-title">${escapeHtml(titleText(next.title))}</div>
     </a>` : '<div class="pager-empty"></div>'}
  `;
  document.querySelectorAll('.nav-list a').forEach(a => a.classList.toggle('active', Number(a.dataset.ch) === num));
  window.scrollTo({top:0, behavior:'smooth'});
  history.replaceState(null, '', '#ch-' + num);
  closeDrawer();
}

// === 移动端抽屉控制 ===
function openDrawer(){document.body.classList.add('drawer-open');}
function closeDrawer(){document.body.classList.remove('drawer-open');}
document.getElementById('menuBtn').addEventListener('click', openDrawer);
document.getElementById('edgeTrigger').addEventListener('click', openDrawer);
document.getElementById('sidebarMask').addEventListener('click', closeDrawer);
// 触摸边缘滑动也能开
let touchStartX = null;
document.addEventListener('touchstart', e=>{
  if(window.innerWidth > 900) return;
  if(e.touches[0].clientX < 24) touchStartX = e.touches[0].clientX;
}, {passive:true});
document.addEventListener('touchmove', e=>{
  if(touchStartX === null) return;
  const dx = e.touches[0].clientX - touchStartX;
  if(dx > 50){openDrawer(); touchStartX = null;}
}, {passive:true});
document.addEventListener('touchend', ()=>{ touchStartX = null; }, {passive:true});

const initial = parseInt((location.hash.match(/ch-(\\d+)/)||[])[1]||'1', 10);
goto(initial);
</script>

</body>
</html>
'''

def build_for_lang(lang_code, cfg):
    src_path = cfg['src']
    if not os.path.exists(src_path):
        print(f'[{lang_code}] 源文件不存在: {src_path} — 跳过')
        return False
    src = open(src_path).read()
    chapter_re = re.compile(r'^## (\d+)\. (.+)$', re.MULTILINE)
    matches = list(chapter_re.finditer(src))
    chapters = []
    for i, m in enumerate(matches):
        num = int(m.group(1))
        title = m.group(2).strip()
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(src)
        body = src[start:end].strip()
        body = re.sub(r'\n---\s*$', '', body).strip()
        body = re.sub(r'\n+---\s*\n+#\s+[^\n]+\s*\n*---\s*$', '', body).strip()
        body = re.sub(r'\n+---\s*\n+#\s+[^\n]+\s*$', '', body).strip()
        chapters.append({'num': num, 'title': title, 'body': body})

    groups = cfg['groups']
    sidebar_parts = []
    for emoji, label, nums in groups:
        sidebar_parts.append(f'<div class="nav-group"><div class="nav-group-title"><span class="nav-emoji">{emoji}</span>{label}</div><ul class="nav-list">')
        for n in nums:
            if n <= len(chapters):
                c = chapters[n-1]
                sidebar_title = c["title"].replace("|||", " ")
                if n in DISABLED_CHAPTERS:
                    sidebar_parts.append(f'<li class="disabled"><span data-ch="{n}">🚧 {sidebar_title}</span></li>')
                else:
                    sidebar_parts.append(f'<li><a href="javascript:void(0)" onclick="goto({n})" data-ch="{n}">{sidebar_title}</a></li>')
        sidebar_parts.append('</ul></div>')
    sidebar_html = '\n'.join(sidebar_parts)

    for c in chapters:
        c['html'] = render_with_figures(c['body'])
        def fix_link(m):
            href = m.group(1)
            anchor = href.lstrip('#')
            m_num = re.match(r'^(\d+)', anchor)
            if m_num:
                target = int(m_num.group(1))
                if 1 <= target <= 29:
                    return f'href="javascript:void(0)" onclick="goto({target})"'
            return m.group(0)
        c['html'] = re.sub(r'href="(#[^"]+)"', fix_link, c['html'])
        c['html'] = add_future_class(c['html'])

    chapters_data = [{'num': c['num'], 'title': c['title'], 'html': c['html']} for c in chapters]
    groups_for_js = [{'label': g[1], 'nums': g[2]} for g in groups]

    # 拼接 chapter format JS
    if lang_code == 'en':
        cf = '`Chapter ${String(n).padStart(2,"0")}`'
    elif lang_code == 'ja':
        cf = '`第 ${String(n).padStart(2,"0")} 章`'
    else:
        cf = '`第 ${String(n).padStart(2,"0")} 章`'

    urls = cfg['urls']
    active_zh = 'active' if lang_code == 'zh' else ''
    active_ja = 'active' if lang_code == 'ja' else ''
    active_en = 'active' if lang_code == 'en' else ''

    site = TEMPLATE
    site = site.replace('__LANG__', cfg['lang_attr'])
    site = site.replace('__TITLE__', cfg['title'])
    site = site.replace('__BRAND_TAG__', cfg['brand_tag'])
    site = site.replace('__TOPBAR_PILL__', cfg['topbar_pill'])
    site = site.replace('__TOPBAR_SUB__', cfg['topbar_sub'])
    site = site.replace('__MENU_LABEL__', cfg['menu_label'])
    site = site.replace('__PREV_LABEL__', cfg['prev_label'])
    site = site.replace('__NEXT_LABEL__', cfg['next_label'])
    site = site.replace('__SEP__', cfg['separator'])
    site = site.replace('__CHAPTER_FORMAT__', cf)
    site = site.replace('__HOME_URL__', cfg['home_url'])
    site = site.replace('__OG_LOCALE__', cfg['og_locale'])
    site = site.replace('__OG_IMAGE__', cfg['og_image'])
    site = site.replace('__OG_DESCRIPTION__', cfg['og_description'])
    site = site.replace('__URL_ZH__', urls['zh'])
    site = site.replace('__URL_JA__', urls['ja'])
    site = site.replace('__URL_EN__', urls['en'])
    site = site.replace('__ACTIVE_ZH__', active_zh)
    site = site.replace('__ACTIVE_JA__', active_ja)
    site = site.replace('__ACTIVE_EN__', active_en)
    site = site.replace('__SIDEBAR__', sidebar_html)
    site = site.replace('__LOGO_PNG_V__', LOGO_PNG_V)
    site = site.replace('__CHAPTERS_JSON__', json.dumps(chapters_data, ensure_ascii=False))
    site = site.replace('__GROUPS_JSON__', json.dumps(groups_for_js, ensure_ascii=False))
    site = site.replace('__DISABLED_JSON__', json.dumps(sorted(DISABLED_CHAPTERS)))

    with open(cfg['out_path'], 'w') as f:
        f.write(site)
    print(f'[{lang_code}] Built: chapters={len(chapters_data)}, html_size={len(site)} bytes')
    return True

# 构建所有语言版本
for lang_code, cfg in LANGS.items():
    build_for_lang(lang_code, cfg)
