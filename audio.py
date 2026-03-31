import edge_tts
import asyncio
import subprocess

def audio(text_file_path, file_path="audio/output.wav", speaker_wav=None, voice="en-US-JennyNeural"):
    """Generate speech using Microsoft Edge TTS (female voice)"""
    
    with open(text_file_path, 'r', encoding='utf-8') as file:
        text = file.read().strip()
    
    if len(text) > 2500:
        text = text[:2500]
    
    print(f"🎙️  Generating audio with voice: {voice}")
    
    async def generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(file_path)
    
    asyncio.run(generate())
    print(f"✅ Audio saved to: {file_path}")


def convert_audio(input_path, output_path):
    """Convert audio to 16kHz, 16-bit, mono for force alignment"""
    command = [
        'ffmpeg',
        '-y',
        '-i', input_path,
        '-ac', '1',
        '-ar', '16000',
        '-sample_fmt', 's16',
        '-c:a', 'pcm_s16le',
        '-af', 'volume=2.0',
        output_path
    ]
    subprocess.run(command, check=True)
    print("✅ AUDIO CONVERSION DONE!")