#!/usr/bin/env python3                                                                                

import pprint

#built-in
#import speech_recognition as sr  

#custom
import custom_speech_recognition as sr

# get audio from the microphone                                                                       
r = sr.Recognizer()                                                                                   

with sr.Microphone() as source:                                                                       
    print("Speak:")                                                                                   
    audio = r.listen(source)   

try:
    #print("You said " + r.recognize_google(audio))
    #pprint.pprint(r.recognize_google(audio, show_all=True))
    #print("You said " + r.recognize_sphinx(audio))
    #pprint.pprint(r2.recognize_sphinx(audio, show_all=True))
    decoder = r.recognize_sphinx(audio, show_all=True)
    hypothesis = decoder.hyp()
    hypstr = hypothesis.hypstr
    pprint.pprint(hypstr)
    segments = [(s.word, s.start_frame, s.end_frame) for s in decoder.seg()]
    pprint.pprint(segments)

except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
