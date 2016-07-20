import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

files2look = ['N2 on food L_2010_04_08__11_25_23___8___1.hdf5',
'N2 on food L_2010_04_09__10_26_05__1.hdf5',
'N2 on food R_2010_03_05__09_35_10___8___1.hdf5',
'N2 on food R_2010_04_15__10_10_45__1.hdf5',
'N2 on food R_2011_11_11__12_56_36__3.hdf5',
'unc-63 (ok1075) on food L_2010_04_09__11_45_50___8___5.hdf5',
'unc-63 (ok1075) on food L_2010_04_16__12_57_13___8___8.hdf5',
'unc-63 (ok1075) on food R_2010_04_09__11_46_33__4.hdf5',
'unc-63 (ok1075) on food R_2010_04_13__11_24_05___2___4.hdf5',
'unc-63 (ok1075) on food R_2010_04_13__11_25_42___8___4.hdf5']

files2look = [os.path.splitext(x)[0] for x in files2look]

copy_dir = ''

if __name__ == '__main__':
	engine_v2 = create_engine(r'mysql+pymysql://ajaver:@localhost/single_worm_db_v2')
	Base = automap_base()
	Base.prepare(engine_v2, reflect=True)

	Experiment = Base.classes.experiments;
	ProgressTrack = Base.classes.progress_tracks;
	
	session_v2 = Session(engine_v2)

	all_segworm = session_v2.query(ProgressTrack.skeletons_file).\
	join(Experiment).filter(Experiment.base_name.in_(files2look)).\
	all()

	for file, in all_segworm:
		print(file)
		shutil.copy(file, os.path.expanduser('~/skel'))

