from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,subprocess,time,re
root=Path(__file__).parent
sources=json.loads((root/'sources.json').read_text())
parts=root/'ocr_bilingual';parts.mkdir(exist_ok=True)
# Reuse the complete, previously saved OCR of the identical supplied mmg PDF.
mmg=root.parents[0]/'mmg_ocr.txt'
text=mmg.read_text()
text=re.sub(r'===== /tmp/mmg_png/p(\d+)\.png =====',lambda m:f'===== PAGE {int(m[1])} =====',text)
(root/'提取文本/S07.txt').write_text(text)
jobs=[]
for s in sources:
 if s['id']=='S07' or (not s['sparse_pages'] and s['id'] not in ['S06','S37','S38','S39','S40']):continue
 if s['id']=='S01':continue # image-only cover, text pages already extracted
 for start in range(1,s['pages']+1,6):
  end=min(start+5,s['pages']);p=parts/f"{s['id']}_{start:03}_{end:03}.txt"
  jobs.append((s,start,end,p))
def run(job):
 s,start,end,p=job
 if not p.exists():subprocess.run([str(root/'ocr_pdf'),s['path'],str(start),str(end),str(p)],check=True,capture_output=True)
 return f"{s['id']} {start}-{end}"
started=time.time()
with ThreadPoolExecutor(max_workers=4) as pool:
 futures=[pool.submit(run,j) for j in jobs]
 for i,f in enumerate(as_completed(futures),1):
  print(i,len(jobs),f.result(),f'{time.time()-started:.0f}s',flush=True)
for s in sources:
 chunks=sorted(parts.glob(s['id']+'_*.txt'))
 if chunks:(root/'提取文本'/f"{s['id']}.txt").write_text(''.join(p.read_text() for p in chunks))
 s['text_chars']=len((root/'提取文本'/f"{s['id']}.txt").read_text())
 s['text_method']='prior Vision OCR' if s['id']=='S07' else 'Vision OCR' if chunks else 'PDF text layer'
(root/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
print('DONE',flush=True)
