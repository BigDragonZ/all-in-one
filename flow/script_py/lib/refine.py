"""
Markdown content refinement via Gemini.

Tasks:
  1. Text cleaning & restructuring: remove filler words, add punctuation, segment by logic
  2. Terminology & math correction: fix finance/tech terms, rewrite math in LaTeX
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
   - 例如：$E[R] = R_f + \beta(E[R_m] - R_f)$
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


def _build_refine_script(content: str, api_key: str, model: str = "gemini-3.1-pro-preview") -> str:
    return f'''
import urllib.request
import json

api_key = {json.dumps(api_key)}
model = {json.dumps(model)}

url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    f"models/{{model}}:generateContent?key={{api_key}}"
)

system_prompt = {json.dumps(REFINE_PROMPT)}
content = {json.dumps(content)}

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


def refine_markdown(content: str, model: str = "gemini-2.5-pro") -> str:
    """
    Refine markdown content using Gemini.
    Returns cleaned, structured text with LaTeX math and bolded key terms.
    """
    cfg = load_config()
    
    # Prefer GEMINI_API_KEY for standard API; fallback to gcp-vertex-key
    api_key = cfg.google_api_key or cfg.gcp_api_key
    if not api_key:
        raise RuntimeError("No API key available for refinement")

    print(f"[INFO] Refining content ({len(content)} chars)...")
    script = _build_refine_script(content, api_key, model)
    refined = _run_python(script)
    print(f"[INFO] Refined to {len(refined)} chars")
    return refined
