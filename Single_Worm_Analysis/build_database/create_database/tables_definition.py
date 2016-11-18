# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 18:54:08 2016

@author: ajaver
"""
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, Sequence, ForeignKey, DateTime

#from sqlalchemy.ext.declarative import declarative_base

engine_v2 = create_engine(r'mysql+pymysql://ajaver:@localhost/single_worm_db_v2')
Base = declarative_base()

#### experiments table core
class Allele(Base):
    __tablename__ = 'alleles'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20), unique=True)
    strains = relationship('Strain', backref="alleles")

class Gene(Base):
    __tablename__ = 'genes'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20), unique=True)
    strains = relationship('Strain', backref="genes")

class Strain(Base):
    __tablename__ = 'strains'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20), unique=True)
    genotype  = Column(String(200))
    gene_id = Column(Integer, ForeignKey('genes.id'), nullable=False)
    allele_id = Column(Integer, ForeignKey('alleles.id'), nullable=False)
    
    gene = relationship(Gene, primaryjoin="Strain.gene_id == Gene.id")
    allele = relationship(Allele, primaryjoin="Strain.allele_id == Allele.id")
    experiments = relationship('Experiment', backref="strains")
    
class Tracker(Base):
    __tablename__ = 'trackers'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20), unique=True)
    experiments = relationship('Experiment', backref="trackers")

class Sex(Base):
    __tablename__ = 'sexes'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20), unique=True)
    experiments = relationship('Experiment', backref="sexes")

class DevelopmentalStage(Base):
    __tablename__ = 'developmental_stages'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20), unique=True)
    experiments = relationship('Experiment', backref="developmental_stages")

class VentralSide(Base):
    __tablename__ = 'ventral_sides'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20), unique=True)
    experiments = relationship('Experiment', backref="ventral_sides")

class Food(Base):
    __tablename__ = 'foods'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20), unique=True)
    experiments = relationship('Experiment', backref="foods")

class Arena(Base):
    __tablename__ = 'arenas'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(100), unique=True)
    experiments = relationship('Experiment', backref="arenas")

class Habituation(Base):
    __tablename__ = 'habituations'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20), unique=True)
    experiments = relationship('Experiment', backref="habituations")

class Experimenter(Base):
    __tablename__ = 'experimenters'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20), unique=True)
    experiments = relationship('Experiment', backref="experimenters")

class Experiment(Base):
    __tablename__ = 'experiments'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    base_name = Column(String(200), unique=True, index=True, nullable=False)
    date = Column(DateTime())

    strain_id = Column(Integer, ForeignKey('strains.id'), nullable=False)
    tracker_id = Column(Integer, ForeignKey('trackers.id'), nullable=False)
    sex_id = Column(Integer, ForeignKey('sexes.id'), nullable=False)
    developmental_stage_id = Column(Integer, ForeignKey('developmental_stages.id'), nullable=False)
    ventral_side_id = Column(Integer, ForeignKey('ventral_sides.id'), nullable=False)
    food_id = Column(Integer, ForeignKey('foods.id'), nullable=False)
    arena_id = Column(Integer, ForeignKey('arenas.id'), nullable=False)
    habituation_id = Column(Integer, ForeignKey('habituations.id'), nullable=False)
    experimenter_id = Column(Integer, ForeignKey('experimenters.id'), nullable=False)
    
    strain = relationship(Strain, primaryjoin="Experiment.strain_id == Strain.id")
    tracker = relationship(Tracker, primaryjoin="Experiment.tracker_id == Tracker.id")
    sex = relationship(Sex, primaryjoin="Experiment.sex_id == Sex.id")
    developmental_stage = relationship(DevelopmentalStage, \
        primaryjoin="Experiment.developmental_stage_id == DevelopmentalStage.id")
    
    ventral_side = relationship(VentralSide, primaryjoin="Experiment.ventral_side_id == VentralSide.id")
    food = relationship(Food, primaryjoin="Experiment.food_id == Food.id")
    arena = relationship(Arena, primaryjoin="Experiment.arena_id == Arena.id")
    habituation = relationship(Habituation, primaryjoin="Experiment.habituation_id == Habituation.id")
    experimenter = relationship(Experimenter, primaryjoin="Experiment.experimenter_id == Experimenter.id")

#### link with the original videos
class OriginalVideo(Base):
    __tablename__ = 'original_videos'
    experiment_id = Column(Integer, ForeignKey('experiments.id'), primary_key=True)
    name = Column(String(200), unique=True, nullable = False)
    directory = Column(String(500), nullable = False)
    sizeMB = Column(Float)
    experiment = relationship(Experiment, primaryjoin="Experiment.id == OriginalVideo.id")


#### progress table
dict_mask_flags = {'Missed auxiliary files':101, 'Incomplete mask file':102, 'Finished mask file':103}

dict_track_flags = {
'TRAJ_CREATE':(201, 'Create trajectories'), 
'TRAJ_JOIN':(202, 'Join trajectories'), 'SKE_CREATE':(203, 'Create skeletons'), 
'SKE_ORIENT':(204, 'Orient skeletons movement'), 'SKE_FILT':(205, 'Filter skeletons'),
'STAGE_ALIGMENT':(206,'Strage aligment'), 
'INT_PROFILE':(207, 'Intensity profile'), 'INT_SKE_ORIENT':(208, 'Orient skeletons intensity'), 
'CONTOUR_ORIENT':(209, 'Orient ventral side'),
'FEAT_CREATE':(210, 'Obtain features'), 'END':(211, 'Finished'), 
}

class ExitFlag(Base):
    __tablename__ = 'exit_flags'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    track_checkpoint = Column(String(20))
    
class ProgressMask(Base):
    __tablename__ = 'progress_masks'
    __table_args__ = {'extend_existing': True}
    experiment_id = Column(Integer, ForeignKey('experiments.id'), primary_key=True)
    exit_flag_id = Column(Integer, ForeignKey('exit_flags.id'))
    mask_file = Column(String(500))
    n_valid_frames = Column(Integer)
    n_missing_frames = Column(Integer)
    fps = Column(Float)
    total_time = Column(Float)
    exit_flag = relationship(ExitFlag, primaryjoin="ProgressMask.exit_flag_id == ExitFlag.id")
    
class ProgressTrack(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'progress_tracks'
    experiment_id = Column(Integer, ForeignKey('experiments.id'), primary_key=True)
    exit_flag_id = Column(Integer, ForeignKey('exit_flags.id'))
    skeletons_file = Column(String(500))
    features_file = Column(String(500))
    n_segmented_skeletons = Column(Integer)
    n_filtered_skeletons = Column(Integer)
    n_valid_skeletons = Column(Integer)
    n_timestamps = Column(Integer)
    first_frame = Column(Integer)
    last_frame = Column(Integer)
    
    exit_flag = relationship(ExitFlag, primaryjoin="ProgressTrack.exit_flag_id == ExitFlag.id")

#### link to old segworm features
class SegwormFeature(Base):
    __tablename__ = 'segworm_features'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key = True)
    segworm_file = Column(String(500), nullable = False) #before file_name
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    fps = Column(Float)
    total_time = Column(Float)
    n_segworm_skeletons = Column(Integer) #before n_valid_skeletons
    n_timestamps = Column(Integer)
    experiment = relationship(Experiment, backref= 'segworm_features', 
                              primaryjoin="SegwormFeature.experiment_id == experiments.id")

#### segworm comparision
class SegWormComparison(Base):
    __tablename__ = 'segworm_comparisons'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key = True)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    segworm_feature_id = Column(Integer, ForeignKey('segworm_features.id'))
    n_mutual_skeletons = Column(Integer)
    error_05th = Column(Float)
    error_50th = Column(Float)
    error_95th = Column(Float)

