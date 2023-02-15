from collections import defaultdict
from datetime import datetime
import numpy as np


def __calc_time_diffs(datetime_objects:list):
    return [datetime_objects[i+1] - datetime_objects[i] for i in range(len(datetime_objects) - 1)]
    
    
def __group_datetime(datatime_list):
    groups = defaultdict(list)
    for d in datatime_list:
        minute = d.strftime('%Y-%m-%dT%H:%M')
        groups[minute].append(d)
    return dict(groups)    

def get_median_frames(data):
    m = "{:.2f}".format(np.mean([i.in_frames for i in data]))
    return 0 if m == "nan" else m

def get_street_moviment_list(data:list) -> list:
    output = []
    gps = __group_datetime([i.detected_at for i in data])
    difs = __calc_time_diffs([datetime.strptime(i, '%Y-%m-%dT%H:%M') for i in list(gps.keys())])

    for index, gp in enumerate(gps):
        output.append(len(gps[gp]))
        if index == 0: continue
        index -= 1
        dif = difs[index].seconds / 60
        while dif != 1:
            output.append(0)
            dif -= 1

    return output

def get_street_moviment_rate(data:list) -> float:
    all_datetimes = [d.detected_at for d in data ]
    all_datetimes.reverse()
    all_diffs = [ ]
    for index,i in enumerate(all_datetimes):
        if index + 1 != len(all_datetimes):
            all_diffs.append(i - all_datetimes[index + 1])

    all_diffs.reverse()
    cp_all_diffs = all_diffs.copy()
    cp_all_diffs = [ d.seconds for d in cp_all_diffs]
    
    r = float("{:.2f}".format(60 / np.std(cp_all_diffs)))
    print(r)
    print(np.isnan(r))
    print(np.isinf(r))
    
    if np.isinf(r) or np.isnan(r):
        return 0
    return r

def __count_frequency(data:list):
        count = {}
        for i in data: count[i[0]] = count.get(i[0], 0) + 1
        
        return count

def get_recurring_plates(data:list,min_dif:int = 200) -> float:
    data = [(i.content,i.detected_at) for i in data]
    frequency = __count_frequency(data)
    to_get_diff = {}
    for i in frequency:
        if frequency[i] > 1:
            contents = []
            for register in data:
                if register[0] == i:
                    contents.append(register[1])
            to_get_diff[i] = contents
                    
    
    recurring_plates = 0
    
    for i in to_get_diff:
        diffs =  [i.seconds for i in __calc_time_diffs(to_get_diff[i])]
        for dif in diffs:
            std = np.std(diffs)
            if not std and dif > min_dif: recurring_plates += 1
            if dif > min_dif and std > min_dif: recurring_plates += 1
        
    
    return recurring_plates