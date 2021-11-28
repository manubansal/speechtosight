#!/usr/bin/env python3

from speech_recognition import *

import os

class Recognizer(Recognizer):

    def build_decoder(self, language="en-US", keyword_entries=None, grammar=None):
            """
            Performs speech recognition on ``audio_data`` (an ``AudioData`` instance), using CMU Sphinx.
            The recognition language is determined by ``language``, an RFC5646 language tag like ``"en-US"`` or ``"en-GB"``, defaulting to US English. Out of the box, only ``en-US`` is supported. See `Notes on using `PocketSphinx <https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst>`__ for information about installing other languages. This document is also included under ``reference/pocketsphinx.rst``. The ``language`` parameter can also be a tuple of filesystem paths, of the form ``(acoustic_parameters_directory, language_model_file, phoneme_dictionary_file)`` - this allows you to load arbitrary Sphinx models.
            If specified, the keywords to search for are determined by ``keyword_entries``, an iterable of tuples of the form ``(keyword, sensitivity)``, where ``keyword`` is a phrase, and ``sensitivity`` is how sensitive to this phrase the recognizer should be, on a scale of 0 (very insensitive, more false negatives) to 1 (very sensitive, more false positives) inclusive. If not specified or ``None``, no keywords are used and Sphinx will simply transcribe whatever words it recognizes. Specifying ``keyword_entries`` is more accurate than just looking for those same keywords in non-keyword-based transcriptions, because Sphinx knows specifically what sounds to look for.
            Sphinx can also handle FSG or JSGF grammars. The parameter ``grammar`` expects a path to the grammar file. Note that if a JSGF grammar is passed, an FSG grammar will be created at the same location to speed up execution in the next run. If ``keyword_entries`` are passed, content of ``grammar`` will be ignored.
            Returns the most likely transcription if ``show_all`` is false (the default). Otherwise, returns the Sphinx ``pocketsphinx.pocketsphinx.Decoder`` object resulting from the recognition.
            Raises a ``speech_recognition.UnknownValueError`` exception if the speech is unintelligible. Raises a ``speech_recognition.RequestError`` exception if there are any issues with the Sphinx installation.
            """
            assert isinstance(language, str) or (isinstance(language, tuple) and len(language) == 3), "``language`` must be a string or 3-tuple of Sphinx data file paths of the form ``(acoustic_parameters, language_model, phoneme_dictionary)``"
            assert keyword_entries is None or all(isinstance(keyword, (type(""), type(u""))) and 0 <= sensitivity <= 1 for keyword, sensitivity in keyword_entries), "``keyword_entries`` must be ``None`` or a list of pairs of strings and numbers between 0 and 1"

            # import the PocketSphinx speech recognition module
            try:
                from pocketsphinx import pocketsphinx, Jsgf, FsgModel, get_model_path, get_data_path

            except ImportError:
                raise RequestError("missing PocketSphinx module: ensure that PocketSphinx is set up correctly.")
            except ValueError:
                raise RequestError("bad PocketSphinx installation; try reinstalling PocketSphinx version 0.0.9 or better.")
            if not hasattr(pocketsphinx, "Decoder") or not hasattr(pocketsphinx.Decoder, "default_config"):
                raise RequestError("outdated PocketSphinx installation; ensure you have PocketSphinx version 0.0.9 or better.")


            model_path = get_model_path()
            data_path = get_data_path()

            config_dict = {
                'hmm': os.path.join(model_path, 'en-us'),
                'lm': os.path.join(model_path, 'en-us.lm.bin'),
                'dict': os.path.join(model_path, 'cmudict-en-us.dict'),
                'allphone': os.path.join(model_path, 'en-us.lm.dmp'),
                'lw': 2.0,
                'beam': 1e-10,
                'pbeam': 1e-10
            }


            acoustic_parameters_directory, language_model_file, phoneme_dictionary_file = config_dict['hmm'], config_dict['lm'], config_dict['dict']
            if not os.path.isdir(acoustic_parameters_directory):
                raise RequestError("missing PocketSphinx language model parameters directory: \"{}\"".format(acoustic_parameters_directory))
            if not os.path.isfile(language_model_file):
                raise RequestError("missing PocketSphinx language model file: \"{}\"".format(language_model_file))
            if not os.path.isfile(phoneme_dictionary_file):
                raise RequestError("missing PocketSphinx phoneme dictionary file: \"{}\"".format(phoneme_dictionary_file))

            # create decoder object
            config = pocketsphinx.Decoder.default_config()
            config.set_string("-hmm", acoustic_parameters_directory)  # set the path of the hidden Markov model (HMM) parameter files
            config.set_string("-lm", language_model_file)
            config.set_string("-dict", phoneme_dictionary_file)
            config.set_string("-allphone", config_dict['allphone'])
            config.set_float("-lw", config_dict['lw'])
            config.set_float("-beam", config_dict['beam'])
            config.set_float("-pbeam", config_dict['pbeam'])
            config.set_string("-logfn", os.devnull)  # disable logging (logging causes unwanted output in terminal)
            decoder = pocketsphinx.Decoder(config)

            # obtain recognition results
            if keyword_entries is not None:  # explicitly specified set of keywords
                with PortableNamedTemporaryFile("w") as f:
                    # generate a keywords file - Sphinx documentation recommendeds sensitivities between 1e-50 and 1e-5
                    f.writelines("{} /1e{}/\n".format(keyword, 100 * sensitivity - 110) for keyword, sensitivity in keyword_entries)
                    f.flush()

                    # perform the speech recognition with the keywords file (this is inside the context manager so the file isn;t deleted until we're done)
                    decoder.set_kws("keywords", f.name)
                    decoder.set_search("keywords")
            elif grammar is not None:  # a path to a FSG or JSGF grammar
                if not os.path.exists(grammar):
                    raise ValueError("Grammar '{0}' does not exist.".format(grammar))
                grammar_path = os.path.abspath(os.path.dirname(grammar))
                grammar_name = os.path.splitext(os.path.basename(grammar))[0]
                fsg_path = "{0}/{1}.fsg".format(grammar_path, grammar_name)
                if not os.path.exists(fsg_path):  # create FSG grammar if not available
                    jsgf = Jsgf(grammar)
                    rule = jsgf.get_rule("{0}.{0}".format(grammar_name))
                    fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
                    fsg.writefile(fsg_path)
                else:
                    fsg = FsgModel(fsg_path, decoder.get_logmath(), 7.5)
                decoder.set_fsg(grammar_name, fsg)
                decoder.set_search(grammar_name)

            return decoder

