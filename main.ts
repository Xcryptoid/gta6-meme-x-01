// gta6-meme-x-01 entry (Node 22, standard library only).
// The entry is the X post itself: a GTA 6 meme with make.fun's ghost as the
// sun over Vice City, posted from a public account. This program only copies
// POST.json from the repository root to /output/POST.json, where the gate
// reads it. POST.json holds the post's address as
// {"url": "https://x.com/<handle>/status/<id>"}.
// Run locally: mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(botDir, "POST.json");
const target = join(outDir, "POST.json");

if (!existsSync(source)) {
  console.error(
    `no POST.json in ${botDir}: post the meme on X first, then write its address into POST.json`,
  );
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
