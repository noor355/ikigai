# SVG Illustrations

Add your custom SVG vector images here. These illustrations will be used throughout the application to enhance the UI.

## Usage

Place your SVG files in this directory and reference them in components like this:

```jsx
<img src="/assets/illustrations/your-image.svg" alt="Description" />
```

Or for relative imports in components:

```jsx
import illustration from '../assets/illustrations/your-image.svg';

export default function Component() {
  return <img src={illustration} alt="Description" />;
}
```

## Recommended SVG Sources

- **Undraw** (undraw.co) - Free, customizable, high quality
- **Blush** (blush.design) - Beautiful illustrations
- **Pexels** - Free SVG graphics
- **Pixabay** - Free vectors

## Tips for SVGs

- Keep file sizes under 50KB for optimal performance
- Use descriptive filenames
- Ensure accessibility with proper alt text
- Test colors match your brand palette
