import speech_recognition as sr
from gtts import gTTS
import os, time

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
    audio = gTTS(text='listening now, please speak aloud, speak now', lang="en", slow=False)
    audio.save("example.mp3")
    os.system("start example.mp3")
    time.sleep(5)
    recorded_audio = recognizer.listen(source, timeout=4)
    print("Done recording")

try:
    print("Recognizing the text")
    text = recognizer.recognize_google(
            recorded_audio, 
            language="en-US"
        )
    expected_command='book cab auto ola uber'
    res = any(i in expected_command.split(' ') for i in text.split(' '))
    print('your ride home')
    # call selenium here
    print("Decoded Text : {}".format(text))

except Exception as ex:

    print(ex)
    audio = gTTS(text='audio unclear please try again', lang="en", slow=False)
    audio.save("example.mp3")
    os.system("start example.mp3")


sr.Microphone.list_microphone_names()



