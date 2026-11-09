from pathlib import Path
p=Path('build_pdf.py');s=p.read_text().replace("+cols+'}\\toprule\\n'", "+cols+r'}\\toprule'+'\\n'").replace('[10.5pt,a4paper,fontset=macnew]','[11pt,a4paper,fontset=macnew]')
p.write_text(s)
