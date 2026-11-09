import json,re,unicodedata
from pathlib import Path
R=Path(__file__).parent;P=R.parent/'多源融合模板'
d=json.loads((R/'content.json').read_text());sources=json.loads((P/'sources.json').read_text())
def tokens(s):
 s=re.sub(r'【.*?】',' ',s)
 s=re.sub(r'===== PAGE \d+ =====',' ',s,flags=re.I)
 return re.findall('[a-z]+',unicodedata.normalize('NFKC',s).lower().replace('’',"'"))
def grams(t,n):return {tuple(t[i:i+n]) for i in range(len(t)-n+1)}
def coverage(t,g,n):
 covered=set()
 for i in range(len(t)-n+1):
  if tuple(t[i:i+n]) in g:covered.update(range(i,i+n))
 return round(100*len(covered)/len(t),2) if t else 0
corpus=[(s,tokens((P/'提取文本'/f"{s['id']}.txt").read_text())) for s in sources]
corpus=[(s,grams(t,4),grams(t,5)) for s,t in corpus]
pieces=[]
for x in d['cores']:
 pieces.extend([(x['id']+'固定模板',' '.join(x['template'])),(x['id']+'完整示例',' '.join(x['body']))])
x=d['chart']
for v in ['static','dynamic']:pieces.append(('M5'+('静态' if v=='static' else '动态')+'固定模板',x[v]+' '+' '.join(x['shared'])))
pieces.append(('M5完整示例',' '.join(x['body'])))
pieces.append(('功能卡英文合并',' '.join(r[2] for r in d['cards'])))
rows=[]
for label,t in pieces:
 tok=tokens(t);results=[dict(source=s['id'],coverage4=coverage(tok,g4,4),coverage5=coverage(tok,g5,5)) for s,g4,g5 in corpus]
 m=max(results,key=lambda z:z['coverage4'])
 rows.append(dict(label=label,tokens=len(tok),max4=m['coverage4'],max5=max(z['coverage5'] for z in results),source=m['source'],all=results))
result=dict(method='normalized English exact 4-token coverage; candidate-word denominator; 5-token auxiliary; original 40 source PDFs only',max4=max(x['max4'] for x in rows),max5=max(x['max5'] for x in rows),rows=rows)
(R/'重合检查.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
for x in rows:print(x['label'],x['tokens'],x['max4'],x['source'])
assert result['max4']<50
