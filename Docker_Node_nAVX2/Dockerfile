FROM ubuntu

MAINTAINER Sebastian Mettes version: 0.1

RUN DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN TZ=US/Denver apt-get install -y tzdata
RUN apt-get install -y git build-essential sudo nano tzdata

RUN apt-get install -y wget
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN chmod +x Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda && \
    echo ". /root/miniconda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    /root/miniconda/bin/conda clean -afy
    
RUN git clone https://github.com/SebastianMettes/pychronoExp
COPY environment.yml /environment.yml

SHELL ["/root/miniconda/bin/conda", "run", "-n", "base", "/bin/bash", "-c"]
RUN conda env create -f environment.yml

SHELL ["/root/miniconda/bin/conda", "run", "-n", "379", "/bin/bash", "-c"]
RUN conda remove pytorch
RUN conda install ninja pyyaml mkl mkl-include setuptools cmake cffi typing_extensions future six requests dataclasses
RUN git clone --recursive https://github.com/pytorch/pytorch
RUN cd pytorch
ENV USE_CUDA=0
RUN export CMAKE_PREFIX_PATH=${CONDA_PREFIX:-"$(dirname $(which conda))/../"}
RUN cd pytorch && python setup.py build --cmake-only
RUN cmake build -DDISABLE_AVX2:BOOL=TRUE -DCXX_AVX2_FOUND:BOOL=FALSE -DC_AVX2_FOUND:BOOL=FALSE -DDISABLE_AVX512F:BOOL=TRUE .
RUN python -u setup.py install

RUN git pull
RUN pip install -e /pychronoExp/gym-multiarm
COPY pythonenv.sh /pythonenv.sh
RUN mkdir /data
RUN mkdir /data/sim
RUN mkdir /data/sim/trial

RUN mkdir /data/sim/agent

COPY config.json /data/sim/config.json
CMD "/pythonenv.sh"



