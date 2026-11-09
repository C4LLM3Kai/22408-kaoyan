import json,re,csv,unicodedata
from pathlib import Path
R=Path(__file__).parent
items=json.loads((R/'templates.json').read_text());sources=json.loads((R/'sources.json').read_text())
def tokens(s):
 s=unicodedata.normalize('NFKC',s).lower().replace('’',"'")
 s=re.sub(r'===== PAGE \d+ =====',' ',s,flags=re.I)
 s=re.sub(r'【.*?】',' ',s)
 # Split compounds, omit numerals and punctuation; compare all English tokens, including function words.
 return re.findall('[a-z]+',s)
def ngrams(t,n):return set(tuple(t[i:i+n]) for i in range(len(t)-n+1))
def coverage(t,ng,n):
 covered=set()
 for i in range(len(t)-n+1):
  if tuple(t[i:i+n]) in ng:covered.update(range(i,i+n))
 return round(100*len(covered)/len(t),2) if t else 0
corpus=[]
for s in sources:
 text=(R/'提取文本'/f"{s['id']}.txt").read_text();t=tokens(text)
 corpus.append((s,t,ngrams(t,4),ngrams(t,5)))
rows=[]
for x in items:
 for form in ['template','body']:
  t=tokens(' '.join(x[form]));compare=[]
  for s,st,g4,g5 in corpus:
   compare.append(dict(source=s['id'],coverage4=coverage(t,g4,4),coverage5=coverage(t,g5,5)))
  worst=max(compare,key=lambda a:a['coverage4'])
  rows.append(dict(id=x['id'],title=x['title'],form=form,tokens=len(t),max4=worst['coverage4'],max5=max(a['coverage5'] for a in compare),worst_source=worst['source'],by_source=compare))
source_rows=[]
all_body=tokens(' '.join(' '.join(x['body']) for x in items))
all_template=tokens(' '.join(' '.join(x['template']) for x in items))
for s,st,g4,g5 in corpus:
 source_rows.append(dict(id=s['id'],name=s['name'],english_tokens=len(st),body4=coverage(all_body,g4,4),template4=coverage(all_template,g4,4),maximum_piece4=max(c['coverage4'] for r in rows for c in r['by_source'] if c['source']==s['id'])))
result=dict(method='English normalized 4-token exact-match coverage, denominator=candidate tokens, matched positions counted once; Chinese slots, numbers, headings, greetings and sign-offs excluded. 5-token result also recorded.',sources=len(sources),pages=sum(s['pages'] for s in sources),max4=max(r['max4'] for r in rows),max5=max(r['max5'] for r in rows),pieces=rows,source_results=source_rows)
(R/'overlap_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
with (R/'逐篇重合检查.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['编号','类型','英文词元数','最大4词覆盖率%','最大5词覆盖率%','4词对应来源'])
 for r in rows:w.writerow([r['id'],r['form'],r['tokens'],r['max4'],r['max5'],r['worst_source']])
print('MAX4',result['max4'],'MAX5',result['max5'])
for r in sorted(rows,key=lambda a:-a['max4'])[:12]:print(r['id'],r['form'],r['max4'],r['max5'],r['worst_source'])
assert all(r['max4']<50 for r in rows),'Overlap target exceeded'
