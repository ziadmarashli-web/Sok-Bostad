#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re,urllib.request,urllib.error
from concurrent.futures import ThreadPoolExecutor,as_completed

def validate(a):
    e=[];w=[];seen={}
    if not isinstance(a,list):return ["Roten måste vara en lista"],w
    for i,c in enumerate(a,1):
        name=str(c.get("name","")).strip();url=str(c.get("url","")).strip();orter=c.get("orter")
        if not name:e.append(f"Rad {i}: namn saknas")
        elif name.casefold() in seen:e.append(f"Dubblett: {name}")
        else:seen[name.casefold()]=i
        if not url:e.append(f"{name}: URL saknas")
        elif not re.match(r"^https://",url):w.append(f"{name}: bör använda https")
        if not isinstance(orter,list):e.append(f"{name}: orter måste vara lista")
        elif not c.get("nationwide") and not orter:e.append(f"{name}: ort eller nationwide=true krävs")
    return e,w

def fetch(url,timeout):
    h={"User-Agent":"Mozilla/5.0 (compatible; SokBostadLinkCheck/1.0)"}
    for method in ("HEAD","GET"):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers=h,method=method),timeout=timeout)
            return r.status,r.geturl(),"ok"
        except urllib.error.HTTPError as x:
            if method=="HEAD" and x.code in (403,405,429):continue
            return x.code,url,str(x)
        except Exception as x:
            if method=="HEAD":continue
            return 0,url,str(x)

ap=argparse.ArgumentParser()
ap.add_argument("file",nargs="?",default="bolag.json")
ap.add_argument("--links",action="store_true")
ap.add_argument("--expected-count",type=int)
ap.add_argument("--timeout",type=int,default=12)
ap.add_argument("--workers",type=int,default=8)
args=ap.parse_args()
a=json.loads(Path(args.file).read_text(encoding="utf-8"))
e,w=validate(a)
print("Bolag:",len(a))
if args.expected_count is not None and len(a)!=args.expected_count:e.append(f"Förväntade {args.expected_count}, fick {len(a)}")
for x in w:print("VARNING:",x)
for x in e:print("FEL:",x)
fail=[]
if args.links and not e:
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        jobs={ex.submit(fetch,c["url"],args.timeout):c for c in a}
        for f in as_completed(jobs):
            c=jobs[f];status,final,note=f.result()
            if 200<=status<400: print("OK",status,c["name"],final)
            else: print("GRANSKA",status or "-",c["name"],c["url"],note);fail.append(c["name"])
raise SystemExit(2 if e else (1 if fail else 0))
