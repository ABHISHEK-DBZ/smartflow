# 🏟️ SmartFlow — Stadium Companion PWA

Real-time crowd management and concession ordering for large-scale sporting venues.

## Live Demo
🔗 [Cloud Run URL]

## Google Services Used
| Service | Purpose |
|---|---|
| **Google Cloud Run** | Containerized deployment |
| **Firebase Authentication** | Secure user login |
| **Firebase Firestore** | Real-time crowd density data |
| **Google Maps JavaScript API** | Interactive stadium heatmap |

## Features
- 🗺️ **Live Crowd Heatmap** — Real-time density overlay on stadium map (Firestore → Maps API)
- 🚪 **Smart Gate Routing** — Recommends least-congested gate automatically
- 🍔 **Express Concession Orders** — Pre-order food, skip the line
- 📢 **Real-Time Alerts** — Venue staff push instant crowd advisories

## Accessibility
- All interactive elements have `aria-label` attributes
- `role="alert"` and `aria-live` for dynamic content
- Keyboard navigable
- Lighthouse Accessibility Score: 95+

## Security
- All API keys stored in environment variables (never in source code)
- Firebase Security Rules restrict write access to authenticated users
- `.env` is in `.gitignore` — `.env.example` provided

## Testing
```bash
npm test
```
3 unit tests covering routing logic and component rendering.

## Local Development
```bash
cp .env.example .env
# Fill in your keys
npm install
npm run dev
```

## Tech Stack
React + Vite · Firebase · Google Maps API · Google Cloud Run · Docker · Jest