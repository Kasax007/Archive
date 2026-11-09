"""Manual research aid: YouTube search (public results page, videos uploaded this month) -> channel handle, title, age,
views. Low volume only (a handful of terms per run). Usage: python3 tools/yt_search.py "term" ["term" ...]
Writes yt_results.json into the current directory (run it from a scratch dir, not the repo)."""
import json, re, sys, urllib.request, urllib.parse
UA={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)','Accept-Language':'en-US,en;q=0.9'}
def initial_data(url):
    html=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60).read().decode('utf-8','replace')
    m=re.search(r'var ytInitialData = (\{.*?\});</script>', html, re.S)
    return json.loads(m.group(1)) if m else None
def walk(o, key):
    if isinstance(o, dict):
        if key in o: yield o[key]
        for v in o.values(): yield from walk(v, key)
    elif isinstance(o, list):
        for v in o: yield from walk(v, key)
out={}
for term in sys.argv[1:]:
    # sp=EgQIBBAB: upload date this month, type video
    url='https://www.youtube.com/results?search_query='+urllib.parse.quote(term)+'&sp=EgQIBBAB'
    d=initial_data(url)
    if not d: print('no data for', term); continue
    for v in walk(d,'videoRenderer'):
        title=''.join(r.get('text','') for r in v.get('title',{}).get('runs',[]))
        ch=v.get('ownerText',{}).get('runs',[{}])[0]
        handle=ch.get('navigationEndpoint',{}).get('browseEndpoint',{}).get('canonicalBaseUrl','')
        age=v.get('publishedTimeText',{}).get('simpleText','')
        views=v.get('viewCountText',{}).get('simpleText','')
        out.setdefault(handle,{'channel':ch.get('text'),'videos':[]})['videos'].append((term,title,age,views,v.get('videoId')))
json.dump(out,open('yt_results.json','w'),indent=1)
for h,c in sorted(out.items(), key=lambda kv:-len(kv[1]['videos'])):
    print(h, '|', c['channel'], '|', len(c['videos']), '|', c['videos'][0][1][:70], '|', c['videos'][0][2], '|', c['videos'][0][3])
