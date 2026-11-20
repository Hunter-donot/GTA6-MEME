// GTA 6 meme v5 entrypoint (Node 22, stdlib only).
// Reads POST.json from the repo root, validates it names a real X post,
// and copies POST.json and meme.jpg to /output for the bounty harness.
// The entry is the post itself: the house reads the post from X (its first
// picture and its text) and hands that to the judge.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const postPath = join(here, "POST.json");
if (!existsSync(postPath)) {
  console.error("POST.json not found at repo root");
  process.exit(1);
}

const raw = readFileSync(postPath, "utf8");
let post: unknown;
try {
  post = JSON.parse(raw);
} catch {
  console.error("POST.json is not valid JSON");
  process.exit(1);
}

// The kit names the field "url"; accept "post_url" too, same value.
const rawUrl = (post as { url?: unknown; post_url?: unknown }).url
  ?? (post as { post_url?: unknown }).post_url;
if (
  typeof rawUrl !== "string" ||
  !(rawUrl.startsWith("https://x.com/") || rawUrl.startsWith("https://twitter.com/"))
) {
  console.error("POST.json url must be an https://x.com/ or https://twitter.com/ post link");
  process.exit(1);
}

// Strip any query string or fragment (e.g. tracking params) so the
// stored URL is the clean post link.
const url = rawUrl.split("?")[0].split("#")[0];

const statusId = url.split("/status/")[1];
if (!statusId || !/^\d+$/.test(statusId)) {
  console.error("POST.json url must name an X post with a numeric status id");
  process.exit(1);
}

copyFileSync(postPath, join(outDir, "POST.json"));
console.log("copied POST.json to", join(outDir, "POST.json"));

const memePath = join(here, "meme.jpg");
if (!existsSync(memePath)) {
  console.error("meme.jpg not found at repo root");
  process.exit(1);
}
copyFileSync(memePath, join(outDir, "meme.jpg"));
console.log("copied meme.jpg to", join(outDir, "meme.jpg"));
