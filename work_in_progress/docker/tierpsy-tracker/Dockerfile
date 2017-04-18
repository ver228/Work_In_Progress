FROM miniconda3

RUN yum -y install git gcc ffmpeg && yum clean all
RUN conda install -y numpy matplotlib pytables pandas \
	h5py scipy scikit-learn scikit-image seaborn xlrd cython statsmodels pyqt gitpython && \
	conda install -y --channel https://conda.anaconda.org/ver228 opencv3 && \
	conda install -y -c conda-forge tensorflow && \
	conda clean -y --all && \
	pip install --no-cache-dir keras
RUN cd ~ && \
	git clone --depth=1 --recursive https://github.com/openworm/open-worm-analysis-toolbox \
	~/open-worm-analysis-toolbox && \
	git clone --depth=1 --recursive  https://github.com/ver228/tierpsy-tracker \
	~/tierpsy-tracker && \
	cd ~/open-worm-analysis-toolbox/ && \
	source ~/.bashrc && \
	python setup.py develop && \
	cd ./open_worm_analysis_toolbox && mv user_config_example.txt user_config.py && \
	cd ~/tierpsy-tracker/ && python setup.py develop
