import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

def create_audio(summaries):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise Exception("❌ ELEVENLABS_API_KEY not found in environment variables")

    client = ElevenLabs(api_key=api_key)

    script = "\n\n".join(
        [f"{summary['category']}: {summary['summary']}" for summary in summaries]
    )

    print("🎙️ Generating audio with ElevenLabs...")

    audio = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel (or replace with your chosen voice)
        model_id="eleven_monolingual_v1",
        text=script
    )

    output_path = "daily_email_recap.mp3"
    with open(output_path, "wb") as f:
        f.write(audio)

    print(f"✅ Audio saved to {output_path}")