#!/usr/bin/env -S deno run --allow-net --allow-read --allow-write --allow-run --allow-env
/**
 * Transcribe audio file using GCP Vertex AI or Gemini.
 *
 * Usage:
 *   deno run --allow-net --allow-read --allow-write --allow-run --allow-env \
 *     flow/script/transcribe_audio.ts <AUDIO_PATH> <COURSE_NAME> <INDEX>
 *
 * Environment:
 *   gcp-vertex-key    : GCP Vertex AI API key
 *   GEMINI_API_KEY    : Gemini standard API key
 *   TRANSCRIBER       : Explicit backend (gcp-vertex | gemini), null = auto
 */

import { courseDir, buildFilename } from "./config/paths.ts";
import { transcribeAudio } from "./lib/transcribe.ts";

const audioPath = Deno.args[0];
const courseName = Deno.args[1];
const indexStr = Deno.args[2];

if (!audioPath || !courseName || !indexStr) {
  console.error("Usage: transcribe_audio.ts <AUDIO_PATH> <COURSE_NAME> <INDEX>");
  Deno.exit(1);
}

const index = parseInt(indexStr, 10);
if (isNaN(index) || index < 1) {
  console.error("[ERROR] INDEX must be a positive integer");
  Deno.exit(1);
}

// Validate input
try {
  await Deno.stat(audioPath);
} catch {
  console.error(`[ERROR] Audio file not found: ${audioPath}`);
  Deno.exit(1);
}

const outDir = courseDir(courseName);
await Deno.mkdir(outDir, { recursive: true });

console.log(`[INFO] Audio:  ${audioPath}`);
console.log(`[INFO] Course: ${courseName}`);
console.log(`[INFO] Index:  ${index}`);
console.log(`[INFO] Output: ${outDir}`);

try {
  const result = await transcribeAudio(audioPath);

  const filename = buildFilename(index, `Transcription ${courseName}`, "md");
  const outputPath = `${outDir}/${filename}`;

  const content = `# Transcription

## 元信息

- **序号**: ${index}
- **课程**: ${courseName}
- **音频**: ${audioPath}
- **后端**: ${result.backend}
- **模型**: ${result.model}
- **处理时间**: ${new Date().toISOString().slice(0, 19).replace("T", " ")}

---

## 转写内容

${result.text}
`;

  await Deno.writeTextFile(outputPath, content);

  console.log(`[SUCCESS] Transcription saved to: ${outputPath}`);
  console.log(`[INFO] Backend: ${result.backend}`);
  console.log(`[INFO] Model:   ${result.model}`);
  console.log(`[INFO] Chars:   ${result.text.length}`);

  Deno.exit(0);
} catch (e: any) {
  console.error(`[ERROR] ${e.message}`);
  Deno.exit(1);
}
