#!/usr/bin/env -S deno run --allow-net --allow-read --allow-write --allow-run --allow-env
/**
 * Download a single YouTube video.
 *
 * Usage:
 *   deno run --allow-net --allow-read --allow-write --allow-run --allow-env \
 *     flow/script/download_youtube.ts <URL>
 */

import { PATHS } from "./config/paths.ts";
import { downloadVideo } from "./lib/download.ts";

const url = Deno.args[0];
if (!url) {
  console.error("Usage: download_youtube.ts <YOUTUBE_URL>");
  Deno.exit(1);
}

console.log(`[INFO] Target URL: ${url}`);
console.log(`[INFO] Download dir: ${PATHS.downloadDir}`);

try {
  await Deno.mkdir(PATHS.downloadDir, { recursive: true });
  const saved = await downloadVideo({ url, outputDir: PATHS.downloadDir });
  console.log(`[SUCCESS] Saved to: ${saved}`);
  Deno.exit(0);
} catch (e: any) {
  console.error(`[ERROR] ${e.message}`);
  Deno.exit(1);
}
