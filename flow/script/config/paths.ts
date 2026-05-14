/**
 * Centralized path configuration for all scripts.
 * Modify here when project structure changes.
 */

import { dirname, join, resolve } from "https://deno.land/std@0.224.0/path/mod.ts";

export const PROJECT_ROOT = dirname(dirname(dirname(dirname(import.meta.url)))).replace("file://", "");
const SCRIPT_DIR = dirname(dirname(import.meta.url)).replace("file://", "");

export const PATHS = {
  projectRoot: PROJECT_ROOT,
  scriptDir: SCRIPT_DIR,
  venvBin: join(PROJECT_ROOT, ".venv", "bin"),
  flowDir: join(PROJECT_ROOT, "flow"),
  downloadDir: "/tmp/video_audio_downloads",
} as const;

export const BINARIES = {
  ytDlp: join(PATHS.venvBin, "yt-dlp"),
  ffmpeg: resolve("/opt/homebrew/bin/ffmpeg"),
} as const;

/** Resolve course output directory */
export function courseDir(courseName: string): string {
  return join(PATHS.flowDir, courseName);
}

/** Build standardized filename: {index}-{safeTitle}.{ext} */
export function buildFilename(
  index: number,
  title: string,
  ext: string,
): string {
  const safe = title.replace(/[<>:\"/\\|?*]/g, "_").trim();
  return `${String(index).padStart(2, "0")}-${safe}.${ext}`;
}
