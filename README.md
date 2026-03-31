🎬 Reels_maker

100% Offline AI-Powered Viral Video Generator

Transform Reddit stories into engaging short-form videos (TikTok/Reels/Shorts) - No APIs, No Cloud, 100% Local!

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Offline](https://img.shields.io/badge/Offline-100%25-brightgreen.svg)

---

✨ Features

🎯 Three Input Modes

| Mode | Description | Processing Time |
|------|-------------|-----------------|
| **Reddit URL** | Paste any Reddit thread URL → Auto-scrape → AI analysis → Video | ~3-5 minutes |
| **Manual Story** | Write your own title + story → Video | ~3-5 minutes |
| **MP4 Upload** | Upload your own video + Add Reddit card overlay | ~30-60 seconds ⚡ |

🚀 Key Features

- ✅ **100% Offline** - No external APIs, no internet required after setup
- ✅ **Local LLM** - Llama-3-8B for thread analysis (runs on your machine)
- ✅ **Local TTS** - Microsoft Edge TTS for voice generation
- ✅ **Word-Level Subtitles** - wav2vec2 force alignment for perfect timing
- ✅ **9 Voice Options** - Multiple US/UK/AU voices available
- ✅ **Background Videos** - Support for Minecraft, GTA, or any gameplay footage
- ✅ **Reddit Card Overlay** - Professional-looking Reddit post cards
- ✅ **No Time Limit** - Videos match audio duration (up to 5 min backgrounds)
- ✅ **Dark Theme UI** - Modern, clean web interface

---

📁 Project Structure

Reels_maker/
├── main.py                 # Main pipeline orchestration <br>
├── server.py               # Flask web server <br>
├── video_generator.py      # Video processing (Modes 1&2)<br>
├── quick_overlay.py        # MP4 overlay mode (Mode 3)<br>
├── reddit_card.py          # Reddit card generation<br>
├── audio.py                # TTS audio generation<br>
├── force_alignment.py      # Word-level timestamps (wav2vec2)<br>
├── dict.py                 # Text preprocessing<br>
├── scraping.py             # Reddit scraping<br>
├── llm_service.py          # Local LLM (Llama-3-8B)<br>
├── search.py               # Sentiment analysis (VADER)<br>
├── image_overlay.py        # Character overlay<br>
├── requirements.txt        # Python dependencies<br>
├── templates/<br>
│   └── web.html          # Web interface<br>
├── reddit_card/<br>
│   └── template.png       # Card template<br>
├── models/                 # LLM model (download separately)<br>
└── reels/<br>
    └── videos/            # Background videos<br>


👀 FAQ

Q: Do I need internet connection?
A: Only for initial setup (downloading model, dependencies). After that, works offline.

Q: Can I use my own voices?
A: Currently supports 9 Microsoft Edge TTS voices. Custom voices require code modification.

Q: How long does video generation take?
A: 3-5 minutes for full pipeline, 30-60 seconds for MP4 upload mode.

Q: Can I use this commercially?
A: Yes, MIT License allows commercial use.

Q: Is my data sent anywhere?
A: No, everything runs locally on your machine.


