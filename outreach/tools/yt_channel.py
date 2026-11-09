"""Manual research aid: channel description (e-mail addresses masked) and the latest 12 videos with age, views, id.
Usage: python3 tools/yt_channel.py @handle ..."""
import json, re, sys, urllib.request
UA={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)','Accept-Language':'en-US,en;q=0.9'}
EM=re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60).read().decode('utf-8','replace')
def walk(o, key):
    if isinstance(o, dict):
        if key in o: yield o[key]
        for v in o.values(): yield from walk(v, key)
    elif isinstance(o, list):
        for v in o: yield from walk(v, key)
for h in sys.argv[1:]:
    html=get(f'https://www.youtube.com/{h}/about?hl=en&gl=US')
    desc=(re.search(r'"description":"(.*?)","',html) or [None,''])[1]
    desc=json.loads('"'+desc+'"') if desc else ''
    desc=EM.sub(lambda m: m.group(0)[0]+'***@'+m.group(0).split('@')[1], desc)
    print('=====',h); print(desc[:900])
    html=get(f'https://www.youtube.com/{h}/videos?hl=en&gl=US')
    m=re.search(r'var ytInitialData = (\{.*?\});</script>', html, re.S)
    d=json.loads(m.group(1)) if m else {}
    n=0
    for v in walk(d,'videoRenderer'):
        title=''.join(r.get('text','') for r in v.get('title',{}).get('runs',[]))
        print('  -', title[:90], '|', v.get('publishedTimeText',{}).get('simpleText',''), '|', v.get('viewCountText',{}).get('simpleText',''), '|', v.get('videoId'))
        n+=1
        if n>=12: break
    if n==0:
        for v in walk(d,'lockupViewModel'):
            t=v.get('metadata',{}).get('lockupMetadataViewModel',{})
            title=t.get('title',{}).get('content','')
            rows=[p.get('text',{}).get('content','') for r in t.get('metadata',{}).get('contentMetadataViewModel',{}).get('metadataRows',[]) for p in r.get('metadataParts',[])]
            print('  -', title[:90], '|', ' / '.join(rows), '|', v.get('contentId'))
            n+=1
            if n>=12: break
        if n==0:
            for v in walk(d,'richItemRenderer'):
                c=v.get('content',{})
                vr=c.get('videoRenderer') or {}
                title=''.join(r.get('text','') for r in vr.get('title',{}).get('runs',[]))
                print('  -', title[:90], '|', vr.get('publishedTimeText',{}).get('simpleText',''), '|', vr.get('viewCountText',{}).get('simpleText',''))
                n+=1
                if n>=12: break
