# video_generator.py
import subprocess
import os
import random
import json
from pathlib import Path
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

# ✅ GENERIC PATH - Users can change this in .env or config
GAMEPLAY_DIR = os.getenv('GAMEPLAY_DIR', 'reels/videos')

def get_available_videos():
    """Scan reels/videos directory for all available videos in subfolders"""
    videos = []
    gameplay_path = Path(GAMEPLAY_DIR)
    if not gameplay_path.exists():
        print(f"⚠️  Gameplay directory not found: {GAMEPLAY_DIR}")
        return videos
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    for folder in gameplay_path.iterdir():
        if folder.is_dir():
            for file in folder.iterdir():
                if file.suffix.lower() in video_extensions:
                    videos.append({
                        'folder': folder.name,
                        'file': file.name,
                        'path': str(file)
                    })
    return videos

def get_random_gameplay_video():
    """Select a random video from your reels/videos folder"""
    gameplay_path = Path(GAMEPLAY_DIR)
    if not gameplay_path.exists():
        print(f"⚠️  Gameplay directory not found: {GAMEPLAY_DIR}")
        print("Using default subway.mp4...")
        return 'assets/subway.mp4'
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    video_files = [
        f for f in gameplay_path.iterdir()
        if f.suffix.lower() in video_extensions
    ]
    if not video_files:
        print(f"⚠️  No video files found in {GAMEPLAY_DIR}")
        print("Using default subway.mp4...")
        return 'assets/subway.mp4'
    selected = random.choice(video_files)
    print(f"🎮 Using gameplay footage: {selected.name}")
    return str(selected)

def add_reddit_card_overlay(video_path, card_image_path, output_path, duration=5):
    """
    Add Reddit card overlay at the start of video with fade-in/out effects
    Used for Modes 1 & 2 (Full Pipeline)
    """
    print(f"🎴 Adding Reddit card overlay...")
    video_clip = VideoFileClip(video_path)
    card_clip = ImageClip(card_image_path).set_duration(duration)
    video_width, video_height = video_clip.size
    card_width, card_height = card_clip.size
    card_x = (video_width - card_width) // 2
    card_y = (video_height - card_height) // 2
    card_clip = card_clip.set_position((card_x, card_y))
    card_clip = card_clip.crossfadein(0.5).crossfadeout(0.5)
    final_clip = CompositeVideoClip([video_clip, card_clip], size=video_clip.size)
    final_clip.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        fps=video_clip.fps,
        preset='medium'
    )
    video_clip.close()
    final_clip.close()
    print(f"✅ Card overlay added: {output_path}")
    return output_path

def add_subtitles_and_overlay_audio(video_path, audio_path, subtitles_path, output_path):
    """
    Combine video, audio, and subtitles with professional styling for vertical video.
    Used for Modes 1 & 2 (Full Pipeline)
    """
    print("🎨 Combining video, audio, and subtitles...")
    probe_cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        audio_path
    ]
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    audio_info = json.loads(result.stdout)
    audio_duration = float(audio_info['format']['duration'])
    video_duration = audio_duration
    print(f"📊 Audio duration: {audio_duration:.2f} seconds")
    subtitle_style = (
        "FontSize=20,"
        "FontName=Arial Black,"
        "PrimaryColour=&H00FFFFFF,"
        "SecondaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,"
        "Bold=1,"
        "Outline=2,"
        "Shadow=2,"
        "Alignment=2,"
        "MarginV=100,"
        "MarginH=40,"
        "BorderStyle=1"
    )
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-i', audio_path,
        '-filter_complex',
        f"[0:v]subtitles={subtitles_path}:force_style='{subtitle_style}',scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(in_w-out_w)/2:(in_h-out_h)/2,fps=30[v];[1:a]aresample=44100[a]",
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        output_path
    ]
    try:
        print(f"🎬 Rendering: {output_path}")
        print(f"   Final Duration: {audio_duration:.2f} seconds (no time limit)")
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ Video rendered successfully!")
        print(f"📁 Output: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error:")
        print(f"   STDOUT: {e.stdout}")
        print(f"   STDERR: {e.stderr}")
        raise