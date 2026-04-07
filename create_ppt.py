from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Palette douce et épurée ──────────────────────────────────────
BG          = RGBColor(0xFA, 0xF9, 0xF7)   # blanc cassé chaud
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
SAND        = RGBColor(0xF2, 0xEE, 0xE8)   # beige sable
TEAL        = RGBColor(0x4A, 0x9E, 0x9E)   # vert-bleu doux
TEAL_LIGHT  = RGBColor(0xD6, 0xED, 0xED)   # teal très clair
CORAL       = RGBColor(0xE8, 0x7B, 0x6A)   # corail doux
CORAL_LIGHT = RGBColor(0xF9, 0xE4, 0xE1)   # corail très clair
DARK        = RGBColor(0x2D, 0x2D, 0x2D)   # gris foncé (texte)
MID         = RGBColor(0x7A, 0x7A, 0x7A)   # gris moyen
LIGHT_GREY  = RGBColor(0xEE, 0xEC, 0xE9)   # gris très clair

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

def solid(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

def no_line(shape):
    shape.line.fill.background()

def add_rect(slide, l, t, w, h, color):
    s = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    solid(s, color)
    no_line(s)
    return s

def add_rrect(slide, l, t, w, h, color, adj=0.08):
    s = slide.shapes.add_shape(5, Inches(l), Inches(t), Inches(w), Inches(h))
    solid(s, color)
    no_line(s)
    s.adjustments[0] = adj
    return s

def tb(slide, l, t, w, h, text, size,
       bold=False, color=DARK, align=PP_ALIGN.LEFT, italic=False, wrap=True):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    box.word_wrap = wrap
    tf = box.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return box

blank = prs.slide_layouts[6]

# ════════════════════════════════════════════════════════
# SLIDE 1 — Couverture
# ════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(blank)

# Fond
add_rect(s1, 0, 0, 13.33, 7.5, BG)

# Bloc couleur gauche (teal doux)
add_rect(s1, 0, 0, 5.4, 7.5, TEAL_LIGHT)

# Fine bande teal sur le bord gauche
add_rect(s1, 0, 0, 0.06, 7.5, TEAL)

# ── Texte gauche ─────────────────────────────────────
tb(s1, 0.45, 0.7, 4.6, 0.5, "À VENDRE — OCCASION", 10,
   bold=True, color=TEAL, italic=False)

# Titre
box = s1.shapes.add_textbox(Inches(0.45), Inches(1.2), Inches(4.6), Inches(2.4))
box.word_wrap = True
tf = box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.LEFT
r = p.add_run()
r.text = "Château\nGonflable"
r.font.size = Pt(46)
r.font.bold = True
r.font.color.rgb = DARK

p2 = tf.add_paragraph()
p2.alignment = PP_ALIGN.LEFT
r2 = p2.add_run()
r2.text = "Pirate"
r2.font.size = Pt(46)
r2.font.bold = True
r2.font.color.rgb = TEAL

# Sous-titre
tb(s1, 0.45, 3.75, 4.6, 0.45,
   "Multiactivités · Toboggan · Escalade · Parcours",
   12, color=MID, italic=True)

# Séparateur
add_rect(s1, 0.45, 4.3, 2.0, 0.03, TEAL)

# Prix
tb(s1, 0.45, 4.5, 2.5, 0.4, "Prix de vente HT", 10, color=MID)
tb(s1, 0.45, 4.85, 4.0, 0.75, "1 700,00 €", 38, bold=True, color=CORAL)

# Norme
add_rrect(s1, 0.45, 5.75, 2.0, 0.42, TEAL_LIGHT)
tb(s1, 0.55, 5.82, 1.9, 0.32, "Conforme EN 14960", 10, bold=True, color=TEAL, align=PP_ALIGN.CENTER)

# ── Zone image droite ────────────────────────────────
add_rect(s1, 5.5, 0, 7.83, 7.5, SAND)
add_rrect(s1, 6.0, 0.6, 6.9, 6.3, WHITE, adj=0.04)
tb(s1, 6.0, 3.6, 6.9, 0.5, "[ Image produit ]",
   16, color=LIGHT_GREY, align=PP_ALIGN.CENTER, italic=True)

# Footer
tb(s1, 0.45, 7.15, 12.5, 0.3,
   "jeux-gonflables.net — Parcours gonflable occasion #1359",
   8, color=MID)


# ════════════════════════════════════════════════════════
# SLIDE 2 — Fiche technique
# ════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(blank)
add_rect(s2, 0, 0, 13.33, 7.5, BG)
add_rect(s2, 0, 0, 0.06, 7.5, TEAL)

# Header
tb(s2, 0.35, 0.32, 10, 0.42, "FICHE TECHNIQUE", 11,
   bold=True, color=TEAL)
tb(s2, 0.35, 0.68, 8, 0.6, "Château Gonflable Pirate", 28,
   bold=True, color=DARK)
add_rect(s2, 0.35, 1.35, 12.6, 0.03, LIGHT_GREY)

# ── Colonne gauche : tableau ──────────────────────────
add_rrect(s2, 0.35, 1.55, 5.9, 5.6, WHITE, adj=0.04)
tb(s2, 0.65, 1.75, 5.3, 0.4, "Caractéristiques", 13, bold=True, color=DARK)
add_rect(s2, 0.65, 2.18, 5.3, 0.025, LIGHT_GREY)

rows = [
    ("Dimensions",    "L 8 m × P 5,1 m × H 4,3 m"),
    ("Alimentation",  "220 V / 16 A — prise standard"),
    ("Capacité max",  "12 enfants  ou  6 adultes"),
    ("Certification", "Conforme EN 14960"),
    ("État",          "Occasion — bon état général"),
    ("Livraison",     "À définir selon localisation"),
]
for i, (label, val) in enumerate(rows):
    y = 2.28 + i * 0.78
    if i % 2 == 0:
        add_rrect(s2, 0.37, y, 5.86, 0.72, SAND, adj=0.02)
    tb(s2, 0.65, y + 0.08, 1.8, 0.3, label, 10, bold=True, color=MID)
    tb(s2, 0.65, y + 0.35, 5.3, 0.3, val, 12, bold=False, color=DARK)

# ── Colonne droite : points forts ────────────────────
add_rrect(s2, 6.65, 1.55, 6.33, 5.6, WHITE, adj=0.04)
tb(s2, 6.95, 1.75, 5.7, 0.4, "Points forts", 13, bold=True, color=DARK)
add_rect(s2, 6.95, 2.18, 5.7, 0.025, LIGHT_GREY)

highlights = [
    (TEAL_LIGHT,  TEAL,  "Thème immersif",
     "Décoration pirate ultra-réaliste, idéale\npour anniversaires et événements."),
    (CORAL_LIGHT, CORAL, "Multi-activités",
     "Toboggan, escalade, parcours d'obstacles —\nplusieurs jeux en un seul module."),
    (TEAL_LIGHT,  TEAL,  "Sécurité certifiée",
     "Norme EN 14960 — garantit la sécurité\ndes utilisateurs enfants et adultes."),
    (CORAL_LIGHT, CORAL, "Installation simple",
     "Prise 220 V standard, gonflage rapide,\nprêt à l'emploi en quelques minutes."),
]
for i, (bg_c, dot_c, title, desc) in enumerate(highlights):
    y = 2.28 + i * 1.3
    add_rrect(s2, 6.67, y, 6.29, 1.18, bg_c, adj=0.04)
    add_rrect(s2, 6.85, y + 0.32, 0.18, 0.18, dot_c, adj=0.5)
    tb(s2, 7.15, y + 0.1, 5.6, 0.38, title, 13, bold=True, color=DARK)
    tb(s2, 7.15, y + 0.46, 5.6, 0.65, desc, 11, color=MID, wrap=True)

# Footer
tb(s2, 0.35, 7.15, 12.5, 0.3,
   "jeux-gonflables.net — Parcours gonflable occasion #1359", 8, color=MID)


# ════════════════════════════════════════════════════════
# SLIDE 3 — Arguments & contact
# ════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(blank)
add_rect(s3, 0, 0, 13.33, 7.5, BG)
add_rect(s3, 0, 0, 0.06, 7.5, TEAL)

tb(s3, 0.35, 0.32, 10, 0.42, "POURQUOI CHOISIR CE PRODUIT ?", 11,
   bold=True, color=TEAL)
tb(s3, 0.35, 0.68, 10, 0.6, "4 bonnes raisons", 28, bold=True, color=DARK)
add_rect(s3, 0.35, 1.35, 12.6, 0.03, LIGHT_GREY)

cards = [
    (TEAL,  TEAL_LIGHT,  "Prix compétitif",
     "1 700 € HT pour une structure\nde grande dimension avec\nplusieurs activités intégrées."),
    (CORAL, CORAL_LIGHT, "Grande superficie",
     "8 × 5,1 × 4,3 m — un espace\nde jeu généreux adapté\naux enfants comme aux adultes."),
    (TEAL,  TEAL_LIGHT,  "Très polyvalent",
     "Idéal pour la location,\nles animations événementielles\net les centres de loisirs."),
    (CORAL, CORAL_LIGHT, "Normes européennes",
     "Certification EN 14960\npour une utilisation\nen toute sérénité."),
]

for i, (accent, bg_c, title, desc) in enumerate(cards):
    col = i % 2
    row = i // 2
    l = 0.35 + col * 6.52
    t = 1.55 + row * 2.78
    add_rrect(s3, l, t, 6.15, 2.55, WHITE, adj=0.04)
    add_rect(s3, l, t, 6.15, 0.05, accent)
    add_rrect(s3, l + 0.25, t + 0.22, 0.45, 0.45, bg_c, adj=0.5)
    tb(s3, l + 0.25 + 0.14, t + 0.29, 0.2, 0.3, "●", 10, color=accent, align=PP_ALIGN.CENTER)
    tb(s3, l + 0.85, t + 0.2, 5.1, 0.42, title, 15, bold=True, color=DARK)
    tb(s3, l + 0.25, t + 0.82, 5.7, 1.55, desc, 12, color=MID, wrap=True)

# Bandeau contact
add_rrect(s3, 0.35, 7.0, 12.6, 0.38, TEAL_LIGHT, adj=0.08)
tb(s3, 0.35, 7.06, 12.6, 0.3,
   "Pour plus d'informations : jeux-gonflables.net — Parcours gonflable occasion #1359",
   11, color=TEAL, align=PP_ALIGN.CENTER)


out = "/home/user/fiestalok/chateau_gonflable_pirate.pptx"
prs.save(out)
print(f"Saved -> {out}")
