from pathlib import Path
p=Path('build_pdf.py');s=p.read_text()
a=s.index(' if isbig:\n  s.append(blocktitle(\'填空提示\'))')
b=s.index(" bcount=wc",a)
s=s[:a]+" s.append(blocktitle('完整套用示例'))\n"+s[b:]
s=s.replace(" if not isbig:s.append(r'{\\small\\textbf{核对重点：}'+txt(x['check'])+'}\\par\\n')", " s.append(r'{\\small\\textbf{核对重点：}'+txt(x['check'])+'}\\par\\n')")
a=s.index(" if isbig:\n  s.append(blocktitle('对标批改指令'))")
b=s.index(" s.append(r'{\\fontsize{8}{10}",a)
s=s[:a]+s[b:]
old=" ss=r'\\noindent '+r'\\\\'.join(txt(z) for z in h.split('\\n'))+r'\\par'+'\\n'\n return ss"
new=""" lines=h.split('\\n')
 if x['kind'] in ['通知','告示','倡议']:
  return r'{\\centering '+r'\\\\'.join(txt(z) for z in lines)+r'\\par}'+ '\\n'
 if x['kind']=='纪要':
  return r'{\\centering '+txt(lines[0])+r'\\par}'+ '\\n'+r'\\noindent '+r'\\\\'.join(txt(z) for z in lines[1:])+r'\\par'+'\\n'
 ss=r'\\noindent '+r'\\\\'.join(txt(z) for z in lines)+r'\\par'+'\\n'
 return ss"""
assert old in s
s=s.replace(old,new)
p.write_text(s)
