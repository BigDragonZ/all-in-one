/**
 * Audio transcription via GCP Vertex AI and Gemini fallback.
 *
 * Architecture:
 *   1. Try GCP Vertex AI first (project credits, recommended)
 *   2. Fallback to Gemini standard API if Vertex fails
 *
 * Implementation uses direct REST API calls to avoid google-genai
 * client initialization issues with API key + project combos.
 */

import { loadConfig, validateConfig, type TranscribeConfig } from "../config/transcribe.ts";
import { BINARIES } from "../config/paths.ts";

const PYTHON = BINARIES.ytDlp.replace("yt-dlp", "python3");

export interface TranscribeResult {
  text: string;
  backend: string;
  model: string;
}

/** Run Python script via subprocess */
async function runPython(script: string): Promise<string> {
  const cmd = new Deno.Command(PYTHON, {
    args: ["-c", script],
    stdout: "piped",
    stderr: "piped",
  });
  const { code, stdout, stderr } = await cmd.output();
  const out = new TextDecoder().decode(stdout);
  const err = new TextDecoder().decode(stderr);

  if (code !== 0) {
    throw new Error(`Python exited ${code}: ${err.slice(0, 500)}`);
  }
  return out.trim();
}

// ── GCS upload helper ─────────────────────────────────────────────────

/** Upload file to GCS bucket */
async function uploadToGcs(
  localPath: string,
  cfg: TranscribeConfig,
): Promise<string> {
  const script = `
import sys
import os
from google.cloud import storage

client = storage.Client(project=${JSON.stringify(cfg.gcpProjectId)})
bucket = client.bucket(${JSON.stringify(cfg.gcsBucket)})
blob_name = ${JSON.stringify(cfg.gcsPrefix)} + os.path.basename(${JSON.stringify(localPath)})
blob = bucket.blob(blob_name)
blob.upload_from_filename(${JSON.stringify(localPath)})
print(f"gs://${cfg.gcsBucket}/{blob_name}")
`;
  return await runPython(script);
}

// ── Vertex AI transcription via REST ──────────────────────────────────

/** Transcribe via Vertex AI REST API with inline audio */
async function transcribeVertex(
  audioPath: string,
  cfg: TranscribeConfig,
): Promise<string> {
  const script = `
import urllib.request
import json
import base64

api_key = ${JSON.stringify(cfg.gcpApiKey)}
audio_path = ${JSON.stringify(audioPath)}

with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

url = (
    f"https://${cfg.gcpLocation}-aiplatform.googleapis.com/v1/"
    f"projects/${cfg.gcpProjectId}/locations/${cfg.gcpLocation}/"
    f"publishers/google/models/${cfg.gcpModel}:generateContent"
    f"?key={api_key}"
)

data = {
    "contents": [{
        "role": "user",
        "parts": [
            {"text": "Transcribe this audio accurately."},
            {"inline_data": {"mime_type": "audio/mpeg", "data": audio_b64}}
        ]
    }],
    "generationConfig": {"temperature": 0, "maxOutputTokens": 8192}
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode(),
    headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())
text = result["candidates"][0]["content"]["parts"][0]["text"]
print(text)
`;
  return await runPython(script);
}

// ── Gemini standard API transcription ─────────────────────────────────

/** Transcribe via Gemini standard API with inline audio */
async function transcribeGemini(
  audioPath: string,
  cfg: TranscribeConfig,
): Promise<string> {
  const script = `
import urllib.request
import json
import base64

api_key = ${JSON.stringify(cfg.googleApiKey)}
audio_path = ${JSON.stringify(audioPath)}

with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    f"models/${cfg.geminiStdModel}:generateContent?key={api_key}"
)

data = {
    "contents": [{
        "parts": [
            {"text": "Transcribe this audio accurately."},
            {"inline_data": {"mime_type": "audio/mpeg", "data": audio_b64}}
        ]
    }],
    "generationConfig": {"temperature": 0, "maxOutputTokens": 8192}
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode(),
    headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())
text = result["candidates"][0]["content"]["parts"][0]["text"]
print(text)
`;
  return await runPython(script);
}

// ── Public API ────────────────────────────────────────────────────────

/**
 * Transcribe audio file.
 * Fault-tolerant: tries Vertex AI first, falls back to Gemini.
 */
export async function transcribeAudio(
  audioPath: string,
  preferredBackend?: "gcp-vertex" | "gemini",
): Promise<TranscribeResult> {
  const cfg = loadConfig();
  validateConfig(cfg);

  // Determine backend order
  const backends: Array<"gcp-vertex" | "gemini"> = [];
  if (preferredBackend) {
    backends.push(preferredBackend);
  } else if (cfg.transcriber) {
    backends.push(cfg.transcriber);
  } else {
    // Auto failover chain: vertex first, then gemini
    if (cfg.gcpApiKey) backends.push("gcp-vertex");
    if (cfg.googleApiKey) backends.push("gemini");
  }

  if (backends.length === 0) {
    throw new Error("No transcription backend available");
  }

  const errors: string[] = [];

  for (const backend of backends) {
    try {
      if (backend === "gcp-vertex") {
        console.log(`[INFO] Trying GCP Vertex AI (${cfg.gcpModel})...`);
        const text = await transcribeVertex(audioPath, cfg);
        return { text, backend, model: cfg.gcpModel };
      } else {
        console.log(`[INFO] Trying Gemini API (${cfg.geminiStdModel})...`);
        const text = await transcribeGemini(audioPath, cfg);
        return { text, backend, model: cfg.geminiStdModel };
      }
    } catch (e: any) {
      console.warn(`[WARN] ${backend} failed: ${e.message.slice(0, 200)}`);
      errors.push(`${backend}: ${e.message}`);
    }
  }

  throw new Error(
    `All transcription backends failed:\n${errors.join("\n")}`,
  );
}
