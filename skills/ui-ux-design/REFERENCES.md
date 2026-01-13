# UI/UX Design References

Implementation values, patterns, and code snippets. Consult when generating interfaces.

## Table of Contents

- [Aesthetic Directions](#aesthetic-directions)
- [Color Palettes](#color-palettes)
- [Font Pairings](#font-pairings)
- [Spacing & Layout Tokens](#spacing--layout-tokens)
- [Typography Tokens](#typography-tokens)
- [Component Patterns](#component-patterns)
- [Animation Tokens](#animation-tokens)
- [Utility Classes](#utility-classes)
- [CSS Reset](#css-reset)
- [External Resources](#external-resources)

---

## Aesthetic Directions

### Minimalism

- Generous whitespace, limited palette (2-3 colors)
- Typography as primary visual element
- Subtle borders, minimal shadows
- Best for: productivity tools, professional services, portfolios

### Glassmorphism

- Frosted glass effects (`backdrop-filter: blur`)
- Layered depth with transparency
- Gradient backgrounds behind glass panels
- Best for: dashboards, tech products, futuristic interfaces

```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}
```

### Neubrutalism

- High contrast, bold colors (often black + bright accent)
- Hard shadows (no blur): `box-shadow: 4px 4px 0 #000`
- Thick borders, raw/unpolished aesthetic
- Best for: creative agencies, startups, distinctive brands

```css
.neu-card {
  background: #fff;
  border: 3px solid #000;
  box-shadow: 6px 6px 0 #000;
}

.neu-button {
  background: #ffde59;
  border: 2px solid #000;
  box-shadow: 4px 4px 0 #000;
}

.neu-button:active {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 #000;
}
```

### Editorial

- Strong typography hierarchy (serif headings common)
- Grid-based layouts with clear columns
- Photo-forward with intentional cropping
- Best for: content sites, publications, blogs

### Organic

- Rounded corners (12-24px), soft shapes
- Warm color palettes, earth tones or pastels
- Friendly, approachable illustrations
- Best for: consumer apps, wellness, community platforms

### Dark Mode

- Dark surfaces (#0a0a0b base, #141416 elevated)
- Reduced brightness on accents
- Careful contrast management
- Best for: user preference, low-light, media apps

---

## Color Palettes

### Neutral Foundation

```css
:root {
  --gray-50: #fafafa;
  --gray-100: #f4f4f5;
  --gray-200: #e4e4e7;
  --gray-300: #d4d4d8;
  --gray-400: #a1a1aa;
  --gray-500: #71717a;
  --gray-600: #52525b;
  --gray-700: #3f3f46;
  --gray-800: #27272a;
  --gray-900: #18181b;
  --gray-950: #09090b;
}
```

### Accent Colors (WCAG AA on White)

```css
/* Blue - Trust, Professional */
--blue-500: #3b82f6;  /* Hover */
--blue-600: #2563eb;  /* 4.54:1 - Primary */
--blue-700: #1d4ed8;  /* 5.96:1 - Pressed */

/* Green - Success */
--green-600: #16a34a; /* 4.52:1 */
--green-700: #15803d; /* 5.94:1 */

/* Red - Error */
--red-600: #dc2626;   /* 4.53:1 */
--red-700: #b91c1c;   /* 5.98:1 */

/* Amber - Warning */
--amber-600: #d97706; /* 4.5:1 */
--amber-700: #b45309; /* 5.92:1 */

/* Violet - Creative */
--violet-600: #7c3aed; /* 4.51:1 */
--violet-700: #6d28d9; /* 5.96:1 */

/* Teal - Modern */
--teal-600: #0d9488;  /* 4.52:1 */
--teal-700: #0f766e;  /* 5.91:1 */
```

### Dark Mode Foundation

```css
:root[data-theme="dark"] {
  --background: #0a0a0b;
  --surface: #141416;
  --surface-elevated: #1c1c1f;
  --border: #27272a;
  --border-subtle: #1f1f22;
  --text-primary: #fafafa;
  --text-secondary: #a1a1aa;
  --text-muted: #71717a;
}
```

### Semantic Mapping

```css
:root {
  --color-primary: var(--blue-600);
  --color-primary-hover: var(--blue-700);
  --color-success: var(--green-600);
  --color-warning: var(--amber-600);
  --color-error: var(--red-600);
  --color-text-primary: var(--gray-900);
  --color-text-secondary: var(--gray-600);
  --color-text-muted: var(--gray-500);
  --color-border: var(--gray-200);
  --color-border-strong: var(--gray-300);
}
```

---

## Font Pairings

### Modern Tech

```css
--font-heading: 'Geist', 'Inter', system-ui, sans-serif;
--font-body: 'Geist', 'Inter', system-ui, sans-serif;
--font-mono: 'Geist Mono', 'JetBrains Mono', monospace;
```

### Editorial Elegance

```css
--font-heading: 'Playfair Display', 'Georgia', serif;
--font-body: 'Source Serif Pro', 'Georgia', serif;
--font-mono: 'IBM Plex Mono', monospace;
```

### Friendly & Approachable

```css
--font-heading: 'DM Sans', 'Nunito', sans-serif;
--font-body: 'DM Sans', 'Nunito', sans-serif;
--font-mono: 'Fira Code', monospace;
```

### Bold & Distinctive

```css
--font-heading: 'Cabinet Grotesk', 'Satoshi', sans-serif;
--font-body: 'Satoshi', 'DM Sans', sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

### Corporate Professional

```css
--font-heading: 'IBM Plex Sans', 'Source Sans Pro', sans-serif;
--font-body: 'IBM Plex Sans', 'Source Sans Pro', sans-serif;
--font-mono: 'IBM Plex Mono', monospace;
```

### Google Fonts Imports

```css
/* Modern Tech */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Editorial */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Source+Serif+Pro:wght@400;600&display=swap');

/* Friendly */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

/* Professional */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono&display=swap');
```

---

## Spacing & Layout Tokens

```css
:root {
  /* 8px grid */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 16px;
  --space-4: 24px;
  --space-5: 32px;
  --space-6: 48px;
  --space-7: 64px;
  --space-8: 96px;
  
  /* Container widths */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  
  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-full: 9999px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}
```

---

## Typography Tokens

```css
:root {
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
  --text-5xl: 3rem;      /* 48px */
  --text-6xl: 3.75rem;   /* 60px */
  
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

---

## Component Patterns

### Button

```css
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 150ms ease-out;
  background: var(--color-primary);
  color: white;
}

.button:hover { background: var(--color-primary-hover); }
.button:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }
.button:active { transform: scale(0.98); }
.button:disabled { opacity: 0.5; cursor: not-allowed; pointer-events: none; }

/* Variants */
.button-secondary {
  background: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-strong);
}
.button-secondary:hover { background: var(--gray-50); border-color: var(--gray-400); }

.button-ghost { background: transparent; color: var(--color-text-primary); }
.button-ghost:hover { background: var(--gray-100); }

.button-destructive { background: var(--color-error); }
.button-destructive:hover { background: var(--red-700); }

/* Sizes */
.button-sm { padding: 6px 12px; font-size: 13px; }
.button-lg { padding: 12px 24px; font-size: 16px; }
```

### Input Field

```css
.input-group { display: flex; flex-direction: column; gap: 6px; }

.input-label { font-size: 14px; font-weight: 500; color: var(--color-text-primary); }
.input-label-required::after { content: " *"; color: var(--color-error); }

.input {
  padding: 10px 12px;
  font-size: 16px; /* Prevents iOS zoom */
  line-height: 24px;
  color: var(--color-text-primary);
  background: white;
  border: 1px solid var(--color-border-strong);
  border-radius: 6px;
  transition: border-color 150ms, box-shadow 150ms;
}

.input::placeholder { color: var(--color-text-muted); }
.input:hover { border-color: var(--gray-400); }
.input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }
.input:disabled { background: var(--gray-50); color: var(--color-text-muted); cursor: not-allowed; }

.input-error { border-color: var(--color-error); }
.input-error:focus { box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1); }

.input-hint { font-size: 13px; color: var(--color-text-muted); }
.input-error-message { font-size: 13px; color: var(--color-error); }
```

### Card

```css
.card {
  background: var(--color-surface, white);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 24px;
}

.card-interactive { cursor: pointer; transition: box-shadow 200ms ease-out, border-color 200ms ease-out; }
.card-interactive:hover { border-color: var(--color-border-strong); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); }
.card-interactive:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }

.card-title { font-size: 18px; font-weight: 600; margin: 0 0 4px 0; }
.card-description { font-size: 14px; color: var(--color-text-secondary); margin: 0; }
.card-footer { margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--color-border); }
```

### Loading States

```css
/* Spinner */
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--gray-200);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
.spinner-sm { width: 16px; height: 16px; }
.spinner-lg { width: 32px; height: 32px; border-width: 3px; }

@keyframes spin { to { transform: rotate(360deg); } }

/* Skeleton */
.skeleton {
  background: linear-gradient(90deg, var(--gray-100) 25%, var(--gray-200) 50%, var(--gray-100) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-text { height: 16px; margin-bottom: 8px; }
.skeleton-text:last-child { width: 60%; }
.skeleton-title { height: 24px; width: 50%; margin-bottom: 16px; }
.skeleton-avatar { width: 40px; height: 40px; border-radius: 50%; }
```

### Badge

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  font-size: 12px;
  font-weight: 500;
  line-height: 18px;
  border-radius: 4px;
  background: var(--gray-100);
  color: var(--color-text-secondary);
}

.badge-primary { background: #eff6ff; color: var(--blue-700); }
.badge-success { background: #dcfce7; color: var(--green-700); }
.badge-warning { background: #fef3c7; color: var(--amber-700); }
.badge-error { background: #fee2e2; color: var(--red-700); }
```

### Alert

```css
.alert {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid;
}

.alert-icon { flex-shrink: 0; width: 20px; height: 20px; }
.alert-content { flex: 1; }
.alert-title { font-weight: 600; margin-bottom: 4px; }
.alert-description { font-size: 14px; }

.alert-info { background: #eff6ff; border-color: #bfdbfe; color: var(--blue-700); }
.alert-success { background: #f0fdf4; border-color: #bbf7d0; color: var(--green-700); }
.alert-warning { background: #fffbeb; border-color: #fde68a; color: var(--amber-700); }
.alert-error { background: #fef2f2; border-color: #fecaca; color: var(--red-700); }
```

---

## Animation Tokens

```css
:root {
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
  
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in: cubic-bezier(0.7, 0, 0.84, 0);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes scaleIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }

.animate-fade-in { animation: fadeIn var(--duration-normal) var(--ease-out); }
.animate-fade-in-up { animation: fadeInUp var(--duration-normal) var(--ease-out); }
```

---

## Utility Classes

```css
/* Screen reader only */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Focus ring */
.focus-ring:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }

/* Truncate */
.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.line-clamp-3 { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
```

---

## CSS Reset

```css
*, *::before, *::after { box-sizing: border-box; }
* { margin: 0; }
html { -webkit-text-size-adjust: 100%; }
body { line-height: 1.5; -webkit-font-smoothing: antialiased; }
img, picture, video, canvas, svg { display: block; max-width: 100%; }
input, button, textarea, select { font: inherit; }
p, h1, h2, h3, h4, h5, h6 { overflow-wrap: break-word; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## External Resources

| Resource | Use For |
|----------|---------|
| [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker) | Contrast validation |
| [Google Fonts](https://fonts.google.com) | Free web fonts |
| [Fontshare](https://fontshare.com) | Premium free fonts |
| [Coolors](https://coolors.co) | Palette generation |
| [Heroicons](https://heroicons.com) | Clean SVG icons |
| [Lucide](https://lucide.dev) | Open source icons |
| [Radix Icons](https://icons.radix-ui.com) | UI icons |

---
