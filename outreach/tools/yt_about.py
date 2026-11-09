"""Manual research aid: channel facts from the public About page - subscribers, videos and the e-mail addresses the
channel writes in its own description (masked). --show prints them unmasked to the console so they can be typed into
the approval page database; never redirect this output into a file or commit it.
Usage: python3 tools/yt_about.py [--show] @handle ..."""
import json, re, sys, urllib.request
UA={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)','Accept-Language':'en-US,en;q=0.9'}
EM=re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')
SHOW = '--show' in sys.argv
for h in [a for a in sys.argv[1:] if a != '--show']:
    url=f'https://www.youtube.com/{h}/about?hl=en&gl=US'
    try:
        html=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60).read().decode('utf-8','replace')
    except Exception as e:
        print(h,'ERR',e); continue
    subs=(re.search(r'"subscriberCountText":"([^"]+)"',html) or re.search(r'([\d.,]+[KM]?) subscribers',html))
    vids=re.search(r'"videoCountText":"([^"]+)"',html) or re.search(r'([\d,]+) videos',html)
    desc=(re.search(r'"description":"(.*?)","',html) or [None,''])[1]
    emails=sorted({e for e in EM.findall(desc) if not e.endswith(('.png','.jpg'))})
    masked=emails if SHOW else [e[0]+'***@'+e.split('@')[1] for e in emails]
    has_button='View email address' in html or 'businessEmail' in html
    print(f"{h:22} subs={subs.group(1) if subs else '?':14} videos={vids.group(1) if vids else '?':12} email_in_desc={masked} captcha_button={has_button}")
