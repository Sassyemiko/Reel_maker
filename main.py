# main.py
from scraping import *
from audio import *
from force_alignment import *
from dict import *
from video_generator import *
from search import *
from reddit_card import create_reddit_card
from llm_service import SentimentAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
from dotenv import load_dotenv

load_dotenv()

llm_analyzer = None
vader_analyzer = SentimentIntensityAnalyzer()

def analyze_with_vader(text):
    scores = vader_analyzer.polarity_scores(text)
    if scores['compound'] >= 0.05:
        sentiment = "positive"
    elif scores['compound'] <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return {
        'sentiment': sentiment,
        'scores': scores,
        'compound': scores['compound']
    }

def main(reddit_url=None, llm=False, mode='url', voice="en-US-JennyNeural",
         background_video=None, character='none',
         manual_title=None, manual_story=None,
         scraped_url='texts/scraped_url.txt',
         output_pre='texts/processed_output.txt',
         final_output='texts/oof.txt',
         speech_final='audio/output_converted.wav',
         subtitle_path='texts/testing.ass',
         output_path_before_overlay='final/before_overlay.mp4',
         output_path_before_card='final/before_card.mp4',
         output_path="final/final.mp4"):
    
    if not output_path.endswith('.mp4'):
        output_path = output_path + '.mp4'
    
    if background_video is None:
        video_path = get_random_gameplay_video()
        print(f"🎮 Using selected gameplay video: {video_path}")
    else:
        video_path = background_video
        print(f"🎮 Using selected gameplay video: {video_path}")
    
    print("="*60)
    print("🎬 Reels_maker - Offline Video Generator")
    print("="*60)
    print(f"⏱️  No Time Limit - Full audio duration will be used")
    print("="*60)
    
    map_request = {}
    post_title = ""
    subreddit = "r/confession"
    
    # STEP 1: CONTENT ACQUISITION
    print("\n📥 L1: CONTENT ACQUISITION")
    print("-" * 40)
    if mode == 'manual':
        print("✍️  Mode: Manual Story Input")
        if not manual_title or not manual_story:
            raise ValueError("Manual mode requires title and story")
        map_request = {
            'title': manual_title,
            'desc': manual_story,
            'score': 'N/A',
            'sentiment': 'neutral',
            'hook_potential': 'high'
        }
        post_title = manual_title
        os.makedirs(os.path.dirname(scraped_url), exist_ok=True)
        with open(scraped_url, 'w', encoding='utf-8') as f:
            f.write(f"TITLE: {manual_title}\n")
            f.write(f"CONTENT: {manual_story}\n")
        print(f"✅ Manual story saved to: {scraped_url}")
    else:
        print("🌐 Mode: Reddit URL Scraping")
        if not reddit_url:
            raise ValueError("URL mode requires a reddit_url")
        print("🤖 Using LOCAL LLM (Llama-3-8B) for thread analysis")
        try:
            global llm_analyzer
            if llm_analyzer is None:
                llm_analyzer = SentimentAnalyzer()
            scrape_result = scrape(reddit_url)
            reddit_title = scrape_result[0][0] if scrape_result else "Reddit Thread"
            reddit_content = scrape_result[0][1] if scrape_result else ""
            if '/r/' in reddit_url:
                subreddit = reddit_url.split('/r/')[1].split('/')[0]
            post_title = reddit_title
            print("\n🔍 Running VADER sentiment analysis...")
            vader_result = analyze_with_vader(reddit_content)
            print(f"VADER Sentiment: {vader_result['sentiment']} (compound: {vader_result['compound']:.3f})")
            print("\n🧠 Running LLM analysis...")
            map_request = llm_analyzer.analyze_thread(
                title=reddit_title,
                comments=reddit_content
            )
            print(f"\n✅ LLM Analysis Complete:")
            print(f"   Score: {map_request.get('score', 'N/A')}/10")
            print(f"   Sentiment: {map_request.get('sentiment', 'N/A')}")
            print(f"   Hook Potential: {map_request.get('hook_potential', 'N/A')}")
        except Exception as e:
            print(f"\n⚠️  LLM Analysis failed: {e}")
            scrape_result = scrape(reddit_url)
            reddit_content = scrape_result[0][1] if scrape_result else ""
            vader_result = analyze_with_vader(reddit_content)
            map_request = {
                'score': 7 if abs(vader_result['compound']) > 0.5 else 5,
                'sentiment': vader_result['sentiment'],
                'best_segment': reddit_content[:300],
                'reason': 'VADER fallback analysis',
                'hook_potential': 'high' if abs(vader_result['compound']) > 0.5 else 'medium',
                'title': scrape_result[0][0] if scrape_result else "Reddit Thread",
                'desc': reddit_content
            }
            if scrape_result:
                post_title = scrape_result[0][0]
            save_map_to_txt([map_request], scraped_url)
    
    print(f"\n📝 Content Preview:")
    print(f"   Title: {map_request.get('title', 'N/A')}")
    print(f"   Length: {len(map_request.get('desc', ''))} chars")
    print("-" * 40)
    
    # STEP 2: AUDIO GENERATION
    print("\n🎙️  L2: AUDIO CONVERSION (TTS)")
    print("-" * 40)
    print(f"🎤 Using Voice: {voice}")
    audio(scraped_url, speaker_wav=None, voice=voice)
    convert_audio('audio/output.wav', speech_final)
    print("✅ Audio generation complete!")
    
    # STEP 3: TEXT PRE-PROCESSING
    print("\n📝 L3: TEXT PRE-PROCESSING")
    print("-" * 40)
    process_text(scraped_url, output_pre)
    process_text_section2(output_pre, final_output)
    with open(final_output, 'r') as file:
        text = file.read().strip()
    
    # STEP 4: FORCED ALIGNMENT
    print("\n⏱️  L4: FORCE ALIGNMENT (Word-level timestamps)")
    print("-" * 40)
    transcript = format_text(text)
    bundle, waveform, labels, emission1 = class_label_prob(speech_final)
    trellis, emission, tokens = trellis_algo(labels, text, emission1)
    path = backtrack(trellis, emission, tokens)
    segments = merge_repeats(path, transcript)
    word_segments = merge_words(segments)
    timing_list = []
    for (i, word) in enumerate(word_segments):
        timing_list.append((display_segment(bundle, trellis, word_segments, waveform, i)))
    with open("testing.txt", "w") as file:
        for item in timing_list:
            word, start_time, end_time = item
            file.write(f"{word} {start_time} {end_time}\n")
    print(f"✅ Generated {len(timing_list)} word-level timestamps")
    
    # STEP 5: VIDEO GENERATION (with subtitles)
    print("\n🎬 L5: VIDEO GENERATION")
    print("-" * 40)
    convert_timing_to_ass(timing_list, subtitle_path)
    print(f"✅ Subtitles saved to: {subtitle_path}")
    print("🎥 Rendering video with subtitles and audio...")
    add_subtitles_and_overlay_audio(
        video_path, 
        speech_final, 
        subtitle_path, 
        output_path_before_overlay
    )
    print("✅ Base video rendered!")
    
    # STEP 6: REDDIT CARD OVERLAY
    print("\n🎴 L6: REDDIT CARD OVERLAY")
    print("-" * 40)
    card_path = "reddit_card/card.png"
    create_reddit_card(
        title=post_title,
        subreddit=subreddit,
        upvotes="20K+",
        comments="100+",
        output_path=card_path
    )
    add_reddit_card_overlay(
        output_path_before_overlay,
        card_path,
        output_path_before_card,
        duration=5
    )
    print("✅ Card overlay added!")
    
    # STEP 7: FINAL OUTPUT (Character overlay removed)
    print("\n🖼️  L7: FINAL OUTPUT")
    print("-" * 40)
    import shutil
    shutil.copy(output_path_before_card, output_path)
    
    print("\n" + "="*60)
    print(f"✅ DONE! Video saved at: {output_path}")
    print("="*60)

def quick_overlay_mode(video_path, title, card_duration=7, output_path="final/final.mp4"):
    """
    Mode 3: Quick overlay mode - MP4 + Reddit Card only
    No TTS, no subtitles, no force alignment, no character overlay
    """
    from video_generator import add_reddit_card_overlay_quick
    from reddit_card import create_reddit_card
    
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
    add_reddit_card_overlay_quick(
        video_path=video_path,
        card_image_path=card_path,
        output_path=output_path,
        duration=card_duration
    )
    
    print("\n" + "="*60)
    print(f"✅ DONE! Video saved at: {output_path}")
    print("="*60)

if __name__ == "__main__":
    test_url = "https://www.reddit.com/r/confessions/comments/1jt63ey/i_pooped_during_my_run_yesterday/"
    main(reddit_url=test_url, llm=True, mode='url', character='none')