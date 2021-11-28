#!/usr/bin/env python3                                                                                

import pprint

#built-in
#import speech_recognition as sr  

#custom
import custom_speech_recognition as sr
from speech_recognition import AudioData
import pocketsphinx as px
import os

# get audio from the microphone                                                                       
r = sr.Recognizer()                                                                                   

def decode_sample(decoder):
    print("Decoding sample:")
    # Decode streaming data
    buf = bytearray(1024)
    with open(os.path.join(px.get_data_path(), 'goforward.raw'), 'rb') as f:
        decoder.start_utt()
        while f.readinto(buf):
            decoder.process_raw(buf, False, False)
        decoder.end_utt()
    #print('Best hypothesis segments:', [seg.word for seg in decoder.s

def decode_capture(decoder):
    with sr.Microphone() as source:                                                                       
        print("Speak:")                                                                                   
        audio = r.listen(source)   

    assert isinstance(audio, AudioData), "``audio_data`` must be audio data"

    # obtain audio data
    raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)  # the included language models require audio to be 16-bit mono 16 kHz in little-endian format

    decoder.start_utt()  # begin utterance processing
    decoder.process_raw(raw_data, False, True)  # process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
    decoder.end_utt()  # stop utterance processing

def print_phonemes(decoder):
        hypothesis = decoder.hyp()
        hypstr = hypothesis.hypstr
        pprint.pprint(hypstr)
        segments = [(s.word, s.start_frame, s.end_frame) for s in decoder.seg()]
        pprint.pprint(segments)

def main():
    try:
        #print("You said " + r.recognize_google(audio))
        #pprint.pprint(r.recognize_google(audio, show_all=True))
        #print("You said " + r.recognize_sphinx(audio))
        #pprint.pprint(r2.recognize_sphinx(audio, show_all=True))
        #decoder = r.recognize_sphinx(audio, show_all=True)
        decoder = r.build_decoder()
        decode_sample(decoder)
        print_phonemes(decoder)

        decoder = r.build_decoder()
        decode_capture(decoder)
        print_phonemes(decoder)



    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

if __name__ == "__main__":
    main()
