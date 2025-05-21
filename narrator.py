import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

def create_audio(summaries):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise Exception("❌ ELEVENLABS_API_KEY not found in environment variables")

    client = ElevenLabs(api_key=api_key)

    if not summaries:
        raise Exception("❌ No summaries provided to generate audio.")

    # Handle case where summaries might be strings instead of dicts
    if isinstance(summaries[0], str):
        script = "\n\n".join(summaries)
    elif isinstance(summaries[0], dict):
        # Expected structure: [{ "category": "...", "summary": "..." }, ...]
        script = "\n\n".join(
            [f"{s.get('category', 'General')}: {s.get('summary', '')}" for s in summaries]
        )
    else:
        raise Exception("❌ Unexpected summary structure.")

    print("🎙️ Generating audio with ElevenLabs...")

    try:
        audio = client.text_to_speech.convert(
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel (or replace with your chosen voice)
            model_id="eleven_monolingual_v1",
            text=script
        )
    except Exception as e:
        raise Exception(f"❌ Failed to generate audio: {str(e)}")

    output_path = "daily_email_recap.mp3"
    with open(output_path, "wb") as f:
        f.write(audio)

    print(f"✅ Audio saved to {output_path}")