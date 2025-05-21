import os
from elevenlabs import generate, Voice, VoiceSettings, save
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def create_audio(summaries):
    from elevenlabs import set_api_key
    set_api_key(ELEVENLABS_API_KEY)

    script = "\n\n".join(
        [f"{summary['category']}: {summary['summary']}" for summary in summaries]
    )

    print("🎙️ Generating chunk 1/1...")

    audio = generate(
        text=script,
        voice=Voice(
            voice_id="Rachel",  # You can replace with a specific voice ID
            settings=VoiceSettings(stability=0.4, similarity_boost=0.85)
        ),
        model="eleven_monolingual_v1"
    )

    save(audio, "daily_email_recap.mp3")