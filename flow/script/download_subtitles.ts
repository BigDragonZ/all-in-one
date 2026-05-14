#!/usr/bin/env -S deno run --allow-net --allow-read --allow-write --allow-run --allow-env
/**
 * Download YouTube video subtitles and convert to Markdown.
 *
 * Usage:
 *   deno run --allow-net --allow-read --allow-write --allow-run --allow-env \
 *     flow/script/download_subtitles.ts <URL> <COURSE_NAME> <INDEX>
 *
 * Architecture:
 *   - config/paths.ts    : Centralized paths & binaries
 *   - types/video.ts     : Domain types
 *   - lib/youtube.ts     : YouTube operations (fetch, download, parse, format)
 *   - lib/download.ts    : Video download operations
 *   - This script        : CLI entrypoint, orchestration only
 */

import { courseDir, buildFilename } from "./config/paths.ts";
import { fetchTitle, downloadSubtitle, parseSrt, toMarkdown } from "./lib/youtube.ts";

// ── CLI ───────────────────────────────────────────────────────────────
const url = Deno.args[0];
const courseName = Deno.args[1];
const indexStr = Deno.args[2];

if (!url || !courseName || !indexStr) {
  console.error("Usage: download_subtitles.ts <URL> <COURSE_NAME> <INDEX>");
  Deno.exit(1);
}

const index = parseInt(indexStr, 10);
if (isNaN(index) || index < 1) {
  console.error("[ERROR] INDEX must be a positive integer");
  Deno.exit(1);
}

// ── Orchestration ─────────────────────────────────────────────────────
const outDir = courseDir(courseName);
await Deno.mkdir(outDir, { recursive: true });

console.log(`[INFO] URL: ${url}`);
console.log(`[INFO] Course: ${courseName}`);
console.log(`[INFO] Index: ${index}`);
console.log(`[INFO] Output dir: ${outDir}`);

try {
  const title = await fetchTitle(url);
  const filename = buildFilename(index, title, "md");
  const outputPath = `${outDir}/${filename}`;

  console.log(`[INFO] Video title: ${title}`);
  console.log(`[INFO] Downloading subtitle...`);

  const tempBase = `${outDir}/_tmp_${Date.now()}`;
  const srtFile = await downloadSubtitle(url, tempBase);

  console.log(`[INFO] Converting SRT to Markdown...`);
  const srtContent = await Deno.readTextFile(srtFile);
  const entries = parseSrt(srtContent);
  const markdown = toMarkdown(entries, { title, url, course: courseName, index });

  await Deno.writeTextFile(outputPath, markdown);

  // Cleanup
  await Deno.remove(srtFile);
  try { await Deno.remove(`${tempBase}.en.srt`); } catch { /* ignore */ }

  console.log(`[SUCCESS] Markdown saved to: ${outputPath}`);
  console.log(`[INFO] Total entries: ${entries.length}`);

  Deno.exit(0);
} catch (e: any) {
  console.error(`[ERROR] ${e.message}`);
  Deno.exit(1);
}
