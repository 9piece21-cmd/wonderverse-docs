"""生成 Wonderverse OG 卡片三张：zh / ja / en
布局：左右型 (ii) — 左 1/3 蝴蝶 logo，右 2/3 文字
规格：1200x630 PNG
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = '/Users/bella/WorkBuddy/20260616115607/wonderverse-site/assets'
LOGO_PATH = os.path.join(OUT_DIR, 'logo-butterfly.png')

# 字体
F_PLAYFAIR_ITALIC = '/tmp/wv_fonts/PlayfairDisplay-Italic.ttf'
F_PLAYFAIR = '/tmp/wv_fonts/PlayfairDisplay.ttf'
F_HIRAGINO_GB = '/System/Library/Fonts/Hiragino Sans GB.ttc'  # 中文黑体
F_HIRAGINO_JP_W6 = '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'  # 日文黑体
F_HIRAGINO_JP_W3 = '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'
F_INTER_FALLBACK = '/System/Library/Fonts/HelveticaNeue.ttc'

W, H = 1200, 630
BG = (10, 10, 10)
ACCENT = (139, 139, 255)
TEXT = (232, 232, 240)
DIM = (154, 154, 170)
MUTED = (102, 102, 122)

def load_font(path, size, index=0):
    try:
        if path.endswith('.ttc'):
            return ImageFont.truetype(path, size, index=index)
        return ImageFont.truetype(path, size)
    except Exception as e:
        print(f'⚠️  字体加载失败 {path}: {e}')
        return ImageFont.load_default()

def draw_card(out_path, locale, brand_caption, headline_serif, slogan, slogan_font_path, slogan_size, slogan_index=0, headline_index=0):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img, 'RGBA')

    # 背景紫色光晕（左下角）
    for r, alpha in [(420, 14), (320, 18), (220, 22)]:
        d.ellipse([-100, H-r, -100+r*2, H+r], fill=(139, 139, 255, alpha))
    # 右上角光晕
    for r, alpha in [(380, 10), (280, 14)]:
        d.ellipse([W-r, -r//2, W+r, r//2+r], fill=(139, 139, 255, alpha))

    # 边框装饰：极细紫色线
    d.rectangle([24, 24, W-24, H-24], outline=(40, 40, 60), width=1)

    # === 左 1/3：蝴蝶 logo ===
    logo = Image.open(LOGO_PATH).convert('RGBA')
    target_h = 280
    ratio = target_h / logo.height
    logo_resized = logo.resize((int(logo.width * ratio), target_h), Image.LANCZOS)
    # 居中放在左 1/3 区域
    logo_x = (W // 3 - logo_resized.width) // 2 + 30
    logo_y = (H - logo_resized.height) // 2
    img.paste(logo_resized, (logo_x, logo_y), logo_resized)

    # 左右分隔线
    sep_x = W // 3 + 60
    d.line([sep_x, 130, sep_x, H - 130], fill=(40, 40, 60), width=1)

    # === 右 2/3：文字 ===
    text_x = sep_x + 50

    # 顶部小标 caption（如 "USER MANUAL · 中文版"）
    f_caption = load_font(F_PLAYFAIR, 18)
    d.text((text_x, 130), brand_caption, font=f_caption, fill=MUTED)

    # 紫色短分隔线
    d.line([text_x, 165, text_x + 36, 165], fill=ACCENT, width=2)

    # 大标题 Wonderverse（衬线斜体粗）
    f_brand = load_font(F_PLAYFAIR_ITALIC, 96)
    d.text((text_x, 188), 'Wonderverse', font=f_brand, fill=TEXT)

    # Slogan（本地化语言）— 自动换行
    f_slogan = load_font(slogan_font_path, slogan_size, index=slogan_index)
    max_text_width = W - text_x - 80
    lines = wrap_text(slogan, f_slogan, max_text_width, d)
    y = 320
    for line in lines:
        d.text((text_x, y), line, font=f_slogan, fill=DIM)
        y += slogan_size + 10

    # 底部域名
    f_url = load_font(F_PLAYFAIR, 16)
    d.text((text_x, H - 90), 'wonderverse-docs.vercel.app', font=f_url, fill=MUTED)

    img.save(out_path, 'PNG', optimize=True)
    print(f'✓ {out_path}  {os.path.getsize(out_path)//1024} KB')

def wrap_text(text, font, max_width, draw):
    """按 max_width 换行；优先按标点符号断"""
    if not text:
        return ['']
    # 先看整段宽度，能放下就一行
    bbox = draw.textbbox((0, 0), text, font=font)
    if bbox[2] - bbox[0] <= max_width:
        return [text]
    # 尝试按标点（中英日）断
    breakers = ['，', '、', '。', ',', '. ', ' — ', '・']
    for b in breakers:
        if b in text:
            parts = text.split(b)
            # 拼成两行试试
            for i in range(1, len(parts)):
                line1 = b.join(parts[:i]) + (b if b not in [' — '] else b.rstrip())
                line2 = b.join(parts[i:])
                bb1 = draw.textbbox((0,0), line1, font=font)
                bb2 = draw.textbbox((0,0), line2, font=font)
                if bb1[2]-bb1[0] <= max_width and bb2[2]-bb2[0] <= max_width:
                    return [line1.strip(), line2.strip()]
    # 兜底：按字符强切
    lines = []
    cur = ''
    for ch in text:
        test = cur + ch
        bb = draw.textbbox((0,0), test, font=font)
        if bb[2]-bb[0] > max_width and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines

# 中文版
draw_card(
    out_path=os.path.join(OUT_DIR, 'og-zh.png'),
    locale='zh',
    brand_caption='USER MANUAL  ·  中文版',
    headline_serif='Wonderverse',
    slogan='一键全流程生成，轻松将创意转化为完整故事、成片视频或营销活动方案。',
    slogan_font_path=F_HIRAGINO_GB,
    slogan_size=28,
    slogan_index=1,  # Hiragino Sans GB W6 (粗) at index 1
)

# 英文版
draw_card(
    out_path=os.path.join(OUT_DIR, 'og-en.png'),
    locale='en',
    brand_caption='USER MANUAL  ·  ENGLISH',
    headline_serif='Wonderverse',
    slogan='Turn an idea into a finished story, video, or campaign — generated end-to-end in a single click.',
    slogan_font_path=F_INTER_FALLBACK,
    slogan_size=28,
    slogan_index=2,  # HelveticaNeue Medium-ish
)

# 日文版
draw_card(
    out_path=os.path.join(OUT_DIR, 'og-ja.png'),
    locale='ja',
    brand_caption='USER MANUAL  ·  日本語版',
    headline_serif='Wonderverse',
    slogan='ワンクリックで、アイデアを物語・映像・キャンペーンへ。',
    slogan_font_path=F_HIRAGINO_JP_W6,
    slogan_size=32,
)

print('\n🦋 OG 卡片三张全部生成完毕')
