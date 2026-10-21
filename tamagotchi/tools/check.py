"""Whisper-Pruefung: welche Skriptwoerter hat der Zuhoerer (Whisper) NICHT erkannt?"""
import re
from script import HEARD
DIG = {'1': 'one', '2': 'two', '10': 'ten', '20': 'twenty', '27': 'twentyseven', 'oars': 'ores'}


def norm(s):
    s = s.lower().replace('-', '').replace('twenty seven', 'twentyseven').replace("'s ", ' ').replace('\u2019s ', ' ')
    s = re.sub(r"\b(\w+)'s\b", r'\1', s)
    toks = re.sub(r"[^a-z0-9 ]", '', s).split()
    return [DIG.get(t, t) for t in toks]


def missing(want_text, heard_text):
    """-> (list of script words not heard, number of script words)"""
    want, got = norm(want_text.replace('*', '')), norm(heard_text)
    gs = set(got) | {a + b for a, b in zip(got, got[1:])}
    gs |= {a + b + c for a, b, c in zip(got, got[1:], got[2:])}
    out, skip = [], False
    for i, w in enumerate(want):
        if skip:
            skip = False
            continue
        if w in gs or any(a in gs for a in HEARD.get(w, [])):
            continue
        if i + 1 < len(want) and (w + want[i + 1]) in gs:     # "every one" heard as "everyone"
            skip = True
            continue
        out.append(w)
    return out, len(want)
