#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger index.html och lankkontroll.html från bolag.json.
Kräver endast Python 3 och fungerar utan internet.
"""
from pathlib import Path
import json, re, shutil, sys

HERE=Path(__file__).resolve().parent
DATA=HERE/'bolag.json'
TARGETS=[HERE/'index.html', HERE/'lankkontroll.html']
VG_ORTS={"Göteborg","Ale","Alingsås","Bengtsfors","Bollebygd","Borås","Ed","Essunga","Falköping","Floda","Gråbo","Götene","Herrljunga","Hindås","Härryda","Kungälv","Kållered","Landvetter","Lerum","Lidköping","Lilla Edet","Lysekil","Mark","Mariestad","Mellerud","Munkedal","Mölndal","Mölnlycke","Orust","Partille","Rydal","Rävlanda","Sandared","Skara","Skövde","Stenkullen","Svenljunga","Tanum","Tidaholm","Tibro","Tollered","Tranemo","Trollhättan","Töreboda","Uddevalla","Ulricehamn","Vara","Vänersborg","Vårgårda","Åmål","Färgelanda","Gullspång","Karlsborg","Sotenäs","Strömstad"}
START='/* BOLAG_DATA_START */'
END='/* BOLAG_DATA_END */'

def fail(msg):
    print('FEL:',msg); sys.exit(1)

def load_and_validate():
    if not DATA.exists(): fail('bolag.json saknas.')
    try: data=json.loads(DATA.read_text(encoding='utf-8'))
    except Exception as e: fail(f'bolag.json är inte giltig JSON: {e}')
    if not isinstance(data,list) or not data: fail('bolag.json måste vara en lista med minst ett bolag.')
    seen=set(); problems=[]
    for i,c in enumerate(data,1):
        if not isinstance(c,dict): problems.append(f'Post {i}: måste vara ett objekt.'); continue
        name=str(c.get('name','')).strip(); url=str(c.get('url','')).strip(); orter=c.get('orter')
        if not name: problems.append(f'Post {i}: saknar name.')
        if name in seen: problems.append(f'Post {i}: dubblett av {name}.')
        seen.add(name)
        if not url.startswith('https://'): problems.append(f'{name or "Post "+str(i)}: url måste börja med https://')
        if not isinstance(orter,list) or not orter: problems.append(f'{name or "Post "+str(i)}: orter måste vara en icke-tom lista.')
        else:
            bad=[o for o in orter if o not in VG_ORTS]
            if bad: problems.append(f'{name}: ort utanför Västra Götaland i denna app: {", ".join(bad)}')
        if c.get('note') not in (None,'kommunal','formedling'): problems.append(f'{name}: note får bara vara kommunal eller formedling.')
    if problems:
        print('Hittade problem – inga filer ändrades:')
        for p in problems: print(' -',p)
        sys.exit(1)
    return data

def replace_block(path,data):
    if not path.exists(): fail(f'{path.name} saknas.')
    text=path.read_text(encoding='utf-8')
    pattern=re.escape(START)+r'.*?'+re.escape(END)
    if path.name=='index.html': payload='var COMPANIES = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';'
    else: payload='const COMPANIES = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';'
    replacement=START+'\n'+payload+'\n'+END
    new,n=re.subn(pattern,replacement,text,count=1,flags=re.S)
    if n!=1: fail(f'Kunde inte hitta bolagsmarkörerna i {path.name}.')
    shutil.copy2(path,path.with_suffix(path.suffix+'.backup'))
    path.write_text(new,encoding='utf-8')

if __name__=='__main__':
    data=load_and_validate()
    for target in TARGETS: replace_block(target,data)
    print(f'KLART! {len(data)} bolag har skrivits till index.html och lankkontroll.html.')
    print('Säkerhetskopior skapades med ändelsen .backup.')
