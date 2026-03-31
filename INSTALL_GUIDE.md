📖 Detailed Installation Guide

# Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step-by-Step Installation](#step-by-step-installation)
3. [Model Download](#model-download)
4. [FFmpeg Installation](#ffmpeg-installation)
5. [Configuration](#configuration)
6. [First Run](#first-run)
7. [Troubleshooting](#troubleshooting)

---

# Prerequisites

Required Software

- Python 3.10 or higher
  - Download: https://www.python.org/downloads/
  - ✅ Check "Add Python to PATH" during installation

- Git (optional, for cloning)
  - Download: https://git-scm.com/downloads

- FFmpeg
  - Required for video processing
  - See installation steps below

-LLM: model
  - Go to https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF
  - Download Meta-Llama-3-8B-Instruct-Q4_K_M.gguf

Hardware Requirements

- RAM: 8GB minimum, 16GB recommended
- Storage: 10GB free space
- GPU: Optional (NVIDIA with 6GB+ VRAM for faster processing)

---

# Step-by-Step Installation

# Step 1: Install Python

1. Download Python 3.10+ from https://www.python.org/downloads/
2. Run installer
3. IMPORTANT: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   python --version
     Should show: Python 3.10.x or higher

# Step 2: Clone or Download Project

Option A:  Git Clone ->git clone https://github.com/Sassyemiko/Reels_maker.git
cd Reels_maker

Option B: Download ZIP-> Download the zip and extract in the folder whichever you want. 

# Step 3: Install Python Dependencies
pip install -r requirements.txt

if error came then do this:
Upgrade pip first
python -m pip install --upgrade pip

# Then install dependencies
pip install -r requirements.txt

# Step 4: Download LLM Model
The project uses Meta Llama-3-8B for local AI analysis.

Download Link:
Model: Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
Size: ~4.9GB
Format: GGUF (quantized)

Go to https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF
Download Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
Create folder: models/ in project root
Place model file in: models/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf

Verify:
# Check file exists
dir models\Meta-Llama-3-8B-Instruct-Q4_K_M.gguf

# Step 5: Install FFmpeg

1.Windows:

Download FFmpeg:

Go to https://www.gyan.dev/ffmpeg/builds/
Download "ffmpeg-release-essentials.zip"

Extract ZIP file:
# Example location after extraction:
C:\ffmpeg\bin\ffmpeg.exe

Add to PATH:
Open "Environment Variables" (search in Start menu)
Edit "Path" under "System variables"
Click "New"
Add: C:\ffmpeg\bin (or your extraction path)
Click "OK"

Verify:
ffmpeg -version

Linux (Ubuntu/Debian):
sudo apt update
sudo apt install ffmpeg

Linux (CentOS/RHEL):
sudo yum install epel-release
sudo yum install ffmpeg

Mac:
brew install ffmpeg

# Step 6: Configure Environment
1. Copy example file:
copy .env.example .env

2. Edit .env (optional):
Most settings work with defaults
Adjust REDDIT_VIDEOS_DIR if needed

# Step 7: Add Background Videos (Optional)
reels/
└── videos/
    ├── minecraft/
    │   ├── video1.mp4
    │   ├── video2.mp4
    │   └── video3.mp4
    └── gta/
        ├── gameplay1.mp4
        └── gameplay2.mp4

Supported formats: MP4, MOV, AVI, MKV
Recommended: Vertical videos (9:16 aspect ratio)

# Step 8: Run the server
python server.py

expected output
 * Serving Flask app 'server'
 * Debug mode: on
WARNING: This is a development server...
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 556-165-067

# Step 9. Testing face

1. Mode 3 (Fastest):

Select "MP4 Upload"
Upload any MP4 video
Enter title
Click "Generate Video"
Should complete in ~30 seconds

2. Mode 1 or 2:

Takes 3-5 minutes
First run downloads wav2vec2 model (~350MB)