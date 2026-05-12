# flake8: noqa
# pylint: skip-file
# list of constants needed for KCC and feature generation
# consonant and independent vowels
KHCONST = set(u'កខគឃងចឆជឈញដឋឌឍណតថទធនបផពភមយរលវឝឞសហឡអឣឤឥឦឧឨឩឪឫឬឭឮឯឰឱឲឳ')
KHVOWEL = set(u'឴឵ាិីឹឺុូួើឿៀេែៃោៅ\u17c6\u17c7\u17c8')
# subscript, diacritics
KHSUB = set(u'្')
KHDIAC = set(u"\u17c9\u17ca\u17cb\u17cc\u17cd\u17ce\u17cf\u17d0") #MUUSIKATOAN, TRIISAP, BANTOC,ROBAT,
KHSYM = set('៕។៛ៗ៚៙៘')
KHNUMBER = set(u'០១២៣៤៥៦៧៨៩0123456789') # remove 0123456789
# lunar date:  U+19E0 to U+19FF ᧠...᧿
KHLUNAR = set('᧠᧡᧢᧣᧤᧥᧦᧧᧨᧩᧪᧫᧬᧭᧮᧯᧰᧱᧲᧳᧴᧵᧶᧷᧸᧹᧺᧻᧼᧽᧾᧿')
# English character and number
EN = set(u'abcdefghijklmnopqrstuvwxyz0123456789')

# if khmer character return True else return False
def is_khmer_char(ch):
  if (ch >= '\u1780') and (ch <= '\u17ff'): return True
  if ch in KHLUNAR: return True
  return False

# if character is part of KHCONST KHSYM KHNUMBER KHLUNAR or not khmer character then it will be starter of KCC (return true) else false
def is_start_of_kcc(ch):
  if is_khmer_char(ch):
    if ch in KHCONST: return True
    if ch in KHSYM: return True
    if ch in KHNUMBER: return True
    if ch in KHLUNAR: return True
    return False
  return True

# Segment the each word (var phr) to KCC form.
def seg_kcc(str_sentence):
    str_sentence = str_sentence.replace(u'\u200b','')
    segs = []
    cur = ""
    for phr in str_sentence.split(' '):
        #print("PHR:[%s] len:%d" %(phr, len(phr)))
        for i,c in enumerate(phr):
            cur += c  # continue add char until 
            nextchar = phr[i+1] if (i+1 < len(phr)) else ""
            
            # cluster non-khmer chars together
            if not is_khmer_char(c) and nextchar != "" and not is_khmer_char(nextchar): continue
            # cluster number together
            if c in KHNUMBER and nextchar in KHNUMBER: continue
            
            # cluster non-khmer together
            # non-khmer character has no cluster
            if not is_khmer_char(c) or nextchar=="":
                segs.append(cur)
                cur=""
            elif is_start_of_kcc(nextchar) and not (c in KHSUB):
                segs.append(cur)
                cur=""
    return segs
