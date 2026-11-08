"""Local port of Modrinth's description checks (labrinth validate/project/description.rs, markdown.rs, text.rs):
long headers (> 80 characters), adjacent same-level headers, ending header, images without alt text, spam.
Usage: python3 mr_check.py FILE.md [...]  -> prints the nags each file would get."""
import re, sys, unicodedata
from collections import Counter

HTML_HEADER = re.compile(r'(?is)<h([1-6])\b[^>]*>(.*?)</h[1-6]>')
ADJ_HTML = re.compile(r'(?is)</h([1-6])>\s*<h([1-6])\b')
TRAIL_HTML = re.compile(r'(?is)</h[1-6]>\s*(?:</[a-z][^>]*>\s*)*$')
SPAM_TOKEN = re.compile(r"[\w]+(?:['_’.:+/-][\w]+)*", re.U)
MARKDOWN_LINK = re.compile(r'!?\[([^\]]*)\]\([^)]+\)')
MARKDOWN_IMAGE = re.compile(r'!\[([^\]]*)\]\([^)]+\)')
HTML_TAG = re.compile(r'(?is)<!--.*?-->|</?[a-z][^>]*>')
HTML_ENTITY = re.compile(r'&(?:#[0-9]+|#[xX][0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]+);')
INLINE_CODE = re.compile(r'`([^`]*)`')
HTML_IMAGE = re.compile(r'(?is)<img\b[^>]*>')
ALT = re.compile(r'''(?is)\balt\s*=\s*(?:"([^"]*)"|'([^']*)')''')
LINK = re.compile(r'(?:[a-zA-Z][a-zA-Z0-9+.-]*://|www\.)[^\s<>"]+')
FENCE = re.compile(r'(?ms)^(```|~~~).*?^\1[^\n]*$')

def without_code(md):
    return FENCE.sub(' ', md)

def md_headings(md):
    """ATX headings outside HTML blocks (good enough for our files): (level, text, start, end)."""
    out = []
    for m in re.finditer(r'(?m)^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$', md):
        out.append((len(m.group(1)), m.group(2), m.start(), m.end()))
    return out

def rendered_len(text):
    t = re.sub(r'<[^>]+>', '', text)
    t = re.sub(r'[*_`]', '', t)
    t = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', t)
    return len(t)

def long_headers(md):
    md = without_code(md)
    n = sum(1 for h in md_headings(md) if rendered_len(h[1]) > 80)
    n += sum(1 for m in HTML_HEADER.finditer(md) if rendered_len(m.group(2)) > 80)
    return n

def ends_with_header(md):
    md = without_code(md)
    hs = md_headings(md)
    if hs and not md[hs[-1][3]:].strip():
        return True
    return bool(TRAIL_HTML.search(md.rstrip()))

def adjacent_headers(md):
    md = without_code(md)
    hs = md_headings(md)
    for a, b in zip(hs, hs[1:]):
        if a[0] == b[0] and not md[a[3]:b[2]].strip():
            return True
    return any(m.group(1) == m.group(2) for m in ADJ_HTML.finditer(md))

def missing_alt(md):
    md = INLINE_CODE.sub('', without_code(md))
    if any(not m.group(1).strip() for m in MARKDOWN_IMAGE.finditer(md)):
        return True
    for img in HTML_IMAGE.finditer(md):
        a = ALT.search(img.group(0))
        if not a or not (a.group(1) or a.group(2) or '').strip():
            return True
    return False

def spam_blocks(md):
    t = INLINE_CODE.sub(r'\1', md)
    t = MARKDOWN_IMAGE.sub(' ', t)
    t = MARKDOWN_LINK.sub(r'\1', t)
    t = HTML_IMAGE.sub(' ', t)
    t = HTML_TAG.sub(' ', t)
    t = HTML_ENTITY.sub(' ', t)
    t = LINK.sub(' ', t)
    blocks, para = [], ''
    for line in t.splitlines():
        line = line.strip()
        if not line:
            if para: blocks.append(para); para = ''
            continue
        s = line.lstrip('>').lstrip()
        standalone = s.startswith('#') or any(s.startswith(p) for p in ('- ', '* ', '+ ', '•')) \
            or (('. ' in s) and s.split('. ', 1)[0].isdigit()) or '|' in s
        if standalone:
            if para: blocks.append(para); para = ''
            blocks.append(line)
        else:
            para = (para + ' ' + line) if para else line
    if para: blocks.append(para)
    return blocks

def words_of(b):
    return [unicodedata.normalize('NFC', w).lower() for w in SPAM_TOKEN.findall(b)]

def rep_words(w, k=6):
    r = 1
    for a, b in zip(w, w[1:]):
        r = r + 1 if a == b else 1
        if r >= k: return True
    return False

def rep_phrase(w, k=12):
    mx = min(8, len(w) // 3)
    for pw in range(mx, 1, -1):
        for s in range(0, len(w) - pw * 3 + 1):
            ph = w[s:s + pw]; r = 1
            while s + pw * (r + 1) <= len(w) and ph == w[s + pw * r:s + pw * (r + 1)]:
                r += 1
            if r >= 3 and pw * r >= k: return ' '.join(ph)
    return False

def ngram_density(w):
    if len(w) < 30: return False
    grams = [tuple(w[i:i + 4]) for i in range(len(w) - 3)]
    c = Counter(grams)
    dup = sum(v - 1 for v in c.values())
    if dup * 100 < len(grams) * 50: return False
    cov = [False] * len(w)
    for i, g in enumerate(grams):
        if c[g] > 1:
            for j in range(i, i + 4): cov[j] = True
    return sum(cov) * 100 >= len(w) * 70

def spam(md):
    md = without_code(md)
    counts = Counter(); vis = exc = longest = total = 0
    for b in spam_blocks(md):
        w = words_of(b)
        if not w: continue
        total += len(w)
        for word in w:
            vis += len(word); prev = None; run = 0
            for ch in word:
                if ch == prev: run += 1
                else:
                    exc += max(0, run - 3); longest = max(longest, run); prev = ch; run = 1
            exc += max(0, run - 3); longest = max(longest, run)
        if rep_words(w): return 'repeated words: ' + b[:80]
        p = rep_phrase(w)
        if p: return 'repeated phrase "%s" in: %s' % (p, b[:80])
        if ngram_density(w): return 'ngram density: ' + b[:80]
        s = b.lstrip('>').lstrip()
        if not s.startswith('#') and '|' not in s:
            counts[tuple(w)] += 1
    dupw = sum(len(k) * (v - 1) for k, v in counts.items() if v >= 3 and len(k) * v >= 12)
    if dupw > 0 and dupw * 100 >= total * 20:
        return 'duplicate blocks: ' + ' / '.join(' '.join(k)[:40] for k, v in counts.items() if v >= 3)
    if longest >= 64 or (longest >= 16 and exc >= 20 and exc * 100 >= vis * 10):
        return 'character runs'
    return False

def text_len(md):
    t = HTML_TAG.sub(' ', without_code(md)); t = HTML_ENTITY.sub(' ', t)
    return len(re.sub(r'\s+', ' ', t).strip())

def check(md):
    nags = []
    if long_headers(md): nags.append('long_headers %d' % long_headers(md))
    if adjacent_headers(md): nags.append('adjacent_headers')
    if ends_with_header(md): nags.append('ends_with_header')
    if missing_alt(md): nags.append('missing_alt_text')
    s = spam(md)
    if s: nags.append('spam (%s)' % s)
    if text_len(md) < 125: nags.append('too_short')
    return nags

if __name__ == '__main__':
    for f in sys.argv[1:]:
        print(f.split('/')[-1], check(open(f).read()) or 'OK')
