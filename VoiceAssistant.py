import openai
import json
import requests
from elevenlabs import generate, play
import time
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

# Set up OpenAI API key
openai.api_key = "API KEY"

def generate_text(prompt):
    # Call OpenAI API to generate text based on the input prompt
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the generated text from the response
    generated_text = response.choices[0].text.strip()
    return generated_text

def record_speech(duration, sample_rate=16000):
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    return recording

def save_wav(audio_data, filename, sample_rate):
    sf.write(filename, audio_data, sample_rate)

def speech_to_text(audiofile):
    rec = sr.Recognizer()
    with sr.AudioFile(audiofile) as source:
        audio = rec.record(source)

    try:
        text = rec.recognize_google(audio)
    except sr.UnknownValueError:
        text = ""
    return text

# Run the script constantly until you close it
while True:
    # Record speech for 5 seconds
    record_duration = 5
    sample_rate = 16000
    audio_data = record_speech(record_duration, sample_rate)
    audiofile = "speech_recording.wav"
    save_wav(audio_data, audiofile, sample_rate)

    # Convert recorded speech to text
    input_text = speech_to_text(audiofile)
    print("Input Text: ", input_text)

    # Generate new text using OpenAI API
    generated_text = generate_text(input_text)

    print("Generated Text: ", generated_text)

    # Synthesize the generated text using Eleven Labs API
    audio = generate(
      text=generated_text,
      voice="Bella",
      model="eleven_monolingual_v1"
    )

    # Play the synthesized audio
    play(audio)

    # Add a delay of 1 second before recording speech again
    time.sleep(1)
