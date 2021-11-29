import pprint

phoneme_ylevel_vowels = {
  'aa': 1,

  'ah': 2,
  'ax': 3,
  'er': 4,
  'axr': 5,

  'iy': 6,
  'ih': 7,

  'ae': 8,
  'ey': 9,
  'eh': 10,

  'uw': 11,
  'uh': 12,

  'ao': 13,
  'ow': 14,

  'aw': 15,
  'ay': 16,
  'oy': 17
}

phoneme_ylevel_consonants = {
  'b': 1,

  'p': 2,

  'd': 3,
  'dh': 4,

  't': 5,
  'th': 6,

  'g': 7,
  'k': 8,
  'ng': 9,

  'v': 10,
  'f': 11,

  'z': 12,
  's': 13,

  'ch': 14,
  'jh': 15,
  
  'm': 16,
  'n': 17,

  'w': 18,

  'y': 19,

  'hh': 20,

  'r': 21,

  'l': 22,

  'zh': 23,
  'sh': 24
}

phoneme_ylevel_specials = {
  '+spn+': 1,
  '+nsn+': 2, 
  'sil'  : 3
}

#TOTAL_LEVELS = 46


class PhonemeMap:
  def __init__(self):
    keymap = {}
    num_vowels = len(phoneme_ylevel_vowels)
    num_consonants = len(phoneme_ylevel_consonants)
    num_specials = len(phoneme_ylevel_specials)
    assert num_vowels == 17
    assert num_consonants == 24
    assert num_specials == 3
    gap1 = 1
    gap2 = 1
    km_v = phoneme_ylevel_vowels
    km_c = {k: v + num_vowels + gap1 for k, v in phoneme_ylevel_consonants.items()} 
    km_s = {k: v + num_vowels + num_consonants + gap1 + gap2 for k, v in phoneme_ylevel_specials.items()} 
    km_g1 = dict([('.' + str(idx), idx) for idx in range(num_vowels + 1, num_vowels + 1 + gap1)])
    km_g2 = dict([('.' + str(idx), idx) for idx in range(num_vowels + 1 + gap1 + num_consonants, num_vowels + 1 + gap1 + num_consonants + gap2)])
    keymap = {**km_v, **km_g1, **km_c, **km_g2, **km_s}
    keymap = {k.upper(): v for k, v in keymap.items()}
    self.keymap = keymap
    pprint.pprint(keymap)

  def get_key_list(self):
    key_list = [t for t in self.keymap.items()]
    key_list.sort(key = lambda t: t[1])
    key_idxs = [v for k, v in key_list]
    key_ids = [k for k, v in key_list]
    return key_list, key_idxs, key_ids

