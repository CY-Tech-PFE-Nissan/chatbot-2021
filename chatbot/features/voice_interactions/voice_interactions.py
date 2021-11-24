import os
import speech_recognition as sr
from pathlib import Path
from gtts import gTTS
import re


UPLOAD_FOLDER = Path(__file__).resolve().parent.parent.parent.parent
UPLOAD_FOLDER = UPLOAD_FOLDER / "static" / "uploads" / "audios"


def get_text_from_audio(path: str) -> str:
    """Converts file audio content to string data

    Parameter
    ---------
    path: str
    """
    r = sr.Recognizer()
    query = sr.AudioFile(path)
    with query as source:
        audio = r.record(source)

    output = r.recognize_google(audio, show_all=False)
    print(output)
    return output


def get_audio_from_text(text: str, filename: str) -> None:
    """Creates an audio file based on text
    filename has to have the .mp3 extension

    Parameter
    ---------
    text: str
    filename: str
    """
    text = "".join(re.split("<[^>]*>", text))
    tts = gTTS(text=text, lang="en")
    tts.save(filename)


def remove_audios():
    """Cleans the audio folder to prevent bugs"""
    for filename in os.listdir(UPLOAD_FOLDER):
        os.remove(str(UPLOAD_FOLDER / filename))
