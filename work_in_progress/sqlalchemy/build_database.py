# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 23:23:09 2016

@author: ajaver
"""
import os
import re

agar_file = '/Users/ajaver/Documents/GitHub/Work_In_Progress/Single_Worm_Analysis/all_files/all_agar.txt'

with open(agar_file, 'r') as fid:
    all_data = fid.read()
    
data = [os.path.split(x) for x in all_data.split('\n') if x]
directories, file_names = zip(*data)
file_names = [x.rpartition('.avi')[0] for x in file_names]


STR_S = '(?P<left>.*?).(?P<side>(L|R)?_)(?P<date>\d{4}(_\d{2}){2}_(_\d{2}){2,3})(?P<tracker>(_{2,3}\d*)+)$'
prog = re.compile(STR_S, re.M|re.I)

file_parts = []
weird_names = []
for file_name in file_names:
    result = prog.match(file_name)
    if not result is None:
        file_parts.append((result.group('left'), result.group('side'), 
              result.group('date'), result.group('tracker')))
    else:
        weird_names.append(file_name)


left_str, side_str, date_str, tracker_str = zip(*file_parts)

assert all(len(x)>=1 for x in side_str)
side_str = [x[0].upper() for x in side_str]

#%%
left_parts = []
weird_left = []
STR_S2 = '(?P<strain>.*?)(?P<media>(o?(n|m)|off|all) *\w?oo\w?).?'
prog2 = re.compile(STR_S2, re.M|re.I)
for ii, l_str in enumerate(left_str):
    result = prog2.match(l_str)
    if not result is None:
        left_parts.append((result.group('strain'),result.group('media')))
    else:
        left_parts.append((l_str, ''))
        weird_left.append((l_str, file_names[ii]))

remain_left, media = zip(*left_parts)

#%%
from sqlalchemy import create_engine, MetaData, Table, sql, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


myengine = create_engine(r'mysql+pymysql://ajaver:@localhost/single_worm_old')

meta = MetaData()
meta.reflect(bind=myengine)

Base = automap_base(metadata=meta)
Base.prepare()

Experiments = Base.classes.experiments
VentralSide = Base.classes.ventralside
ExpAnnotation = Base.classes.exp_annotation


session = Session(myengine)
result = session.query(ExpAnnotation.id, Experiments.wormFileName, VentralSide.ventralSideName).join(VentralSide).join(Experiments)
experiments_side = result.all()


#%%
name_side_map = {x:y for x,y in zip(*(file_names,side_str))}
db_side_map = {x[1]:x[2] for x in experiments_side}
#%%
good_names = []
bad_names = []
for x in name_side_map:
    if x in db_side_map:
        good_names.append(x)
    else:
        bad_names.append(x)

#%%
comp = [(name_side_map[x], db_side_map[x]) for x in good_names]

comp_dict = {}
for x in good_names:
    dd = (name_side_map[x], db_side_map[x])
    if not dd in comp_dict:
        comp_dict[dd] = []
    comp_dict[dd].append(x)
#%%
#[name_side_map[x] for x in bad_names]
diff_dict = {}
for x in bad_names:
    dd = name_side_map[x]
    if not dd in diff_dict:
        diff_dict[dd] = []
    diff_dict[dd].append(x)
