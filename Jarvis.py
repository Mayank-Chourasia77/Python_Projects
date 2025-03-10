# pip install speechrecognition
#pip install setuptools , pip install webbrowser , install pyttsx3 (text to audio)
import speech_recognition as sr
import webbrowser
import pyttsx3
from pywin.tools.TraceCollector import outputWindow

import music
from openai import OpenAI

recognizer = sr.Recognizer()   # speech to text
engine = pyttsx3.init()                #tts engine active

def aiprocess(command) :
    client = OpenAI(api_key="your api key")

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user",
         "content":command }

    ]
)

    return(completion.choices[0].message.content);



def speak(text):
    engine.say(text)
    engine.runAndWait()


def processCommand(command):
    if command.lower() == "open youtube":
        webbrowser.open("https://youtube.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = music.music_album[song]
        webbrowser.open(link)
    else:
        output = aiprocess(command)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis..")
    while True:
        r = sr.Recognizer()   #obtain audio from microphone
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=5,phrase_time_limit=3)
            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Ya")
                #listen command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error:{0}".format(e))




