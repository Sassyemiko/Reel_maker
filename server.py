# server.py
from flask import Flask, request, jsonify, render_template, send_from_directory
from main import main, quick_overlay_mode
import os
import werkzeug

app = Flask(__name__)

# ✅ GENERIC PATHS - Users can change these in .env
REDDIT_VIDEOS_DIR = os.getenv('REDDIT_VIDEOS_DIR', 'reels/videos')
FINAL_DIR = os.getenv('FINAL_DIR', 'final')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

# Available Microsoft Edge Voices (9 Options)
AVAILABLE_VOICES = [
    {"id": "en-US-JennyNeural", "name": "Jenny (US Female)"},
    {"id": "en-US-AriaNeural", "name": "Aria (US Female)"},
    {"id": "en-US-GuyNeural", "name": "Guy (US Male)"},
    {"id": "en-US-MichelleNeural", "name": "Michelle (US Female) - Clear, Expressive"},
    {"id": "en-US-EricNeural", "name": "Eric (US Male) - Natural Sounding"},
    {"id": "en-US-SteffanNeural", "name": "Steffan (US Male) - Young, Energetic"},
    {"id": "en-GB-SoniaNeural", "name": "Sonia (UK Female)"},
    {"id": "en-GB-RyanNeural", "name": "Ryan (UK Male)"},
    {"id": "en-AU-NatashaNeural", "name": "Natasha (AU Female)"}
]

# Available Characters (kept for future use)
AVAILABLE_CHARACTERS = [
    {"id": "none", "name": "None (No Overlay)"},
    {"id": "spongebob", "name": "Spongebob"},
    {"id": "trump", "name": "Trump"},
    {"id": "lebron", "name": "LeBron"},
    {"id": "griffin", "name": "Griffin"}
]

def get_available_backgrounds():
    """Scan reels/videos directory for available backgrounds"""
    backgrounds = []
    if os.path.exists(REDDIT_VIDEOS_DIR):
        for folder in os.listdir(REDDIT_VIDEOS_DIR):
            folder_path = os.path.join(REDDIT_VIDEOS_DIR, folder)
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith('.mp4'):
                        backgrounds.append({
                            "folder": folder,
                            "file": file,
                            "path": os.path.join(folder_path, file),
                            "name": f"{folder} - {file}"
                        })
    return backgrounds

@app.route('/')
def index():
    return render_template('web.html')

@app.route('/api/options', methods=['GET'])
def get_options():
    """Provide frontend with available options"""
    return jsonify({
        "voices": AVAILABLE_VOICES,
        "characters": AVAILABLE_CHARACTERS,
        "backgrounds": get_available_backgrounds()
    })

@app.route('/generate', methods=['POST'])
def generate():
    """Modes 1 & 2: Reddit URL or Manual Story"""
    print("Received request at /generate")
    try:
        data = request.get_json()
        print(f"🔍 DEBUG: mode={data.get('mode')}")
        mode = data.get('mode', 'url')
        voice = data.get('voice', 'en-US-JennyNeural')
        background = data.get('background', None)
        character = data.get('character', 'none')
        if mode == 'url':
            reddit_url = data.get('url')
            if not reddit_url:
                return jsonify({'error': 'Reddit URL is required for URL mode'}), 400
            print(f"🔗 Processing Reddit URL: {reddit_url}")
            main(
                reddit_url=reddit_url,
                llm=True,
                mode='url',
                voice=voice,
                background_video=background,
                character=character
            )
        elif mode == 'manual':
            title = data.get('title')
            story = data.get('story')
            if not title or not story:
                return jsonify({'error': 'Title and Story are required for Manual mode'}), 400
            print(f"✍️  Processing Manual Story: {title}")
            main(
                reddit_url=None,
                llm=False,
                mode='manual',
                manual_title=title,
                manual_story=story,
                voice=voice,
                background_video=background,
                character=character
            )
        else:
            return jsonify({'error': 'Invalid mode selected'}), 400
        video_filename = 'final.mp4'
        video_path = os.path.join(FINAL_DIR, video_filename)
        if os.path.exists(video_path):
            print("✅ Video generation successful")
            return jsonify({
                'success': True,
                'video_url': f'/final/{video_filename}',
                'message': 'Video generated successfully!'
            })
        else:
            print("❌ Video generation failed")
            return jsonify({'error': 'Video generation failed. Check server logs.'}), 500
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/generate-quick', methods=['POST'])
def generate_quick():
    """Mode 3: MP4 Upload + Reddit Card Overlay"""
    print("Received request at /generate-quick")
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not file.filename.endswith('.mp4'):
            return jsonify({'error': 'Only MP4 files allowed'}), 400
        upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(upload_path)
        print(f"✅ Uploaded: {upload_path}")
        title = request.form.get('title', 'Reddit Story')
        duration = request.form.get('duration', '7')
        try:
            duration = int(duration)
            if duration < 0 or duration > 10:
                duration = 7
        except:
            duration = 7
        print(f"📝 Title: {title}")
        print(f"⏱️  Card Duration: {duration} seconds")
        quick_overlay_mode(
            video_path=upload_path,
            title=title,
            card_duration=duration,
            output_path="final/final.mp4"
        )
        video_filename = 'final.mp4'
        video_path = os.path.join(FINAL_DIR, video_filename)
        if os.path.exists(video_path):
            print("✅ Quick overlay generation successful")
            return jsonify({
                'success': True,
                'video_url': f'/final/{video_filename}',
                'message': 'Video generated successfully!'
            })
        else:
            print("❌ Video generation failed")
            return jsonify({'error': 'Video generation failed. Check server logs.'}), 500
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/final/<path:filename>')
def serve_video(filename):
    return send_from_directory(FINAL_DIR, filename, mimetype='video/mp4')

if __name__ == "__main__":
    app.run(debug=True, port=5000)