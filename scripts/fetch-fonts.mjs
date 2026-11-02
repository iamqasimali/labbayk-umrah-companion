// Downloads the Google Fonts used by the app so they work offline.
// Run once: node scripts/fetch-fonts.mjs
import { writeFile, mkdir } from "node:fs/promises";
const CSS_URL = "https://fonts.googleapis.com/css2?family=Marcellus&family=Figtree:wght@400;500;600;700&family=Scheherazade+New:wght@400;700&family=Noto+Nastaliq+Urdu:wght@400;600&display=swap";
const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";
// Keep only the subsets this app shows: Latin, Arabic script, and the punctuation used.
const KEEP = /^(latin|latin-ext|arabic)$/;
const css = await (await fetch(CSS_URL, { headers: { "User-Agent": UA } })).text();
await mkdir("public/fonts", { recursive: true });
let out = "", n = 0;
for (const m of css.matchAll(/\/\*\s*([\w-]+)\s*\*\/\s*(@font-face\s*{[^}]*})/g)) {
  const [, subset, block] = m;
  if (!KEEP.test(subset)) continue;
  const url = block.match(/url\((https:[^)]+)\)/)[1];
  const fam = block.match(/font-family:\s*'([^']+)'/)[1].replace(/\s+/g, "");
  const wt = block.match(/font-weight:\s*(\d+)/)[1];
  const name = `${fam}-${wt}-${subset}.woff2`;
  const buf = Buffer.from(await (await fetch(url)).arrayBuffer());
  await writeFile(`public/fonts/${name}`, buf);
  out += `/* ${subset} */\n` + block.replace(url, `/fonts/${name}`) + "\n";
  n++;
}
await writeFile("public/fonts/fonts.css", out);
console.log(`Saved ${n} font files`);
