import pprint

phoneme_vowels = {
  'aa',
  'ah',
  'ax',
  'er',
  'axr',
  'ay',
  'iy',
  'ih',
  'ae',
  'ey',
  'eh',
  'oy',
  'aw',
  'uw',
  'uh',
  'ao',
  'ow'
}

phoneme_consonants = {
  'b',
  'p',
  'd',
  'dh',
  't',
  'th',
  'g',
  'k',
  'ng',
  'v',
  'f',
  'z',
  's',
  'ch',
  'jh',
  'm',
  'n',
  'w',
  'y',
  'hh',
  'r',
  'l',
  'zh',
  'sh'
}

phoneme_specials = {
  '+spn+',
  '+nsn+',
  'sil'
}

def is_consonant(phone):
  return phone.lower() in phoneme_consonants


'''this method translates a phoneme list like [(ph1, start, end, ...), (ph2,
start, end, ...), ...] to a list of lists where each element in the outer
list is a phoneme group where the first phoneme in the group is a consonant.
so it will look like [[(ph1,..),(ph2,..)], [(ph3,...),(ph4,...)], ...] where
ph1 is a consonant and ph2 is a vowel, ph3 is a consonant and the rest of the
phones in the group are all vowels, and so on.'''
def phoneme_list_to_groups(phonemes):
  if len(phonemes) == 0:
    return []
  g = [phonemes[0]]
  if len(phonemes) == 1:
    return [g]
  r = []
  for t in phonemes[1:]:
    p = t[0]
    print(p, is_consonant(p))
    if not is_consonant(p):
      g.append(t)
      continue
    else:
      r.append(g)
      g = [t]
  if g:
    r.append(g)
  return r


def phone_groups_to_group_lengths(phone_groups):
  lengths = []
  for g in phone_groups:
    start = g[0][1]
    end = g[-1][2]
    lengths.append(end - start + 1)
  return lengths

class BilinearPhonemeMap:
  phoneme_ylevels = {
    'b'    : 1,     'aa' : 1,
    '.2'   : 2,
    'p'    : 3,
    '.4'   : 4,
    'd'    : 5,
    'dh'   : 6,     'ah' : 6,
    '.7'   : 7,     'ax' : 7,
    't'    : 8,     'er' : 8,
    'th'   : 9,     'axr': 9,
    '.10'  : 10,
    'g'    : 11,
    'k'    : 12,
    'ng'   : 13,
    '.14'  : 14,    'ay' : 14,
    'v'    : 15,    'iy' : 15,
    'f'    : 16,    'ih' : 16,
    '.17'  : 17,
    'z'    : 18,
    's'    : 19,
    '.20'  : 20,
    'ch'   : 21,    'ae' : 21,
    'jh'   : 22,    'ey' : 22,
    '.23'  : 23,    'eh' : 23,
    'm'    : 24,    'oy' : 24,
    'n'    : 25,
    '.26'  : 26,
    'w'    : 27,
    '.28'  : 28,
    'y'    : 29,    'aw': 29,
    '.30'  : 30,    'uw': 30,
    'hh'   : 31,    'uh': 31,
    '.32'  : 32,
    'r'    : 33,
    '.34'  : 34,
    'l'    : 35,
    'zh'   : 36,    'ao': 36,
    'sh'   : 37,    'ow': 37,
    '.38'  : 38,
    '+spn+': 39,
    '+nsn+': 40,
    'sil'  : 41
  }

class LinearPhonemeMap:
  phoneme_ylevel_vowels = {
    'aa': 1,

    'ah': 2,
    'ax': 3,
    'er': 4,
    'axr': 5,

    'ay': 6,
    'iy': 7,
    'ih': 8,

    'ae': 9,
    'ey': 10,
    'eh': 11,
    'oy': 12,

    'aw': 13,
    'uw': 14,
    'uh': 15,

    'ao': 16,
    'ow': 17
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

  def __init__(self):
    keymap = {}
    num_vowels = len(self.phoneme_ylevel_vowels)
    num_consonants = len(self.phoneme_ylevel_consonants)
    num_specials = len(self.phoneme_ylevel_specials)
    assert num_vowels == 17
    assert num_consonants == 24
    assert num_specials == 3
    gap1 = 1
    gap2 = 1
    km_v = self.phoneme_ylevel_vowels
    km_c = {k: v + num_vowels + gap1 for k, v in self.phoneme_ylevel_consonants.items()} 
    km_s = {k: v + num_vowels + num_consonants + gap1 + gap2 for k, v in self.phoneme_ylevel_specials.items()} 
    km_g1 = dict([('.' + str(idx), idx) for idx in range(num_vowels + 1, num_vowels + 1 + gap1)])
    km_g2 = dict([('.' + str(idx), idx) for idx in range(num_vowels + 1 + gap1 + num_consonants, num_vowels + 1 + gap1 + num_consonants + gap2)])
    keymap = {**km_v, **km_g1, **km_c, **km_g2, **km_s}
    keymap = {k.upper(): v for k, v in keymap.items()}
    self.keymap = keymap
    pprint.pprint(keymap)

    self.key_list = [t for t in self.keymap.items()]
    self.key_list.sort(key = lambda t: t[1])
    self.key_idxs = [v for k, v in self.key_list]
    self.key_ids = [k for k, v in self.key_list]

  def get_key_list(self):
    return self.key_list, self.key_idxs, self.key_ids

