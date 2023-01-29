import speech_recognition as sr
from gtts import gTTS
import os, time, winsound
from cab import book_a_cab

recognizer = sr.Recognizer()

saved_address_list={'home':"          ",
               'work':"               ",
               'friend': "            "}


audio = gTTS(text='listening now, please speak loud and clear', lang="en", slow=False)
audio.save("example.mp3")
os.system("start example.mp3")
time.sleep(5)

with sr.Microphone() as source:
    print("Adjusting noise ")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Recording for 5 seconds")
    recorded_audio = recognizer.listen(source, timeout=5)
    print("Done recording")

try:
    print("Recognizing the text")
    text = recognizer.recognize_google(
            recorded_audio, 
            language="en-US"
        )
    expected_command='book cab auto ola uber'
    res = any(i in expected_command.split(' ') for i in text.split(' '))
    if res:
        print('your ride home')
        book_a_cab()
        audio = gTTS(text='Your ride will arrive in twenty minutes to the current location', lang="en", slow=False)
        audio.save("example.mp3")
        os.system("start example.mp3")
    # call selenium here
    print("Decoded Text : {}".format(text))


except Exception as ex:

    print(ex)


sr.Microphone.list_microphone_names()