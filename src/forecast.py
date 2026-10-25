from statistics import mean

def _slope(values):
    if len(values)<2: return 0.0
    xbar=(len(values)-1)/2; ybar=mean(values); den=sum((i-xbar)**2 for i in range(len(values))) or 1
    return sum((i-xbar)*(v-ybar) for i,v in enumerate(values))/den

def project_history(rows,days=7):
    if len(rows)<3: raise ValueError('at least three readings are required')
    days=max(1,min(int(days),14)); fields=['resting_hr','hrv_ms','sleep_hours','steps','spo2']
    projections={}
    for field in fields:
        vals=[float(r[field]) for r in rows if field in r]
        if len(vals)<3: continue
        slope=_slope(vals); last=vals[-1]; projections[field]=[round(last+slope*i,2) for i in range(1,days+1)]
    recent=rows[-min(7,len(rows)):]; sleep=mean(float(r.get('sleep_hours',0)) for r in recent); steps=mean(float(r.get('steps',0)) for r in recent); hrv=mean(float(r.get('hrv_ms',0)) for r in recent); hr=mean(float(r.get('resting_hr',0)) for r in recent)
    readiness=max(0,min(100,50+(sleep-7)*8+(steps-7000)/700+(hrv-50)*.5-(hr-70)*.7))
    return {'days':days,'projections':projections,'wellness_readiness_score':round(readiness,1),'notice':'Descriptive wellness projection only; not a diagnosis, prognosis or heart-attack prediction.'}
