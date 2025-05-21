import os
from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError
from httpx import Timeout

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
    timeout=Timeout(60.0)
)

def create_audio(summaries):
    intro = (
        "🎙️ Good morning, Mr President. Welcome to another day. "
        "Here’s what you need to know today, fresh out of the inbox."
    )

    outro = (
        "☕ That’s your lot. Give 'em hell today, chief."
    )

    all_sections = [intro] + summaries + [outro]
    full_script = "\n\n".join(all_sections)

    # Character limit buffer to stay under ElevenLabs and time constraints
    max_characters = 8000  # Roughly aligns with a 10-minute podcast
    trimmed_script = full_script[:max_characters]

    # Split into ~2500-character chunks
    def split_script(text, limit=2500):
        chunks = []
        while len(text) > limit:
            split_at = text.rfind("\n", 0, limit)
            if split_at == -1:
                split_at = limit
            chunks.append(text[:split_at].strip())
            text = text[split_at:].strip()
        if text:
            chunks.append(text)
        return chunks

    text_chunks = split_script(trimmed_script)

    audio_parts = []
    for i, chunk in enumerate(text_chunks):
        print(f"🎤 Generating chunk {i + 1}/{len(text_chunks)}...")
        try:
            audio = client.generate(
                text=chunk,
                voice="Rachel",
                model="eleven_monolingual_v1"
            )
            audio_parts.append(b"".join(audio))
        except ApiError as e:
            print(f"❌ Error generating audio for chunk {i + 1}: {e}")
            continue

    if not audio_parts:
        raise Exception("❌ All audio generation attempts failed")

    with open("daily_email_recap.mp3", "wb") as f:
        for part in audio_parts:
            f.write(part)

    print("✅ Podcast audio saved as daily_email_recap.mp3")
