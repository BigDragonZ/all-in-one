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

REFINE_PROMPT = """你是一位专业的课程笔记编辑。请对以下课程转录文本进行优化，要求：

1. **去除口语化填充词**：
   - 删除"嗯"、"啊"、"那个"、"就是"、"对吧"、"那么"等无意义的填充词
   - 删除重复啰嗦的表达
   - 保持所有实质性内容，不要删减知识点

2. **修正识别错误**：
   - 修正金融/经济/技术术语的识别错误
   - 修正人名、地名、公司名
   - 修正数学公式和符号
   - 不要改变原文的术语选择，只修正明显的识别错误

3. **添加标点与分段**：
   - 在适当位置添加句号、逗号
   - 按语义逻辑分段（每段一个主题）
   - 保持原文的讲解顺序和结构

4. **关键术语加粗**：
   - 首次出现的重要概念加粗
   - 定义性语句中的核心词加粗
   - 不要过度加粗，保持阅读舒适度

5. **数学公式**：
   - 识别数学表达式，用 LaTeX 格式重写
   - 例如：$E[R] = R_f + \\beta(E[R_m] - R_f)$
   - 变量定义用 $...$ 包裹

6. **禁止行为**：
   - 不要提炼总结，不要省略原文内容
   - 不要改变原文的论证顺序
   - 不要添加原文没有的观点
   - 不要用自己的话重新表述，保持原文风格

7. **输出格式**：
   - 纯 Markdown 文本
   - 直接输出优化后的正文
   - 保留原文的标题层级结构

请优化以下内容：
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
