from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import urllib.request
import os

# Colors
NAVY       = RGBColor(0x0A, 0x1F, 0x44)   # dark navy background
GOLD       = RGBColor(0xF5, 0xC5, 0x18)   # pirate gold
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
RED        = RGBColor(0xCC, 0x1F, 0x1F)
LIGHT_BLUE = RGBColor(0xD6, 0xEA, 0xF8)
DARK_GOLD  = RGBColor(0xB8, 0x8A, 0x00)
ORANGE     = RGBColor(0xF3, 0x9C, 0x12)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

# ─────────────────────────────────────────────
# Helper: solid fill for a shape
# ─────────────────────────────────────────────
def solid(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

def no_fill(shape):
    shape.fill.background()

def add_rect(slide, l, t, w, h, color, radius=False):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(l), Inches(t), Inches(w), Inches(h)
    )
    solid(shape, color)
    shape.line.fill.background()
    return shape

def add_rounded_rect(slide, l, t, w, h, color):
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    shape = slide.shapes.add_shape(
        5,  # rounded rectangle
        Inches(l), Inches(t), Inches(w), Inches(h)
    )
    solid(shape, color)
    shape.line.fill.background()
    shape.adjustments[0] = 0.05
    return shape

def tf_para(tf, text, size, bold=False, color=WHITE, align=PP_ALIGN.LEFT, italic=False):
    p = tf.add_paragraph()
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return p

def add_textbox(slide, l, t, w, h, text, size, bold=False, color=WHITE,
                align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    # clear default empty paragraph
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


# ══════════════════════════════════════════════════════════════════
# SLIDE 1 — Hero / cover
# ══════════════════════════════════════════════════════════════════
blank_layout = prs.slide_layouts[6]
slide1 = prs.slides.add_slide(blank_layout)

# Full background
bg = add_rect(slide1, 0, 0, 13.33, 7.5, NAVY)

# Decorative gold stripe at top
add_rect(slide1, 0, 0, 13.33, 0.12, GOLD)
# Decorative gold stripe at bottom
add_rect(slide1, 0, 7.38, 13.33, 0.12, GOLD)

# Left gold vertical accent
add_rect(slide1, 0, 0.12, 0.08, 7.26, DARK_GOLD)

# ── Big title ──────────────────────────────────
# Shadow effect rectangle
sh = add_rect(slide1, 0.42, 0.88, 7.8, 1.55, RGBColor(0x05, 0x10, 0x25))
txb = slide1.shapes.add_textbox(Inches(0.4), Inches(0.85), Inches(7.8), Inches(1.6))
txb.word_wrap = False
tf = txb.text_frame
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.LEFT
run = p.add_run()
run.text = "Château Gonflable"
run.font.size = Pt(52)
run.font.bold = True
run.font.color.rgb = WHITE

p2 = tf.add_paragraph()
p2.alignment = PP_ALIGN.LEFT
run2 = p2.add_run()
run2.text = "Pirate"
run2.font.size = Pt(62)
run2.font.bold = True
run2.font.color.rgb = GOLD

# ── Skull & crossbones unicode decoration ──
add_textbox(slide1, 0.4, 0.3, 2, 0.6, "☠  Occasion — Stock limité  ☠",
            13, bold=True, color=GOLD, align=PP_ALIGN.LEFT)

# ── Price badge ────────────────────────────────
badge = add_rounded_rect(slide1, 0.4, 2.65, 3.4, 1.1, RED)
add_textbox(slide1, 0.4, 2.68, 3.4, 0.45, "Prix HT", 14, color=WHITE,
            align=PP_ALIGN.CENTER, bold=False)
add_textbox(slide1, 0.4, 3.02, 3.4, 0.7, "1 700,00 €", 34, bold=True,
            color=WHITE, align=PP_ALIGN.CENTER)

# ── Tagline ────────────────────────────────────
add_textbox(slide1, 0.4, 3.95, 6, 0.5,
            "Multiactivités · Toboggan · Escalade · Parcours",
            15, color=LIGHT_BLUE, align=PP_ALIGN.LEFT, italic=True)

# ── Specs quick-view ──────────────────────────
specs_bg = add_rounded_rect(slide1, 0.4, 4.6, 5.6, 2.55, RGBColor(0x10, 0x2A, 0x5E))

specs = [
    ("📐", "Dimensions",  "L 8 m × P 5,1 m × H 4,3 m"),
    ("⚡", "Alimentation", "220 V / 16 A (prise standard)"),
    ("👥", "Capacité max", "12 enfants  ou  6 adultes"),
    ("✅", "Norme",        "Conforme EN 14960"),
]
for i, (icon, label, val) in enumerate(specs):
    y = 4.7 + i * 0.58
    add_textbox(slide1, 0.55, y, 0.45, 0.48, icon, 18, color=GOLD)
    add_textbox(slide1, 0.95, y, 1.6,  0.48, label + " :", 13,
                bold=True, color=GOLD)
    add_textbox(slide1, 2.55, y, 3.3,  0.48, val, 13, color=WHITE)

# ── Right-side image placeholder (decorative frame) ──
frame = add_rounded_rect(slide1, 6.5, 0.5, 6.5, 6.6, RGBColor(0x12, 0x2B, 0x5E))
# Gold border
border_shapes = [
    (6.5,  0.5,  6.5,  0.05),   # top
    (6.5,  7.05, 6.5,  0.05),   # bottom
    (6.5,  0.5,  0.05, 6.6),    # left
    (12.95,0.5,  0.05, 6.6),    # right
]
for (bl, bt, bw, bh) in border_shapes:
    add_rect(slide1, bl, bt, bw, bh, GOLD)

add_textbox(slide1, 6.55, 3.3, 6.4, 0.9,
            "[ Image produit ]",
            20, color=RGBColor(0x5A, 0x7A, 0xAA),
            align=PP_ALIGN.CENTER, italic=True)

# ── Source URL (footer) ───────────────────────
add_textbox(slide1, 0.4, 7.1, 12.5, 0.35,
            "Source : https://jeux-gonflables.net — Parcours gonflable occasion #1359",
            9, color=RGBColor(0x88, 0xAA, 0xCC), align=PP_ALIGN.LEFT)


# ══════════════════════════════════════════════════════════════════
# SLIDE 2 — Fiche technique détaillée
# ══════════════════════════════════════════════════════════════════
slide2 = prs.slides.add_slide(blank_layout)
bg2 = add_rect(slide2, 0, 0, 13.33, 7.5, NAVY)
add_rect(slide2, 0, 0, 13.33, 0.12, GOLD)
add_rect(slide2, 0, 7.38, 13.33, 0.12, GOLD)
add_rect(slide2, 0, 0.12, 0.08, 7.26, DARK_GOLD)

# Header band
add_rect(slide2, 0.08, 0.12, 13.25, 1.05, RGBColor(0x0E, 0x27, 0x55))
add_textbox(slide2, 0.3, 0.18, 9, 0.9,
            "Fiche Technique — Château Gonflable Pirate",
            30, bold=True, color=GOLD)
add_textbox(slide2, 10.0, 0.32, 3.0, 0.55,
            "1 700,00 € HT", 22, bold=True, color=RED,
            align=PP_ALIGN.RIGHT)

# ── Left column: specs table ──────────────────
col_specs = [
    ("Dimensions",    "L 8 m × Profondeur 5,1 m × Hauteur 4,3 m"),
    ("Alimentation",  "1 prise 220 V / 16 A (standard)"),
    ("Capacité",      "12 enfants  OU  6 adultes"),
    ("Certification", "Conforme EN 14960"),
    ("État",          "Occasion — bon état général"),
    ("Livraison",     "À définir selon localisation"),
]

add_rounded_rect(slide2, 0.3, 1.35, 6.0, 5.75, RGBColor(0x0D, 0x24, 0x52))
add_textbox(slide2, 0.45, 1.42, 5.7, 0.5,
            "Caractéristiques techniques", 16, bold=True, color=GOLD)

for i, (label, value) in enumerate(col_specs):
    y_top = 1.95 + i * 0.88
    row_bg_color = RGBColor(0x12, 0x2C, 0x5E) if i % 2 == 0 else RGBColor(0x0D, 0x22, 0x4A)
    add_rect(slide2, 0.32, y_top, 5.96, 0.82, row_bg_color)
    add_textbox(slide2, 0.45, y_top + 0.05, 1.7, 0.38,
                label, 12, bold=True, color=GOLD)
    add_textbox(slide2, 0.45, y_top + 0.38, 5.7, 0.38,
                value, 12, color=WHITE)

# ── Right column: highlights ──────────────────
add_rounded_rect(slide2, 6.6, 1.35, 6.45, 5.75, RGBColor(0x0D, 0x24, 0x52))
add_textbox(slide2, 6.75, 1.42, 6.1, 0.5,
            "Points forts", 16, bold=True, color=GOLD)

highlights = [
    ("🏴‍☠️", "Thème Pirate immersif",
     "Décoration pirates ultra-réaliste, idéale pour les anniversaires et événements."),
    ("🎢", "Multi-activités",
     "Toboggan, parcours d'obstacles, escalade — plusieurs attractions en un seul module."),
    ("🔒", "Sécurité certifiée",
     "Conforme à la norme européenne EN 14960 pour les structures gonflables."),
    ("⚡", "Installation facile",
     "Branchement sur prise 220V standard, gonflage rapide inclus."),
]

for i, (icon, title, desc) in enumerate(highlights):
    y = 2.0 + i * 1.3
    icon_bg = add_rounded_rect(slide2, 6.75, y, 0.55, 0.55, DARK_GOLD)
    add_textbox(slide2, 6.75, y + 0.02, 0.55, 0.5,
                icon, 20, align=PP_ALIGN.CENTER)
    add_textbox(slide2, 7.4, y, 5.5, 0.45,
                title, 14, bold=True, color=GOLD)
    add_textbox(slide2, 7.4, y + 0.42, 5.5, 0.78,
                desc, 11, color=LIGHT_BLUE, wrap=True)

# Footer
add_textbox(slide2, 0.3, 7.1, 12.5, 0.35,
            "Source : https://jeux-gonflables.net — Parcours gonflable occasion #1359",
            9, color=RGBColor(0x88, 0xAA, 0xCC))


# ══════════════════════════════════════════════════════════════════
# SLIDE 3 — Pourquoi choisir / Call to action
# ══════════════════════════════════════════════════════════════════
slide3 = prs.slides.add_slide(blank_layout)
bg3 = add_rect(slide3, 0, 0, 13.33, 7.5, NAVY)
add_rect(slide3, 0, 0, 13.33, 0.12, GOLD)
add_rect(slide3, 0, 7.38, 13.33, 0.12, GOLD)
add_rect(slide3, 0, 0.12, 0.08, 7.26, DARK_GOLD)

# Header
add_rect(slide3, 0.08, 0.12, 13.25, 1.05, RGBColor(0x0E, 0x27, 0x55))
add_textbox(slide3, 0.3, 0.18, 12, 0.9,
            "Pourquoi choisir ce château gonflable ?",
            30, bold=True, color=GOLD)

# Cards
cards = [
    ("💰", "Prix compétitif",
     "1 700 € HT seulement pour\nune structure multiactivités\nde grande dimension."),
    ("📐", "Grande superficie",
     "8 × 5,1 × 4,3 m offrent\nun espace de jeu généreux\npour les enfants."),
    ("🎉", "Polyvalent",
     "Parfait pour locations,\nanimations événementielles,\ncentres de loisirs."),
    ("🛡️", "Normes européennes",
     "Certification EN 14960\ngarantit la sécurité\nde tous les utilisateurs."),
]

for i, (icon, title, desc) in enumerate(cards):
    col = i % 2
    row = i // 2
    l = 0.55 + col * 6.45
    t = 1.45 + row * 2.85
    card = add_rounded_rect(slide3, l, t, 6.1, 2.6, RGBColor(0x0E, 0x27, 0x55))
    # top accent
    add_rect(slide3, l, t, 6.1, 0.06, GOLD)
    add_textbox(slide3, l + 0.25, t + 0.15, 0.7, 0.7, icon, 32)
    add_textbox(slide3, l + 1.05, t + 0.18, 4.8, 0.55,
                title, 18, bold=True, color=GOLD)
    add_textbox(slide3, l + 0.25, t + 0.85, 5.6, 1.6,
                desc, 13, color=LIGHT_BLUE, wrap=True)

# CTA banner
add_rounded_rect(slide3, 2.5, 7.0, 8.33, 0.35, RED)  # thin – just decorative
add_textbox(slide3, 0.3, 7.08, 12.6, 0.35,
            "Contactez-nous pour plus d'informations · jeux-gonflables.net",
            11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════
out = "/home/user/fiestalok/chateau_gonflable_pirate.pptx"
prs.save(out)
print(f"Saved → {out}")
