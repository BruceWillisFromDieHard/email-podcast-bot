import os
from dotenv import load_dotenv
from elevenlabs import Voice, VoiceSettings, generate
from datetime import datetime

load_dotenv()

def get_today_string():
    return datetime.now().strftime("%A_%Y-%m-%d")

def create_audio(summaries):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise Exception("❌ ELEVENLABS_API_KEY not found in environment variables")

    # Custom intro and outro
    intro = (
        "🎙️ Good morning, Mr President. Welcome to another day. "
        "Here’s what you need to know today, fresh out of the inbox."
    )

    outro = "☕ That’s your lot. Give em hell today chief."

    # Group summaries by tag with structure
    body = ""
    for item in summaries:
        body += f"{item['category'].capitalize()}:\n{item['summary']}\n\n"

    full_script = f"{intro}\n\n{body.strip()}\n\n{outro}"

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
            audio_chunk = generate(
                api_key=api_key,
                text=chunk,
                voice="Rachel",
                model="eleven_monolingual_v1",
                stream=False  # stream must be set to False when collecting all at once
            )
            audio_output += audio_chunk
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