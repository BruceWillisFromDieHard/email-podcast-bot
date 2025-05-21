import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import math

load_dotenv()

def create_audio(summaries):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise Exception("❌ ELEVENLABS_API_KEY not found in environment variables")

    client = ElevenLabs(api_key=api_key)

    # Custom intro and outro
    intro = (
        "🎙️ Good morning, Mr President. Welcome to another day. "
        "Here’s what you need to know today, fresh out of the inbox."
    )

    outro = "☕ That’s your lot. Give em hell today chief."

    # Combine all summaries into one script with intro/outro
    body = "\n\n".join([f"{summary['summary']}" for summary in summaries])
    full_script = f"{intro}\n\n{body}\n\n{outro}"

    if len(full_script) > 10000:
        print("⚠️ Script too long, splitting into chunks...")
        chunk_size = 9500
        chunks = [
            full_script[i:i + chunk_size] for i in range(0, len(full_script), chunk_size)
        ]
    else:
        chunks = [full_script]

    audio_output = b""
    for idx, chunk in enumerate(chunks):
        print(f"🎤 Generating chunk {idx + 1}/{len(chunks)}...")
        try:
            audio = client.text_to_speech.convert(
                voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
                model_id="eleven_monolingual_v1",
                text=chunk
            )
            audio_output += audio
        except Exception as e:
            print(f"❌ Error generating audio for chunk {idx + 1}: {e}")
            continue

    if audio_output:
        filename = f"daily_email_recap_{get_today_string()}.mp3"
        with open(filename, "wb") as f:
            f.write(audio_output)
        print(f"✅ Audio saved to {filename}")
    else:
        raise Exception("❌ All audio generation attempts failed")

def get_today_string():
    from datetime import datetime
    return datetime.now().strftime("%A_%Y-%m-%d")