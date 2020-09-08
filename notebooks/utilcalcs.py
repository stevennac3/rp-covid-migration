import math
import numpy as np

def get_moe(m):
    result = math.sqrt(sum(map(lambda x: x**2, m)))
    return result

def get_cv(e, m): 
    if e == 0:
        return np.nan
    else:
        return np.absolute(m/1.645/e*100)
    
def get_pct(e,agg_e):
    if agg_e == 0:
        return np.nan
    else:
        return e/agg_e

def get_pctmoe(e,m,agg_e,agg_m): 
    if agg_e == 0:
        return np.nan
    else: 
        result = (1/agg_e) * math.sqrt((m**2)-(((e/agg_e)**2)*(agg_m**2)))
        return result
    
def get_median(buckets, row):
    ordered = list(buckets.keys())
    orderedE = [i+'e' for i in ordered]
    N = row[orderedE].sum()
    C = 0
    i = 0
    while C <= N/2 and i<=len(buckets.keys())-1:
        C += int(row[orderedE[i]])
        i += 1
    i = i-1
    if i == 0:
        median = list(buckets.values())[0][1]
    elif C == 0: 
        median =0
    elif i == len(buckets.keys())-1:
        median = list(buckets.values())[-1][1]
    else: 
        C = C - int(row[orderedE[i]])
        L = buckets[ordered[i]][0]
        F = int(row[orderedE[i]])
        W = buckets[ordered[i]][1] - buckets[ordered[i]][0]
        median = L + (N/2 - C)*W/F
    return median

def get_median_moe(buckets, row, DF=1.1):
    ordered = list(buckets.keys())
    orderedE = [i+'e' for i in ordered]
    B = row[orderedE].sum()
    if B == 0: 
        return np.nan
    else:
        cumm_dist = list(np.cumsum(row[orderedE])/B*100)

        se_50 = DF*(((93/(7*B))*2500))**0.5
        
        if se_50 >= 50:
            return np.nan
        else: 
            p_lower = 50 - se_50
            p_upper = 50 + se_50
            
            lower_bin = min([cumm_dist.index(i) for i in cumm_dist if i > p_lower])
            upper_bin = min([cumm_dist.index(i) for i in cumm_dist if i > p_upper])
            
            if lower_bin >= len(ordered)-1 or upper_bin >= len(ordered)-1:
                return np.nan
            else:
                if lower_bin == upper_bin:
                    A1 = min(buckets[ordered[lower_bin]])
                    A2 = min(buckets[ordered[lower_bin+1]])
                    C1 = cumm_dist[lower_bin-1]
                    C2 = cumm_dist[lower_bin]
                    lowerbound = (p_lower - C1)*(A2-A1)/(C2-C1) + A1 
                    upperbound = (p_upper - C1)*(A2-A1)/(C2-C1) + A1

                else:
                    A1_l = min(buckets[ordered[lower_bin]])
                    A2_l = min(buckets[ordered[lower_bin+1]])
                    C1_l = cumm_dist[lower_bin-1]
                    C2_l = cumm_dist[lower_bin]

                    A1_u = min(buckets[ordered[upper_bin]])
                    A2_u = min(buckets[ordered[upper_bin+1]])
                    C1_u = cumm_dist[upper_bin-1]
                    C2_u = cumm_dist[upper_bin]

                    lowerbound = (p_lower - C1_l)*(A2_l-A1_l)/(C2_l-C1_l) + A1_l 
                    upperbound = (p_upper - C1_u)*(A2_u-A1_u)/(C2_u-C1_u) + A1_u

                return (upperbound - lowerbound)*1.645/2