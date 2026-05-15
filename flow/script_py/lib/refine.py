"""
Markdown content refinement via unified Gemini client.

Backend chain:
  1. GCP Vertex AI (gemini-3.1-pro-preview) - primary
  2. Gemini Standard API (gemini-2.5-flash-lite) - fallback

Tasks:
  1. Text cleaning & restructuring
  2. Terminology & math correction (LaTeX)
  3. Key concept bolding
"""

from google.genai.types import GenerateContentConfig

from lib.gemini_client import generate_content

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


def refine_markdown(content: str) -> str:
    """
    Refine markdown content using Gemini.
    Fault-tolerant: Vertex AI -> Gemini fallback.
    """
    print(f"[INFO] Refining content ({len(content)} chars)...")

    text = generate_content(
        contents=REFINE_PROMPT + content,
        config=GenerateContentConfig(temperature=0.2, max_output_tokens=8192, top_p=0.95),
    )

    print(f"[INFO] Refined to {len(text)} chars")
    return text
