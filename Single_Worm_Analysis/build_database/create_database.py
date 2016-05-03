# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 08:52:54 2016

@author: ajaver
"""
from sqlalchemy import create_engine, MetaData, UniqueConstraint
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, Sequence, ForeignKey, DateTime, distinct, func
from sqlalchemy.schema import Table

#%%
Base = declarative_base()

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
    
    #__table_args__ = (UniqueConstraint('id', 'gene_id', 'allele_id',
    #                                   name='_strain_uc'),)

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
    directory = Column(String(500))
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


class OriginalVideo(Base):
    __tablename__ = 'original_videos'
    id = Column(Integer, ForeignKey('experiments.id'), primary_key=True)
    video_name = Column(String(200), unique=True, nullable = False)
    directory = Column(String(500), nullable = False)
    video_size = Column(Float)
    experiment = relationship(Experiment, primaryjoin="Experiment.id == OriginalVideo.id")
#%%
if __name__ == '__main__':
    engine_old = create_engine(r'mysql+pymysql://ajaver:@localhost/single_worm_old')
    engine_v2 = create_engine(r'mysql+pymysql://ajaver:@localhost/single_worm_db_v2')
    
    all_tables = [Allele, Gene, Strain, Tracker, Sex, DevelopmentalStage, 
                  VentralSide, Food, Arena, Habituation, Experimenter, 
                  Strain, Experiment, OriginalVideo]
    
    for new_table in all_tables[::-1]:
        new_table.__table__.drop(engine_v2, checkfirst=True)
    
    for new_table in all_tables:
        new_table.__table__.create(engine_v2, checkfirst=True)
    
    
    session_old = Session(engine_old)
    session_v2 = Session(engine_v2)
    
    meta = MetaData()
    meta.reflect(bind = engine_old, views=True)
    experiments_full_new =Table('experiments_full_new', meta, autoload=True)
    
    #%%
    
    singleTables = [('allele',Allele), ('gene',Gene), ('tracker',Tracker),('sex',Sex),
     ('developmental_stage',DevelopmentalStage), ('ventral_side',VentralSide), 
    ('food',Food),('arena',Arena), ('habituation',Habituation),('experimenter',Experimenter)]
    
    for old_col_str, obj_new in singleTables:
        dat = session_old.query(distinct(experiments_full_new.c[old_col_str])).all()
        dat_obj = [obj_new(name = x[0]) for x in dat]
        session_v2.add_all(dat_obj)
    
    #%%
    def get_table_keys(Obj):
        dat = session_v2.query(getattr(Obj, 'id'), getattr(Obj, 'name')).all()
        return {n:i for i,n in dat}
    #%%
    #create strain to insert
    dd = [experiments_full_new.c.strain, experiments_full_new.c.allele, 
          experiments_full_new.c.gene, experiments_full_new.c.genotype]
    strains = session_old.query(*dd).distinct(*dd).all()
    
    genes_d = get_table_keys(Gene)
    alleles_d = get_table_keys(Allele)
    
    strains_k = [(s,alleles_d[a],genes_d[g],gt) for (s,a,g,gt) in strains]
    #%%
    strains_obj = [Strain(name=s, allele_id=a, gene_id=g, genotype=gt) for (s,a,g,gt) in strains_k]
    session_v2.add_all(strains_obj)
    
    #%%
    dd = [experiments_full_new.c.base_name, experiments_full_new.c.directory, 
          experiments_full_new.c.date, 
          experiments_full_new.c.strain, experiments_full_new.c.tracker, 
          experiments_full_new.c.sex, experiments_full_new.c.developmental_stage, 
          experiments_full_new.c.ventral_side,
          experiments_full_new.c.food, experiments_full_new.c.arena, 
          experiments_full_new.c.habituation, experiments_full_new.c.experimenter]
    experiments = session_old.query(*dd).distinct(*dd).all()
    
    #%%
    experiments_obj = []
    exp_fields = ['base_name', 'directory', 'date',
                'strain_id', 'tracker_id', 'sex_id',
                'developmental_stage_id', 'ventral_side_id', 'food_id','arena_id',
                'habituation_id','experimenter_id']
    
    obj4keys = {'strain_id':Strain, 'tracker_id':Tracker, 'sex_id':Sex,
                'developmental_stage_id':DevelopmentalStage, 'ventral_side_id':VentralSide,
                'food_id':Food, 'arena_id':Arena, 'habituation_id':Habituation,
                'experimenter_id':Experimenter}
    dict4keys = {x:get_table_keys(obj4keys[x]) for x in obj4keys}
    #%%
    exp_rows = []
    for exp_dat in experiments:
        exp_dict = {}
        for ii, key in enumerate(exp_fields):
            if key in obj4keys:
                id_dict = dict4keys[key]
                exp_dict[key] = id_dict[exp_dat[ii]]
            else:
                exp_dict[key] = exp_dat[ii]
        
        #let's save the masked directories as the main directory
        exp_dict['directory'] = exp_dict['directory'].replace('/thecus/','/MaskedVideos/')
        exp_rows.append(Experiment(**exp_dict))
    
    session_v2.add_all(exp_rows)
    session_v2.commit()
    #%% Let's add the fields from the original videos
    video_rows = []
    for exp in exp_rows:
        vid_dict = {'id':exp.id,
        'directory':exp.directory.replace('/MaskedVideos/' , 'thecus'), 
        'video_name': exp.base_name + '.avi'}
        video_rows.append(OriginalVideo(**vid_dict))
    session_v2.add_all(video_rows)
    #%%
    session_v2.commit()
