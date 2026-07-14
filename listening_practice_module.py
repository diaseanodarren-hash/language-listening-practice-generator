"""
Language listening practice generator.

Uses a local Ollama LLM to write a short conversation in a target language,
then reads it aloud using edge-tts (free, high-quality neural voices from
Microsoft Edge) and plays the resulting audio.

Requirements:
    pip install ollama edge-tts pygame

You also need Ollama installed and running locally (https://ollama.com),
with the model you plan to use already pulled, e.g.:
    ollama pull llama3.1
"""

import asyncio
import ollama
import edge_tts
import pygame

# --- Placeholder: set this to whatever model you have pulled in Ollama ---
OLLAMA_MODEL = "qwen3:8b"  # e.g. "gemma3", "llama3.2", "qwen3", etc.

# Maps a language name (as you'd type it in the `language` parameter) to a
# good default edge-tts neural voice. Add more as needed — full list here:
# https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462
LANGUAGE_VOICE_MAP = {
    "mandarin": "zh-CN-XiaoxiaoNeural",
    "chinese": "zh-CN-XiaoxiaoNeural",
    "spanish": "es-ES-ElviraNeural",
    "french": "fr-FR-DeniseNeural",
    "japanese": "ja-JP-NanamiNeural",
    "german": "de-DE-KatjaNeural",
    "korean": "ko-KR-SunHiNeural",
    "italian": "it-IT-ElsaNeural",
    "english": "en-US-AriaNeural",
    "portuguese": "pt-BR-FranciscaNeural",
    "russian": "ru-RU-SvetlanaNeural",
    "indian": "gu-IN-NiranjanNeural",
    "indonesian": "id-ID-GadisNeural"
}


def _pick_voice(language: str, voice: str | None) -> str:
    """Resolve which edge-tts voice to use."""
    if voice:
        return voice
    key = language.strip().lower()
    if key in LANGUAGE_VOICE_MAP:
        return LANGUAGE_VOICE_MAP[key]
    raise ValueError(
        f"No default voice mapped for language '{language}'. "
        f"Pass an explicit `voice=` (e.g. 'zh-CN-XiaoxiaoNeural'). "
        f"See https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462 "
        f"for the full voice list."
    )


async def _synthesize_and_play(text: str, voice: str, out_file: str) -> None:
    """Generate speech audio with edge-tts, save it, then play it."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_file)

    pygame.mixer.init()
    pygame.mixer.music.load(out_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()


def generate_listening_practice(
    language: str,
    topic: str,
    length: str = "medium",
    extra_notes: str = "",
    voice: str | None = None,
    out_file: str = "listening_practice.mp3",
) -> str:
    """
    Generate a conversation in the target language for listening practice,
    convert it to speech with edge-tts, and play it aloud.

    Args:
        language: The language the conversation should be written/spoken in
                  (e.g. "Mandarin", "Spanish", "Japanese", "French").
        topic: The main subject of the conversation (e.g. "ordering food
               at a restaurant", "planning a weekend trip").
        length: Rough desired length of the conversation. Can be a
                descriptive term ("short", "medium", "long") or something
                more specific like "10 lines" or "2 minutes of dialogue".
        extra_notes: Any additional instructions for the AI, e.g.
                     "use formal speech", "include slang", "beginner level
                     vocabulary only", "include English translations after
                     each line".
        voice: Optional explicit edge-tts voice name (e.g.
               "zh-CN-YunxiNeural"). If omitted, a sensible default is
               chosen based on `language` via LANGUAGE_VOICE_MAP.
        out_file: Path to save the generated audio (.mp3).

    Returns:
        The generated conversation text (str), in case you want to display,
        log, or save it.
    """

    # 1. Build the prompt for the LLM
    system_prompt = (
        "You are a helpful language-learning assistant. You write natural, "
        "realistic conversations for listening practice. Only output the "
        "conversation itself (with speaker labels like 'A:' and 'B:'), and "
        "nothing else — no preamble, no explanations, no markdown, no repeating the same sentence in different writing (ie. chinese character then pinyin)."
    )

    user_prompt = (
        f"Write a conversation entirely in {language} for language "
        f"listening practice.\n"
        f"Topic: {topic}\n"
        f"Desired length: {length}\n"
    )

    if extra_notes:
        user_prompt += f"Extra instructions: {extra_notes}\n"

    # 2 & 3 & 4 & 5: language, topic, length, and extra_notes all feed into the prompt above.

    # Call the Ollama model
    print("generating text...")
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    conversation_text = response["message"]["content"].strip()

    print("----- Generated Conversation -----")
    print(conversation_text)
    print("-----------------------------------")

    # 6 & 7. Convert the generated text to speech with edge-tts, then play it
    resolved_voice = _pick_voice(language, voice)
    print("generating audio...")
    asyncio.run(_synthesize_and_play(conversation_text, resolved_voice, out_file))
    print("audio played!")

    return conversation_text


if __name__ == "__main__":
    # Example usage
    generate_listening_practice(
        language="mandarin",
        topic="ordering coffee at a cafe",
        length="short (about 6-8 lines)",
        extra_notes="Use beginner-friendly vocabulary, simple grammar and include an English translation after each line",
    )
