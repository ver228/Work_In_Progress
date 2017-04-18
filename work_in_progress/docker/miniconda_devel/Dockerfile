FROM miniconda3

RUN yum -y groupinstall "Development tools" && yum clean all
RUN conda install -y conda-build anaconda-client && conda clean -y --all

COPY opencv_conda_build.sh /root/opencv_conda_build.sh
