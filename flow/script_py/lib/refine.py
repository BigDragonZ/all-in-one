"""
Markdown content refinement via Gemini.

Fault-tolerant chain:
  1. GCP Vertex AI (gemini-2.5-pro) - project credits
  2. Gemini Standard API (gemini-2.5-flash-lite) - fallback

Tasks:
  1. Text cleaning & restructuring
  2. Terminology & math correction (LaTeX)
  3. Key concept bolding
"""

import json
import urllib.request
from typing import Optional

from config.paths import BINARIES
from config.transcribe import load_config

PYTHON = BINARIES["python"]

REFINE_PROMPT = """你是一位专业的学术编辑。请对以下文本进行精修，要求：

1. **文本清洗与重构**：
   - 去除口语化填充词（"嗯"、"啊"、"那个"、"就是"等）
   - 添加准确的标点符号
   - 按逻辑语义分段，每段一个核心观点
   - 保持原文的学术深度和论证结构

2. **术语与数理修正**：
   - 精准识别金融/经济/技术术语，确保使用标准译法
   - 识别所有数学推导和公式，使用标准 LaTeX 格式重写
   - 例如：$E[R] = R_f + \\beta(E[R_m] - R_f)$
   - 变量定义使用 $...$ 包裹

3. **关键加粗**：
   - 核心概念、定义、结论使用 **加粗**
   - 重要术语首次出现时加粗
   - 不要过度加粗，保持阅读舒适度

4. **输出格式**：
   - 纯 Markdown 文本
   - 不要添加元信息或解释
   - 直接输出精修后的正文

请精修以下内容：
"""


def _build_vertex_script(content: str, cfg) -> str:
    """Build Python script for Vertex AI REST API call."""
    return f'''
import urllib.request
import json

api_key = {json.dumps(cfg.gcp_api_key)}
audio_path = {json.dumps(content)}

url = (
    f"https://{cfg.gcp_location}-aiplatform.googleapis.com/v1/"
    f"projects/{cfg.gcp_project_id}/locations/{cfg.gcp_location}/"
    f"publishers/google/models/{cfg.gcp_model}:generateContent"
    f"?key={{api_key}}"
)

system_prompt = {json.dumps(REFINE_PROMPT)}

data = {{
    "contents": [{{
        "role": "user",
        "parts": [
            {{"text": system_prompt + audio_path}}
        ]
    }}],
    "generationConfig": {{
        "temperature": 0.2,
        "maxOutputTokens": 8192,
        "topP": 0.95
    }}
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


def _build_gemini_script(content: str, cfg) -> str:
    """Build Python script for Gemini Standard API REST call."""
    return f'''
import urllib.request
import json

api_key = {json.dumps(cfg.google_api_key)}
content = {json.dumps(content)}

url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    f"models/{cfg.gemini_std_model}:generateContent?key={{api_key}}"
)

system_prompt = {json.dumps(REFINE_PROMPT)}

data = {{
    "contents": [{{
        "parts": [
            {{"text": system_prompt + content}}
        ]
    }}],
    "generationConfig": {{
        "temperature": 0.2,
        "maxOutputTokens": 8192,
        "topP": 0.95
    }}
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


def refine_markdown(content: str) -> str:
    """
    Refine markdown content using Gemini.
    Fault-tolerant: Vertex AI (gemini-2.5-pro) -> Gemini API (gemini-2.5-flash-lite).
    """
    cfg = load_config()

    # Determine backend order
    backends: list[str] = []
    if cfg.gcp_api_key:
        backends.append("gcp-vertex")
    if cfg.google_api_key:
        backends.append("gemini")

    if not backends:
        raise RuntimeError(
            "No API key available for refinement. "
            "Set gcp-vertex-key or GEMINI_API_KEY environment variable."
        )

    errors: list[str] = []

    for backend in backends:
        try:
            if backend == "gcp-vertex":
                print(f"[INFO] Trying GCP Vertex AI ({cfg.gcp_model})...")
                script = _build_vertex_script(content, cfg)
                refined = _run_python(script)
                print(f"[INFO] Refined to {len(refined)} chars")
                return refined
            else:
                print(f"[INFO] Trying Gemini API ({cfg.gemini_std_model})...")
                script = _build_gemini_script(content, cfg)
                refined = _run_python(script)
                print(f"[INFO] Refined to {len(refined)} chars")
                return refined
        except Exception as e:
            msg = f"{backend} failed: {str(e)[:200]}"
            print(f"[WARN] {msg}")
            errors.append(msg)

    raise RuntimeError(f"All refinement backends failed:\n" + "\n".join(errors))
