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
from sqlalchemy.ext.automap import automap_base


import json
import os
import tables
import stat
import numpy as np

from MWTracker.featuresAnalysis.obtainFeaturesHelper import switchCntSingleWorm, isBadVentralOrient
from MWTracker.batchProcessing.trackSingleWorker import isBadStageAligment

if __name__ == '__main__':
    engine_v2 = create_engine(r'mysql+pymysql://ajaver:@localhost/single_worm_db_v2')
    Base = automap_base()
    Base.prepare(engine_v2, reflect=True)
    Experiment = Base.classes.experiments;
    Strain = Base.classes.strains;
    Tracker = Base.classes.trackers;
    Sex = Base.classes.sexes;
    DevelopmentalStage = Base.classes.developmental_stages;
    VentralSide = Base.classes.ventral_sides;
    Food = Base.classes.foods;
    Arena = Base.classes.arenas;
    Habituation = Base.classes.habituations;
    Experimenter = Base.classes.experimenters;
    Allele = Base.classes.alleles;
    Gene = Base.classes.genes;
    OriginalVideo = Base.classes.original_videos;
    session_v2 = Session(engine_v2)

    headers = ['base_name', 'original_directory', 'original_video_name', 'date', 'tracker', 
                'sex', 'developmental_stage', 'ventral_side', 'food', 'arena', 
                'habituation', 'experimenter', 'strain', 'genotype', 'gene', 'allele', 'original_video'];
    all_data = session_v2.query(Experiment.base_name, OriginalVideo.directory,
                     OriginalVideo.name, Experiment.date,
                     Tracker.name,
                     Sex.name, DevelopmentalStage.name, VentralSide.name, 
                     Food.name, Arena.name, Habituation.name, Experimenter.name,
                     Strain.name, Strain.genotype, Gene.name, Allele.name).\
                     join(Tracker).join(Sex).join(DevelopmentalStage).\
                     join(VentralSide).join(Food).\
                     join(Arena).join(Habituation).join(Experimenter).\
                     join(Strain).join(Gene).join(Allele).\
                     join(OriginalVideo).\
                     all()
    
    for ii_dat, dat in enumerate(all_data):
        dat_dict = {x:y for x,y in zip(*(headers, dat))}
        dat_dict['date'] = dat_dict['date'].isoformat()
        variables2save = bytes(json.dumps(dat_dict), 'utf-8')
        
        mask_dir = dat_dict['original_directory'].replace('/thecus/', '/MaskedVideos/')
        results_dir = dat_dict['original_directory'].replace('/thecus/', '/Results/')
        #mask_dir = '/Users/ajaver/Desktop/Videos/single_worm/switched_sample'
        #results_dir = '/Users/ajaver/Desktop/Videos/single_worm/switched_sample/Results/'
        
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
                    
                    if fname == skeletons_file and dat_dict['ventral_side'] is not None:
                        switchCntSingleWorm(fname)
        
                
        if os.path.exists(masked_image_file) and os.path.exists(skeletons_file):
            if not isBadStageAligment(skeletons_file):
                with tables.File(skeletons_file, 'r') as fid:
                    rotation_matrix = fid.get_node('/stage_movement')._v_attrs['rotation_matrix']
                    micronsPerPixel = fid.get_node('/stage_movement')._v_attrs['pixel_per_micron_scale']
                    stage_vec_ori = fid.get_node('/stage_movement/stage_vec')[:]
                
                #%%
                
                #%%
                rotation_matrix_inv = rotation_matrix*[(1,-1),(-1,1)]
                stage_position_pix = -np.dot(rotation_matrix_inv, (stage_vec_ori/micronsPerPixel).T).T
                micronsPerPixel_rot = np.dot(rotation_matrix_inv, micronsPerPixel)
                with tables.File(masked_image_file, 'r+') as fid:
                    if '/stage_position_pix' in fid: fid.remove_node('/', 'stage_position_pix')
                    fid.create_array('/', 'stage_position_pix', obj=stage_position_pix)
                    fid.get_node('/stage_position_pix')._v_attrs['pixel_per_micron_scale'] = micronsPerPixel_rot
                    fid.get_node('/stage_position_pix')._v_attrs['rotation_matrix'] = rotation_matrix_inv
        
        if os.path.exists(masked_image_file):
            with tables.File(masked_image_file, 'r+') as fid:
                if '/stage_data' in fid:
                    fid.get_node('/stage_data').rename('stage_log')
            os.chflags(masked_image_file, stat.UF_IMMUTABLE)




