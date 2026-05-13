**角色定位：** 你是一位精通 Google Cloud Platform (GCP) 和 Python 自动化开发的专家。请为我编写一个生产环境级别的音视频转录脚本。

**技术栈与鉴权要求：**

1. **SDK：** 使用最新版 `google-genai` (2026 接口) 及 `google-cloud-storage`。
    
2. **鉴权模式：** 采用 **API Key 方式**。初始化 Client 时必须声明 `vertexai=True`，以确保请求走 Vertex AI 通道并精准抵扣我账户中 **$2,351** 的赠金。
    
3. **核心参数：**
    
    - **Project ID:** `gen-lang-client-0385617544`
        
    - **Location:** `us-central1`
        
    - **Model ID:** `gemini-2.5-flash-lite`
        
    - **GCS Bucket:** `hermes_brain`
        

**脚本核心逻辑流：**

- **音频预处理：** 脚本需调用本地 `yt-dlp` 抓取视频音频流，并利用 `ffmpeg` 将其压制为 **64kbps** 的单声道 **mp3** 文件（以优化上传速度并节省云端存储空间）。
    
- **云端中转：** 自动将压制后的音频上传至 `gs://hermes_brain/`。
    
- **异步转录：**
    
    - 使用 `Part.from_uri` 引用 GCS 路径。
        
- **清理与入库：** 转录完成后，将结果保存至我的本地 Obsidian 目录，并**立即删除** GCS 存储桶中的临时音频文件以防止产生额外费用。
- **性能与健壮性：**

- **高并发支持：** 脚本需具备多线程或异步并发处理能力，充分利用 Tier 1 账号的 **300 RPM** 限额。
    
- **环境变量：** API Key 必须从环境变量 `GEMINI_API_KEY` 中动态读取。
    

请直接输出完整的、可直接运行的 Python 代码。