from pathlib import Path
import fitz,json,hashlib
base=Path('/Users/shaoyikai/Desktop/考研/英语二')
other=Path('/Users/shaoyikai/Downloads/27南山作文模板吃鸡计划4.0（英二）')
out=base/'源文件/多源融合模板/提取文本'
files=sorted(base.glob('*.pdf'))+sorted(other.rglob('*.pdf'))
manifest=[]
for i,p in enumerate(files,1):
 d=fitz.open(p); pages=[page.get_text(sort=True) for page in d]
 text='\n'.join(f'===== PAGE {j+1} =====\n{s}' for j,s in enumerate(pages))
 sid=f'S{i:02}'
 (out/f'{sid}.txt').write_text(text)
 row=dict(id=sid,path=str(p),name=p.name,pages=len(pages),chars=sum(map(len,pages)),sparse_pages=[j+1 for j,s in enumerate(pages) if len(s.strip())<100],sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 manifest.append(row)
 print(sid,len(pages),row['chars'],'sparse',len(row['sparse_pages']),p.name)
(out.parent/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
