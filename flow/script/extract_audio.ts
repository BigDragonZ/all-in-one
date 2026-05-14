#!/usr/bin/env -S deno run --allow-net --allow-read --allow-write --allow-run --allow-env
/**
 * Extract audio from video file using ffmpeg.
 *
 * Usage:
 *   deno run --allow-net --allow-read --allow-write --allow-run --allow-env \
 *     flow/script/extract_audio.ts <VIDEO_PATH> [OUTPUT_PATH]
 *
 * Example:
 *   deno run ... flow/script/extract_audio.ts \
 *     /tmp/video_audio_downloads/video.mp4 \
 *     flow/Valuation_Undergrad_2022/01-audio.mp3
 */

import { extractAudio, probeFile } from "./lib/audio.ts";

const videoPath = Deno.args[0];
const outputPath = Deno.args[1];

if (!videoPath) {
  console.error("Usage: extract_audio.ts <VIDEO_PATH> [OUTPUT_PATH]");
  console.error("  VIDEO_PATH:   Path to input video file");
  console.error("  OUTPUT_PATH:  Optional output path (default: input.mp3)");
  Deno.exit(1);
}

// Validate input exists
try {
  await Deno.stat(videoPath);
} catch {
  console.error(`[ERROR] Input file not found: ${videoPath}`);
  Deno.exit(1);
}

const outPath = outputPath || videoPath.replace(/\.[^.]+$/, ".mp3");

console.log(`[INFO] Input:  ${videoPath}`);
console.log(`[INFO] Output: ${outPath}`);

try {
  console.log(`[INFO] Probing input file...`);
  const info = await probeFile(videoPath);
  console.log(`[INFO] Duration: ${info.duration.toFixed(2)}s, Codec: ${info.codec}`);

  console.log(`[INFO] Extracting audio...`);
  const result = await extractAudio({
    inputPath: videoPath,
    outputPath: outPath,
    sampleRate: 22050,
    channels: 1,
    bitrate: "64k",
    format: "mp3",
  });

  const outInfo = await probeFile(result);
  const sizeMb = (await Deno.stat(result)).size / (1024 * 1024);

  console.log(`[SUCCESS] Audio saved to: ${result}`);
  console.log(`[INFO] Size: ${sizeMb.toFixed(2)} MB`);
  console.log(`[INFO] Duration: ${outInfo.duration.toFixed(2)}s`);
  console.log(`[INFO] Bitrate: ${outInfo.bitrate} bps`);

  Deno.exit(0);
} catch (e: any) {
  console.error(`[ERROR] ${e.message}`);
  Deno.exit(1);
}
