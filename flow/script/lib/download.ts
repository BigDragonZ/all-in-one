/**
 * Video download operations via yt-dlp.
 */

import { BINARIES } from "../config/paths.ts";

const YTDLP = BINARIES.ytDlp;

export interface DownloadOptions {
  url: string;
  outputDir: string;
  playlistItems?: string;
  format?: string;
  mergeFormat?: string;
}

export async function downloadVideo(options: DownloadOptions): Promise<string> {
  const {
    url,
    outputDir,
    playlistItems = "1",
    format = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    mergeFormat = "mp4",
  } = options;

  const args = [
    "--cookies-from-browser", "chrome",
    "--playlist-items", playlistItems,
    "--format", format,
    "--merge-output-format", mergeFormat,
    "--output", `${outputDir}/%(title)s.%(ext)s`,
    "--no-warnings",
    url,
  ];

  const cmd = new Deno.Command(YTDLP, {
    args,
    stdout: "piped",
    stderr: "piped",
  });

  const { code, stdout, stderr } = await cmd.output();
  const out = new TextDecoder().decode(stdout);
  const err = new TextDecoder().decode(stderr);

  if (code !== 0) {
    throw new Error(`yt-dlp exited ${code}\n${err}`);
  }

  // Extract destination from output
  const match = out.match(/\[download\] Destination: (.+)/m) ||
    err.match(/\[download\] Destination: (.+)/m);
  if (match) return match[1].trim();

  // Fallback: newest file in output dir
  const files: string[] = [];
  for await (const entry of Deno.readDir(outputDir)) {
    if (entry.isFile) files.push(entry.name);
  }
  if (files.length === 0) throw new Error("No file found after download");

  files.sort((a, b) => {
    const sa = Deno.statSync(`${outputDir}/${a}`).mtime ?? new Date(0);
    const sb = Deno.statSync(`${outputDir}/${b}`).mtime ?? new Date(0);
    return sb.getTime() - sa.getTime();
  });

  return `${outputDir}/${files[0]}`;
}
