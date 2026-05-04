# How to Add SVG Images to Journal Page

## Quick Start

1. **Place your SVG files** in this folder: `src/assets/illustrations/`
2. **Import in your component** and use it

## Methods to Use SVG Images

### Method 1: Direct Image Import (Easiest)
```jsx
// In JournalPage.js
import journalIllustration from '../assets/illustrations/journal-meditation.svg';

// In the illustration-placeholder div
<img src={journalIllustration} alt="Journal Meditation" />
```

### Method 2: Static URL (For public folder)
Copy your SVG to `public/illustrations/` and reference it:
```jsx
<img 
  src="/illustrations/journal-meditation.svg" 
  alt="Journal Meditation" 
  className="journal-illustration"
/>
```

### Method 3: Inline SVG Component
Create a reusable SVG component:

**Create file: `src/components/Icons/JournalSVG.jsx`**
```jsx
export const JournalSVG = () => (
  <svg viewBox="0 0 200 200" className="journal-illustration">
    {/* Your SVG content here */}
  </svg>
);
```

Then use it:
```jsx
import { JournalSVG } from '../components/Icons/JournalSVG';

// In component
<JournalSVG />
```

## Current Placeholder

The journal page has a `illustration-placeholder` div with these characteristics:
- **Size**: 140px × 140px (responsive)
- **Location**: Top right of journal header
- **Styling**: Gradient background with dashed border
- **Current content**: "Your SVG here" placeholder

## How to Replace the Placeholder

Edit `src/pages/JournalPage.js` around line 110:

```jsx
{/* Illustration Space */}
<div className="journal-illustration-space">
  <div className="illustration-placeholder">
    {/* REPLACE THIS SECTION */}
    <img 
      src={require('../assets/illustrations/your-image.svg').default}
      alt="Journal illustration"
      style={{ maxWidth: '100%', height: 'auto' }}
    />
  </div>
</div>
```

## Recommended SVG Properties

For best results, your SVG should have:
- **Viewbox**: Defined for responsiveness
- **Dimensions**: Square or slightly rectangular (140x140px base)
- **Colors**: Match your color palette or use CSS variables
- **Transparency**: Support for semi-transparent areas
- **File size**: Under 50KB

## Example SVG Download Sources

### Free SVG Libraries
- 🎨 **Undraw** (undraw.co) - High quality, customize colors
- 🎪 **Blush** (blush.design) - Beautiful illustrations
- 📦 **Pexels** - Free vectors
- 🎯 **Pixabay** - Large collection

### Recommended for Journal Page
- Meditation/mindfulness scenes
- Writing/journaling themes
- Growth/progress visuals
- Light bulbs/inspiration
- Daily routine themes

## CSS Class for Styling

The placeholder has these CSS classes you can reference:
- `.journal-illustration-space` - Container
- `.illustration-placeholder` - Placeholder div
- Update `JournalPage.css` to customize further

## Color Palette for SVGs

Use these CSS variables or hex colors in your SVGs:
```
--primary-100: #5DA399 (teal)
--primary-200: #40867d (darker teal)
--primary-300: #004840 (deep teal)
--accent-100: #FF6B6B (red)
--accent-200: #8f001a (dark red)
--text-100: #333333 (dark text)
--text-200: #5c5c5c (medium text)
--bg-100: #E0E7E9 (light background)
```

## Testing Your SVG

1. Place SVG in `src/assets/illustrations/`
2. Update the import in `JournalPage.js`
3. Test responsiveness on mobile
4. Verify colors match your theme
5. Check file size for performance

## Questions?

- **Need a custom illustration?** Use Undraw (customize colors to match your palette)
- **Want animation?** Convert SVG to React component for animated effects
- **SVG won't display?** Check the path, ensure file extension is `.svg`, verify viewBox
