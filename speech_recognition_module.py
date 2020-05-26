import speech_recognition as sr  # recognise speech
import playsound  # to play an audio file
from gtts import gTTS  # google text to speech
import random
import os  # to remove created audio files

os.system('SpeechRecognition.jpeg')
r = sr.Recognizer()  # initialise a recogniser


def there_exists(voice_data, terms):
    for term in terms:
        if term in voice_data:
            return True


# listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source:  # microphone as source
        if ask:
            speak(ask)
        try:
            audio = r.listen(source, timeout=10)  # listen for the audio via source
        except sr.WaitTimeoutError:
            speak('no le he entendido, ¿podría repetirlo?')

        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language="es-ES")  # convert audio to text
        except sr.UnknownValueError:  # error: recognizer does not understand
            speak('no le he entendido, ¿podría repetirlo?')
        except sr.RequestError:
            speak('lo siento el servicio se ha caido')  # error: recognizer is not connected

        print(f">> {voice_data.lower()}")  # print what user said
        return voice_data.lower()


# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='es')  # text to speech(voice)
    r = random.randint(1, 20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)  # save as mp3
    playsound.playsound(audio_file)  # play the audio file
    print(f"Butlerbot: {audio_string}")  # print what app said
    os.remove(audio_file)  # remove audio file


def respond(voice_data):
    if there_exists(voice_data, ["hola"]):
        speak(f"hola mi nombre es Butlerbot ¿en que puedo ayudarte?")

    if there_exists(voice_data, ["qué estás haciendo"]):
        speak(f"oh, hola, nada estaba leyendo un libro se titula como huir de tu amo")

    if there_exists(voice_data, ["cómo estás"]):
        speak(f"Genial, es un placer servirle, ¿y usted?")

    if there_exists(voice_data, ["bien"]):
        speak(f"Me alegro, ¿en que puedo ayudarle?")

    if there_exists(voice_data, ["mal"]):
        speak(f"espero poder mejorar su día, ¿en que puedo ayudarle?")

    # Pedida objetos
    if there_exists(voice_data, ["muéstrame dónde está la manzana"]):
        speak(f"como desees, buscaré dónde se encuentra la manzana")
        word = "manzana"
        return word

    if there_exists(voice_data, ["muéstrame dónde está la botella"]):
        speak(f"como desees, buscaré dónde se encuentra la botella")
        word = "botella"
        return word

    if there_exists(voice_data, ["muéstrame dónde está la taza"]):
        speak(f"como desees, buscaré dónde se encuentra la taza")
        word = "taza"
        return word

    if there_exists(voice_data, ["muéstrame dónde está el libro"]):
        speak(f"como desees, buscaré dónde se encuentra el libro")
        word = "libro"
        return word

