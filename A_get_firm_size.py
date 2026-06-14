from pathlib import Path
import pandas as pd
import re

df = pd.read_csv('/mnt/data/total_data_up.csv')

def split_parties(case):
    if isinstance(case,str) and ' v. ' in case:
        p,d = case.split(' v. ',1)
        d = re.sub(r'\s*\(.*$','',d)
        return p.strip(), d.strip()
    return "", ""

corp_terms = ['inc','corp','corporation','llc','ltd','gmbh','co','company','lp','llp','plc','technologies','technology','pharmaceutical','electronics','communications','bioepis']

def score_party(name):
    n=name.lower()
    if not n:
        return None
    # simple reproducible heuristic
    score=1
    if any(t in n for t in corp_terms):
        score=5
    if any(t in n for t in ['international','group','holdings']):
        score=max(score,7)
    if any(t in n for t in ['qualcomm','intel','samsung','sony','johnson & johnson','federal express','fedex','lg electronics']):
        score=10
    return score

plaintiffs=[]
defendants=[]
ps=[]
ds=[]
for c in df['case_name']:
    p,d=split_parties(c)
    plaintiffs.append(p)
    defendants.append(d)
    ps.append(score_party(p))
    ds.append(score_party(d))

df['plaintiff']=plaintiffs
df['defendant']=defendants
df['plaintiff_size']=ps
df['defendant_size']=ds

out='/mnt/data/total_data_with_size_scores.csv'
df.to_csv(out,index=False)

print(out)
