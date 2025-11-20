# Creating a Preview Image for Social Media Embeds

To create a proper preview image for Discord/Twitter/Facebook embeds, you have a few options:

## Option 1: Use a Screenshot Tool
1. Open `static/images/preview-template.html` in your browser
2. Set your browser window to 1200x630 pixels
3. Take a screenshot and save it as `static/images/music-preview.png`

## Option 2: Use an Online Tool
Use a free OG image generator like:
- https://www.opengraph.xyz/
- https://ogimage.gallery/
- https://www.bannerbear.com/

Create an image that is **1200x630 pixels** (recommended for Open Graph)

## Option 3: Design Your Own
Create an image with:
- **Dimensions**: 1200x630 pixels (Open Graph standard)
- **Content**: Logo, site name, and a visual representation of music
- **Format**: PNG or JPG
- **Size**: Keep it under 5MB (ideally under 1MB)

## Option 4: Use a Simple Placeholder
For now, you can use a solid color image or any music-related image as a placeholder.

## Quick Command (macOS)
If you have ImageMagick installed:
```bash
convert -size 1200x630 gradient:#667eea-#764ba2 \
  -gravity center -pointsize 72 -fill white \
  -annotate +0-50 "🎵 Discord Music Queue" \
  -pointsize 36 -annotate +0+50 "View what's playing now" \
  static/images/music-preview.png
```

Save your preview image as: `static/images/music-preview.png`
