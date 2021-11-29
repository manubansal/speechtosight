#!/usr/bin/env python3                                                                                

import os
import pprint
import argparse

#import speech_recognition as sr    #built-in
import custom_speech_recognition as sr  #custom
from speech_recognition import AudioData
import pocketsphinx as px
from vizualization import Viz

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
      if hypothesis:
        hypstr = hypothesis.hypstr
        pprint.pprint(hypstr)
        #segments = [(s.word, s.start_frame, s.end_frame, s.prob, s.ascore, s.lscore, s.lback) for s in decoder.seg()]
        segments = [(s.word, s.start_frame, s.end_frame, s.ascore) for s in decoder.seg()]
        pprint.pprint(segments)
      else:
        print("could not decode any speech")

      return segments

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", "-t", help="run on test audio sample", action="store_true")
    args = parser.parse_args()
    try:
        if args.test:
            decoder = r.build_decoder()
            viz = Viz()
            decode_sample(decoder)
            phonemes = print_phonemes(decoder)
            viz.viz_phonemes(phonemes)

            return

        decoder = r.build_decoder()
        viz = Viz()
        decode_capture(decoder)
        phonemes = print_phonemes(decoder)
        viz.viz_phonemes(phonemes)

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

if __name__ == "__main__":
    main()
