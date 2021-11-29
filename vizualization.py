import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pprint
import seaborn as sns
import phoneme_map as pm
from phoneme_map import LinearPhonemeMap
import abc
from abc import ABC

class Viz(ABC):
  @abc.abstractmethod
  def viz_phonemes(self, phonemes):
    pass


class VizSimple(Viz):
  def __init__(self):
    self.pm = LinearPhonemeMap()

  def phoneme_to_key(self, phonemes):
    n_phones = len(phonemes)
    _, min_frame, _, _ = phonemes[0]
    _, _, max_frame, _ = phonemes[-1]
    n_keys = max(self.pm.keymap.values())
    n_frames = max_frame - min_frame + 1
    keys = np.array(np.zeros([n_keys, n_frames]))
    for phone in phonemes:
      ph, start, end, ascore = phone
      key = self.pm.keymap[ph] - 1
      keys[key, start - min_frame:end - min_frame] = ascore
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


class VizChunked(VizSimple):
  def __init__(self):
    super().__init__()

  def viz_phonemes(self, phonemes):
        pprint.pprint(phonemes)
        phone_groups = pm.phoneme_list_to_groups(phonemes)
        pprint.pprint(phone_groups)

        n_groups = len(phone_groups)
        group_lengths = pm.phone_groups_to_group_lengths(phone_groups)
        pprint.pprint(group_lengths)

        VMIN = -500
        VMAX = 0

        fig, axs = plt.subplots(ncols=n_groups, figsize=(18,8), gridspec_kw=dict(width_ratios=group_lengths))

        key_list, key_idxs, key_ids = self.pm.get_key_list()
        for i, g in enumerate(phone_groups):
          keys = self.phoneme_to_key(g)
          if i == 0:
            sns.heatmap(keys, cbar=False, ax=axs[i], yticklabels=key_list, vmin=VMIN, vmax=VMAX)
          else:
            #sns.heatmap(keys, cbar=False, ax=axs[i], yticklabels=key_list, vmin=VMIN, vmax=VMAX)
            sns.heatmap(keys, cbar=False, ax=axs[i], yticklabels=range(1,len(key_list)+1), vmin=VMIN, vmax=VMAX)


        #fig.colorbar(axs[1].collections[0], cax=axs[2])

        fig.tight_layout()
        plt.show()


class VizBilinear(Viz):
  def __init__(self):
    pass

  def viz_phonemes(self, phonemes):
      pass
