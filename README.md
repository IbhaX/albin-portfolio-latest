# Albin Anthony — Portfolio

`profile.json` is the source of truth for every section of the site (basic info, contact, skills,
experience, projects, workshops, education, languages, references). `index.html` fetches it at load
time; the data inlined in `index.html` is only a fallback if the fetch fails.

## Editing content

Open `/update-profile.html` (login: see `login.html`) to add, edit, reorder and delete entries in any
section, or edit the raw JSON in the same page. Actions:

- **Preview** — opens `index.html?preview=1`, which renders your unsaved draft from localStorage.
- **Download JSON** — saves `profile.json`; commit it to the repo to publish.
- **Publish** — posts to the `save-profile` Netlify function, which commits `profile.json` to GitHub
  and triggers a Netlify deploy.

The edit key is the current date and time as `MMyyHHmm` (29 Sep 2026 22:30 -> `09262230`),
in Asia/Kolkata, accepted within one minute either side.

Publishing needs these Netlify environment variables:

| Variable | Purpose |
| --- | --- |
| `GITHUB_TOKEN` | Fine-grained PAT for this repo with `contents: write` |
| `EDIT_KEY` | Optional static key accepted alongside the time-based one |
| `EDIT_KEY_TZ` | Optional, defaults to `Asia/Kolkata` |
| `GITHUB_REPO` | Optional, defaults to `IbhaX/albin-portfolio-latest` |
| `GITHUB_BRANCH` | Optional, defaults to `main` |

---

# 1000064977 - Favicon Package

This package contains all the favicon files and configuration needed for complete browser and platform support.

## 📁 Files Included

### Standard Favicons
- `favicon.ico` - Traditional favicon (16x16, 32x32, 48x48)
- `favicon-16x16.png` - Small favicon for browsers
- `favicon-32x32.png` - Standard favicon for browsers

### Apple Touch Icons
- `apple-touch-icon-180x180.png` - iPhone 6 Plus, iPhone 6s Plus, iPhone 7 Plus, iPhone 8 Plus, iPhone X, iPhone XS, iPhone XS Max, iPhone 11 Pro Max
- `apple-touch-icon-152x152.png` - iPad, iPad mini
- `apple-touch-icon-120x120.png` - iPhone 6, iPhone 6s, iPhone 7, iPhone 8, iPhone SE
- `apple-touch-icon-76x76.png` - iPad (iOS 7+)
- `apple-touch-icon-60x60.png` - iPhone (iOS 7+)

### Android & PWA Icons
- `android-chrome-192x192.png` - Android homescreen icon
- `android-chrome-512x512.png` - Android splash screen icon
- `site.webmanifest` - PWA manifest file

### Microsoft Tiles
- `mstile-150x150.png` - Windows 8+ tiles
- `browserconfig.xml` - Microsoft browser configuration

### Additional Files
- `favicon-meta-tags.html` - Complete HTML meta tags
- `README.md` - This file



## 🚀 Installation

1. **Upload all files** to your website's root directory
2. **Copy the HTML meta tags** from `favicon-meta-tags.html` into your website's `<head>` section
3. **Test your favicons** using online favicon checkers

## 💡 Usage Tips

- Place all files in your website's root directory (e.g., `https://yoursite.com/favicon.ico`)
- The HTML meta tags should be placed in the `<head>` section of every page
- Test on different devices and browsers to ensure proper display
- Consider using a CDN for better performance

## 🔧 Advanced Configuration

### PWA (Progressive Web App)
Your `site.webmanifest` file enables PWA features:
- Add to homescreen functionality
- Splash screen customization
- App-like experience on mobile

### Microsoft Integration
The `browserconfig.xml` file configures:
- Windows 8+ tile colors
- Tile icon selection
- Browser-specific settings

## 🌟 Features

- ✅ Complete browser support (Chrome, Firefox, Safari, Edge, IE)
- ✅ All device support (Desktop, Mobile, Tablet)
- ✅ Platform integration (iOS, Android, Windows)
- ✅ PWA ready with manifest.json
- ✅ Optimized file sizes

## 📱 Supported Platforms

- **Web Browsers**: Chrome, Firefox, Safari, Edge, Opera
- **Mobile**: iOS Safari, Android Chrome, Samsung Internet
- **Desktop**: Windows, macOS, Linux
- **Tablets**: iPad, Android tablets
- **PWA**: Progressive Web App support

## 🛠️ Generated with

This favicon package was generated using [Favicon AI](https://favicon-ai.com) - the free favicon generator with AI-powered optimization.

---

Need help? Visit [Favicon AI](https://favicon-ai.com) for more favicon tools and resources.
