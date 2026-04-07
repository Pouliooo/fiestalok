# Fiestalo'K — Site Vitrine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a one-page showcase website for Fiestalo'K, a bouncy castle rental company, following the "Pop Décalé" artistic direction defined in the design spec.

**Architecture:** Single HTML page with external CSS and minimal JS. No build tools or frameworks — pure static files ready to deploy anywhere. Sections scroll vertically: Hero, Catalogue, How It Works, Pricing, Testimonials, Contact, Footer.

**Tech Stack:** HTML5, CSS3 (custom properties for design tokens), vanilla JS (smooth scroll, mobile menu, form validation), Google Fonts (Bangers + Nunito)

**Design spec:** `docs/superpowers/specs/2026-04-07-moodboard-direction-artistique-design.md`

**Visual mockup reference:** `.superpowers/brainstorm/2366-1775570576/moodboard-final.html`

---

## File Structure

```
index.html          — Single page, all sections
css/
  tokens.css        — Design tokens (colors, fonts, spacing, radii)
  reset.css         — Minimal CSS reset
  layout.css        — Global layout, grid, containers
  components.css    — Reusable components (badges, buttons, cards)
  sections.css      — Section-specific styles (hero, catalogue, etc.)
  responsive.css    — Mobile/tablet breakpoints
js/
  main.js           — Mobile menu toggle, smooth scroll, form handling
assets/
  images/           — Placeholder images for gonflables
```

---

### Task 1: Project scaffold & design tokens

**Files:**
- Create: `css/tokens.css`
- Create: `css/reset.css`
- Create: `index.html` (minimal shell)

- [ ] **Step 1: Create `css/tokens.css`**

```css
:root {
  /* Colors */
  --color-bg: #F8F9FA;
  --color-text: #2D3436;
  --color-text-light: #666666;
  --color-text-muted: #999999;
  --color-primary: #4ECDC4;
  --color-accent: #FFE66D;
  --color-secondary: #44CF6C;
  --color-alert: #FF6B6B;
  --color-white: #FFFFFF;

  /* Typography */
  --font-display: 'Bangers', 'Impact', cursive;
  --font-body: 'Nunito', 'Quicksand', sans-serif;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.5rem;
  --font-size-2xl: 2rem;
  --font-size-3xl: 3rem;
  --font-size-hero: clamp(2.5rem, 5vw, 4rem);

  /* Spacing */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 1.5rem;
  --space-lg: 2rem;
  --space-xl: 3rem;
  --space-2xl: 5rem;
  --space-section: 6rem;

  /* Radii */
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-pill: 9999px;

  /* Shadows */
  --shadow-button: 0 4px 12px rgba(0, 0, 0, 0.1);
  --shadow-card: 0 8px 24px rgba(0, 0, 0, 0.08);

  /* Layout */
  --container-max: 1200px;
  --container-padding: 1.5rem;
}
```

- [ ] **Step 2: Create `css/reset.css`**

```css
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: var(--font-body);
  font-size: var(--font-size-base);
  color: var(--color-text);
  background-color: var(--color-bg);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

img {
  max-width: 100%;
  display: block;
}

a {
  color: inherit;
  text-decoration: none;
}

ul {
  list-style: none;
}

button,
input,
textarea {
  font: inherit;
  color: inherit;
}
```

- [ ] **Step 3: Create minimal `index.html` shell**

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fiestalo'K — Location de Châteaux Gonflables</title>
  <meta name="description" content="Location de châteaux gonflables pour anniversaires, EVJF, team building & plus. On gonfle, vous kiffez !">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/tokens.css">
  <link rel="stylesheet" href="css/reset.css">
</head>
<body>
  <!-- Sections will be added in subsequent tasks -->
</body>
</html>
```

- [ ] **Step 4: Open in browser and verify**

Run: `open index.html`
Expected: Blank white page (#F8F9FA), no console errors, fonts loading.

- [ ] **Step 5: Commit**

```bash
git add index.html css/tokens.css css/reset.css
git commit -m "scaffold: project structure with design tokens and CSS reset"
```

---

### Task 2: Global layout & reusable components

**Files:**
- Create: `css/layout.css`
- Create: `css/components.css`
- Modify: `index.html` (add stylesheet links)

- [ ] **Step 1: Create `css/layout.css`**

```css
.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--container-padding);
}

.section {
  padding: var(--space-section) 0;
}

.section-title {
  font-family: var(--font-display);
  font-size: var(--font-size-3xl);
  letter-spacing: 2px;
  text-align: center;
  margin-bottom: var(--space-lg);
}

.section-subtitle {
  text-align: center;
  color: var(--color-text-light);
  font-size: var(--font-size-lg);
  max-width: 600px;
  margin: 0 auto var(--space-xl);
}
```

- [ ] **Step 2: Create `css/components.css`**

```css
/* Buttons */
.btn {
  display: inline-block;
  padding: 14px 32px;
  border-radius: var(--radius-pill);
  font-family: var(--font-body);
  font-weight: 800;
  font-size: var(--font-size-base);
  cursor: pointer;
  border: none;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-button);
}

.btn--primary {
  background: var(--color-accent);
  color: var(--color-text);
}

.btn--secondary {
  background: transparent;
  border: 2px solid var(--color-text);
  color: var(--color-text);
}

.btn--cta {
  background: var(--color-alert);
  color: var(--color-white);
}

/* Badge */
.badge {
  display: inline-block;
  padding: 6px 18px;
  border-radius: var(--radius-pill);
  font-weight: 800;
  font-size: var(--font-size-sm);
  transform: rotate(-2deg);
}

.badge--alert {
  background: var(--color-alert);
  color: var(--color-white);
}

.badge--accent {
  background: var(--color-accent);
  color: var(--color-text);
}

.badge--primary {
  background: var(--color-primary);
  color: var(--color-white);
}

/* Card */
.card {
  background: var(--color-white);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-card);
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-4px);
}

.card__image {
  width: 100%;
  height: 220px;
  object-fit: cover;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
}

.card__body {
  padding: var(--space-md);
}

.card__title {
  font-family: var(--font-display);
  font-size: var(--font-size-xl);
  letter-spacing: 1px;
  margin-bottom: var(--space-xs);
}

.card__text {
  color: var(--color-text-light);
  font-size: var(--font-size-sm);
}

.card__price {
  font-family: var(--font-display);
  font-size: var(--font-size-xl);
  color: var(--color-primary);
  margin-top: var(--space-sm);
}
```

- [ ] **Step 3: Add stylesheet links to `index.html`**

Add after the reset.css link:

```html
<link rel="stylesheet" href="css/layout.css">
<link rel="stylesheet" href="css/components.css">
```

- [ ] **Step 4: Commit**

```bash
git add css/layout.css css/components.css index.html
git commit -m "feat: add global layout and reusable component styles"
```

---

### Task 3: Navbar

**Files:**
- Create: `css/sections.css`
- Modify: `index.html` (add navbar HTML)

- [ ] **Step 1: Create `css/sections.css` with navbar styles**

```css
/* ===================== NAVBAR ===================== */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: var(--color-bg);
  border-bottom: 2px solid rgba(78, 205, 196, 0.15);
  padding: var(--space-sm) 0;
}

.navbar__inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar__logo {
  font-family: var(--font-display);
  font-size: var(--font-size-xl);
  letter-spacing: 3px;
  color: var(--color-text);
}

.navbar__links {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.navbar__link {
  font-weight: 600;
  font-size: var(--font-size-sm);
  color: var(--color-text-light);
  transition: color 0.2s;
}

.navbar__link:hover,
.navbar__link--active {
  color: var(--color-primary);
}

.navbar__toggle {
  display: none;
  background: none;
  border: none;
  font-size: var(--font-size-xl);
  cursor: pointer;
}
```

- [ ] **Step 2: Add navbar HTML to `index.html` `<body>`**

```html
<nav class="navbar">
  <div class="container navbar__inner">
    <a href="#" class="navbar__logo">FIESTALO'K</a>
    <button class="navbar__toggle" aria-label="Menu" aria-expanded="false">☰</button>
    <ul class="navbar__links" id="nav-links">
      <li><a href="#gonflables" class="navbar__link navbar__link--active">Nos Gonflables</a></li>
      <li><a href="#fonctionnement" class="navbar__link">Comment ça marche</a></li>
      <li><a href="#tarifs" class="navbar__link">Tarifs</a></li>
      <li><a href="#temoignages" class="navbar__link">Témoignages</a></li>
      <li><a href="#contact" class="navbar__link">Contact</a></li>
      <li><a href="#contact" class="btn btn--cta">Réserver 🎉</a></li>
    </ul>
  </div>
</nav>
```

Also add the stylesheet link in `<head>`:

```html
<link rel="stylesheet" href="css/sections.css">
```

- [ ] **Step 3: Verify in browser**

Run: `open index.html`
Expected: Fixed navbar at top with logo left, links right, "Réserver" button in corail.

- [ ] **Step 4: Commit**

```bash
git add css/sections.css index.html
git commit -m "feat: add fixed navbar with navigation links"
```

---

### Task 4: Hero section

**Files:**
- Modify: `css/sections.css` (append hero styles)
- Modify: `index.html` (add hero HTML after navbar)

- [ ] **Step 1: Append hero styles to `css/sections.css`**

```css
/* ===================== HERO ===================== */
.hero {
  padding-top: calc(80px + var(--space-2xl));
  padding-bottom: var(--space-2xl);
  text-align: center;
}

.hero__badge {
  margin-bottom: var(--space-md);
}

.hero__title {
  font-family: var(--font-display);
  font-size: var(--font-size-hero);
  letter-spacing: 3px;
  line-height: 1.2;
  margin-bottom: var(--space-md);
}

.hero__title span {
  color: var(--color-primary);
}

.hero__subtitle {
  color: var(--color-text-light);
  font-size: var(--font-size-lg);
  max-width: 540px;
  margin: 0 auto var(--space-lg);
  line-height: 1.6;
}

.hero__buttons {
  display: flex;
  gap: var(--space-sm);
  justify-content: center;
  flex-wrap: wrap;
}

.hero__trust {
  display: flex;
  justify-content: center;
  gap: var(--space-xl);
  flex-wrap: wrap;
  margin-top: var(--space-2xl);
  padding-top: var(--space-lg);
  border-top: 2px solid rgba(0, 0, 0, 0.05);
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
}
```

- [ ] **Step 2: Add hero HTML to `index.html` after `</nav>`**

```html
<section class="hero" id="hero">
  <div class="container">
    <div class="hero__badge">
      <span class="badge badge--alert">LES KINGS DU GONFLABLE 👑</span>
    </div>
    <h1 class="hero__title">TA FÊTE VA <span>DÉCOLLER</span> 🚀</h1>
    <p class="hero__subtitle">
      Location de châteaux gonflables pour anniversaires, EVJF,
      team building & plus. On livre, on installe, tu kiffes.
    </p>
    <div class="hero__buttons">
      <a href="#gonflables" class="btn btn--primary">VOIR LES GONFLABLES 💥</a>
      <a href="#fonctionnement" class="btn btn--secondary">COMMENT ÇA MARCHE ?</a>
    </div>
    <div class="hero__trust">
      <span>⚡ Livraison express</span>
      <span>👑 +500 fêtes réussies</span>
      <span>🛡️ Assurance incluse</span>
      <span>💬 Réponse en 1h</span>
    </div>
  </div>
</section>
```

- [ ] **Step 3: Verify in browser**

Expected: Hero section matching the approved moodboard mockup — badge penché, big title, two buttons, trust bar.

- [ ] **Step 4: Commit**

```bash
git add css/sections.css index.html
git commit -m "feat: add hero section with badge, CTA buttons, and trust bar"
```

---

### Task 5: Catalogue "Nos Gonflables"

**Files:**
- Modify: `css/sections.css` (append catalogue styles)
- Modify: `index.html` (add catalogue section)

- [ ] **Step 1: Append catalogue styles to `css/sections.css`**

```css
/* ===================== CATALOGUE ===================== */
.catalogue__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-lg);
}

.card__tags {
  display: flex;
  gap: var(--space-xs);
  flex-wrap: wrap;
  margin-top: var(--space-sm);
}

.card__tag {
  font-size: var(--font-size-xs);
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  background: var(--color-bg);
  color: var(--color-text-light);
  font-weight: 600;
}
```

- [ ] **Step 2: Add catalogue HTML after hero section**

Use 6 placeholder cards with fictional bouncy castle names, dimensions, and prices. Each card has: colored gradient placeholder for image, title, short description, tags (age range, dimensions), and price.

```html
<section class="section" id="gonflables">
  <div class="container">
    <h2 class="section-title">NOS GONFLABLES</h2>
    <p class="section-subtitle">Choisis ton château, on s'occupe du reste 🏰</p>
    <div class="catalogue__grid">

      <div class="card">
        <div class="card__image" style="background: linear-gradient(135deg, #4ECDC4, #44CF6C);"></div>
        <div class="card__body">
          <h3 class="card__title">Le Classique</h3>
          <p class="card__text">Le château gonflable incontournable pour les anniversaires. Parfait pour les petits aventuriers.</p>
          <div class="card__tags">
            <span class="card__tag">3-12 ans</span>
            <span class="card__tag">4m x 3m</span>
          </div>
          <div class="card__price">À partir de 149€</div>
        </div>
      </div>

      <div class="card">
        <div class="card__image" style="background: linear-gradient(135deg, #FFE66D, #FF6B6B);"></div>
        <div class="card__body">
          <h3 class="card__title">Le Méga Toboggan</h3>
          <p class="card__text">Un toboggan géant qui fera hurler de joie petits et grands. Sensations garanties !</p>
          <div class="card__tags">
            <span class="card__tag">5-99 ans</span>
            <span class="card__tag">8m x 4m</span>
          </div>
          <div class="card__price">À partir de 249€</div>
        </div>
      </div>

      <div class="card">
        <div class="card__image" style="background: linear-gradient(135deg, #FF6B6B, #FFE66D);"></div>
        <div class="card__body">
          <h3 class="card__title">Le Parcours Ninja</h3>
          <p class="card__text">Obstacles, escalade et sauts — le combo parfait pour les team buildings délirants.</p>
          <div class="card__tags">
            <span class="card__tag">8-99 ans</span>
            <span class="card__tag">12m x 4m</span>
          </div>
          <div class="card__price">À partir de 349€</div>
        </div>
      </div>

      <div class="card">
        <div class="card__image" style="background: linear-gradient(135deg, #44CF6C, #4ECDC4);"></div>
        <div class="card__body">
          <h3 class="card__title">La Licorne Magique</h3>
          <p class="card__text">Un château enchanté avec licorne géante. Le rêve de toutes les princesses et princes !</p>
          <div class="card__tags">
            <span class="card__tag">3-10 ans</span>
            <span class="card__tag">5m x 4m</span>
          </div>
          <div class="card__price">À partir de 179€</div>
        </div>
      </div>

      <div class="card">
        <div class="card__image" style="background: linear-gradient(135deg, #4ECDC4, #FFE66D);"></div>
        <div class="card__body">
          <h3 class="card__title">Le Ring de Sumo</h3>
          <p class="card__text">Enfile le costume de sumo et affronte tes potes. Fous rires assurés pour les EVJF !</p>
          <div class="card__tags">
            <span class="card__tag">12-99 ans</span>
            <span class="card__tag">5m x 5m</span>
          </div>
          <div class="card__price">À partir de 199€</div>
        </div>
      </div>

      <div class="card">
        <div class="card__image" style="background: linear-gradient(135deg, #FFE66D, #44CF6C);"></div>
        <div class="card__body">
          <h3 class="card__title">Le Pack Fiesta XXL</h3>
          <p class="card__text">Château + toboggan + jeux. Le pack complet pour une fête dont tout le monde parlera.</p>
          <div class="card__tags">
            <span class="card__tag">Tous âges</span>
            <span class="card__tag">Sur mesure</span>
          </div>
          <div class="card__price">À partir de 449€</div>
        </div>
      </div>

    </div>
  </div>
</section>
```

- [ ] **Step 3: Verify in browser**

Expected: 6 cards in a responsive grid, each with gradient placeholder, title in Bangers, price in turquoise.

- [ ] **Step 4: Commit**

```bash
git add css/sections.css index.html
git commit -m "feat: add bouncy castle catalogue section with 6 product cards"
```

---

### Task 6: "Comment ça marche" section

**Files:**
- Modify: `css/sections.css` (append steps styles)
- Modify: `index.html` (add section)

- [ ] **Step 1: Append steps styles to `css/sections.css`**

```css
/* ===================== HOW IT WORKS ===================== */
.steps {
  background: var(--color-white);
}

.steps__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-lg);
  text-align: center;
}

.step__icon {
  width: 80px;
  height: 80px;
  margin: 0 auto var(--space-sm);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.step__number {
  font-family: var(--font-display);
  font-size: var(--font-size-2xl);
  color: var(--color-primary);
  margin-bottom: var(--space-xs);
}

.step__title {
  font-family: var(--font-display);
  font-size: var(--font-size-xl);
  letter-spacing: 1px;
  margin-bottom: var(--space-xs);
}

.step__text {
  color: var(--color-text-light);
  font-size: var(--font-size-sm);
}
```

- [ ] **Step 2: Add "Comment ça marche" HTML after catalogue**

```html
<section class="section steps" id="fonctionnement">
  <div class="container">
    <h2 class="section-title">COMMENT ÇA MARCHE ?</h2>
    <p class="section-subtitle">En 4 étapes, ta fête est prête 🎯</p>
    <div class="steps__grid">

      <div class="step">
        <div class="step__icon" style="background: rgba(78,205,196,0.15);">🏰</div>
        <div class="step__number">1</div>
        <h3 class="step__title">CHOISIS</h3>
        <p class="step__text">Parcours notre catalogue et trouve le gonflable parfait pour ta fête.</p>
      </div>

      <div class="step">
        <div class="step__icon" style="background: rgba(255,230,109,0.2);">📅</div>
        <div class="step__number">2</div>
        <h3 class="step__title">RÉSERVE</h3>
        <p class="step__text">Choisis ta date et réserve en ligne. On te confirme en moins d'1h.</p>
      </div>

      <div class="step">
        <div class="step__icon" style="background: rgba(68,207,108,0.15);">🚚</div>
        <div class="step__number">3</div>
        <h3 class="step__title">ON LIVRE</h3>
        <p class="step__text">On amène le gonflable, on l'installe, on vérifie que tout est nickel.</p>
      </div>

      <div class="step">
        <div class="step__icon" style="background: rgba(255,107,107,0.15);">🎉</div>
        <div class="step__number">4</div>
        <h3 class="step__title">TU KIFFES</h3>
        <p class="step__text">Profite à fond ! On revient tout récupérer après la fête.</p>
      </div>

    </div>
  </div>
</section>
```

- [ ] **Step 3: Verify in browser**

Expected: 4 steps in a row, each with emoji icon, number, title, and description.

- [ ] **Step 4: Commit**

```bash
git add css/sections.css index.html
git commit -m "feat: add 'how it works' section with 4 illustrated steps"
```

---

### Task 7: Tarifs section

**Files:**
- Modify: `css/sections.css` (append pricing styles)
- Modify: `index.html` (add section)

- [ ] **Step 1: Append pricing styles to `css/sections.css`**

```css
/* ===================== PRICING ===================== */
.pricing__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-lg);
  max-width: 960px;
  margin: 0 auto;
}

.pricing-card {
  background: var(--color-white);
  border-radius: var(--radius-md);
  padding: var(--space-xl);
  text-align: center;
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
}

.pricing-card--featured {
  border: 3px solid var(--color-accent);
}

.pricing-card--featured::before {
  content: "BEST SELLER ⭐";
  position: absolute;
  top: 16px;
  right: -32px;
  background: var(--color-accent);
  color: var(--color-text);
  padding: 4px 40px;
  font-size: var(--font-size-xs);
  font-weight: 800;
  transform: rotate(45deg);
}

.pricing-card__title {
  font-family: var(--font-display);
  font-size: var(--font-size-xl);
  letter-spacing: 1px;
  margin-bottom: var(--space-sm);
}

.pricing-card__price {
  font-family: var(--font-display);
  font-size: var(--font-size-3xl);
  color: var(--color-primary);
  margin-bottom: var(--space-xs);
}

.pricing-card__unit {
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  margin-bottom: var(--space-md);
}

.pricing-card__features {
  text-align: left;
  margin-bottom: var(--space-lg);
}

.pricing-card__feature {
  padding: var(--space-xs) 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-light);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.pricing-card__feature::before {
  content: "✓ ";
  color: var(--color-secondary);
  font-weight: 800;
}
```

- [ ] **Step 2: Add pricing HTML after "Comment ça marche"**

```html
<section class="section" id="tarifs">
  <div class="container">
    <h2 class="section-title">TARIFS</h2>
    <p class="section-subtitle">Des prix tout doux pour des fêtes de ouf 💰</p>
    <div class="pricing__grid">

      <div class="pricing-card">
        <h3 class="pricing-card__title">MINI FIESTA</h3>
        <div class="pricing-card__price">149€</div>
        <div class="pricing-card__unit">la journée</div>
        <ul class="pricing-card__features">
          <li class="pricing-card__feature">1 château gonflable classique</li>
          <li class="pricing-card__feature">Livraison & installation</li>
          <li class="pricing-card__feature">Récupération en fin de journée</li>
          <li class="pricing-card__feature">Assurance incluse</li>
        </ul>
        <a href="#contact" class="btn btn--secondary">CHOISIR</a>
      </div>

      <div class="pricing-card pricing-card--featured">
        <h3 class="pricing-card__title">MEGA FIESTA</h3>
        <div class="pricing-card__price">299€</div>
        <div class="pricing-card__unit">la journée</div>
        <ul class="pricing-card__features">
          <li class="pricing-card__feature">Château gonflable au choix</li>
          <li class="pricing-card__feature">Toboggan ou jeu bonus inclus</li>
          <li class="pricing-card__feature">Livraison & installation</li>
          <li class="pricing-card__feature">Récupération en fin de journée</li>
          <li class="pricing-card__feature">Assurance incluse</li>
          <li class="pricing-card__feature">Photos souvenirs offertes</li>
        </ul>
        <a href="#contact" class="btn btn--primary">CHOISIR 💥</a>
      </div>

      <div class="pricing-card">
        <h3 class="pricing-card__title">FIESTA ROYALE</h3>
        <div class="pricing-card__price">499€</div>
        <div class="pricing-card__unit">la journée</div>
        <ul class="pricing-card__features">
          <li class="pricing-card__feature">Pack complet sur mesure</li>
          <li class="pricing-card__feature">2 structures gonflables</li>
          <li class="pricing-card__feature">Animation optionnelle</li>
          <li class="pricing-card__feature">Livraison & installation</li>
          <li class="pricing-card__feature">Récupération en fin de journée</li>
          <li class="pricing-card__feature">Assurance incluse</li>
          <li class="pricing-card__feature">Conseiller dédié</li>
        </ul>
        <a href="#contact" class="btn btn--secondary">CHOISIR</a>
      </div>

    </div>
  </div>
</section>
```

- [ ] **Step 3: Verify in browser**

Expected: 3 pricing cards, middle one highlighted with "BEST SELLER" ribbon and accent border.

- [ ] **Step 4: Commit**

```bash
git add css/sections.css index.html
git commit -m "feat: add pricing section with 3 tiers and featured highlight"
```

---

### Task 8: Témoignages section

**Files:**
- Modify: `css/sections.css` (append testimonials styles)
- Modify: `index.html` (add section)

- [ ] **Step 1: Append testimonials styles to `css/sections.css`**

```css
/* ===================== TESTIMONIALS ===================== */
.testimonials {
  background: var(--color-white);
}

.testimonials__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-lg);
}

.testimonial {
  padding: var(--space-lg);
  background: var(--color-bg);
  border-radius: var(--radius-md);
  position: relative;
}

.testimonial__stars {
  color: var(--color-accent);
  font-size: var(--font-size-lg);
  margin-bottom: var(--space-sm);
}

.testimonial__text {
  font-size: var(--font-size-base);
  color: var(--color-text-light);
  line-height: 1.7;
  margin-bottom: var(--space-md);
  font-style: italic;
}

.testimonial__author {
  font-weight: 700;
  color: var(--color-text);
}

.testimonial__context {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}
```

- [ ] **Step 2: Add testimonials HTML after pricing**

```html
<section class="section testimonials" id="temoignages">
  <div class="container">
    <h2 class="section-title">ILS ONT KIFFÉ</h2>
    <p class="section-subtitle">+500 fêtes réussies et des sourires plein la face 😍</p>
    <div class="testimonials__grid">

      <div class="testimonial">
        <div class="testimonial__stars">⭐⭐⭐⭐⭐</div>
        <p class="testimonial__text">"Les enfants étaient comme des fous ! Installation hyper rapide, et le château était nickel. On recommande à 200% !"</p>
        <div class="testimonial__author">Sophie M.</div>
        <div class="testimonial__context">Anniversaire — 8 ans de Lucas</div>
      </div>

      <div class="testimonial">
        <div class="testimonial__stars">⭐⭐⭐⭐⭐</div>
        <p class="testimonial__text">"On a pris le Ring de Sumo pour l'EVJF de ma meilleure pote. Meilleure idée de notre vie. Les photos sont légendaires."</p>
        <div class="testimonial__author">Camille R.</div>
        <div class="testimonial__context">EVJF — Août 2025</div>
      </div>

      <div class="testimonial">
        <div class="testimonial__stars">⭐⭐⭐⭐⭐</div>
        <p class="testimonial__text">"Team building mémorable. Même le directeur s'est retrouvé dans le toboggan. Fiestalo'K a géré de A à Z, top pro."</p>
        <div class="testimonial__author">Thomas D.</div>
        <div class="testimonial__context">Team building — Entreprise TechCorp</div>
      </div>

    </div>
  </div>
</section>
```

- [ ] **Step 3: Verify in browser**

Expected: 3 testimonial cards with stars, quote, author, and context.

- [ ] **Step 4: Commit**

```bash
git add css/sections.css index.html
git commit -m "feat: add testimonials section with 3 client reviews"
```

---

### Task 9: Contact / Réservation section

**Files:**
- Modify: `css/sections.css` (append contact styles)
- Modify: `index.html` (add section)

- [ ] **Step 1: Append contact styles to `css/sections.css`**

```css
/* ===================== CONTACT ===================== */
.contact__inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-xl);
  align-items: start;
}

.contact__info {
  padding: var(--space-xl);
}

.contact__info-title {
  font-family: var(--font-display);
  font-size: var(--font-size-2xl);
  letter-spacing: 1px;
  margin-bottom: var(--space-md);
}

.contact__info-text {
  color: var(--color-text-light);
  margin-bottom: var(--space-lg);
  line-height: 1.7;
}

.contact__detail {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) 0;
  color: var(--color-text-light);
}

.contact__detail-icon {
  font-size: var(--font-size-xl);
}

.contact__form {
  background: var(--color-white);
  border-radius: var(--radius-md);
  padding: var(--space-xl);
  box-shadow: var(--shadow-card);
}

.form__group {
  margin-bottom: var(--space-md);
}

.form__label {
  display: block;
  font-weight: 700;
  font-size: var(--font-size-sm);
  margin-bottom: var(--space-xs);
  color: var(--color-text);
}

.form__input,
.form__select,
.form__textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-base);
  background: var(--color-bg);
  transition: border-color 0.2s;
}

.form__input:focus,
.form__select:focus,
.form__textarea:focus {
  outline: none;
  border-color: var(--color-primary);
}

.form__textarea {
  min-height: 120px;
  resize: vertical;
}
```

- [ ] **Step 2: Add contact HTML after testimonials**

```html
<section class="section" id="contact">
  <div class="container">
    <h2 class="section-title">RÉSERVE TA FIESTA</h2>
    <p class="section-subtitle">Dis-nous tout, on te répond en moins d'1h 🚀</p>
    <div class="contact__inner">

      <div class="contact__info">
        <h3 class="contact__info-title">ON EST LÀ POUR TOI</h3>
        <p class="contact__info-text">
          Une question ? Une envie de fête ? Remplis le formulaire ou
          contacte-nous directement. On adore parler fiesta !
        </p>
        <div class="contact__detail">
          <span class="contact__detail-icon">📞</span>
          <span>06 XX XX XX XX</span>
        </div>
        <div class="contact__detail">
          <span class="contact__detail-icon">✉️</span>
          <span>hello@fiestalok.fr</span>
        </div>
        <div class="contact__detail">
          <span class="contact__detail-icon">📍</span>
          <span>Région parisienne & alentours</span>
        </div>
        <div class="contact__detail">
          <span class="contact__detail-icon">🕐</span>
          <span>Lun-Sam : 9h-19h</span>
        </div>
      </div>

      <form class="contact__form" id="contact-form">
        <div class="form__group">
          <label class="form__label" for="name">Ton prénom *</label>
          <input class="form__input" type="text" id="name" name="name" placeholder="Comment tu t'appelles ?" required>
        </div>
        <div class="form__group">
          <label class="form__label" for="email">Ton email *</label>
          <input class="form__input" type="email" id="email" name="email" placeholder="Pour qu'on te réponde !" required>
        </div>
        <div class="form__group">
          <label class="form__label" for="phone">Ton téléphone</label>
          <input class="form__input" type="tel" id="phone" name="phone" placeholder="Si tu préfères qu'on t'appelle">
        </div>
        <div class="form__group">
          <label class="form__label" for="event-type">Type d'événement *</label>
          <select class="form__select" id="event-type" name="event-type" required>
            <option value="">Choisis ton type de fête</option>
            <option value="anniversaire">🎂 Anniversaire</option>
            <option value="evjf">🥂 EVJF / EVG</option>
            <option value="teambuilding">💼 Team building</option>
            <option value="corporate">🏢 Événement corporate</option>
            <option value="kermesse">🎪 Kermesse / Fête de village</option>
            <option value="autre">🎉 Autre</option>
          </select>
        </div>
        <div class="form__group">
          <label class="form__label" for="date">Date souhaitée *</label>
          <input class="form__input" type="date" id="date" name="date" required>
        </div>
        <div class="form__group">
          <label class="form__label" for="message">Dis-nous tout !</label>
          <textarea class="form__textarea" id="message" name="message" placeholder="Nombre d'invités, lieu, envies particulières..."></textarea>
        </div>
        <button type="submit" class="btn btn--primary" style="width: 100%;">ENVOYER MA DEMANDE 🎉</button>
      </form>

    </div>
  </div>
</section>
```

- [ ] **Step 3: Verify in browser**

Expected: Two-column layout — contact info left, form right. Form fields styled with design tokens.

- [ ] **Step 4: Commit**

```bash
git add css/sections.css index.html
git commit -m "feat: add contact section with info and reservation form"
```

---

### Task 10: Footer

**Files:**
- Modify: `css/sections.css` (append footer styles)
- Modify: `index.html` (add footer)

- [ ] **Step 1: Append footer styles to `css/sections.css`**

```css
/* ===================== FOOTER ===================== */
.footer {
  background: var(--color-text);
  color: rgba(255, 255, 255, 0.7);
  padding: var(--space-xl) 0 var(--space-lg);
}

.footer__inner {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: var(--space-xl);
  margin-bottom: var(--space-xl);
}

.footer__logo {
  font-family: var(--font-display);
  font-size: var(--font-size-xl);
  letter-spacing: 3px;
  color: var(--color-accent);
  margin-bottom: var(--space-sm);
}

.footer__tagline {
  font-size: var(--font-size-sm);
  margin-bottom: var(--space-md);
}

.footer__heading {
  font-family: var(--font-display);
  font-size: var(--font-size-base);
  letter-spacing: 1px;
  color: var(--color-white);
  margin-bottom: var(--space-sm);
}

.footer__link {
  display: block;
  padding: 4px 0;
  font-size: var(--font-size-sm);
  transition: color 0.2s;
}

.footer__link:hover {
  color: var(--color-primary);
}

.footer__bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: var(--space-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--font-size-xs);
}

.footer__socials {
  display: flex;
  gap: var(--space-sm);
  font-size: var(--font-size-xl);
}
```

- [ ] **Step 2: Add footer HTML before `</body>`**

```html
<footer class="footer">
  <div class="container">
    <div class="footer__inner">
      <div>
        <div class="footer__logo">FIESTALO'K</div>
        <p class="footer__tagline">On gonfle, vous kiffez 🎉<br>Les Kings du Gonflable depuis 2024.</p>
      </div>
      <div>
        <div class="footer__heading">NAVIGATION</div>
        <a href="#gonflables" class="footer__link">Nos Gonflables</a>
        <a href="#fonctionnement" class="footer__link">Comment ça marche</a>
        <a href="#tarifs" class="footer__link">Tarifs</a>
        <a href="#temoignages" class="footer__link">Témoignages</a>
        <a href="#contact" class="footer__link">Contact</a>
      </div>
      <div>
        <div class="footer__heading">INFOS</div>
        <a href="#" class="footer__link">Mentions légales</a>
        <a href="#" class="footer__link">CGV</a>
        <a href="#" class="footer__link">Politique de confidentialité</a>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2024 Fiestalo'K — Tous droits réservés</span>
      <div class="footer__socials">
        <a href="#" aria-label="Instagram">📸</a>
        <a href="#" aria-label="Facebook">👍</a>
        <a href="#" aria-label="TikTok">🎵</a>
      </div>
    </div>
  </div>
</footer>
```

- [ ] **Step 3: Verify in browser**

Expected: Dark footer with logo, navigation, legal links, and social icons.

- [ ] **Step 4: Commit**

```bash
git add css/sections.css index.html
git commit -m "feat: add footer with navigation, legal links, and socials"
```

---

### Task 11: Mobile responsive

**Files:**
- Create: `css/responsive.css`
- Modify: `index.html` (add stylesheet link)

- [ ] **Step 1: Create `css/responsive.css`**

```css
/* ===================== TABLET (< 768px) ===================== */
@media (max-width: 768px) {
  .navbar__links {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    flex-direction: column;
    background: var(--color-bg);
    padding: var(--space-md);
    border-bottom: 2px solid rgba(78, 205, 196, 0.15);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .navbar__links--open {
    display: flex;
  }

  .navbar__toggle {
    display: block;
  }

  .hero__title {
    font-size: var(--font-size-3xl);
  }

  .hero__trust {
    gap: var(--space-md);
  }

  .contact__inner {
    grid-template-columns: 1fr;
  }

  .footer__inner {
    grid-template-columns: 1fr;
    gap: var(--space-lg);
  }

  .pricing__grid {
    grid-template-columns: 1fr;
    max-width: 400px;
    margin: 0 auto;
  }
}

/* ===================== MOBILE (< 480px) ===================== */
@media (max-width: 480px) {
  :root {
    --space-section: 4rem;
  }

  .hero__title {
    font-size: var(--font-size-2xl);
  }

  .hero__buttons {
    flex-direction: column;
    align-items: center;
  }

  .hero__trust {
    flex-direction: column;
    gap: var(--space-sm);
    align-items: center;
  }

  .steps__grid {
    grid-template-columns: 1fr;
    max-width: 320px;
    margin: 0 auto;
  }

  .section-title {
    font-size: var(--font-size-2xl);
  }

  .footer__bottom {
    flex-direction: column;
    gap: var(--space-sm);
    text-align: center;
  }
}
```

- [ ] **Step 2: Add stylesheet link in `index.html` `<head>`**

Add after `sections.css`:

```html
<link rel="stylesheet" href="css/responsive.css">
```

- [ ] **Step 3: Verify in browser**

Test at 375px, 768px, and 1200px widths. Verify: navbar collapses to hamburger, grids stack vertically, hero text scales, form takes full width on mobile.

- [ ] **Step 4: Commit**

```bash
git add css/responsive.css index.html
git commit -m "feat: add responsive styles for mobile and tablet breakpoints"
```

---

### Task 12: JavaScript — mobile menu, smooth scroll, form handling

**Files:**
- Create: `js/main.js`
- Modify: `index.html` (add script tag)

- [ ] **Step 1: Create `js/main.js`**

```javascript
document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu toggle
  const toggle = document.querySelector('.navbar__toggle');
  const navLinks = document.querySelector('.navbar__links');

  toggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('navbar__links--open');
    toggle.setAttribute('aria-expanded', isOpen);
    toggle.textContent = isOpen ? '✕' : '☰';
  });

  // Close menu on link click
  navLinks.querySelectorAll('.navbar__link').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('navbar__links--open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = '☰';
    });
  });

  // Active link highlight on scroll
  const sections = document.querySelectorAll('section[id]');
  const navItems = document.querySelectorAll('.navbar__link');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY + 100;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollY >= top && scrollY < top + height) {
        navItems.forEach(item => {
          item.classList.remove('navbar__link--active');
          if (item.getAttribute('href') === '#' + id) {
            item.classList.add('navbar__link--active');
          }
        });
      }
    });
  });

  // Form submission
  const form = document.getElementById('contact-form');

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    // Validate required fields
    if (!data.name || !data.email || !data['event-type'] || !data.date) {
      alert('Remplis tous les champs obligatoires stp ! 🙏');
      return;
    }

    // For now, show success message (replace with actual API call later)
    form.innerHTML = `
      <div style="text-align: center; padding: 3rem 1rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
        <h3 style="font-family: var(--font-display); font-size: 1.5rem; letter-spacing: 1px; margin-bottom: 1rem;">
          DEMANDE ENVOYÉE !
        </h3>
        <p style="color: var(--color-text-light);">
          Merci ${data.name} ! On te recontacte en moins d'1h.<br>
          Prépare-toi, ta fiesta arrive bientôt ! 🚀
        </p>
      </div>
    `;
  });
});
```

- [ ] **Step 2: Add script tag before `</body>` in `index.html`**

```html
<script src="js/main.js"></script>
```

- [ ] **Step 3: Verify in browser**

Test: hamburger menu opens/closes on mobile, active link highlights on scroll, form shows success message on submit.

- [ ] **Step 4: Commit**

```bash
git add js/main.js index.html
git commit -m "feat: add mobile menu, scroll spy, and form handling"
```

---

### Task 13: Final polish & verification

**Files:**
- Modify: `index.html` (add favicon, Open Graph meta)

- [ ] **Step 1: Add meta tags to `<head>` in `index.html`**

After the existing `<meta name="description">`:

```html
<meta property="og:title" content="Fiestalo'K — Location de Châteaux Gonflables">
<meta property="og:description" content="On gonfle, vous kiffez ! Location de châteaux gonflables pour anniversaires, EVJF, team building & plus.">
<meta property="og:type" content="website">
<meta name="theme-color" content="#4ECDC4">
```

- [ ] **Step 2: Full visual review**

Open `index.html` in browser. Verify all sections render correctly:
- [ ] Navbar: fixed, logo left, links right, CTA button
- [ ] Hero: badge, title, subtitle, 2 buttons, trust bar
- [ ] Catalogue: 6 cards in responsive grid
- [ ] Comment ça marche: 4 steps in a row
- [ ] Tarifs: 3 cards, middle featured
- [ ] Témoignages: 3 review cards
- [ ] Contact: info + form side by side
- [ ] Footer: dark, 3 columns, socials
- [ ] Mobile: hamburger menu, stacked layouts

- [ ] **Step 3: Final commit**

```bash
git add index.html
git commit -m "feat: add Open Graph meta tags and theme color"
```
