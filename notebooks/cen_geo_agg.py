import math
import numpy as np
import pandas as pd

def calculate_sumgeo(df,sumgeo):
    variables = list(df.columns[1:])
    var = set()
    for i in variables:
        if i[-1] == 'E' or i[-1] == 'M' or i[-1] == 'C':
            i = i[:-1]
            var.add(i)
        else:
            var.add(i)
    var = list(var)
    results = []
    for i in df[sumgeo].unique():
        dff = df[df[sumgeo] == i]
        record = {}
        record[sumgeo] = i
        for v in var:
            e = dff[f'{v}E'].sum()
            if f'{v}M' not in dff.columns:
                m = np.nan
            else:
                m = math.sqrt(dff[f'{v}M'].apply(lambda x: x**2).sum())
            if m == 0 or e == 0:
                c = 0
            else:
                c = np.absolute(m/1.645/e*100)
            record[f'{v}E'] = e
            record[f'{v}M'] = m
            record[f'{v}C'] = c            
        results.append(record)   
    r = pd.DataFrame(results)
    return r

def calc_muni_agg(df,sumgeo):
    variables = list(df.columns[1:])
    var = list(set([i.replace('E', '')\
                .replace('M', '') for i in variables]))
    results = []
    for i in df[sumgeo].unique():
        dff = df[df[sumgeo] == i]
        record = {}
        record[sumgeo] = i
        for v in var:
            e = dff[f'{v}E'].sum()
            if f'{v}M' not in dff.columns:
                m = np.nan
            else:
                m = math.sqrt(dff[f'{v}M'].apply(lambda x: x**2).sum())
            record[f'{v}E'] = e
            record[f'{v}M'] = m            
        results.append(record)   
    r = pd.DataFrame(results)
    return r