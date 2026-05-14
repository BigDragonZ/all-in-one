"""
Audio transcription via GCP Vertex AI and Gemini fallback.

Architecture:
  1. Try GCP Vertex AI first (project credits, recommended)
  2. Fallback to Gemini standard API if Vertex fails

Uses direct REST API calls to avoid google-genai client issues.
"""

import base64
import json
import urllib.request
from typing import Optional

from config.paths import BINARIES
from config.transcribe import TranscribeConfig, load_config

PROMPT = (
    "请仔细转写这段音频的内容。保持原文语言，添加标点，"
    "按语义分段，去除语气词和广告词，输出纯文本。"
)

PYTHON = BINARIES["python"]


def _build_vertex_script(audio_path: str, cfg: TranscribeConfig) -> str:
    return f'''
import urllib.request
import json
import base64

api_key = {json.dumps(cfg.gcp_api_key)}
audio_path = {json.dumps(audio_path)}

with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

url = (
    f"https://{cfg.gcp_location}-aiplatform.googleapis.com/v1/"
    f"projects/{cfg.gcp_project_id}/locations/{cfg.gcp_location}/"
    f"publishers/google/models/{cfg.gcp_model}:generateContent"
    f"?key={{api_key}}"
)

data = {{
    "contents": [{{
        "role": "user",
        "parts": [
            {{"text": "请仔细转写这段音频的内容。保持原文语言，添加标点，按语义分段，去除语气词和广告词，输出纯文本。"}},
            {{"inline_data": {{"mime_type": "audio/mpeg", "data": audio_b64}}}}
        ]
    }}],
    "generationConfig": {{"temperature": 0, "maxOutputTokens": 8192}}
}}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode(),
    headers={{"Content-Type": "application/json"}}
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())
text = result["candidates"][0]["content"]["parts"][0]["text"]
print(text)
'''


def _build_gemini_script(audio_path: str, cfg: TranscribeConfig) -> str:
    return f'''
import urllib.request
import json
import base64

api_key = {json.dumps(cfg.google_api_key)}
audio_path = {json.dumps(audio_path)}

with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    f"models/{cfg.gemini_std_model}:generateContent?key={{api_key}}"
)

data = {{
    "contents": [{{
        "parts": [
            {{"text": "请仔细转写这段音频的内容。保持原文语言，添加标点，按语义分段，去除语气词和广告词，输出纯文本。"}},
            {{"inline_data": {{"mime_type": "audio/mpeg", "data": audio_b64}}}}
        ]
    }}],
    "generationConfig": {{"temperature": 0, "maxOutputTokens": 8192}}
}}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode(),
    headers={{"Content-Type": "application/json"}}
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())
text = result["candidates"][0]["content"]["parts"][0]["text"]
print(text)
'''


def _run_python(script: str) -> str:
    """Run Python script via subprocess."""
    import subprocess
    result = subprocess.run(
        [PYTHON, "-c", script],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Python exited {result.returncode}: {result.stderr[:500]}")
    return result.stdout.strip()


def transcribe_audio(
    audio_path: str,
    preferred_backend: Optional[str] = None,
) -> dict[str, str]:
    """
    Transcribe audio file.
    Fault-tolerant: tries Vertex AI first, falls back to Gemini.
    """
    cfg = load_config()
    cfg.validate()

    # Determine backend order
    backends: list[str] = []
    if preferred_backend:
        backends.append(preferred_backend)
    elif cfg.transcriber:
        backends.append(cfg.transcriber)
    else:
        if cfg.gcp_api_key:
            backends.append("gcp-vertex")
        if cfg.google_api_key:
            backends.append("gemini")

    if not backends:
        raise RuntimeError("No transcription backend available")

    errors: list[str] = []

    for backend in backends:
        try:
            if backend == "gcp-vertex":
                print(f"[INFO] Trying GCP Vertex AI ({cfg.gcp_model})...")
                script = _build_vertex_script(audio_path, cfg)
                text = _run_python(script)
                return {"text": text, "backend": backend, "model": cfg.gcp_model}
            else:
                print(f"[INFO] Trying Gemini API ({cfg.gemini_std_model})...")
                script = _build_gemini_script(audio_path, cfg)
                text = _run_python(script)
                return {"text": text, "backend": backend, "model": cfg.gemini_std_model}
        except Exception as e:
            msg = f"{backend} failed: {str(e)[:200]}"
            print(f"[WARN] {msg}")
            errors.append(msg)

    raise RuntimeError(f"All transcription backends failed:\n" + "\n".join(errors))
