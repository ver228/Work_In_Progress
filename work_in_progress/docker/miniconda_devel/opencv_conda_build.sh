git clone https://github.com/ver228/install_opencv3_conda
conda build install_opencv3_conda
conda install -f --use-local /root/miniconda3/conda-bld/linux-64/opencv3-3.2.0-0.tar.bz2
anaconda upload --force /root/miniconda3/conda-bld/linux-64/opencv3-3.2.0-0.tar.bz2
