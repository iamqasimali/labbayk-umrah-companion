# Labbayk Umrah Companion

Installable, offline web app with every Umrah dua (Arabic, Roman Urdu, Urdu, English),
repeat playback, a big-text practice mode, and a Tawaf/Sa'i round counter.

## Files
- `umrah-companion.html` — the page itself (edit this)
- `scripts/pwa-snippet.html` — install prompt, offline badge, service worker registration
- `scripts/build.mjs` — builds `public/` and generates `public/sw.js` (pre-caches every file)
- `public/` — deployable output: fonts, icons, manifest
- `scripts/fetch-fonts.mjs`, `scripts/make-icons.py` — one-off asset generators

## Run locally
    npm start            # builds, then serves on http://localhost:4173

## Deploy
Vercel:   `vercel login` once, then `npm run deploy:vercel`
Netlify:  `netlify login` once, then `npm run deploy:netlify`
Both read their settings from `vercel.json` / `netlify.toml` (build: `node scripts/build.mjs`, output: `public`).

After any edit, redeploy. Installed phones pick up the new version and show "A new version is ready".

## Recitations (public/audio)
Real human recitations only, never a computer voice:
- Quranic duas: Sheikh Mishary Rashid Alafasy (quranicaudio.com), cut with Quran.com word timings
- Sunnah duas: Hisn al-Muslim audio (hisnmuslim.com)

`scripts/audio-plan.py` lists every cut (source file and seconds, or ayah and word range);
`scripts/make-audio.py` produces one clip per dua plus one per line. Every clip was checked with
Whisper speech recognition against the dua text. Duas with no authentic recording (the niyyah,
the salam at the Prophet's grave) show "no recording" instead of a Play button.
