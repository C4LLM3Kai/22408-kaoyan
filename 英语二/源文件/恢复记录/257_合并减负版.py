from pathlib import Path
p=Path('content.py');s=p.read_text().replace('For 【目标或需求】, I suggest','To 【目标动作，动词原形】, I suggest').replace('For improving your spoken English, I suggest','To improve your spoken English, I suggest');p.write_text(s)
