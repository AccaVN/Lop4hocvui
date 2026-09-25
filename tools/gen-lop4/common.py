import random, json
R=random.Random(20260925)
def rnd(a,b):return R.randint(a,b)
def pick(a):return R.choice(a)
def shuffle(a):a=list(a);R.shuffle(a);return a
def mc(skill,prompt,answer,wrong,**ex):
    answer=str(answer);opts=[answer]
    for w in wrong:
        w=str(w)
        if w not in opts:opts.append(w)
    assert len(opts)>=2 or ex.get('fixed'),(prompt,answer,wrong)
    q={'type':'mc','skill':skill,'prompt':prompt,'answer':answer,'options':opts}
    if ex.get('fixed'):
        q['options']=list(ex['fixed']);q['fixed']=list(ex['fixed']);ex=dict(ex);del ex['fixed']
        assert answer in q['options'],(prompt,answer,q['options'])
    q.update({k:v for k,v in ex.items() if v is not None})
    return q
def inp(skill,prompt,answer,**ex):
    q={'type':'input','skill':skill,'prompt':prompt,'answer':int(answer)}
    q.update({k:v for k,v in ex.items() if v is not None});return q
def ordq(skill,prompt,answer,**ex):
    items=shuffle(answer)
    t=0
    while items==list(answer) and t<20:items=shuffle(answer);t+=1
    q={'type':'order','skill':skill,'prompt':prompt,'answer':list(answer),'items':items}
    q.update({k:v for k,v in ex.items() if v is not None});return q
def key(q):
    return '|'.join(str(q.get(k,'')) for k in ('prompt','big','visual','say','answer','shapes','ruler','clock','block','blocks','voice'))+'|'+(json.dumps(q.get('passage',{}).get('title','')) if q.get('passage') else '')
def fill15(gens,n=15,tries=400):
    """gens: list of zero-arg funcs; round-robin until n unique"""
    out=[];keys=set();i=0;t=0
    while len(out)<n and t<tries:
        g=gens[i%len(gens)];i+=1;t+=1
        q=g()
        if q is None:continue
        k=key(q)
        if k in keys:continue
        keys.add(k);out.append(q)
    assert len(out)==n,(len(out),gens[0])
    return out
