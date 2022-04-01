from typing import Any
import Lib.app_lib as app_lib
from dataclasses import dataclass

@dataclass
class debts:
    name        : str
    amount      : float  
    transfer    : float

def expand (n : int, l : list, fill : Any):
    if n > len(l):
        for i in range(n - len(l)):
            l +=[fill]
    return l

def get_sort_dict (app : app_lib.app_state) -> list:
    totals      : dict = {}
    for data_ in app.data_array:
        if app.settings.month == 'all':
            if data_.person_name in totals:
                totals[data_.person_name] += float(data_.amount)
            else:
                totals[data_.person_name] = float(data_.amount)
        elif f"{app.settings.jear}.{app.settings.month}" in data_.date:
            if data_.person_name in totals:
                totals[data_.person_name] += float(data_.amount)
            else:
                totals[data_.person_name] = float(data_.amount)

    sort_list : list = sorted(totals.items(), key=lambda x:x[1])
    return sort_list

def get_debts_matrix (app : app_lib.app_state):
    d : dict = get_sort_dict(app)
    l : list = []
    for key, value in d:
        l += [debts(key + ' :  ', round(value, 2), 0)]
    return l

def get_average (app : app_lib.app_state):
    d       : dict = get_sort_dict(app)
    total   : float= 0
    if len(d) == 0:
        return 1
    for  key, amount in d:
        total += amount
    return round(total/len(d), 2)

def calc (app : app_lib.app_state) -> list:
    l       : list  = get_debts_matrix(app)
    average : float = get_average(app)
    for i in range(len(l)):
        d1 : debts = l[i]
        if i == 0:
            d1.transfer = round(average - d1.amount, 2)
        else:
            d0  : debts = l[i-1]
            d1.transfer = round((average - d1.amount) + d0.transfer, 2)
    return l

def get_transfere_str (app : app_lib.app_state):
    l : list = calc(app)
    s : list = []
    if len(l) > 1:
        s += [f"{l[0].name[:-4]} -> {l[0].transfer} -> {l[1].name[:-4]}"]
        if len(l) > 2:
            for i in range(1, len(l)-1):
                d0 : debts = l[i]
                d1 : debts = l[i+1]
                s += [f"{d0.name[:-4]} --> {d0.transfer} --> {d1.name[:-4]}"]
        
        return expand(10, s, '')
    s = ['More than 1 person must be stored']
    return expand(10, s, '')

def calc_expand (app : app_lib.app_state):
    l : list = calc(app)
    if len(l) == 0:
        l = [debts('No Data', '', '')]
    return expand(10, l, debts('', '', ''))