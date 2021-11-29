import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pprint
import seaborn as sns
import phoneme_map as pm
from phoneme_map import PhonemeMap


class Viz:
  def __init__(self):
    self.pm = PhonemeMap()

  def phoneme_to_key(self, phonemes):
    n_phones = len(phonemes)
    _, _, max_frame, _ = phonemes[-1]
    print(max_frame)
    n_keys = max(self.pm.keymap.values())
    n_frames = max_frame + 1
    keys = np.array(np.zeros([n_keys, n_frames]))
    for phone in phonemes:
      ph, start, end, ascore = phone
      key = self.pm.keymap[ph] - 1
      keys[key, start:end] = ascore
    pprint.pprint(keys)
    pprint.pprint('n_keys:' + str(n_keys))
    return keys

  def viz_phonemes(self, phonemes):
        pprint.pprint(phonemes)
        keys = self.phoneme_to_key(phonemes)
        key_list, key_idxs, key_ids = self.pm.get_key_list()

        sns.set(rc = {'figure.figsize':(15,8)})
        sns.heatmap(keys, yticklabels=key_list, linewidths=1, linecolor='silver')
        plt.show()
