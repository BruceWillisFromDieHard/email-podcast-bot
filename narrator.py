import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from datetime import datetime

load_dotenv()

def get_today_string():
    return datetime.now().strftime("%A_%Y-%m-%d")

def create_audio(summaries):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise Exception("❌ ELEVENLABS_API_KEY not found in environment variables")

    client = ElevenLabs(api_key=api_key)

    intro = (
        "🎙️ Good morning, Mr President. Welcome to another day. "
        "Here’s what you need to know today, fresh out of the inbox."
    )
    outro = "☕ That’s your lot. Give em hell today chief."

    body = ""
    for summary in summaries:
        body += f"{summary['category'].capitalize()}:\n{summary['summary']}\n\n"

    full_script = f"{intro}\n\n{body.strip()}\n\n{outro}"

    chunk_size = 9500
    chunks = [
        full_script[i:i + chunk_size] for i in range(0, len(full_script), chunk_size)
    ]

    audio_output = b""
    for idx, chunk in enumerate(chunks):
        print(f"🎤 Generating chunk {idx + 1}/{len(chunks)}...")
        try:
            audio = b"".join(client.text_to_speech.convert(
                voice_id="b5Lt58PwhAQYisogJcn6egCE6",  # Mason Reed
                model_id="eleven_monolingual_v1",
                text=chunk
            ))
            audio_output += audio
        except Exception as e:
            print(f"❌ Error generating audio for chunk {idx + 1}: {e}")

    if audio_output:
        filename = f"daily_email_recap_{get_today_string()}.mp3"
        with open(filename, "wb") as f:
            f.write(audio_output)
        print(f"✅ Audio saved to {filename}")
        return filename
    else:
        raise Exception("❌ All audio generation attempts failed")