#!/usr/bin/env -S deno run --allow-net --allow-read --allow-write --allow-run --allow-env
/**
 * Download YouTube video subtitles using yt-dlp.
 *
 * Usage:
 *   deno run --allow-net --allow-read --allow-write --allow-run --allow-env \
 *     flow/script/download_subtitles.ts <URL> <COURSE_NAME> <INDEX>
 *
 * Example:
 *   deno run ... flow/script/download_subtitles.ts \
 *     "https://www.youtube.com/watch?v=LYGYvN5LUbA" \
 *     "Valuation_Undergrad_2022" 1
 *
 * Output:
 *   all-in-one/flow/Valuation_Undergrad_2022/01-Valuation A Preview.srt
 */

import { dirname, join } from "https://deno.land/std@0.224.0/path/mod.ts";

const YTDLP_PATH = new URL("../../.venv/bin/yt-dlp", import.meta.url).pathname;
const PROJECT_ROOT = dirname(dirname(dirname(import.meta.url))).replace("file://", "");

function sanitizeFilename(name: string): string {
  return name.replace(/[<>:"/\\|?*]/g, "_").trim();
}

async function fetchVideoTitle(url: string): Promise<string> {
  const cmd = new Deno.Command(YTDLP_PATH, {
    args: ["--cookies-from-browser", "chrome", "--no-warnings", "--print", "%(title)s", "--skip-download", url],
    stdout: "piped",
    stderr: "piped",
  });
  const { code, stdout, stderr } = await cmd.output();
  if (code !== 0) {
    throw new Error(`Failed to fetch title: ${new TextDecoder().decode(stderr)}`);
  }
  return new TextDecoder().decode(stdout).trim();
}

async function downloadSubtitle(url: string, outputPath: string): Promise<void> {
  const cmd = new Deno.Command(YTDLP_PATH, {
    args: [
      "--cookies-from-browser", "chrome",
      "--no-warnings",
      "--write-auto-subs",
      "--skip-download",
      "--sub-langs", "en",
      "--convert-subs", "srt",
      "--output", outputPath,
      url,
    ],
    stdout: "piped",
    stderr: "piped",
  });

  const { code, stderr } = await cmd.output();
  const err = new TextDecoder().decode(stderr);

  if (code !== 0 && !err.includes("Downloading")) {
    throw new Error(`yt-dlp exited ${code}: ${err}`);
  }
}

// ── main ──────────────────────────────────────────────────────────────
const url = Deno.args[0];
const courseName = Deno.args[1];
const indexStr = Deno.args[2];

if (!url || !courseName || !indexStr) {
  console.error("Usage: download_subtitles.ts <URL> <COURSE_NAME> <INDEX>");
  console.error("  URL:          YouTube video or playlist URL");
  console.error("  COURSE_NAME:  Directory name under flow/");
  console.error("  INDEX:        Video sequence number (e.g., 1, 2, 3)");
  Deno.exit(1);
}

const index = parseInt(indexStr, 10);
if (isNaN(index) || index < 1) {
  console.error("[ERROR] INDEX must be a positive integer");
  Deno.exit(1);
}

const outDir = join(PROJECT_ROOT, "flow", courseName);
await Deno.mkdir(outDir, { recursive: true });

console.log(`[INFO] URL: ${url}`);
console.log(`[INFO] Course: ${courseName}`);
console.log(`[INFO] Index: ${index}`);
console.log(`[INFO] Output dir: ${outDir}`);

try {
  const title = await fetchVideoTitle(url);
  const safeTitle = sanitizeFilename(title);
  const filename = `${String(index).padStart(2, "0")}-${safeTitle}.en.srt`;
  const outputPath = join(outDir, filename);

  // yt-dlp appends .en.srt automatically, so we use base path without extension
  const basePath = join(outDir, `${String(index).padStart(2, "0")}-${safeTitle}`);

  console.log(`[INFO] Video title: ${title}`);
  console.log(`[INFO] Downloading subtitle...`);

  await downloadSubtitle(url, basePath);

  // Check if file was created (yt-dlp may add .en.srt)
  const expectedFile = `${basePath}.en.srt`;
  try {
    await Deno.stat(expectedFile);
    console.log(`[SUCCESS] Subtitle saved to: ${expectedFile}`);
  } catch {
    // Try without .en
    const altFile = `${basePath}.srt`;
    try {
      await Deno.stat(altFile);
      // Rename to include .en
      await Deno.rename(altFile, expectedFile);
      console.log(`[SUCCESS] Subtitle saved to: ${expectedFile}`);
    } catch {
      console.error("[ERROR] Subtitle file not found after download");
      Deno.exit(1);
    }
  }

  Deno.exit(0);
} catch (e: any) {
  console.error(`[ERROR] ${e.message}`);
  Deno.exit(1);
}
