# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 16:17:35 2016

@author: ajaver
"""

from sqlalchemy import create_engine, MetaData, UniqueConstraint
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime, distinct, func
from sqlalchemy.schema import Table

import json
import os
import tables
import stat

from create_database import  Strain, Tracker, Sex, DevelopmentalStage, \
VentralSide, Food, Arena, Habituation, Experimenter, Experiment, Allele, Gene

if __name__ == '__main__':
    engine_v2 = create_engine(r'mysql+pymysql://ajaver:@localhost/single_worm_db_v2')
    session_v2 = Session(engine_v2)
    
    
    headers = ['base_name', 'directory', 'date','original_video_name', 'tracker', 
                'sex', 'developmental_stage', 'ventral_side', 'food', 'arena', 
                'habituation', 'experimenter', 'strain', 'genotype', 'gene', 'allele'];
    all_data = session_v2.query(Experiment.base_name, Experiment.directory, Experiment.date, 
                     Experiment.original_video_name, Tracker.name,
                     Sex.name, DevelopmentalStage.name, VentralSide.name, 
                     Food.name, Arena.name, Habituation.name, Experimenter.name,
                     Strain.name, Strain.genotype, Gene.name, Allele.name).\
                     join(Tracker).join(Sex).join(DevelopmentalStage).\
                     join(VentralSide).join(Food).\
                     join(Arena).join(Habituation).join(Experimenter).\
                     join(Strain).join(Gene).join(Allele).\
                     all()
    
    for ii_dat, dat in enumerate(all_data):
        dat_dict = {x:y for x,y in zip(*(headers, dat))}
        dat_dict['date'] = dat_dict['date'].isoformat()
        variables2save = bytes(json.dumps(dat_dict), 'utf-8')
        
        mask_dir = dat_dict['directory'].replace('/thecus/', '/MaskedVideos/')
        results_dir = dat_dict['directory'].replace('/thecus/', '/Results/')
        #mask_dir = '/Users/ajaver/Desktop/Videos/single_worm/agar_3/MaskedVideos'
        #results_dir = '/Users/ajaver/Desktop/Videos/single_worm/agar_3/Results'
        
        masked_image_file = os.path.join(mask_dir, dat_dict['base_name'] + '.hdf5')
        skeletons_file = os.path.join(results_dir, dat_dict['base_name'] + '_skeletons.hdf5')
        
        for fname in [masked_image_file, skeletons_file]:
            if os.path.exists(fname):
                print('{}) {}'.format(ii_dat, fname))
                os.chflags(masked_image_file, not stat.UF_IMMUTABLE)
                with tables.File(fname, 'r+') as fid:
                    main_node = 'experiment_info'
                    if '/experiment_info' in fid:
                        fid.remove_node('/', 'experiment_info')
                    
                    if '/contour_side2_length' in fid:
                        fid.remove_node('/', 'contour_side2_length')
                    if '/contour_side1_length' in fid:
                        fid.remove_node('/', 'contour_side1_length')
                    
                    fid.create_array('/', 'experiment_info', obj = variables2save)
                    
                if fname == masked_image_file:
                    os.chflags(fname, stat.UF_IMMUTABLE)





