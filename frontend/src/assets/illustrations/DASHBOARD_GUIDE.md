# Dashboard SVG Illustration Guide

## Overview

The enhanced Dashboard has **3 SVG illustration spaces** - one on each card:

1. **Ikigai Snapshot Card** - Top left illustration space
2. **AI Insight Card** - Middle illustration space  
3. **Latest Activity Card** - Bottom illustration space

All illustration boxes are located at: `src/assets/illustrations/`

## Current Placeholder

Each card has a `.illustration-box` with:
- **Size**: 100px × 100px
- **Background**: Gradient with dashed border
- **Current content**: Icon placeholder "Your SVG here"
- **Hover effect**: Border color changes to primary color

## How to Add Your SVGs

### Step 1: Download SVG Images
- **Ikigai Snapshot**: Search for "progress", "growth", "analytics" on Undraw or Blush
- **AI Insight**: Search for "brain", "lightbulb", "idea", "learning"
- **Latest Activity**: Search for "activity", "calendar", "timeline", "notes"

### Step 2: Place Files in Assets
```
frontend/src/assets/illustrations/
├── ikigai-snapshot.svg
├── ai-insight.svg
└── activity-timeline.svg
```

### Step 3: Update DashboardPage.js

Find the illustration boxes and replace with your SVGs:

**For Ikigai Snapshot Card (around line 90):**
```jsx
<div className="illustration-box">
  <img 
    src={require('../assets/illustrations/ikigai-snapshot.svg').default}
    alt="Ikigai illustration"
  />
</div>
```

**For AI Insight Card (around line 130):**
```jsx
<div className="illustration-box">
  <img 
    src={require('../assets/illustrations/ai-insight.svg').default}
    alt="AI Insight"
  />
</div>
```

**For Latest Activity Card (around line 170):**
```jsx
<div className="illustration-box">
  <img 
    src={require('../assets/illustrations/activity-timeline.svg').default}
    alt="Activity Timeline"
  />
</div>
```

## SVG Recommendations

### Best Practices
- ✅ Square or nearly square (100×100px base size)
- ✅ File size: Under 30KB for optimal performance
- ✅ Viewbox properly defined for responsiveness
- ✅ High contrast colors that match your brand

### Color Palette to Match
```css
--primary-100: #5DA399 (teal)
--primary-200: #40867d (darker teal)
--accent-100: #FF6B6B (red)
--text-100: #333333
--bg-100: #E0E7E9
```

### Suggested SVGs by Card

**Ikigai Snapshot Card:**
- Growth chart with upward trends
- Circular progress indicator
- Mountain/peak achievement
- Stacked bars showing balance

**AI Insight Card:**
- Brain/mind with lightbulb
- Neural network visualization
- Book/knowledge theme
- Magnifying glass discovery

**Latest Activity Card:**
- Calendar with checkmarks
- Timeline/timeline events
- Clipboard with items
- Activity graph/trend line

## Size Specifications

The illustration boxes are responsive:
- **Desktop**: 100px × 100px
- **Tablet**: 90px × 90px
- **Mobile**: 80px × 80px

SVGs will auto-scale within these constraints.

## CSS Class Reference

If you need to customize styling, use these classes:

```css
.illustration-box         /* Container box */
.card-illustration        /* Wrapper div */
.dashboard-card           /* Card container */
.card-content             /* Card content area */
```

## Example SVG (Inline Alternative)

If you prefer inline SVG components, create `src/components/Icons/DashboardIcons.jsx`:

```jsx
export const IkigaiIcon = () => (
  <svg viewBox="0 0 100 100" width="100" height="100">
    {/* Your SVG content */}
  </svg>
);

// Usage in DashboardPage.js
<div className="illustration-box">
  <IkigaiIcon />
</div>
```

## Testing & Validation

1. Place SVG in assets folder
2. Add image import to component
3. Test on desktop (100px display)
4. Test on mobile (80px display)
5. Verify colors match theme
6. Check file size < 50KB total

## Color Customization

If your SVGs don't match colors, you can apply CSS filters:

```jsx
<img 
  src="illustration.svg"
  alt="Illustration"
  style={{ filter: 'hue-rotate(20deg) saturate(1.2)' }}
/>
```

## Troubleshooting

**SVG not showing?**
- Check file path is correct
- Verify file exists in assets folder
- Check browser console for 404 errors

**Colors look wrong?**
- Download SVG with editable colors
- Or use CSS filters to adjust hue/saturation
- Verify SVG viewBox attribute

**Size too large?**
- Optimize SVG with SVGO tool
- Remove unnecessary metadata
- Keep file under 30KB

## Resources

- **Undraw.co** - High quality, customize colors easily
- **Blush.design** - Beautiful, pre-styled illustrations
- **Pixabay/Pexels** - Free vector resources
- **SVGO** - Optimize SVG files
