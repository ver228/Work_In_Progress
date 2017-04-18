FROM centos:7

RUN yum install -y bzip2 && \
	yum install -y epel-release && \
	rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm && \
	yum -y install gtk2-devel libdc1394-devel libv4l-devel ffmpeg-devel \
	gstreamer-plugins-base-devel libpng-devel libjpeg-turbo-devel jasper-devel openexr-devel \
	libtiff-devel libwebp-devel tbb-devel eigen3-devel && \
	yum clean all

RUN curl -L "https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh" -o ~/miniconda_installer.sh && \
	bash ~/miniconda_installer.sh -f -b && \
	rm -f ~/miniconda_installer.sh && \
	echo "export PATH=~/miniconda3/bin:\$PATH" >> ~/.bashrc && \
    source ~/.bashrc && \
    conda update conda && \
    conda clean -y --all

ENV PATH ~/miniconda3/bin:$PATH
