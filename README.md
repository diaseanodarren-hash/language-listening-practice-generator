# language-listening-practice-generator
Generates conversation in any language using local ollama LLM which is then played using pygame tts

### Photos & Demos


## How it works
- Prompting -- a set prompt is given to the Ollama LLM with placeholders for variables such as language, topic of text, leght and any extra notes that are then inserted into the chat logs that the LLM recieves
- Text Generation -- The local ollama model generates text in the language selected based on the prompt given
- TTS -- The generated text is then sent to Microsoft's Edge neural voice server via the edge TTS library which then returns a .mp3 audio file
- The audio file is played using pygame's audio system

## What I used & Dependencies
- Ollama and an ollama model (ollama pull (any ollama model))
- edge-tts which converts generated text into audio
- pygame plays the resulting audio file

to download dependencies, run this in terminal:
```bash
pip install ollama edge-tts pygame
```


