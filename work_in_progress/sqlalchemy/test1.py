# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 14:53:13 2016

@author: ajaver
"""

from sqlalchemy import create_engine, MetaData, Table

#from sqlalchemy.orm import mapper, sessionmaker

myengine = create_engine(r'mysql+pymysql://ajaver:@localhost/single_worm_old')

from sqlalchemy import inspect
inspector = inspect(myengine)

for table_name in inspector.get_table_names():
    print('TABLE: %s' % table_name)
    print([x['name'] for x in inspector.get_columns(table_name)])


useful_data = ['age', 'allele', 'avifilesize', 'chromosome', 'correctedvulvaside', 
'experimenterlocation', 'experimenters', 'food', 'gene', 'genotype', 
'habituation', 'sex', 'strain', 'trackerno', 'treatment', 'ventralside', 
'wormside']
['ambiguousstrainexperimentlist']

databases = ['exp_annotationdb', 'info']



meta = MetaData()
meta.reflect(bind=myengine)

info_table = meta.tables['info'];

#%%
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import sql
from sqlalchemy import func
# reflect the tables
#Base = automap_base()
#Base.prepare(myengine, reflect=True)

Base = automap_base(metadata=meta)
Base.prepare()

#TABLE: info
#['id', 'name', 'datestamp', 'food', 'chromosome', 'allele', 'vulvaside', 'strain']

#TABLE: exp_annotationdb
#['id', 'strainID', 'alleleID', 'geneID', 'chromosomeID', 'trackerID', 'sexID', 'ageID', 'ventralSideID', 'agarSideID', 'foodID', 'habitID', 'locationID', 'experimenterID', 'genotypeID', 'treatmentID']

#TABLE: sex
#['sexID', 'sexName']

#Info = Base.classes.info

Experiments = Base.classes.experiments
ExpAnnotation = Base.classes.exp_annotation
Strain = Base.classes.strain
Allele = Base.classes.allele
Gene = Base.classes.gene
Chromosome = Base.classes.chromosome
Tracker = Base.classes.trackerno
Sex = Base.classes.sex
Age = Base.classes.age
VentralSide = Base.classes.ventralside
Food = Base.classes.food
Habituation = Base.classes.habituation
Location = Base.classes.experimenterlocation
Experimenter = Base.classes.experimenters
Genotype = Base.classes.genotype
Treatment = Base.classes.treatment

session = Session(myengine)

q = session.query(Sex)
for row in q.all():
    print(row.sexName)
    
#%%

#%%
conn = myengine.connect()
#%%

result = session.query(ExpAnnotation.id, Experiments.wormFileName, VentralSide.ventralSideName).join(VentralSide).join(Experiments)
experiments_side = result.all()

#filter(Sex.sexID == Exp_annotationdb.sexID).\
#for row in result.all():
#    print(row)
#%%
#row = result.fetchone();
#for row in result:
#    print(row)

