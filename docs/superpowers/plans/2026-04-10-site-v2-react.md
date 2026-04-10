# Site Vitrine Fiestalo'K v2 — React Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construire une v2 multi-pages de Fiestalo'K (Accueil, Catalogue, Produit, Entreprise, Qui sommes-nous) avec panier persistant, en reprenant l'architecture/fonctionnalités du site de référence (`http://localhost:5173/`) et l'identité "Pop Décalé" du moodboard existant.

**Architecture:**
- SPA Vite + React + React Router, dans un nouveau dossier `site/` à la racine du repo (la v1 vanilla est conservée intacte).
- Données produits en JSON local, panier et avis persistés en `localStorage`. Aucune API backend.
- Découpage en **composants UI réutilisables** (Button, Badge, Card, Section, ProductCard, Sticker…) consommant des **design tokens CSS** issus du moodboard. Pas de framework UI ni Tailwind — CSS Modules + variables CSS pour rester proche de la DA et garder un contrôle fin.

**Tech Stack:**
- Vite 5 + React 18 + TypeScript
- React Router 6
- CSS Modules + variables CSS (tokens du moodboard)
- Google Fonts (Bangers, Nunito)
- `date-fns` pour le calendrier de disponibilités
- Vitest + React Testing Library pour les tests

---

## File Structure

Tout est créé sous `site/` (racine = `/Users/admin/Documents/perso/FiestaloK/site/`).

```
site/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── public/
│   └── og-image.png            # placeholder
├── src/
│   ├── main.tsx                # entry, router setup
│   ├── App.tsx                 # layout shell + routes
│   ├── styles/
│   │   ├── tokens.css          # variables CSS issues du moodboard
│   │   ├── reset.css
│   │   └── global.css          # base typography, body, scrollbar
│   ├── data/
│   │   ├── products.json       # 15 produits inspirés de la réf
│   │   ├── categories.ts       # liste catégories + emojis
│   │   └── unavailable.ts      # dates indisponibles mockées par produit
│   ├── lib/
│   │   ├── format.ts           # formatPrice, formatDate
│   │   └── storage.ts          # safeLocal getItem/setItem (JSON)
│   ├── context/
│   │   ├── CartContext.tsx     # provider + hook useCart
│   │   └── ReviewsContext.tsx  # provider + hook useReviews
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.tsx + .module.css
│   │   │   ├── Footer.tsx + .module.css
│   │   │   └── CartDrawer.tsx + .module.css
│   │   ├── ui/
│   │   │   ├── Button.tsx + .module.css
│   │   │   ├── Badge.tsx + .module.css      # sticker rotaté
│   │   │   ├── Section.tsx + .module.css
│   │   │   ├── Card.tsx + .module.css
│   │   │   ├── StarRating.tsx + .module.css
│   │   │   └── EmptyState.tsx + .module.css
│   │   ├── product/
│   │   │   ├── ProductCard.tsx + .module.css
│   │   │   ├── ProductGallery.tsx + .module.css
│   │   │   ├── AvailabilityCalendar.tsx + .module.css
│   │   │   ├── ReviewList.tsx + .module.css
│   │   │   └── ReviewForm.tsx + .module.css
│   │   └── catalogue/
│   │       ├── CatalogueFilters.tsx + .module.css
│   │       └── CategoryTabs.tsx + .module.css
│   ├── pages/
│   │   ├── HomePage.tsx + .module.css
│   │   ├── CataloguePage.tsx + .module.css
│   │   ├── ProductPage.tsx + .module.css
│   │   ├── EntreprisePage.tsx + .module.css
│   │   └── QuiSommesNousPage.tsx + .module.css
│   └── tests/
│       ├── CartContext.test.tsx
│       ├── CatalogueFilters.test.tsx
│       └── AvailabilityCalendar.test.tsx
```

**Decomposition principles**
- Une responsabilité par fichier ; les pages composent des composants, ne contiennent pas de logique métier.
- L'état global (panier, avis) vit dans deux contexts indépendants — pas de store global type Zustand pour rester simple.
- Les CSS Modules co-localisés avec leur composant pour faciliter la suppression.

---

## Task 1 — Scaffolding Vite + React + Router

**Files:**
- Create: `site/package.json`, `site/vite.config.ts`, `site/tsconfig.json`, `site/index.html`, `site/src/main.tsx`, `site/src/App.tsx`, `site/.gitignore`

- [ ] **Step 1: Créer le projet Vite**

```bash
cd /Users/admin/Documents/perso/FiestaloK
npm create vite@latest site -- --template react-ts
cd site
npm install
npm install react-router-dom date-fns
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

- [ ] **Step 2: Nettoyer le scaffold par défaut**

Supprimer : `src/App.css`, `src/index.css`, `src/assets/react.svg`, `public/vite.svg`. Vider `src/App.tsx` et `src/main.tsx` (on les réécrit étape suivante).

- [ ] **Step 3: Configurer Vite + Vitest**

Réécrire `site/vite.config.ts` :

```ts
/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: { port: 5174, open: true },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/tests/setup.ts',
  },
});
```

Créer `site/src/tests/setup.ts` :

```ts
import '@testing-library/jest-dom';
```

- [ ] **Step 4: Mettre en place le routing minimal**

Réécrire `site/src/main.tsx` :

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './styles/reset.css';
import './styles/tokens.css';
import './styles/global.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
```

Réécrire `site/src/App.tsx` :

```tsx
import { Routes, Route } from 'react-router-dom';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<div>Home placeholder</div>} />
    </Routes>
  );
}
```

Créer trois fichiers vides `site/src/styles/{reset,tokens,global}.css` (contenu rempli en Task 2). Mettre à jour `site/index.html` pour utiliser `<title>Fiestalo'K — Location de matériel festif</title>` et ajouter les balises Google Fonts (Bangers + Nunito) + meta viewport + meta description + Open Graph.

- [ ] **Step 5: Vérifier le build**

```bash
cd site && npm run build && npm run dev
```

Expected : `npm run build` exit 0 ; `npm run dev` démarre sur :5174 et affiche "Home placeholder".

- [ ] **Step 6: Commit**

```bash
cd /Users/admin/Documents/perso/FiestaloK
git add site/ -- ':!site/node_modules'
git commit -m "feat(site-v2): scaffold Vite + React + Router project"
```

---

## Task 2 — Design tokens, reset et global styles

**Files:**
- Modify: `site/src/styles/tokens.css`, `site/src/styles/reset.css`, `site/src/styles/global.css`
- Modify: `site/index.html` (s'assurer que les fonts sont préchargées)

- [ ] **Step 1: Écrire `tokens.css`**

```css
:root {
  /* Palette Pop Décalé */
  --color-bg: #F8F9FA;
  --color-bg-alt: #FFFFFF;
  --color-ink: #2D3436;
  --color-ink-soft: #5b6266;
  --color-primary: #4ECDC4;     /* turquoise */
  --color-accent: #FFE66D;      /* jaune pétant */
  --color-success: #44CF6C;     /* vert menthe */
  --color-danger: #FF6B6B;      /* corail punch */
  --color-border: #e6e8eb;

  /* Typography */
  --font-display: 'Bangers', 'Impact', system-ui, sans-serif;
  --font-body: 'Nunito', system-ui, -apple-system, sans-serif;

  /* Scale */
  --space-2xs: 0.25rem;
  --space-xs: 0.5rem;
  --space-sm: 0.75rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2.5rem;
  --space-2xl: 4rem;
  --space-3xl: 6rem;

  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-pill: 999px;

  --shadow-sm: 0 2px 8px rgba(45, 52, 54, 0.06);
  --shadow-md: 0 8px 24px rgba(45, 52, 54, 0.10);
  --shadow-lg: 0 18px 40px rgba(45, 52, 54, 0.14);
  --shadow-sticker: 4px 4px 0 rgba(45, 52, 54, 0.85);

  --container-max: 1200px;
  --navbar-height: 72px;
}
```

- [ ] **Step 2: Écrire `reset.css`**

```css
*, *::before, *::after { box-sizing: border-box; }
* { margin: 0; padding: 0; }
html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body { -webkit-font-smoothing: antialiased; line-height: 1.5; }
img, picture, video, canvas, svg { display: block; max-width: 100%; }
button, input, textarea, select { font: inherit; color: inherit; }
button { background: none; border: none; cursor: pointer; }
a { color: inherit; text-decoration: none; }
ul, ol { list-style: none; }
```

- [ ] **Step 3: Écrire `global.css`**

```css
body {
  font-family: var(--font-body);
  color: var(--color-ink);
  background: var(--color-bg);
  font-weight: 500;
}
h1, h2, h3, h4 {
  font-family: var(--font-display);
  font-weight: 400;
  letter-spacing: 0.02em;
  line-height: 1.05;
  color: var(--color-ink);
}
h1 { font-size: clamp(2.5rem, 5vw + 1rem, 4.5rem); }
h2 { font-size: clamp(2rem, 3vw + 1rem, 3rem); }
h3 { font-size: 1.5rem; }
.container {
  width: 100%;
  max-width: var(--container-max);
  margin: 0 inline;
  margin-inline: auto;
  padding: 0 var(--space-lg);
}
::selection { background: var(--color-accent); color: var(--color-ink); }

/* Pattern décoratif réutilisable (confettis) */
.bg-confetti {
  background-image:
    radial-gradient(circle at 10% 20%, var(--color-accent) 0 6px, transparent 7px),
    radial-gradient(circle at 80% 30%, var(--color-primary) 0 5px, transparent 6px),
    radial-gradient(circle at 30% 80%, var(--color-danger) 0 4px, transparent 5px),
    radial-gradient(circle at 70% 70%, var(--color-success) 0 5px, transparent 6px);
  background-size: 280px 280px;
  background-repeat: repeat;
}
```

- [ ] **Step 4: Vérifier visuellement**

`npm run dev`, ouvrir :5174, l'arrière-plan doit être blanc cassé, la police body Nunito.

- [ ] **Step 5: Commit**

```bash
git add site/src/styles/ site/index.html
git commit -m "feat(site-v2): add Pop Décalé design tokens and base styles"
```

---

## Task 3 — Données produits et utilitaires

**Files:**
- Create: `site/src/data/products.json`, `site/src/data/categories.ts`, `site/src/data/unavailable.ts`, `site/src/lib/format.ts`, `site/src/lib/storage.ts`

- [ ] **Step 1: Définir le type Product et `categories.ts`**

Créer `site/src/data/categories.ts` :

```ts
export type CategoryId = 'chateau-gonflable' | 'accessoire' | 'restauration' | 'enceintes';

export interface Category {
  id: CategoryId;
  label: string;
  emoji: string;
}

export const CATEGORIES: Category[] = [
  { id: 'chateau-gonflable', label: 'Château Gonflable', emoji: '🏰' },
  { id: 'accessoire',        label: 'Accessoire',        emoji: '🎭' },
  { id: 'restauration',      label: 'Restauration',      emoji: '🍴' },
  { id: 'enceintes',         label: 'Sono & Enceintes',  emoji: '🔊' },
];

export const AUDIENCES = ['enfants', 'adultes', 'entreprises'] as const;
export type Audience = typeof AUDIENCES[number];
```

- [ ] **Step 2: Créer `products.json`**

15 produits inspirés du site de référence. Schéma :

```json
[
  {
    "id": "1",
    "name": "Château Gonflable Classique",
    "category": "chateau-gonflable",
    "audiences": ["enfants"],
    "shortDescription": "Le grand classique pour les anniversaires d'enfants. 4×4m, jusqu'à 6 enfants.",
    "longDescription": "Un château gonflable coloré, sécurisé et homologué CE. Parfait pour les 3-10 ans. Installation en 30 min. On gonfle, vous kiffez !",
    "price": 120,
    "rating": 4.5,
    "reviewCount": 2,
    "specs": { "Dimensions": "4m × 4m × 3m", "Âge": "3 - 10 ans", "Capacité": "6 enfants" },
    "images": [
      "https://images.unsplash.com/photo-1516733725897-1aa73b87c8e8?w=800",
      "https://images.unsplash.com/photo-1567606404787-5d9e44d4fb41?w=800",
      "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=800"
    ],
    "badge": null
  }
]
```

Inclure 15 entrées (au minimum) couvrant les 4 catégories : Château Classique, Toboggan, Obstacle, Photobooth Ouvert, Photobooth 360°, Déguisements, Miroir Personnalisé, Popcorn, Crêpes, Barbecue, Barbe à Papa, Enceinte 500W, Pack Sono 2000W, Boule à Facette, Pack DJ Complet. Pour chaque, mettre 1 à 3 URLs d'images Unsplash plausibles (`?w=800`), une note entre 4 et 5, un prix réaliste (30 à 350€/jour), et au moins 2 produits avec un badge ("PROMO", "TOP VENTE", ou "NOUVEAU"). Toutes les `audiences` viennent de `AUDIENCES`.

- [ ] **Step 3: Créer `unavailable.ts`**

```ts
// Map productId -> liste de dates ISO indisponibles (mock).
// Les dates sont relatives à "aujourd'hui" pour rester pertinentes.
import { addDays, format } from 'date-fns';

const today = new Date();
const iso = (d: Date) => format(d, 'yyyy-MM-dd');

export const UNAVAILABLE_DATES: Record<string, string[]> = {
  '1': [iso(addDays(today, 3)), iso(addDays(today, 4)), iso(addDays(today, 10))],
  '2': [iso(addDays(today, 5)), iso(addDays(today, 12))],
  '3': [iso(addDays(today, 7))],
};

export function isDateUnavailable(productId: string, date: Date): boolean {
  const list = UNAVAILABLE_DATES[productId] ?? [];
  return list.includes(iso(date));
}
```

- [ ] **Step 4: Helpers `format.ts` et `storage.ts`**

`site/src/lib/format.ts` :

```ts
export function formatPrice(amount: number): string {
  return `${amount}€/jour`;
}

export function formatDateLong(date: Date): string {
  return new Intl.DateTimeFormat('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric',
  }).format(date);
}
```

`site/src/lib/storage.ts` :

```ts
export function loadJSON<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

export function saveJSON<T>(key: string, value: T): void {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* quota or unavailable — ignore silently */
  }
}
```

- [ ] **Step 5: Type Product partagé**

Créer `site/src/data/types.ts` :

```ts
import type { CategoryId, Audience } from './categories';

export interface Product {
  id: string;
  name: string;
  category: CategoryId;
  audiences: Audience[];
  shortDescription: string;
  longDescription: string;
  price: number;
  rating: number;
  reviewCount: number;
  specs: Record<string, string>;
  images: string[];
  badge: 'PROMO' | 'TOP VENTE' | 'NOUVEAU' | null;
}

export interface Review {
  id: string;
  productId: string;
  author: string;
  rating: number;
  comment: string;
  date: string; // ISO
}

export interface CartItem {
  productId: string;
  startDate: string | null;
  endDate: string | null;
  quantity: number;
}
```

- [ ] **Step 6: Commit**

```bash
git add site/src/data/ site/src/lib/
git commit -m "feat(site-v2): add product data, categories and storage helpers"
```

---

## Task 4 — Composants UI atomiques (Button, Badge, Section, StarRating)

**Files:**
- Create: `site/src/components/ui/Button.tsx` + `Button.module.css`
- Create: `site/src/components/ui/Badge.tsx` + `Badge.module.css`
- Create: `site/src/components/ui/Section.tsx` + `Section.module.css`
- Create: `site/src/components/ui/StarRating.tsx` + `StarRating.module.css`

- [ ] **Step 1: Button**

`Button.tsx` :

```tsx
import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import styles from './Button.module.css';

type Variant = 'primary' | 'secondary' | 'ghost' | 'danger';
type Size = 'sm' | 'md' | 'lg';

interface CommonProps {
  variant?: Variant;
  size?: Size;
  children: ReactNode;
  className?: string;
}

type ButtonProps = CommonProps & ButtonHTMLAttributes<HTMLButtonElement> & { to?: never };
type LinkButtonProps = CommonProps & { to: string; href?: never };

export const Button = forwardRef<HTMLButtonElement, ButtonProps | LinkButtonProps>(
  ({ variant = 'primary', size = 'md', className = '', children, ...rest }, ref) => {
    const cls = `${styles.btn} ${styles[variant]} ${styles[size]} ${className}`;
    if ('to' in rest && rest.to) {
      return <Link to={rest.to} className={cls}>{children}</Link>;
    }
    return (
      <button ref={ref} className={cls} {...(rest as ButtonHTMLAttributes<HTMLButtonElement>)}>
        {children}
      </button>
    );
  }
);
Button.displayName = 'Button';
```

`Button.module.css` :

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-xs);
  font-family: var(--font-body);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-radius: var(--radius-pill);
  transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
  white-space: nowrap;
}
.btn:hover { transform: translateY(-2px); }
.btn:active { transform: translateY(0); }

.sm { padding: 0.5rem 1rem; font-size: 0.8rem; }
.md { padding: 0.75rem 1.5rem; font-size: 0.9rem; }
.lg { padding: 1rem 2rem; font-size: 1rem; }

.primary {
  background: var(--color-accent);
  color: var(--color-ink);
  box-shadow: var(--shadow-md);
}
.primary:hover { background: #ffe24a; }

.secondary {
  background: transparent;
  color: var(--color-ink);
  border: 2px solid var(--color-ink);
}
.secondary:hover { background: var(--color-ink); color: var(--color-bg); }

.danger {
  background: var(--color-danger);
  color: white;
  box-shadow: var(--shadow-md);
}
.danger:hover { background: #ff5252; }

.ghost {
  background: transparent;
  color: var(--color-ink);
}
.ghost:hover { background: rgba(0,0,0,0.04); }
```

- [ ] **Step 2: Badge (sticker rotaté)**

`Badge.tsx` :

```tsx
import type { ReactNode } from 'react';
import styles from './Badge.module.css';

interface BadgeProps {
  children: ReactNode;
  tone?: 'accent' | 'primary' | 'danger' | 'success';
  rotation?: number; // degrés
  className?: string;
}

export function Badge({ children, tone = 'accent', rotation = -3, className = '' }: BadgeProps) {
  return (
    <span
      className={`${styles.badge} ${styles[tone]} ${className}`}
      style={{ transform: `rotate(${rotation}deg)` }}
    >
      {children}
    </span>
  );
}
```

`Badge.module.css` :

```css
.badge {
  display: inline-block;
  padding: 0.4rem 0.9rem;
  font-family: var(--font-display);
  font-size: 0.95rem;
  letter-spacing: 0.06em;
  border-radius: var(--radius-lg);
  border: 2px solid var(--color-ink);
  box-shadow: var(--shadow-sticker);
  white-space: nowrap;
}
.accent  { background: var(--color-accent);  color: var(--color-ink); }
.primary { background: var(--color-primary); color: var(--color-ink); }
.danger  { background: var(--color-danger);  color: white; }
.success { background: var(--color-success); color: var(--color-ink); }
```

- [ ] **Step 3: Section wrapper**

`Section.tsx` :

```tsx
import type { ReactNode } from 'react';
import styles from './Section.module.css';

interface SectionProps {
  eyebrow?: string;
  title?: string;
  subtitle?: string;
  background?: 'light' | 'dark' | 'accent';
  children: ReactNode;
  id?: string;
}

export function Section({ eyebrow, title, subtitle, background = 'light', children, id }: SectionProps) {
  return (
    <section id={id} className={`${styles.section} ${styles[background]}`}>
      <div className="container">
        {(eyebrow || title || subtitle) && (
          <header className={styles.header}>
            {eyebrow && <p className={styles.eyebrow}>{eyebrow}</p>}
            {title && <h2 className={styles.title}>{title}</h2>}
            {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
          </header>
        )}
        {children}
      </div>
    </section>
  );
}
```

`Section.module.css` :

```css
.section { padding: var(--space-3xl) 0; }
.light  { background: var(--color-bg); color: var(--color-ink); }
.dark   { background: var(--color-ink); color: var(--color-bg); }
.accent { background: var(--color-accent); color: var(--color-ink); }

.header { text-align: center; max-width: 720px; margin: 0 auto var(--space-2xl); }
.eyebrow {
  font-family: var(--font-display);
  letter-spacing: 0.15em;
  color: var(--color-danger);
  margin-bottom: var(--space-xs);
  font-size: 0.9rem;
}
.title { margin-bottom: var(--space-sm); }
.subtitle { color: var(--color-ink-soft); font-size: 1.1rem; }
.dark .subtitle { color: rgba(255,255,255,0.75); }
.dark .title    { color: var(--color-bg); }
```

- [ ] **Step 4: StarRating**

`StarRating.tsx` :

```tsx
import styles from './StarRating.module.css';

interface StarRatingProps {
  value: number;
  count?: number;
  size?: 'sm' | 'md';
}

export function StarRating({ value, count, size = 'sm' }: StarRatingProps) {
  const full = Math.floor(value);
  const half = value - full >= 0.5;
  const stars = Array.from({ length: 5 }, (_, i) => {
    if (i < full) return '★';
    if (i === full && half) return '⯨';
    return '☆';
  });
  return (
    <span className={`${styles.wrap} ${styles[size]}`} aria-label={`Note ${value} sur 5`}>
      <span className={styles.stars}>{stars.join('')}</span>
      <span className={styles.value}>{value.toFixed(1)}</span>
      {count !== undefined && <span className={styles.count}>({count})</span>}
    </span>
  );
}
```

`StarRating.module.css` :

```css
.wrap { display: inline-flex; align-items: center; gap: 0.4rem; color: var(--color-danger); }
.stars { letter-spacing: 0.05em; }
.value { font-weight: 800; color: var(--color-ink); }
.count { color: var(--color-ink-soft); font-weight: 600; }
.sm { font-size: 0.85rem; }
.md { font-size: 1rem; }
```

- [ ] **Step 5: Vérifier compilation**

```bash
cd site && npm run build
```

Expected : exit 0, pas d'erreur TS.

- [ ] **Step 6: Commit**

```bash
git add site/src/components/ui/
git commit -m "feat(site-v2): add atomic UI components (Button, Badge, Section, StarRating)"
```

---

## Task 5 — Cart context + tests + Reviews context

**Files:**
- Create: `site/src/context/CartContext.tsx`, `site/src/context/ReviewsContext.tsx`
- Create: `site/src/tests/CartContext.test.tsx`

- [ ] **Step 1: Écrire le test du panier**

`site/src/tests/CartContext.test.tsx` :

```tsx
import { describe, it, expect, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { CartProvider, useCart } from '../context/CartContext';

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <CartProvider>{children}</CartProvider>
);

describe('CartContext', () => {
  beforeEach(() => localStorage.clear());

  it('starts empty', () => {
    const { result } = renderHook(() => useCart(), { wrapper });
    expect(result.current.items).toEqual([]);
    expect(result.current.totalItems).toBe(0);
  });

  it('adds an item', () => {
    const { result } = renderHook(() => useCart(), { wrapper });
    act(() => result.current.add({ productId: '1', startDate: null, endDate: null, quantity: 1 }));
    expect(result.current.items).toHaveLength(1);
    expect(result.current.totalItems).toBe(1);
  });

  it('increments quantity when adding the same product', () => {
    const { result } = renderHook(() => useCart(), { wrapper });
    act(() => result.current.add({ productId: '1', startDate: null, endDate: null, quantity: 1 }));
    act(() => result.current.add({ productId: '1', startDate: null, endDate: null, quantity: 2 }));
    expect(result.current.items).toHaveLength(1);
    expect(result.current.items[0].quantity).toBe(3);
  });

  it('removes an item', () => {
    const { result } = renderHook(() => useCart(), { wrapper });
    act(() => result.current.add({ productId: '1', startDate: null, endDate: null, quantity: 1 }));
    act(() => result.current.remove('1'));
    expect(result.current.items).toEqual([]);
  });

  it('persists across remounts via localStorage', () => {
    const first = renderHook(() => useCart(), { wrapper });
    act(() => first.result.current.add({ productId: '1', startDate: null, endDate: null, quantity: 2 }));
    const second = renderHook(() => useCart(), { wrapper });
    expect(second.result.current.items[0].quantity).toBe(2);
  });
});
```

- [ ] **Step 2: Faire échouer le test**

```bash
cd site && npx vitest run src/tests/CartContext.test.tsx
```

Expected : FAIL (`CartProvider` introuvable).

- [ ] **Step 3: Implémenter `CartContext.tsx`**

```tsx
import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import type { CartItem } from '../data/types';
import { loadJSON, saveJSON } from '../lib/storage';

const STORAGE_KEY = 'fiestalok.cart.v1';

interface CartContextValue {
  items: CartItem[];
  totalItems: number;
  isOpen: boolean;
  open: () => void;
  close: () => void;
  add: (item: CartItem) => void;
  remove: (productId: string) => void;
  setQuantity: (productId: string, quantity: number) => void;
  clear: () => void;
}

const CartContext = createContext<CartContextValue | null>(null);

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>(() => loadJSON<CartItem[]>(STORAGE_KEY, []));
  const [isOpen, setOpen] = useState(false);

  useEffect(() => { saveJSON(STORAGE_KEY, items); }, [items]);

  const value = useMemo<CartContextValue>(() => ({
    items,
    totalItems: items.reduce((sum, i) => sum + i.quantity, 0),
    isOpen,
    open: () => setOpen(true),
    close: () => setOpen(false),
    add: (incoming) => setItems((prev) => {
      const existing = prev.find((i) => i.productId === incoming.productId);
      if (existing) {
        return prev.map((i) =>
          i.productId === incoming.productId
            ? { ...i, quantity: i.quantity + incoming.quantity, startDate: incoming.startDate ?? i.startDate, endDate: incoming.endDate ?? i.endDate }
            : i
        );
      }
      return [...prev, incoming];
    }),
    remove: (id) => setItems((prev) => prev.filter((i) => i.productId !== id)),
    setQuantity: (id, qty) => setItems((prev) => prev.map((i) => i.productId === id ? { ...i, quantity: Math.max(1, qty) } : i)),
    clear: () => setItems([]),
  }), [items, isOpen]);

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart(): CartContextValue {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error('useCart must be used within a CartProvider');
  return ctx;
}
```

- [ ] **Step 4: Faire passer les tests**

```bash
cd site && npx vitest run src/tests/CartContext.test.tsx
```

Expected : 5 passed.

- [ ] **Step 5: Implémenter `ReviewsContext.tsx`**

```tsx
import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import type { Review } from '../data/types';
import { loadJSON, saveJSON } from '../lib/storage';

const STORAGE_KEY = 'fiestalok.reviews.v1';

interface ReviewsContextValue {
  reviews: Review[];
  forProduct: (productId: string) => Review[];
  add: (review: Omit<Review, 'id' | 'date'>) => void;
}

const ReviewsContext = createContext<ReviewsContextValue | null>(null);

export function ReviewsProvider({ children }: { children: ReactNode }) {
  const [reviews, setReviews] = useState<Review[]>(() => loadJSON<Review[]>(STORAGE_KEY, []));
  useEffect(() => { saveJSON(STORAGE_KEY, reviews); }, [reviews]);

  const value = useMemo<ReviewsContextValue>(() => ({
    reviews,
    forProduct: (id) => reviews.filter((r) => r.productId === id),
    add: (r) => setReviews((prev) => [
      ...prev,
      { ...r, id: crypto.randomUUID(), date: new Date().toISOString().slice(0, 10) },
    ]),
  }), [reviews]);

  return <ReviewsContext.Provider value={value}>{children}</ReviewsContext.Provider>;
}

export function useReviews(): ReviewsContextValue {
  const ctx = useContext(ReviewsContext);
  if (!ctx) throw new Error('useReviews must be used within a ReviewsProvider');
  return ctx;
}
```

- [ ] **Step 6: Commit**

```bash
git add site/src/context/ site/src/tests/CartContext.test.tsx
git commit -m "feat(site-v2): add cart and reviews contexts with localStorage persistence"
```

---

## Task 6 — Layout shell : Navbar, Footer, CartDrawer

**Files:**
- Create: `site/src/components/layout/Navbar.tsx` + `.module.css`
- Create: `site/src/components/layout/Footer.tsx` + `.module.css`
- Create: `site/src/components/layout/CartDrawer.tsx` + `.module.css`
- Modify: `site/src/App.tsx` (wrap providers + render layout)

- [ ] **Step 1: Navbar**

`Navbar.tsx` :

```tsx
import { NavLink, Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import styles from './Navbar.module.css';

const LINKS = [
  { to: '/',                label: 'Accueil' },
  { to: '/catalogue',       label: 'Catalogue' },
  { to: '/entreprise',      label: 'Entreprise' },
  { to: '/qui-sommes-nous', label: 'Qui sommes-nous' },
];

export function Navbar() {
  const { totalItems, open } = useCart();
  return (
    <header className={styles.header}>
      <div className={`container ${styles.inner}`}>
        <Link to="/" className={styles.logo}>Fiestalo'<span>K</span></Link>
        <nav className={styles.nav} aria-label="Navigation principale">
          {LINKS.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.to === '/'}
              className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ''}`}
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
        <button className={styles.cart} onClick={open} aria-label={`Panier, ${totalItems} articles`}>
          🛒 Panier {totalItems > 0 && <span className={styles.badge}>{totalItems}</span>}
        </button>
      </div>
    </header>
  );
}
```

`Navbar.module.css` :

```css
.header {
  position: sticky; top: 0; z-index: 50;
  background: var(--color-bg-alt);
  border-bottom: 1px solid var(--color-border);
  height: var(--navbar-height);
  display: flex; align-items: center;
}
.inner { display: flex; align-items: center; justify-content: space-between; gap: var(--space-lg); }
.logo {
  font-family: var(--font-display);
  font-size: 1.8rem;
  letter-spacing: 0.04em;
  color: var(--color-ink);
}
.logo span { color: var(--color-danger); }
.nav { display: flex; gap: var(--space-lg); }
.link {
  font-weight: 700;
  padding: 0.4rem 0.6rem;
  border-bottom: 2px solid transparent;
  transition: color 0.15s ease, border-color 0.15s ease;
}
.link:hover { color: var(--color-primary); }
.active { color: var(--color-primary); border-bottom-color: var(--color-primary); }
.cart {
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: var(--color-ink); color: var(--color-bg);
  padding: 0.6rem 1.2rem; border-radius: var(--radius-pill);
  font-weight: 800; font-size: 0.9rem;
}
.cart:hover { background: var(--color-danger); }
.badge {
  background: var(--color-accent); color: var(--color-ink);
  border-radius: var(--radius-pill);
  padding: 0.05rem 0.5rem; font-size: 0.75rem;
}
```

- [ ] **Step 2: Footer**

`Footer.tsx` :

```tsx
import { Link } from 'react-router-dom';
import styles from './Footer.module.css';

export function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={`container ${styles.grid}`}>
        <div>
          <p className={styles.logo}>Fiestalo'<span>K</span></p>
          <p className={styles.tagline}>Location de matériel festif en Alsace.<br/>On gonfle, vous kiffez.</p>
          <div className={styles.socials}>
            <a href="#" aria-label="Instagram">📷</a>
            <a href="#" aria-label="Facebook">👍</a>
            <a href="#" aria-label="TikTok">🎵</a>
          </div>
        </div>
        <div>
          <h4 className={styles.title}>Navigation</h4>
          <ul>
            <li><Link to="/catalogue">Catalogue</Link></li>
            <li><Link to="/entreprise">Entreprise</Link></li>
            <li><Link to="/qui-sommes-nous">Qui sommes-nous</Link></li>
          </ul>
        </div>
        <div>
          <h4 className={styles.title}>Contact</h4>
          <ul>
            <li>📍 Strasbourg, Alsace</li>
            <li>📞 +33 6 00 00 00 00</li>
            <li>✉️ contact@fiestalok.fr</li>
            <li>🕐 Lun–Sam, 9h–19h</li>
          </ul>
        </div>
      </div>
      <div className={styles.bottom}>
        <p>© 2026 Fiestalo'K — Tous droits réservés</p>
        <p>Fait avec ❤️ en Alsace</p>
      </div>
    </footer>
  );
}
```

`Footer.module.css` :

```css
.footer { background: var(--color-ink); color: var(--color-bg); padding: var(--space-3xl) 0 var(--space-lg); margin-top: var(--space-3xl); }
.grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: var(--space-2xl); }
.logo { font-family: var(--font-display); font-size: 1.8rem; }
.logo span { color: var(--color-danger); }
.tagline { color: rgba(255,255,255,0.75); margin: var(--space-sm) 0 var(--space-md); }
.socials { display: flex; gap: var(--space-sm); font-size: 1.4rem; }
.title { font-family: var(--font-display); color: var(--color-danger); margin-bottom: var(--space-sm); letter-spacing: 0.1em; font-size: 1rem; }
.footer ul { display: flex; flex-direction: column; gap: var(--space-xs); color: rgba(255,255,255,0.75); }
.footer ul a:hover { color: var(--color-accent); }
.bottom { border-top: 1px solid rgba(255,255,255,0.12); margin-top: var(--space-2xl); padding-top: var(--space-md); display: flex; justify-content: space-between; color: rgba(255,255,255,0.5); font-size: 0.85rem; }
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; gap: var(--space-xl); }
  .bottom { flex-direction: column; gap: var(--space-xs); text-align: center; }
}
```

- [ ] **Step 3: CartDrawer**

`CartDrawer.tsx` :

```tsx
import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import productsRaw from '../../data/products.json';
import type { Product } from '../../data/types';
import { Button } from '../ui/Button';
import { formatPrice } from '../../lib/format';
import styles from './CartDrawer.module.css';

const products = productsRaw as Product[];
const findProduct = (id: string) => products.find((p) => p.id === id);

export function CartDrawer() {
  const { isOpen, close, items, remove, setQuantity, clear } = useCart();

  useEffect(() => {
    if (!isOpen) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [isOpen, close]);

  const total = items.reduce((sum, i) => {
    const p = findProduct(i.productId);
    return sum + (p ? p.price * i.quantity : 0);
  }, 0);

  return (
    <>
      <div
        className={`${styles.backdrop} ${isOpen ? styles.open : ''}`}
        onClick={close}
        aria-hidden={!isOpen}
      />
      <aside className={`${styles.drawer} ${isOpen ? styles.open : ''}`} aria-label="Panier">
        <header className={styles.header}>
          <div>
            <h3>Mon panier</h3>
            <p>{items.length === 0 ? 'Aucun article' : `${items.length} article${items.length > 1 ? 's' : ''}`}</p>
          </div>
          <button onClick={close} aria-label="Fermer" className={styles.closeBtn}>✕</button>
        </header>

        {items.length === 0 ? (
          <div className={styles.empty}>
            <div className={styles.emptyIcon}>🛒</div>
            <p className={styles.emptyTitle}>Panier vide</p>
            <p className={styles.emptyText}>Ajoutez des articles depuis le catalogue</p>
            <Button to="/catalogue" variant="primary" size="md">Voir le catalogue</Button>
          </div>
        ) : (
          <>
            <ul className={styles.list}>
              {items.map((i) => {
                const p = findProduct(i.productId);
                if (!p) return null;
                return (
                  <li key={i.productId} className={styles.item}>
                    <img src={p.images[0]} alt={p.name} />
                    <div className={styles.itemBody}>
                      <p className={styles.itemName}>{p.name}</p>
                      <p className={styles.itemPrice}>{formatPrice(p.price)}</p>
                      <div className={styles.qty}>
                        <button onClick={() => setQuantity(i.productId, i.quantity - 1)}>−</button>
                        <span>{i.quantity}</span>
                        <button onClick={() => setQuantity(i.productId, i.quantity + 1)}>+</button>
                      </div>
                    </div>
                    <button className={styles.removeBtn} onClick={() => remove(i.productId)} aria-label="Retirer">🗑</button>
                  </li>
                );
              })}
            </ul>
            <footer className={styles.footer}>
              <div className={styles.totalRow}>
                <span>Total estimé</span>
                <strong>{total}€</strong>
              </div>
              <Button variant="primary" size="lg" onClick={() => alert('Demande de devis envoyée — on vous rappelle !')}>
                Demander un devis
              </Button>
              <button className={styles.clearBtn} onClick={clear}>Vider le panier</button>
            </footer>
          </>
        )}
      </aside>
    </>
  );
}
```

`CartDrawer.module.css` :

```css
.backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); opacity: 0; pointer-events: none; transition: opacity 0.25s ease; z-index: 90; }
.backdrop.open { opacity: 1; pointer-events: auto; }
.drawer {
  position: fixed; top: 0; right: 0; bottom: 0;
  width: min(420px, 100%);
  background: var(--color-bg-alt);
  box-shadow: var(--shadow-lg);
  transform: translateX(100%);
  transition: transform 0.3s ease;
  z-index: 100;
  display: flex; flex-direction: column;
}
.drawer.open { transform: translateX(0); }
.header { display: flex; justify-content: space-between; align-items: center; padding: var(--space-lg); background: var(--color-ink); color: var(--color-bg); }
.header h3 { font-family: var(--font-display); color: var(--color-bg); font-size: 1.6rem; }
.header p { color: rgba(255,255,255,0.7); font-size: 0.9rem; }
.closeBtn { color: var(--color-bg); font-size: 1.4rem; }
.empty { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--space-md); padding: var(--space-2xl); text-align: center; }
.emptyIcon { font-size: 3rem; opacity: 0.5; }
.emptyTitle { font-family: var(--font-display); font-size: 1.5rem; }
.emptyText { color: var(--color-ink-soft); }
.list { flex: 1; overflow-y: auto; padding: var(--space-md); display: flex; flex-direction: column; gap: var(--space-md); }
.item { display: grid; grid-template-columns: 80px 1fr auto; gap: var(--space-sm); align-items: center; padding: var(--space-sm); border: 1px solid var(--color-border); border-radius: var(--radius-md); }
.item img { width: 80px; height: 80px; object-fit: cover; border-radius: var(--radius-sm); }
.itemName { font-weight: 800; font-size: 0.95rem; }
.itemPrice { color: var(--color-danger); font-weight: 700; font-size: 0.85rem; }
.qty { display: flex; align-items: center; gap: var(--space-xs); margin-top: var(--space-2xs); }
.qty button { width: 26px; height: 26px; border-radius: 50%; background: var(--color-bg); border: 1px solid var(--color-border); font-weight: 800; }
.removeBtn { font-size: 1.1rem; }
.footer { padding: var(--space-lg); border-top: 1px solid var(--color-border); display: flex; flex-direction: column; gap: var(--space-sm); }
.totalRow { display: flex; justify-content: space-between; font-size: 1.1rem; }
.totalRow strong { font-family: var(--font-display); font-size: 1.6rem; color: var(--color-danger); }
.clearBtn { color: var(--color-ink-soft); font-size: 0.85rem; text-decoration: underline; }
```

- [ ] **Step 4: Wrapper App.tsx avec providers + layout**

```tsx
import { Routes, Route } from 'react-router-dom';
import { CartProvider } from './context/CartContext';
import { ReviewsProvider } from './context/ReviewsContext';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { CartDrawer } from './components/layout/CartDrawer';
import { HomePage } from './pages/HomePage';
import { CataloguePage } from './pages/CataloguePage';
import { ProductPage } from './pages/ProductPage';
import { EntreprisePage } from './pages/EntreprisePage';
import { QuiSommesNousPage } from './pages/QuiSommesNousPage';

export default function App() {
  return (
    <CartProvider>
      <ReviewsProvider>
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/catalogue" element={<CataloguePage />} />
            <Route path="/produit/:id" element={<ProductPage />} />
            <Route path="/entreprise" element={<EntreprisePage />} />
            <Route path="/qui-sommes-nous" element={<QuiSommesNousPage />} />
          </Routes>
        </main>
        <Footer />
        <CartDrawer />
      </ReviewsProvider>
    </CartProvider>
  );
}
```

- [ ] **Step 5: Stub temporaire pour les pages**

Créer chaque fichier `site/src/pages/{HomePage,CataloguePage,ProductPage,EntreprisePage,QuiSommesNousPage}.tsx` avec :

```tsx
export function HomePage() { return <div className="container" style={{padding:'4rem 0'}}><h1>Home — TODO</h1></div>; }
```

(adapter le nom dans chaque fichier)

- [ ] **Step 6: Build & visual check**

```bash
cd site && npm run build && npm run dev
```

Naviguer sur :5174 — la navbar et le footer doivent s'afficher, le panier doit s'ouvrir/fermer.

- [ ] **Step 7: Commit**

```bash
git add site/src/components/layout/ site/src/App.tsx site/src/pages/
git commit -m "feat(site-v2): add layout shell (Navbar, Footer, CartDrawer) and page stubs"
```

---

## Task 7 — ProductCard et HomePage

**Files:**
- Create: `site/src/components/product/ProductCard.tsx` + `.module.css`
- Modify: `site/src/pages/HomePage.tsx` + `HomePage.module.css`

- [ ] **Step 1: ProductCard**

```tsx
import { Link } from 'react-router-dom';
import type { Product } from '../../data/types';
import { Badge } from '../ui/Badge';
import { StarRating } from '../ui/StarRating';
import { CATEGORIES } from '../../data/categories';
import styles from './ProductCard.module.css';

interface ProductCardProps { product: Product; }

export function ProductCard({ product }: ProductCardProps) {
  const cat = CATEGORIES.find((c) => c.id === product.category);
  return (
    <Link to={`/produit/${product.id}`} className={styles.card}>
      <div className={styles.imgWrap}>
        <img src={product.images[0]} alt={product.name} loading="lazy" />
        {cat && <span className={styles.cat}>{cat.emoji}</span>}
        {product.badge && <Badge tone={product.badge === 'PROMO' ? 'danger' : product.badge === 'NOUVEAU' ? 'primary' : 'accent'} className={styles.badge}>{product.badge}</Badge>}
        <span className={styles.price}>{product.price}€/jour</span>
      </div>
      <div className={styles.body}>
        <h3 className={styles.name}>{product.name}</h3>
        <StarRating value={product.rating} count={product.reviewCount} />
      </div>
    </Link>
  );
}
```

```css
.card {
  display: block;
  background: var(--color-bg-alt);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
.imgWrap { position: relative; aspect-ratio: 4 / 3; background: #eee; }
.imgWrap img { width: 100%; height: 100%; object-fit: cover; }
.cat { position: absolute; top: var(--space-sm); left: var(--space-sm); background: rgba(255,255,255,0.95); width: 36px; height: 36px; border-radius: 50%; display: grid; place-items: center; font-size: 1.2rem; }
.badge { position: absolute; top: var(--space-sm); right: var(--space-sm); }
.price { position: absolute; bottom: var(--space-sm); right: var(--space-sm); background: var(--color-ink); color: var(--color-bg); padding: 0.3rem 0.7rem; border-radius: var(--radius-pill); font-weight: 800; font-size: 0.85rem; }
.body { padding: var(--space-md); }
.name { font-family: var(--font-display); font-size: 1.2rem; margin-bottom: var(--space-2xs); }
```

- [ ] **Step 2: HomePage**

`HomePage.tsx` :

```tsx
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Section } from '../components/ui/Section';
import { ProductCard } from '../components/product/ProductCard';
import productsRaw from '../data/products.json';
import { CATEGORIES } from '../data/categories';
import type { Product } from '../data/types';
import styles from './HomePage.module.css';

const products = productsRaw as Product[];
const featured = products.slice(0, 6);

const STEPS = [
  { n: '01', title: 'Choisissez', text: 'Naviguez par catégorie ou utilisez les filtres. Besoin d\'un conseil ? Contactez-nous.' },
  { n: '02', title: 'Livraison ou retrait', text: 'Livraison sur site en Alsace ou retrait dans notre dépôt à Strasbourg.' },
  { n: '03', title: 'On installe', text: 'Notre équipe monte et sécurise le matériel sur place. Démonstration incluse.' },
  { n: '04', title: 'Vous kiffez', text: 'Profitez de votre fête sans stress. À l\'heure convenue, on revient tout démonter.' },
];

const TRUST = [
  { kicker: 'Pro', label: 'Équipe certifiée' },
  { kicker: '100%', label: 'Alsacien' },
  { kicker: 'Homologué CE', label: 'Norme EN 14960' },
  { kicker: 'RC Pro', label: 'Assurance incluse' },
];

export function HomePage() {
  return (
    <>
      <section className={styles.hero}>
        <div className={`container ${styles.heroInner}`}>
          <div>
            <Badge tone="danger" rotation={-3}>LES KINGS DU GONFLABLE 👑</Badge>
            <h1 className={styles.title}>
              Ta fête va<br/>
              <span className={styles.titleAccent}>décoller.</span>
            </h1>
            <p className={styles.lead}>
              Châteaux gonflables, photobooths, sono et bien plus —<br/>
              on s'occupe de tout, vous kiffez.
            </p>
            <div className={styles.ctas}>
              <Button to="/catalogue" variant="primary" size="lg">Voir le catalogue →</Button>
              <Button to="/entreprise" variant="secondary" size="lg">Offres entreprise</Button>
            </div>
          </div>
          <ul className={styles.trust}>
            {TRUST.map((t) => (
              <li key={t.kicker}><strong>{t.kicker}</strong><span>{t.label}</span></li>
            ))}
          </ul>
        </div>
      </section>

      <Section eyebrow="Simple & rapide" title="Comment ça marche ?">
        <div className={styles.steps}>
          {STEPS.map((s) => (
            <article key={s.n} className={styles.step}>
              <span className={styles.stepNum}>{s.n}</span>
              <h3>{s.title}</h3>
              <p>{s.text}</p>
            </article>
          ))}
        </div>
      </Section>

      <Section eyebrow="Nos catégories" title="Tout ce qu'il faut pour la fête">
        <div className={styles.categories}>
          {CATEGORIES.map((c) => (
            <Link key={c.id} to={`/catalogue?cat=${c.id}`} className={styles.cat}>
              <span className={styles.catEmoji}>{c.emoji}</span>
              <span className={styles.catLabel}>{c.label}</span>
              <span className={styles.catLink}>Voir →</span>
            </Link>
          ))}
        </div>
      </Section>

      <Section eyebrow="Produits stars" title="On dirait qu'ils kiffent.">
        <div className={styles.productGrid}>
          {featured.map((p) => <ProductCard key={p.id} product={p} />)}
        </div>
        <div className={styles.center}>
          <Button to="/catalogue" variant="primary" size="md">Voir tout le catalogue →</Button>
        </div>
      </Section>

      <Section background="dark" eyebrow="Pourquoi nous" title="L'événementiel alsacien, avec le cœur.">
        <p className={styles.darkLead}>Fiestalo'K est née d'une passion simple : rendre chaque fête mémorable. Basée à Strasbourg, on intervient dans tout le Bas-Rhin et le Haut-Rhin.</p>
        <div className={styles.values}>
          {[
            { icon: '🛡️', title: 'Matériel homologué CE', text: 'Norme EN 14960 sur tous nos gonflables.' },
            { icon: '📋', title: 'Assurance RC Pro', text: 'Votre événement est couvert.' },
            { icon: '🎪', title: 'Équipe pro', text: 'On monte, on sécurise, avec le sourire.' },
            { icon: '📍', title: 'Ancrage local', text: 'Livraison Bas-Rhin & Haut-Rhin sans surcoût.' },
          ].map((v) => (
            <article key={v.title} className={styles.value}>
              <span className={styles.valueIcon}>{v.icon}</span>
              <h3>{v.title}</h3>
              <p>{v.text}</p>
            </article>
          ))}
        </div>
      </Section>
    </>
  );
}
```

- [ ] **Step 3: HomePage.module.css**

```css
.hero {
  background: var(--color-bg);
  padding: var(--space-3xl) 0;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background-image:
    radial-gradient(circle at 12% 18%, var(--color-accent) 0 8px, transparent 9px),
    radial-gradient(circle at 85% 24%, var(--color-primary) 0 6px, transparent 7px),
    radial-gradient(circle at 24% 78%, var(--color-danger) 0 5px, transparent 6px),
    radial-gradient(circle at 72% 82%, var(--color-success) 0 7px, transparent 8px);
  opacity: 0.35;
  pointer-events: none;
}
.heroInner { position: relative; display: grid; grid-template-columns: 1.4fr 1fr; gap: var(--space-2xl); align-items: center; }
.title { font-size: clamp(3rem, 6vw + 1rem, 5.5rem); margin: var(--space-md) 0 var(--space-md); }
.titleAccent { color: var(--color-danger); display: inline-block; transform: rotate(-2deg); }
.lead { font-size: 1.2rem; color: var(--color-ink-soft); margin-bottom: var(--space-lg); }
.ctas { display: flex; gap: var(--space-sm); flex-wrap: wrap; }
.trust { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-md); background: var(--color-bg-alt); border: 2px solid var(--color-ink); border-radius: var(--radius-lg); padding: var(--space-lg); box-shadow: var(--shadow-sticker); }
.trust li strong { display: block; font-family: var(--font-display); font-size: 1.4rem; color: var(--color-danger); letter-spacing: 0.04em; }
.trust li span { color: var(--color-ink-soft); font-size: 0.9rem; }

.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-lg); }
.step { background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-lg); box-shadow: var(--shadow-sm); }
.stepNum { font-family: var(--font-display); font-size: 2.4rem; color: var(--color-danger); display: block; }
.step h3 { margin: var(--space-xs) 0; }
.step p { color: var(--color-ink-soft); font-size: 0.95rem; }

.categories { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-md); }
.cat { display: flex; flex-direction: column; align-items: center; gap: var(--space-xs); padding: var(--space-lg); background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-lg); transition: transform 0.2s; }
.cat:hover { transform: translateY(-4px); border-color: var(--color-primary); }
.catEmoji { font-size: 2.4rem; }
.catLabel { font-family: var(--font-display); font-size: 1.1rem; }
.catLink { color: var(--color-danger); font-weight: 800; font-size: 0.85rem; }

.productGrid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-lg); }
.center { text-align: center; margin-top: var(--space-xl); }

.darkLead { text-align: center; max-width: 640px; margin: 0 auto var(--space-2xl); color: rgba(255,255,255,0.8); font-size: 1.05rem; }
.values { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-lg); }
.value { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-radius: var(--radius-lg); padding: var(--space-lg); }
.valueIcon { font-size: 2rem; }
.value h3 { color: var(--color-bg); margin: var(--space-xs) 0; }
.value p { color: rgba(255,255,255,0.7); font-size: 0.9rem; }

@media (max-width: 900px) {
  .heroInner { grid-template-columns: 1fr; }
  .steps, .categories, .values, .productGrid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 560px) {
  .steps, .categories, .values, .productGrid { grid-template-columns: 1fr; }
  .trust { grid-template-columns: 1fr; }
}
```

- [ ] **Step 4: Vérifier visuellement**

`npm run dev`, ouvrir `/`. Hero, steps, catégories, produits stars, bloc valeurs sombre — tout doit être visible et stylé.

- [ ] **Step 5: Commit**

```bash
git add site/src/components/product/ProductCard.tsx site/src/components/product/ProductCard.module.css site/src/pages/HomePage.tsx site/src/pages/HomePage.module.css
git commit -m "feat(site-v2): build HomePage with hero, steps, categories, featured products and values"
```

---

## Task 8 — CataloguePage avec filtres et tests

**Files:**
- Create: `site/src/components/catalogue/CategoryTabs.tsx` + `.module.css`
- Create: `site/src/components/catalogue/CatalogueFilters.tsx` + `.module.css`
- Create: `site/src/tests/CatalogueFilters.test.tsx`
- Modify: `site/src/pages/CataloguePage.tsx` + `CataloguePage.module.css`

- [ ] **Step 1: Test pour la fonction de filtre pure**

Créer `site/src/lib/filterProducts.ts` :

```ts
import type { Product } from '../data/types';
import type { Audience, CategoryId } from '../data/categories';

export interface FilterState {
  category: CategoryId | 'all';
  audiences: Audience[];
  maxPrice: number;
  sort: 'default' | 'price-asc' | 'price-desc' | 'rating';
}

export const DEFAULT_FILTERS: FilterState = {
  category: 'all',
  audiences: [],
  maxPrice: 400,
  sort: 'default',
};

export function filterProducts(products: Product[], f: FilterState): Product[] {
  let out = products.filter((p) => {
    if (f.category !== 'all' && p.category !== f.category) return false;
    if (f.audiences.length > 0 && !f.audiences.some((a) => p.audiences.includes(a))) return false;
    if (p.price > f.maxPrice) return false;
    return true;
  });
  switch (f.sort) {
    case 'price-asc':  out = [...out].sort((a, b) => a.price - b.price); break;
    case 'price-desc': out = [...out].sort((a, b) => b.price - a.price); break;
    case 'rating':     out = [...out].sort((a, b) => b.rating - a.rating); break;
  }
  return out;
}
```

`site/src/tests/CatalogueFilters.test.tsx` :

```tsx
import { describe, it, expect } from 'vitest';
import { filterProducts, DEFAULT_FILTERS } from '../lib/filterProducts';
import type { Product } from '../data/types';

const SAMPLE: Product[] = [
  { id: '1', name: 'Château', category: 'chateau-gonflable', audiences: ['enfants'], shortDescription: '', longDescription: '', price: 120, rating: 4.5, reviewCount: 2, specs: {}, images: [], badge: null },
  { id: '2', name: 'Sono',    category: 'enceintes',         audiences: ['adultes', 'entreprises'], shortDescription: '', longDescription: '', price: 60,  rating: 4.8, reviewCount: 5, specs: {}, images: [], badge: null },
  { id: '3', name: 'BBQ',     category: 'restauration',      audiences: ['adultes'], shortDescription: '', longDescription: '', price: 90, rating: 4.2, reviewCount: 1, specs: {}, images: [], badge: null },
];

describe('filterProducts', () => {
  it('returns everything by default', () => {
    expect(filterProducts(SAMPLE, DEFAULT_FILTERS)).toHaveLength(3);
  });
  it('filters by category', () => {
    expect(filterProducts(SAMPLE, { ...DEFAULT_FILTERS, category: 'enceintes' })).toEqual([SAMPLE[1]]);
  });
  it('filters by audience (OR)', () => {
    const out = filterProducts(SAMPLE, { ...DEFAULT_FILTERS, audiences: ['enfants'] });
    expect(out).toEqual([SAMPLE[0]]);
  });
  it('filters by max price', () => {
    const out = filterProducts(SAMPLE, { ...DEFAULT_FILTERS, maxPrice: 80 });
    expect(out).toEqual([SAMPLE[1]]);
  });
  it('sorts by price asc', () => {
    const out = filterProducts(SAMPLE, { ...DEFAULT_FILTERS, sort: 'price-asc' });
    expect(out.map((p) => p.id)).toEqual(['2', '3', '1']);
  });
  it('sorts by rating desc', () => {
    const out = filterProducts(SAMPLE, { ...DEFAULT_FILTERS, sort: 'rating' });
    expect(out.map((p) => p.id)).toEqual(['2', '1', '3']);
  });
});
```

- [ ] **Step 2: Run tests, expect all to pass**

```bash
cd site && npx vitest run src/tests/CatalogueFilters.test.tsx
```

Expected : 6 passed.

- [ ] **Step 3: CategoryTabs**

`CategoryTabs.tsx` :

```tsx
import { CATEGORIES, type CategoryId } from '../../data/categories';
import styles from './CategoryTabs.module.css';

interface Props {
  active: CategoryId | 'all';
  onChange: (id: CategoryId | 'all') => void;
}

export function CategoryTabs({ active, onChange }: Props) {
  return (
    <div className={styles.tabs}>
      <button className={`${styles.tab} ${active === 'all' ? styles.active : ''}`} onClick={() => onChange('all')}>Tout voir</button>
      {CATEGORIES.map((c) => (
        <button
          key={c.id}
          className={`${styles.tab} ${active === c.id ? styles.active : ''}`}
          onClick={() => onChange(c.id)}
        >
          {c.emoji} {c.label}
        </button>
      ))}
    </div>
  );
}
```

`CategoryTabs.module.css` :

```css
.tabs { display: flex; flex-wrap: wrap; gap: var(--space-sm); justify-content: center; }
.tab {
  padding: 0.6rem 1.2rem;
  border: 2px solid var(--color-ink);
  border-radius: var(--radius-pill);
  background: var(--color-bg-alt);
  font-weight: 800;
  font-size: 0.9rem;
}
.tab:hover { background: var(--color-accent); }
.active { background: var(--color-ink); color: var(--color-bg); }
.active:hover { background: var(--color-ink); }
```

- [ ] **Step 4: CatalogueFilters (sidebar)**

`CatalogueFilters.tsx` :

```tsx
import type { FilterState } from '../../lib/filterProducts';
import { AUDIENCES, type Audience } from '../../data/categories';
import styles from './CatalogueFilters.module.css';

interface Props {
  value: FilterState;
  onChange: (f: FilterState) => void;
}

const AUDIENCE_LABELS: Record<Audience, string> = {
  enfants: '🧒 Enfants',
  adultes: '🎉 Adultes',
  entreprises: '💼 Entreprises',
};

export function CatalogueFilters({ value, onChange }: Props) {
  const toggleAudience = (a: Audience) => {
    const has = value.audiences.includes(a);
    onChange({ ...value, audiences: has ? value.audiences.filter((x) => x !== a) : [...value.audiences, a] });
  };
  return (
    <aside className={styles.sidebar}>
      <h3 className={styles.title}>Filtres</h3>

      <div className={styles.group}>
        <h4>Pour qui ?</h4>
        <div className={styles.chips}>
          {AUDIENCES.map((a) => (
            <button
              key={a}
              type="button"
              className={`${styles.chip} ${value.audiences.includes(a) ? styles.chipActive : ''}`}
              onClick={() => toggleAudience(a)}
            >
              {AUDIENCE_LABELS[a]}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.group}>
        <h4>Prix max : {value.maxPrice}€</h4>
        <input
          type="range"
          min={30}
          max={400}
          step={10}
          value={value.maxPrice}
          onChange={(e) => onChange({ ...value, maxPrice: Number(e.target.value) })}
        />
      </div>
    </aside>
  );
}
```

`CatalogueFilters.module.css` :

```css
.sidebar { background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-lg); position: sticky; top: calc(var(--navbar-height) + var(--space-md)); }
.title { font-family: var(--font-display); font-size: 1.2rem; color: var(--color-danger); letter-spacing: 0.1em; margin-bottom: var(--space-md); }
.group { margin-bottom: var(--space-lg); }
.group h4 { font-family: var(--font-body); font-weight: 800; font-size: 0.85rem; margin-bottom: var(--space-sm); text-transform: uppercase; letter-spacing: 0.05em; }
.chips { display: flex; flex-wrap: wrap; gap: var(--space-xs); }
.chip { padding: 0.4rem 0.8rem; border-radius: var(--radius-pill); border: 1.5px solid var(--color-border); background: var(--color-bg); font-size: 0.85rem; font-weight: 700; }
.chipActive { background: var(--color-accent); border-color: var(--color-ink); }
.group input[type=range] { width: 100%; accent-color: var(--color-danger); }
```

- [ ] **Step 5: CataloguePage**

```tsx
import { useMemo, useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import productsRaw from '../data/products.json';
import type { Product } from '../data/types';
import type { CategoryId } from '../data/categories';
import { filterProducts, DEFAULT_FILTERS, type FilterState } from '../lib/filterProducts';
import { ProductCard } from '../components/product/ProductCard';
import { CategoryTabs } from '../components/catalogue/CategoryTabs';
import { CatalogueFilters } from '../components/catalogue/CatalogueFilters';
import styles from './CataloguePage.module.css';

const products = productsRaw as Product[];

export function CataloguePage() {
  const [params, setParams] = useSearchParams();
  const initial: FilterState = {
    ...DEFAULT_FILTERS,
    category: (params.get('cat') as CategoryId) || 'all',
  };
  const [filters, setFilters] = useState<FilterState>(initial);

  // Sync category to URL
  useEffect(() => {
    if (filters.category === 'all') params.delete('cat');
    else params.set('cat', filters.category);
    setParams(params, { replace: true });
  }, [filters.category]);

  const filtered = useMemo(() => filterProducts(products, filters), [filters]);

  return (
    <>
      <section className={styles.heroBand}>
        <div className="container">
          <p className={styles.eyebrow}>Fiestalo'K</p>
          <h1 className={styles.title}>Notre <span>catalogue</span></h1>
          <p className={styles.lead}>Tout le matériel pour une fête réussie.</p>
        </div>
      </section>

      <div className={`container ${styles.tabsBar}`}>
        <CategoryTabs active={filters.category} onChange={(c) => setFilters((f) => ({ ...f, category: c }))} />
      </div>

      <div className={`container ${styles.layout}`}>
        <CatalogueFilters value={filters} onChange={setFilters} />

        <div className={styles.results}>
          <div className={styles.resultsHeader}>
            <p>{filtered.length} résultat{filtered.length > 1 ? 's' : ''}</p>
            <select
              value={filters.sort}
              onChange={(e) => setFilters((f) => ({ ...f, sort: e.target.value as FilterState['sort'] }))}
              className={styles.sort}
            >
              <option value="default">Tri par défaut</option>
              <option value="price-asc">Prix croissant</option>
              <option value="price-desc">Prix décroissant</option>
              <option value="rating">Mieux notés</option>
            </select>
          </div>

          {filtered.length === 0 ? (
            <div className={styles.empty}>
              <p>Aucun produit ne correspond à tes filtres.</p>
              <button onClick={() => setFilters(DEFAULT_FILTERS)}>Réinitialiser</button>
            </div>
          ) : (
            <div className={styles.grid}>
              {filtered.map((p) => <ProductCard key={p.id} product={p} />)}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
```

`CataloguePage.module.css` :

```css
.heroBand { background: var(--color-ink); color: var(--color-bg); padding: var(--space-2xl) 0; text-align: center; }
.eyebrow { color: var(--color-danger); font-family: var(--font-display); letter-spacing: 0.15em; font-size: 0.9rem; }
.title { color: var(--color-bg); margin: var(--space-xs) 0; }
.title span { color: var(--color-danger); }
.lead { color: rgba(255,255,255,0.75); }

.tabsBar { padding: var(--space-xl) 0; }

.layout { display: grid; grid-template-columns: 260px 1fr; gap: var(--space-xl); padding-bottom: var(--space-3xl); }
.resultsHeader { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-md); }
.sort { padding: 0.5rem 0.8rem; border-radius: var(--radius-pill); border: 1.5px solid var(--color-border); background: var(--color-bg-alt); font-weight: 700; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-lg); }
.empty { padding: var(--space-2xl); text-align: center; background: var(--color-bg-alt); border-radius: var(--radius-lg); border: 1px dashed var(--color-border); }
.empty button { margin-top: var(--space-sm); padding: 0.5rem 1rem; background: var(--color-ink); color: var(--color-bg); border-radius: var(--radius-pill); font-weight: 800; }

@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  .grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 560px) {
  .grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 6: Run all tests + visual check**

```bash
cd site && npx vitest run && npm run dev
```

Naviguer sur `/catalogue`, tester les filtres et les onglets de catégorie.

- [ ] **Step 7: Commit**

```bash
git add site/src/lib/filterProducts.ts site/src/components/catalogue/ site/src/pages/CataloguePage.tsx site/src/pages/CataloguePage.module.css site/src/tests/CatalogueFilters.test.tsx
git commit -m "feat(site-v2): build catalogue page with filters, tabs, sort and tests"
```

---

## Task 9 — ProductPage : galerie, infos, calendrier, avis

**Files:**
- Create: `site/src/components/product/ProductGallery.tsx` + `.module.css`
- Create: `site/src/components/product/AvailabilityCalendar.tsx` + `.module.css`
- Create: `site/src/components/product/ReviewList.tsx` + `.module.css`
- Create: `site/src/components/product/ReviewForm.tsx` + `.module.css`
- Create: `site/src/tests/AvailabilityCalendar.test.tsx`
- Modify: `site/src/pages/ProductPage.tsx` + `ProductPage.module.css`

- [ ] **Step 1: ProductGallery (image principale + thumbs)**

```tsx
import { useState } from 'react';
import styles from './ProductGallery.module.css';

interface Props { images: string[]; alt: string; }

export function ProductGallery({ images, alt }: Props) {
  const [current, setCurrent] = useState(0);
  return (
    <div className={styles.wrap}>
      <div className={styles.main}>
        <img src={images[current]} alt={alt} />
      </div>
      {images.length > 1 && (
        <div className={styles.thumbs}>
          {images.map((src, i) => (
            <button
              key={src}
              className={`${styles.thumb} ${i === current ? styles.active : ''}`}
              onClick={() => setCurrent(i)}
              aria-label={`Image ${i + 1}`}
            >
              <img src={src} alt="" />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
```

```css
.wrap { display: flex; flex-direction: column; gap: var(--space-sm); }
.main { aspect-ratio: 4/3; border-radius: var(--radius-lg); overflow: hidden; background: #eee; box-shadow: var(--shadow-md); }
.main img { width: 100%; height: 100%; object-fit: cover; }
.thumbs { display: flex; gap: var(--space-sm); }
.thumb { width: 80px; height: 80px; border-radius: var(--radius-md); overflow: hidden; border: 2px solid transparent; }
.thumb img { width: 100%; height: 100%; object-fit: cover; }
.active { border-color: var(--color-danger); }
```

- [ ] **Step 2: AvailabilityCalendar — test d'abord**

`site/src/tests/AvailabilityCalendar.test.tsx` :

```tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AvailabilityCalendar } from '../components/product/AvailabilityCalendar';

describe('AvailabilityCalendar', () => {
  it('renders the current month name', () => {
    render(<AvailabilityCalendar productId="1" unavailableDates={[]} value={null} onChange={() => {}} />);
    const monthFr = new Intl.DateTimeFormat('fr-FR', { month: 'long', year: 'numeric' }).format(new Date());
    expect(screen.getByText(new RegExp(monthFr, 'i'))).toBeInTheDocument();
  });

  it('lets the user navigate to next month', async () => {
    render(<AvailabilityCalendar productId="1" unavailableDates={[]} value={null} onChange={() => {}} />);
    const before = screen.getByTestId('current-month').textContent;
    await userEvent.click(screen.getByLabelText('Mois suivant'));
    const after = screen.getByTestId('current-month').textContent;
    expect(after).not.toBe(before);
  });
});
```

- [ ] **Step 3: Implémenter AvailabilityCalendar**

```tsx
import { useMemo, useState } from 'react';
import {
  startOfMonth, endOfMonth, eachDayOfInterval, format,
  addMonths, isSameMonth, isSameDay, isBefore, startOfDay,
} from 'date-fns';
import { fr } from 'date-fns/locale';
import styles from './AvailabilityCalendar.module.css';

interface Props {
  productId: string;
  unavailableDates: string[];
  value: Date | null;
  onChange: (date: Date) => void;
}

export function AvailabilityCalendar({ unavailableDates, value, onChange }: Props) {
  const [view, setView] = useState(() => startOfMonth(new Date()));
  const today = startOfDay(new Date());

  const days = useMemo(() => {
    const start = startOfMonth(view);
    const end = endOfMonth(view);
    return eachDayOfInterval({ start, end });
  }, [view]);

  const isUnavailable = (d: Date) => unavailableDates.includes(format(d, 'yyyy-MM-dd'));
  const startWeekday = (days[0].getDay() + 6) % 7; // Monday = 0

  return (
    <div className={styles.cal}>
      <header className={styles.header}>
        <button onClick={() => setView(addMonths(view, -1))} aria-label="Mois précédent">‹</button>
        <span data-testid="current-month">{format(view, 'MMMM yyyy', { locale: fr })}</span>
        <button onClick={() => setView(addMonths(view, 1))} aria-label="Mois suivant">›</button>
      </header>
      <div className={styles.weekdays}>
        {['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'].map((d) => <span key={d}>{d}</span>)}
      </div>
      <div className={styles.grid}>
        {Array.from({ length: startWeekday }).map((_, i) => <span key={`b${i}`} />)}
        {days.map((d) => {
          const past = isBefore(d, today) && !isSameDay(d, today);
          const unavail = isUnavailable(d);
          const selected = value && isSameDay(d, value);
          return (
            <button
              key={d.toISOString()}
              disabled={past || unavail || !isSameMonth(d, view)}
              className={`${styles.day} ${unavail ? styles.unavail : ''} ${selected ? styles.selected : ''}`}
              onClick={() => onChange(d)}
            >
              {d.getDate()}
            </button>
          );
        })}
      </div>
      <div className={styles.legend}>
        <span><span className={`${styles.dot} ${styles.unavailDot}`} /> Indisponible</span>
        <span><span className={`${styles.dot} ${styles.selectedDot}`} /> Sélectionné</span>
      </div>
    </div>
  );
}
```

```css
.cal { background: var(--color-bg-alt); border-radius: var(--radius-lg); border: 1px solid var(--color-border); overflow: hidden; }
.header { display: flex; justify-content: space-between; align-items: center; background: var(--color-ink); color: var(--color-bg); padding: var(--space-sm) var(--space-md); font-family: var(--font-display); font-size: 1.1rem; text-transform: capitalize; }
.header button { color: var(--color-bg); font-size: 1.4rem; padding: 0 var(--space-sm); }
.weekdays, .grid { display: grid; grid-template-columns: repeat(7, 1fr); }
.weekdays { padding: var(--space-sm); color: var(--color-danger); font-weight: 800; font-size: 0.8rem; text-align: center; text-transform: uppercase; }
.grid { gap: 4px; padding: var(--space-sm); }
.day { aspect-ratio: 1; display: grid; place-items: center; border-radius: var(--radius-sm); background: var(--color-bg); font-weight: 700; font-size: 0.9rem; }
.day:disabled { opacity: 0.35; cursor: not-allowed; }
.day:not(:disabled):hover { background: var(--color-accent); }
.unavail { background: rgba(255,107,107,0.18); color: var(--color-danger); }
.selected { background: var(--color-ink); color: var(--color-bg); }
.legend { display: flex; gap: var(--space-md); padding: var(--space-sm) var(--space-md); font-size: 0.8rem; color: var(--color-ink-soft); border-top: 1px solid var(--color-border); }
.dot { display: inline-block; width: 10px; height: 10px; border-radius: 2px; vertical-align: middle; margin-right: 4px; }
.unavailDot { background: rgba(255,107,107,0.4); }
.selectedDot { background: var(--color-ink); }
```

- [ ] **Step 4: Run AvailabilityCalendar tests**

```bash
cd site && npx vitest run src/tests/AvailabilityCalendar.test.tsx
```

Expected : 2 passed.

- [ ] **Step 5: ReviewList**

```tsx
import type { Review } from '../../data/types';
import { StarRating } from '../ui/StarRating';
import styles from './ReviewList.module.css';

export function ReviewList({ reviews }: { reviews: Review[] }) {
  if (reviews.length === 0) {
    return <p className={styles.empty}>Pas encore d'avis. Sois le premier à kiffer !</p>;
  }
  return (
    <ul className={styles.list}>
      {reviews.map((r) => (
        <li key={r.id} className={styles.item}>
          <div className={styles.head}>
            <span className={styles.avatar}>{r.author.charAt(0).toUpperCase()}</span>
            <strong>{r.author}</strong>
            <StarRating value={r.rating} />
            <time>{r.date}</time>
          </div>
          <p className={styles.body}>{r.comment}</p>
        </li>
      ))}
    </ul>
  );
}
```

```css
.list { display: flex; flex-direction: column; gap: var(--space-md); }
.item { padding: var(--space-md); border: 1px solid var(--color-border); border-radius: var(--radius-md); }
.head { display: flex; align-items: center; gap: var(--space-sm); flex-wrap: wrap; }
.avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--color-danger); color: white; display: grid; place-items: center; font-weight: 800; }
.head time { color: var(--color-ink-soft); font-size: 0.85rem; margin-left: auto; }
.body { margin-top: var(--space-xs); color: var(--color-ink-soft); }
.empty { padding: var(--space-lg); text-align: center; color: var(--color-ink-soft); }
```

- [ ] **Step 6: ReviewForm**

```tsx
import { useState, type FormEvent } from 'react';
import { Button } from '../ui/Button';
import styles from './ReviewForm.module.css';

interface Props {
  onSubmit: (data: { author: string; rating: number; comment: string }) => void;
}

export function ReviewForm({ onSubmit }: Props) {
  const [author, setAuthor] = useState('');
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!author.trim() || !comment.trim()) return;
    onSubmit({ author: author.trim(), rating, comment: comment.trim() });
    setAuthor(''); setComment(''); setRating(5);
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <h4>Laisser un avis</h4>
      <div className={styles.stars}>
        {[1, 2, 3, 4, 5].map((n) => (
          <button type="button" key={n} onClick={() => setRating(n)} aria-label={`${n} étoile${n > 1 ? 's' : ''}`}>
            {n <= rating ? '★' : '☆'}
          </button>
        ))}
      </div>
      <input
        type="text"
        placeholder="Ton prénom"
        value={author}
        onChange={(e) => setAuthor(e.target.value)}
        required
      />
      <textarea
        placeholder="Ton commentaire..."
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        rows={3}
        required
      />
      <Button type="submit" variant="danger" size="md">Publier l'avis</Button>
    </form>
  );
}
```

```css
.form { display: flex; flex-direction: column; gap: var(--space-sm); padding: var(--space-md); border: 1px solid var(--color-border); border-radius: var(--radius-md); }
.form h4 { font-family: var(--font-body); font-weight: 800; }
.stars { display: flex; gap: 4px; font-size: 1.6rem; color: var(--color-danger); }
.stars button { padding: 0 2px; }
.form input, .form textarea {
  padding: 0.7rem 1rem;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg);
  font-family: var(--font-body);
}
.form input:focus, .form textarea:focus { outline: none; border-color: var(--color-primary); }
```

- [ ] **Step 7: ProductPage**

```tsx
import { useState } from 'react';
import { useParams, Link, Navigate } from 'react-router-dom';
import productsRaw from '../data/products.json';
import type { Product } from '../data/types';
import { CATEGORIES } from '../data/categories';
import { UNAVAILABLE_DATES } from '../data/unavailable';
import { useCart } from '../context/CartContext';
import { useReviews } from '../context/ReviewsContext';
import { ProductGallery } from '../components/product/ProductGallery';
import { AvailabilityCalendar } from '../components/product/AvailabilityCalendar';
import { ReviewList } from '../components/product/ReviewList';
import { ReviewForm } from '../components/product/ReviewForm';
import { StarRating } from '../components/ui/StarRating';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { format } from 'date-fns';
import styles from './ProductPage.module.css';

const products = productsRaw as Product[];

export function ProductPage() {
  const { id } = useParams<{ id: string }>();
  const product = products.find((p) => p.id === id);
  const cat = product && CATEGORIES.find((c) => c.id === product.category);
  const { add, open } = useCart();
  const { forProduct, add: addReview } = useReviews();
  const [date, setDate] = useState<Date | null>(null);

  if (!product) return <Navigate to="/catalogue" replace />;

  const reviews = forProduct(product.id);

  function handleAdd() {
    add({
      productId: product.id,
      startDate: date ? format(date, 'yyyy-MM-dd') : null,
      endDate: date ? format(date, 'yyyy-MM-dd') : null,
      quantity: 1,
    });
    open();
  }

  return (
    <div className={`container ${styles.page}`}>
      <nav className={styles.crumbs}>
        <Link to="/catalogue">Catalogue</Link> / <span>{product.name}</span>
      </nav>

      <div className={styles.top}>
        <ProductGallery images={product.images} alt={product.name} />

        <div className={styles.info}>
          {cat && <p className={styles.cat}>{cat.emoji} {cat.label}</p>}
          {product.badge && <Badge tone={product.badge === 'PROMO' ? 'danger' : 'accent'}>{product.badge}</Badge>}
          <h1 className={styles.name}>{product.name}</h1>
          <StarRating value={product.rating} count={product.reviewCount + reviews.length} size="md" />
          <p className={styles.desc}>{product.longDescription}</p>

          <ul className={styles.specs}>
            {Object.entries(product.specs).map(([k, v]) => (
              <li key={k}><span>{k}</span><strong>{v}</strong></li>
            ))}
          </ul>

          <div className={styles.priceRow}>
            <span className={styles.price}>{product.price}€</span>
            <span className={styles.unit}>/jour</span>
          </div>

          <Button variant="primary" size="lg" onClick={handleAdd}>+ Ajouter au panier</Button>
        </div>
      </div>

      <section className={styles.block}>
        <header><h2>Disponibilités</h2><p>Choisis ta date pour vérifier la dispo.</p></header>
        <AvailabilityCalendar
          productId={product.id}
          unavailableDates={UNAVAILABLE_DATES[product.id] ?? []}
          value={date}
          onChange={setDate}
        />
        {date && <p className={styles.selected}>Date sélectionnée : <strong>{format(date, 'dd/MM/yyyy')}</strong></p>}
      </section>

      <section className={styles.block}>
        <header><h2>Avis clients</h2></header>
        <ReviewList reviews={reviews} />
        <ReviewForm onSubmit={(data) => addReview({ productId: product.id, ...data })} />
      </section>

      <Link to="/catalogue" className={styles.back}>← Retour au catalogue</Link>
    </div>
  );
}
```

`ProductPage.module.css` :

```css
.page { padding: var(--space-xl) 0 var(--space-3xl); }
.crumbs { color: var(--color-ink-soft); margin-bottom: var(--space-lg); font-size: 0.9rem; }
.crumbs a:hover { color: var(--color-primary); }

.top { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-2xl); }
.info { display: flex; flex-direction: column; gap: var(--space-sm); align-items: flex-start; }
.cat { color: var(--color-danger); font-weight: 800; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.05em; }
.name { font-size: clamp(2rem, 3vw + 1rem, 3rem); }
.desc { color: var(--color-ink-soft); line-height: 1.6; }

.specs { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-sm); width: 100%; padding: var(--space-md); background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-md); }
.specs li { display: flex; flex-direction: column; }
.specs span { color: var(--color-ink-soft); font-size: 0.8rem; text-transform: uppercase; }
.specs strong { font-weight: 800; }

.priceRow { display: flex; align-items: baseline; gap: var(--space-xs); }
.price { font-family: var(--font-display); font-size: 3rem; color: var(--color-danger); }
.unit { color: var(--color-ink-soft); }

.block { margin-top: var(--space-3xl); }
.block header { margin-bottom: var(--space-md); }
.block h2 { margin-bottom: var(--space-2xs); }
.block header p { color: var(--color-ink-soft); }
.selected { margin-top: var(--space-sm); padding: var(--space-sm); background: var(--color-accent); border-radius: var(--radius-md); display: inline-block; }
.back { display: inline-block; margin-top: var(--space-2xl); color: var(--color-primary); font-weight: 700; }

@media (max-width: 900px) {
  .top { grid-template-columns: 1fr; }
}
```

- [ ] **Step 8: Run all tests + visual check**

```bash
cd site && npx vitest run && npm run dev
```

Naviguer sur `/produit/1` ; vérifier galerie, ajout au panier (le drawer doit s'ouvrir), calendrier (jours indisponibles barrés), avis (en publier un et vérifier qu'il s'affiche après reload).

- [ ] **Step 9: Commit**

```bash
git add site/src/components/product/ site/src/pages/ProductPage.tsx site/src/pages/ProductPage.module.css site/src/tests/AvailabilityCalendar.test.tsx
git commit -m "feat(site-v2): build product page with gallery, calendar, reviews and cart integration"
```

---

## Task 10 — EntreprisePage

**Files:**
- Modify: `site/src/pages/EntreprisePage.tsx` + `EntreprisePage.module.css`

- [ ] **Step 1: Implémenter EntreprisePage**

```tsx
import { Section } from '../components/ui/Section';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import styles from './EntreprisePage.module.css';

const REFS = ['Crédit Mutuel', 'Eurocorps', 'Groupe Eilor', 'EDF Alsace', 'Hôtel Régent'];

const FORMULES = [
  {
    icon: '🏆',
    title: 'Team Building',
    text: 'On vous fournit tout : matériel pour animer votre journée cohésion : parcours gonflables, jeux collectifs, sono pour mettre l\'ambiance.',
    items: ['Parcours & châteaux gonflables', 'Jeux collectifs', 'Matériel sono & enceintes'],
  },
  {
    icon: '🥂',
    title: 'Séminaire & Soirée',
    text: 'On équipe votre événement avec sono pro et photobooth. Vous gérez la com, on s\'occupe du matos.',
    items: ['Sono & enceintes pro', 'Photobooth & miroir 360°', 'Boule à facette & éclairage'],
  },
  {
    icon: '🎪',
    title: 'Kermesse & Famille',
    text: 'On fournit tout le matériel pour régaler petits et grands : châteaux, machines pop-corn & barbe à papa.',
    items: ['Châteaux gonflables', 'Machine pop-corn & barbe à papa', 'Plancha tarte flambée & BBQ'],
  },
];

const EVENTS = [
  'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=600',
  'https://images.unsplash.com/photo-1530023367847-a683933f4172?w=600',
  'https://images.unsplash.com/photo-1543007631-283050bb3e8c?w=600',
  'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=600',
  'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600',
  'https://images.unsplash.com/photo-1517502884422-41eaead166d4?w=600',
];

const COMPLIANCE = [
  { icon: '🛡️', title: 'Norme EN 14960', text: 'Tous nos équipements gonflables sont certifiés CE et conformes à la norme européenne EN 14960. Contrôle technique annuel obligatoire.' },
  { icon: '📋', title: 'RC Pro & Assurance', text: 'Couverture Responsabilité Civile Professionnelle complète pour tous nos événements. Documentation fournie sur demande pour vos services RH et juridiques.' },
  { icon: '⚡', title: 'Conformité électrique', text: 'Tout le matériel électrique (sono, éclairage, machines) est vérifié et conforme aux normes NF C 15-100. Câblage adapté à vos installations.' },
  { icon: '🧯', title: 'Protocole sécurité', text: 'Briefing sécurité avant chaque installation. Présence d\'un responsable Fiestalo\'K durant le montage et le démontage. Vérification des zones d\'installation.' },
];

export function EntreprisePage() {
  return (
    <>
      <section className={styles.hero}>
        <div className="container">
          <Badge tone="danger">SOLUTIONS CORPORATE · ALSACE</Badge>
          <h1 className={styles.title}>L'événementiel<br/>qui donne <span>envie de se retrouver.</span></h1>
          <p className={styles.lead}>De la kermesse d'entreprise au séminaire festif — on s'occupe de tout, vous profitez.</p>
          <div className={styles.ctas}>
            <Button variant="primary" size="lg">Demander un devis →</Button>
            <Button to="/catalogue" variant="secondary" size="lg">Voir le catalogue</Button>
          </div>
        </div>
      </section>

      <Section eyebrow="Références" title="Ils nous ont fait confiance">
        <div className={styles.refs}>
          {REFS.map((r) => (
            <div key={r} className={styles.ref}>
              <span>{r}</span>
            </div>
          ))}
        </div>
        <div className={styles.statsRow}>
          {[
            { v: 'Pro', l: 'Équipe certifiée' },
            { v: 'RC Pro', l: 'Assurance incluse' },
            { v: '100%', l: 'Alsacien' },
          ].map((s) => (
            <div key={s.v} className={styles.stat}>
              <strong>{s.v}</strong>
              <span>{s.l}</span>
            </div>
          ))}
        </div>
      </Section>

      <Section eyebrow="Ce qu'on propose" title="Nos formules entreprise">
        <div className={styles.formules}>
          {FORMULES.map((f) => (
            <article key={f.title} className={styles.formule}>
              <div className={styles.formuleHead}>
                <span className={styles.formuleIcon}>{f.icon}</span>
                <h3>{f.title}</h3>
              </div>
              <p>{f.text}</p>
              <ul>
                {f.items.map((i) => <li key={i}>✓ {i}</li>)}
              </ul>
            </article>
          ))}
        </div>
      </Section>

      <Section background="dark" eyebrow="En images" title="Nos événements corporate">
        <div className={styles.gallery}>
          {EVENTS.map((src) => (
            <div key={src} className={styles.galleryItem}>
              <img src={src} alt="" loading="lazy" />
            </div>
          ))}
        </div>
      </Section>

      <Section eyebrow="Conformité & sécurité" title="Chaque détail, certifié et sécurisé.">
        <div className={styles.compliance}>
          {COMPLIANCE.map((c) => (
            <article key={c.title} className={styles.complianceItem}>
              <span className={styles.complianceIcon}>{c.icon}</span>
              <h3>{c.title}</h3>
              <p>{c.text}</p>
            </article>
          ))}
        </div>
      </Section>

      <Section background="dark" title="Prêt à organiser votre prochain événement ?">
        <p className={styles.darkLead}>Devis gratuit sous 24h. On s'adapte à votre budget et à vos contraintes logistiques.</p>
        <div className={styles.center}>
          <Button variant="primary" size="lg">Demander un devis gratuit →</Button>
        </div>
      </Section>
    </>
  );
}
```

- [ ] **Step 2: EntreprisePage.module.css**

```css
.hero { background: var(--color-ink); color: var(--color-bg); padding: var(--space-3xl) 0; text-align: center; }
.title { color: var(--color-bg); margin: var(--space-md) 0; }
.title span { color: var(--color-danger); }
.lead { color: rgba(255,255,255,0.8); max-width: 640px; margin: 0 auto var(--space-lg); }
.ctas { display: flex; gap: var(--space-sm); justify-content: center; flex-wrap: wrap; }

.refs { display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--space-md); margin-bottom: var(--space-2xl); }
.ref { padding: var(--space-md); background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-md); text-align: center; font-weight: 800; box-shadow: var(--shadow-sm); }
.statsRow { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-md); }
.stat { padding: var(--space-lg); background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-md); text-align: center; }
.stat strong { display: block; font-family: var(--font-display); font-size: 2rem; color: var(--color-danger); }
.stat span { color: var(--color-ink-soft); }

.formules { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-lg); }
.formule { background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-lg); box-shadow: var(--shadow-sm); }
.formuleHead { display: flex; align-items: center; gap: var(--space-sm); margin-bottom: var(--space-sm); }
.formuleIcon { font-size: 2rem; }
.formule p { color: var(--color-ink-soft); margin-bottom: var(--space-sm); }
.formule ul { display: flex; flex-direction: column; gap: var(--space-2xs); font-size: 0.9rem; }

.gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-md); }
.galleryItem { aspect-ratio: 4/3; border-radius: var(--radius-md); overflow: hidden; }
.galleryItem img { width: 100%; height: 100%; object-fit: cover; }

.compliance { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-lg); }
.complianceItem { background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-lg); }
.complianceIcon { font-size: 2rem; }
.complianceItem h3 { margin: var(--space-xs) 0; }
.complianceItem p { color: var(--color-ink-soft); }

.darkLead { text-align: center; color: rgba(255,255,255,0.8); max-width: 640px; margin: 0 auto var(--space-lg); }
.center { text-align: center; }

@media (max-width: 900px) {
  .refs { grid-template-columns: repeat(2, 1fr); }
  .formules, .gallery, .compliance, .statsRow { grid-template-columns: 1fr; }
}
```

- [ ] **Step 3: Visual check**

`/entreprise` doit afficher hero sombre, références, formules, galerie, conformité, CTA final.

- [ ] **Step 4: Commit**

```bash
git add site/src/pages/EntreprisePage.tsx site/src/pages/EntreprisePage.module.css
git commit -m "feat(site-v2): build entreprise page with formulas, references, gallery and compliance"
```

---

## Task 11 — QuiSommesNousPage

**Files:**
- Modify: `site/src/pages/QuiSommesNousPage.tsx` + `QuiSommesNousPage.module.css`

- [ ] **Step 1: Implémenter QuiSommesNousPage**

```tsx
import { Section } from '../components/ui/Section';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import styles from './QuiSommesNousPage.module.css';

const VALUES = [
  { icon: '❤️', title: 'Passion',       text: 'Fiestalo\'K est née d\'une passion simple : rendre chaque fête unique et mémorable, qu\'il s\'agisse d\'un anniv d\'enfant ou d\'un séminaire d\'entreprise.' },
  { icon: '🤝', title: 'Engagement',    text: 'On s\'engage sur chaque prestation : ponctualité, propreté, et une équipe disponible du montage jusqu\'au démontage.' },
  { icon: '📍', title: 'Ancrage local', text: 'Entreprise 100% alsacienne, on connaît le territoire. On livre dans tout le Bas-Rhin et le Haut-Rhin, souvent le jour même.' },
];

const STATS = [
  { v: 'Pro', l: 'Équipe certifiée' },
  { v: 'RC',  l: 'Assurance RC Pro' },
  { v: '2',   l: 'Départements couverts' },
  { v: '98%', l: 'Clients satisfaits' },
];

export function QuiSommesNousPage() {
  return (
    <>
      <section className={styles.hero}>
        <div className="container">
          <Badge tone="danger">NOTRE HISTOIRE</Badge>
          <h1 className={styles.title}>Qui <span>sommes-nous ?</span></h1>
          <p className={styles.lead}>Une équipe alsacienne, pro et passionnée par les belles fêtes.</p>
        </div>
      </section>

      <Section>
        <div className={styles.story}>
          <div className={styles.photo}>
            <img src="https://images.unsplash.com/photo-1543007631-283050bb3e8c?w=900" alt="L'équipe Fiestalo'K" />
            <span className={styles.photoTag}>L'équipe Fiestalo'K · Strasbourg · Alsace</span>
          </div>
          <div className={styles.text}>
            <p className={styles.eyebrow}>Notre histoire</p>
            <h2>Tout a commencé par une envie de faire la fête.</h2>
            <p>Tout a commencé par une décision audacieuse : <strong>6 mecs bien gaulés du cerveau</strong> ont décidé de se lancer dans une aventure magique. Pas de bureau, pas de costard — juste une envie folle de rendre chaque fête inoubliable.</p>
            <p>De cette belle idée est née Fiestalo'K à Strasbourg. On équipe des événements à travers toute l'Alsace — des anniversaires d'enfants aux team buildings d'entreprise, en passant par les kermesses de quartier.</p>
            <p>La magie, on ne l'a pas perdue. Notre équipe est là pour vous, du premier coup de fil jusqu'au démontage du dernier château gonflable.</p>
            <div className={styles.ctas}>
              <Button to="/catalogue" variant="primary" size="md">Voir nos produits →</Button>
              <Button to="/entreprise" variant="secondary" size="md">Offres entreprise</Button>
            </div>
          </div>
        </div>
      </Section>

      <Section eyebrow="Ce qui nous anime" title="Nos valeurs">
        <div className={styles.values}>
          {VALUES.map((v) => (
            <article key={v.title} className={styles.value}>
              <span className={styles.valueIcon}>{v.icon}</span>
              <h3>{v.title}</h3>
              <p>{v.text}</p>
            </article>
          ))}
        </div>
      </Section>

      <section className={styles.stats}>
        <div className={`container ${styles.statsGrid}`}>
          {STATS.map((s) => (
            <div key={s.l} className={styles.stat}>
              <strong>{s.v}</strong>
              <span>{s.l}</span>
            </div>
          ))}
        </div>
      </section>

      <Section title="On se rencontre ?">
        <p className={styles.center}>Venez visiter notre dépôt à Strasbourg ou contactez-nous pour un premier échange sans engagement.</p>
        <div className={styles.center}>
          <Button variant="primary" size="lg">Nous contacter →</Button>
        </div>
      </Section>
    </>
  );
}
```

- [ ] **Step 2: QuiSommesNousPage.module.css**

```css
.hero { background: var(--color-ink); color: var(--color-bg); padding: var(--space-3xl) 0; text-align: center; }
.title { color: var(--color-bg); margin: var(--space-md) 0; }
.title span { color: var(--color-danger); }
.lead { color: rgba(255,255,255,0.8); }

.story { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-2xl); align-items: center; }
.photo { position: relative; }
.photo img { border-radius: var(--radius-lg); box-shadow: var(--shadow-md); }
.photoTag { position: absolute; bottom: var(--space-md); left: var(--space-md); background: rgba(45,52,54,0.85); color: var(--color-bg); padding: 0.5rem 1rem; border-radius: var(--radius-md); font-size: 0.8rem; font-weight: 700; }
.eyebrow { color: var(--color-danger); font-family: var(--font-display); letter-spacing: 0.15em; font-size: 0.9rem; }
.text h2 { margin: var(--space-xs) 0 var(--space-md); }
.text p { color: var(--color-ink-soft); line-height: 1.6; margin-bottom: var(--space-sm); }
.ctas { display: flex; gap: var(--space-sm); flex-wrap: wrap; margin-top: var(--space-md); }

.values { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-lg); }
.value { background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-lg); }
.valueIcon { font-size: 2rem; }
.value h3 { margin: var(--space-xs) 0; }
.value p { color: var(--color-ink-soft); }

.stats { background: var(--color-ink); color: var(--color-bg); padding: var(--space-2xl) 0; }
.statsGrid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-lg); text-align: center; }
.stat strong { display: block; font-family: var(--font-display); font-size: 2.4rem; color: var(--color-danger); }
.stat span { color: rgba(255,255,255,0.7); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; }

.center { text-align: center; }

@media (max-width: 900px) {
  .story, .values, .statsGrid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 3: Visual check**

`/qui-sommes-nous` doit afficher hero sombre, story 2 colonnes, valeurs, stats sombres, CTA contact.

- [ ] **Step 4: Commit**

```bash
git add site/src/pages/QuiSommesNousPage.tsx site/src/pages/QuiSommesNousPage.module.css
git commit -m "feat(site-v2): build qui-sommes-nous page with story, values, stats"
```

---

## Task 12 — Polish responsive et passe finale

**Files:**
- Modify: tous les `.module.css` qui ont besoin d'ajustements mobile
- Modify: `site/src/components/layout/Navbar.module.css` (ajouter menu mobile)
- Modify: `site/src/components/layout/Navbar.tsx` (toggle menu mobile)

- [ ] **Step 1: Ajouter le menu mobile à la Navbar**

Modifier `Navbar.tsx` pour ajouter un état `mobileOpen` :

```tsx
import { useState } from 'react';
// ... imports existants
export function Navbar() {
  const { totalItems, open } = useCart();
  const [mobileOpen, setMobileOpen] = useState(false);
  return (
    <header className={styles.header}>
      <div className={`container ${styles.inner}`}>
        <Link to="/" className={styles.logo} onClick={() => setMobileOpen(false)}>Fiestalo'<span>K</span></Link>
        <nav className={`${styles.nav} ${mobileOpen ? styles.navOpen : ''}`} aria-label="Navigation principale">
          {LINKS.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.to === '/'}
              onClick={() => setMobileOpen(false)}
              className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ''}`}
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className={styles.actions}>
          <button className={styles.cart} onClick={open} aria-label={`Panier, ${totalItems} articles`}>
            🛒 <span className={styles.cartLabel}>Panier</span> {totalItems > 0 && <span className={styles.badge}>{totalItems}</span>}
          </button>
          <button className={styles.burger} onClick={() => setMobileOpen((v) => !v)} aria-label="Menu" aria-expanded={mobileOpen}>
            {mobileOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>
    </header>
  );
}
```

Ajouter au CSS :

```css
.actions { display: flex; align-items: center; gap: var(--space-sm); }
.burger { display: none; font-size: 1.4rem; }
@media (max-width: 768px) {
  .burger { display: block; }
  .nav {
    position: absolute; top: var(--navbar-height); left: 0; right: 0;
    background: var(--color-bg-alt);
    flex-direction: column;
    padding: var(--space-md);
    border-bottom: 1px solid var(--color-border);
    transform: translateY(-110%);
    transition: transform 0.25s ease;
  }
  .navOpen { transform: translateY(0); }
  .cartLabel { display: none; }
}
```

- [ ] **Step 2: Tester chaque page en 375px**

```bash
cd site && npm run dev
```

Ouvrir Chrome devtools mobile (375×812). Pour chaque page, vérifier :
- Navbar : burger fonctionne, menu glisse, panier toujours visible
- Home : sections empilées, pas de débordement horizontal
- Catalogue : filtres au-dessus de la grille, grille 1 col
- Produit : galerie + infos empilées, calendrier lisible
- Entreprise et Qui sommes nous : sections empilées, gallery 1 col

Corriger les overflow horizontaux éventuels en ajoutant `overflow-x: hidden;` sur `body` dans `global.css` si nécessaire.

- [ ] **Step 3: Lighthouse local rapide**

```bash
cd site && npm run build && npx serve dist -l 5180
```

Dans Chrome, ouvrir :5180, lancer Lighthouse (perf + a11y + best-practices). Cibler ≥85 partout. Corriger les `alt=""` manquants si Lighthouse les remonte.

- [ ] **Step 4: Run all tests**

```bash
cd site && npx vitest run
```

Expected : tous les tests verts (CartContext, CatalogueFilters, AvailabilityCalendar).

- [ ] **Step 5: Commit**

```bash
git add site/
git commit -m "feat(site-v2): mobile menu, responsive polish across all pages"
```

---

## Task 13 — README et lien depuis la v1

**Files:**
- Create: `site/README.md`
- Modify: `index.html` (racine, v1) — ajouter un lien discret vers la v2 si besoin (optionnel)

- [ ] **Step 1: Écrire `site/README.md`**

```markdown
# Fiestalo'K — Site v2

Version multi-pages du site Fiestalo'K, basée sur Vite + React + React Router.

## Lancer le site

\`\`\`bash
cd site
npm install
npm run dev      # http://localhost:5174
npm run build    # production build dans site/dist
npm run test     # vitest
\`\`\`

## Architecture

- \`src/pages/\` — une page par route (Home, Catalogue, Produit, Entreprise, Qui sommes-nous)
- \`src/components/{ui,layout,product,catalogue}/\` — composants réutilisables
- \`src/context/\` — CartContext et ReviewsContext (persistés en localStorage)
- \`src/data/\` — products.json, categories, dates indisponibles mockées
- \`src/lib/\` — helpers purs (filtres, format, storage)
- \`src/styles/\` — tokens CSS, reset, global

## Direction artistique

\"Pop Décalé\" — voir \`docs/superpowers/specs/2026-04-07-moodboard-direction-artistique-design.md\`.
```

- [ ] **Step 2: Commit**

```bash
git add site/README.md
git commit -m "docs(site-v2): add README"
```

---

## Self-Review

**Spec coverage check (vs site de référence localhost:5173) :**
- ✅ 5 pages (Home, Catalogue, Produit, Entreprise, Qui sommes-nous) → Tasks 7-11
- ✅ Navbar persistante + Footer + Cart Drawer → Task 6
- ✅ Catégories avec emojis → Task 3 (categories.ts) + Task 7/8
- ✅ Filtres catalogue (catégorie, public, prix, tri) → Task 8
- ✅ Galerie produit + calendrier dispo + avis → Task 9
- ✅ Section corporate avec formules, références, conformité → Task 10
- ✅ Story équipe + valeurs + stats → Task 11
- ✅ Panier persistant localStorage → Task 5
- ✅ Avis persistants localStorage → Task 5/9
- ✅ Identité Pop Décalé (palette, typo, badges stickers) → Task 2/4
- ✅ Responsive mobile → Task 12

**Type consistency check :**
- `Product`, `CartItem`, `Review`, `Category`, `Audience` définis Task 3, importés cohéremment partout.
- `FilterState` défini Task 8 lib, consommé par CataloguePage et CatalogueFilters.
- `useCart()` retourne `{items, totalItems, isOpen, open, close, add, remove, setQuantity, clear}` — utilisé dans Navbar (totalItems, open), CartDrawer (tout), ProductPage (add, open). ✅

**Placeholder scan :** aucun TODO, aucun "implement later", chaque step contient le code complet ou une commande exécutable. ✅

---

Plan complete and saved to `docs/superpowers/plans/2026-04-10-site-v2-react.md`.
