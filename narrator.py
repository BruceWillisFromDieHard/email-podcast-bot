import os
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
from dotenv import load_dotenv
from datetime import datetime

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

    # Combine summaries with category headers
    body = "\n\n".join([
        f"{summary['category'].upper()}:\n{summary['summary']}"
        for summary in summaries
    ])

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
            stream = client.text_to_speech.stream(
                text=chunk,
                voice=Voice(
                    voice_id="21m00Tcm4TlvDq8ikWAM",
                    settings=VoiceSettings(
                        stability=0.4,
                        similarity_boost=0.75,
                        style=0.5,
                        use_speaker_boost=True
                    )
                ),
                model_id="eleven_monolingual_v1"
            )
            for piece in stream:
                audio_output += piece
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
    return datetime.now().strftime("%A_%Y-%m-%d")
