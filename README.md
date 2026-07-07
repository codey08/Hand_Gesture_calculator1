# 🖐️ Hand Gesture Calculator (Web)

Do simple math with your fingers, right in the browser. Hand tracking runs
entirely client-side with [MediaPipe Hands](https://developers.google.com/mediapipe) —
your camera feed never leaves your device.

This is a browser rewrite of the original Python + OpenCV/MediaPipe desktop
script so it can be deployed to a static host like Vercel.

**Live demo:** https://hand-gesture-web-xi.vercel.app

## How it works

1. Hold up fingers for the **first number** (0–5, or up to 10 with both hands).
2. Hold a gesture for the **operator**: `1 = −`, `2 = +`, `3 = ×`, `4 = ÷`.
3. Hold up fingers for the **second number**.
4. Hold any gesture to reveal the **result**.

Hold each pose steady for ~2 seconds — the on-screen ring shows progress.

## Run locally

Because it uses ES modules and the webcam, open it through a local web server
(not `file://`):

```bash
npx serve .
# then open the printed http://localhost:3000
```

Camera access requires a secure context — `localhost` and any `https://`
(such as your Vercel URL) both qualify.

## Test

The pure gesture/calculator logic is unit-tested (no browser needed):

```bash
node calc.test.mjs
```

## Deploy

It's a fully static site — deploy the repo to Vercel:

```bash
npx vercel --prod
```

## Files

- `index.html` — page layout
- `style.css` — styling
- `app.js` — camera, MediaPipe hand tracking, gesture → calculator state machine
- `calc.mjs` — pure finger-counting + calculator logic (DOM-free, testable)
- `calc.test.mjs` — unit tests for `calc.mjs`
- `vercel.json` — static hosting config
