// Entry for the make.fun bounty "Post a GTA 6 meme on X" (gta6-meme-x-01).
//
// The meme itself is posted on X; this program's only job is to hand the
// grader the post's address. It copies POST.json from the repository root
// into the output directory, byte for byte, and nothing else.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(botDir, "POST.json");
const dst = join(outDir, "POST.json");

if (!existsSync(src)) {
  console.error(`POST.json not found at ${src}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });

try {
  copyFileSync(src, dst);
} catch (err) {
  console.error(`failed to copy POST.json to ${dst}: ${err}`);
  process.exit(1);
}

// The copy is byte for byte; now sanity-check the copied file so a broken
// POST.json is caught here instead of silently reaching the grader.
let parsed;
try {
  parsed = JSON.parse(readFileSync(dst, "utf8"));
} catch (err) {
  console.error(`copied POST.json at ${dst} is not valid JSON: ${err}`);
  process.exit(1);
}
if (
  typeof parsed !== "object" ||
  parsed === null ||
  typeof parsed.url !== "string" ||
  (!parsed.url.startsWith("https://x.com/") &&
    !parsed.url.startsWith("https://twitter.com/"))
) {
  console.error(
    `copied POST.json at ${dst} has no valid url: expected a "url" string starting with https://x.com/ or https://twitter.com/`,
  );
  process.exit(1);
}

console.log(`wrote ${dst}`);
