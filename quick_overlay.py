# quick_overlay.py
"""
Quick Overlay Mode - MP4 Upload + Reddit Card Overlay
Used for Mode 3 only
"""

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from reddit_card import create_reddit_card
from PIL import Image
import os

def quick_overlay_mode(video_path, title, card_duration=7, output_path="final/final.mp4"):
    """
    Mode 3: Quick overlay mode - MP4 + Reddit Card only
    No TTS, no subtitles, no force alignment
    """
    print("="*60)
    print("🎬 Reels_maker - Quick Overlay Mode")
    print("="*60)
    print(f"📁 Video: {video_path}")
    print(f"📝 Title: {title}")
    print(f"⏱️  Card Duration: {card_duration} seconds")
    print("="*60)
    
    # Step 1: Generate Reddit card
    print("\n🎴 L1: Generating Reddit Card...")
    card_path = "reddit_card/card.png"
    create_reddit_card(
        title=title,
        subreddit="r/confession",
        upvotes="20K+",
        comments="100+",
        output_path=card_path
    )
    
    # Step 2: Overlay card on video (fade-out only, no fade-in)
    print("\n🎨 L2: Creating Overlay...")
    add_quick_overlay(
        video_path=video_path,
        card_image_path=card_path,
        output_path=output_path,
        duration=card_duration
    )
    
    print("\n" + "="*60)
    print(f"✅ DONE! Video saved at: {output_path}")
    print("="*60)

def add_quick_overlay(video_path, card_image_path, output_path, duration=7):
    """
    Add Reddit card overlay for Mode 3 (MP4 Upload)
    ✅ NO fade-in, ✅ YES fade-out only
    ✅ Card size: 340x160 pixels
    """
    print(f"🎴 Adding Reddit card overlay (Quick Mode)...")
    video_clip = VideoFileClip(video_path)
    video_width, video_height = video_clip.size
    
    # Load card image and resize to 340x160
    card_img = Image.open(card_image_path).convert('RGBA')
    card_img = card_img.resize((340, 160), Image.Resampling.LANCZOS)
    
    # Save resized card temporarily
    temp_card_path = "reddit_card/temp_resized_card.png"
    card_img.save(temp_card_path, 'PNG')
    
    # Create ImageClip from resized image
    card_clip = ImageClip(temp_card_path).set_duration(duration)
    
    # Center the card on video
    card_clip = card_clip.set_position('center')
    
    # ✅ NO fade-in, ✅ YES fade-out only
    if duration > 0:
        card_clip = card_clip.crossfadeout(0.5)
    
    # Composite: card on top of video
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
    
    # Remove temp file
    if os.path.exists(temp_card_path):
        os.remove(temp_card_path)
    
    print(f"✅ Card overlay added: {output_path}")
    return output_path