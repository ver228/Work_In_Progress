FROM docker/centos:7
RUN yum -y install git bzip2 && \
	curl -L "https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh" -o $HOME/miniconda_installer.sh
	bash $HOME/miniconda_installer.sh -b -f -p $HOME/miniconda  && \
	rm -f miniconda_installer.sh && \
	cd && \
	CONDA_PATH="$HOME/miniconda/bin" && \
	echo "export PATH=$CONDA_PATH:\$PATH" >> .bashrc && \
	source .bashrc && \
	hash -r && \
	conda install -y python=3.5.3 pip && \
	conda install -y anaconda-client conda-build numpy matplotlib pytables pandas \
	h5py scipy scikit-learn scikit-image seaborn xlrd cython statsmodels && \
	pip install gitpython pyqt5 keras && \
	conda install -y -c conda-forge tensorflow

	git clone https://github.com/ver228/tierpsy-tracker
	git clone https://github.com/openworm/open-worm-analysis-toolbox

	yum -y install gcc gcc-c++ cmake 
	yum -y install epel-release 
	rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm

	yum -y install gtk2-devel libdc1394-devel libv4l-devel ffmpeg-devel \
	gstreamer-plugins-base-devel libpng-devel libjpeg-turbo-devel jasper-devel openexr-devel \
	libtiff-devel libwebp-devel tbb-devel eigen3-devel

	conda install -y conda-build
	conda config --add channels menpo
	conda build --no-anaconda-upload tierpsy-tracker/installation/menpo_conda-opencv3
	conda install -y --use-local opencv3
	python3 -c "import cv2; print(cv2.__version__)"


	USER_CONFIG=$OPENWORM_DIR/open_worm_analysis_toolbox/user_config.py
	if [ ! -f $USER_CONFIG ]; then
	mv $OPENWORM_DIR/open_worm_analysis_toolbox/user_config_example.txt $USER_CONFIG
	fi