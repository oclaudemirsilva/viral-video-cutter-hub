# 🚀 Viral Video Cutter Hub

Transform long videos into high-impact viral content for TikTok, Reels, and Shorts using AI-driven automation.

![Project Preview](file:///C:/Users/ClaudemirNotebook/.gemini/antigravity/brain/b6f37022-015c-4a90-a43d-7b7fe6dc87ed/media__1774449205271.png)

## ✨ Key Features

-   **🧠 Smart Viral Segmentation**: Uses Gemini/GPT-4 to analyze transcripts and identify high-retention moments.
-   **🎭 Active Speaker Detection**: Automatically crops video to 9:16 and focuses on the speaker's face.
-   **🎙️ AI Hooks**: Generates narrated introductions (TTS) with high-converting titles automatically overlayed.
-   **🎨 Style Hub (IA B-Roll)**: Matches transcript segments with AI-generated images to create dynamic B-roll coverage.
-   **🏷️ SEO Export**: Generates titles, descriptions, and metadata optimized for social media growth.
-   **🛡️ Branding**: Support for dynamic watermarks with custom opacity and positioning.
-   **☁️ Colab Ready**: Seamless integration with Google Drive for high-speed cloud processing.

## 🛠️ Tech Stack

-   **Backend**: Python, FFmpeg, MoviePy
-   **IA Models**: WhisperX (Transcription), MediaPipe (Face Tracking), Edge-TTS, Gemini/OpenAI (Logics)
-   **UI**: Gradio Web Interface

## 🚀 Quick Start

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/oclaudemirsilva/viral-video-cutter-hub.git
    cd viral-video-cutter-hub
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Web UI**:
    ```bash
    python webui/app.py
    ```

---

## 📂 Project Structure

-   `webui/`: Gradio application and UI components.
-   `style_hub/`: Style references and B-roll generation engine.
-   `utils/`: Core utilities for hooks, watermarks, and video processing.
-   `scripts/`: Logic for transcription, cutting, and AI analysis.

---
Developed with ❤️ by [Claudemir Silva](https://github.com/oclaudemirsilva)
