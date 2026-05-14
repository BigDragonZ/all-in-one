/**
 * Audio extraction and processing via ffmpeg.
 */

import { BINARIES } from "../config/paths.ts";

const FFMPEG = BINARIES.ffmpeg;

export interface ExtractOptions {
  inputPath: string;
  outputPath: string;
  sampleRate?: number;
  channels?: number;
  bitrate?: string;
  format?: string;
}

/** Extract audio from video using ffmpeg */
export async function extractAudio(options: ExtractOptions): Promise<string> {
  const {
    inputPath,
    outputPath,
    sampleRate = 22050,
    channels = 1,
    bitrate = "64k",
    format = "mp3",
  } = options;

  const cmd = new Deno.Command(FFMPEG, {
    args: [
      "-y",
      "-i", inputPath,
      "-vn",
      "-ar", String(sampleRate),
      "-ac", String(channels),
      "-b:a", bitrate,
      "-f", format,
      outputPath,
    ],
    stdout: "piped",
    stderr: "piped",
  });

  const { code, stderr } = await cmd.output();
  const err = new TextDecoder().decode(stderr);

  if (code !== 0) {
    throw new Error(`ffmpeg exited ${code}: ${err.slice(0, 500)}`);
  }

  // Verify output exists
  try {
    await Deno.stat(outputPath);
  } catch {
    throw new Error(`ffmpeg did not produce output file: ${outputPath}`);
  }

  return outputPath;
}

/** Get audio/video file info via ffprobe */
export async function probeFile(path: string): Promise<{
  duration: number;
  bitrate: number;
  codec: string;
  sampleRate?: number;
}> {
  const ffprobe = FFMPEG.replace("ffmpeg", "ffprobe");
  const cmd = new Deno.Command(ffprobe, {
    args: [
      "-v", "error",
      "-show_entries", "format=duration,bit_rate",
      "-show_entries", "stream=codec_name,sample_rate",
      "-of", "json",
      path,
    ],
    stdout: "piped",
    stderr: "piped",
  });

  const { code, stdout, stderr } = await cmd.output();
  if (code !== 0) {
    throw new Error(`ffprobe failed: ${new TextDecoder().decode(stderr)}`);
  }

  const data = JSON.parse(new TextDecoder().decode(stdout));
  const format = data.format || {};
  const stream = (data.streams || [])[0] || {};

  return {
    duration: parseFloat(format.duration) || 0,
    bitrate: parseInt(format.bit_rate) || 0,
    codec: stream.codec_name || "unknown",
    sampleRate: stream.sample_rate ? parseInt(stream.sample_rate) : undefined,
  };
}
