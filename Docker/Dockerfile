FROM ubuntu

MAINTAINER Kimbro Staken version: 0.1

RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive"
ENV TZ=US/Denver
RUN apt-get install -y tzdata

RUN apt-get install -y wget
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN chmod +x Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda && \
    echo ". /root/miniconda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    /root/miniconda/bin/conda clean -afy

#RUN eval "$(/root/miniconda/bin/conda shell.bash hook)" && conda init && 
SHELL ["/root/miniconda/bin/conda", "run", "-n", "base", "/bin/bash", "-c"]
RUN conda create -n py379 -y python==3.7.9

SHELL ["/root/miniconda/bin/conda", "run", "-n", "py379", "/bin/bash", "-c"]

#RUN conda activate py379
#RUN python --version



