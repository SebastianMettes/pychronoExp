FROM ubuntu

MAINTAINER Kimbro Staken version: 0.1

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

SHELL ["/root/miniconda/bin/conda", "run", "-n", "379h", "/bin/bash", "-c"]
RUN pip install -e /pychronoExp/gym-multiarm
COPY pythonhostenv.sh /pythonhostenv.sh
RUN mkdir /data
RUN mkdir /data/sim
RUN mkdir /data/sim/trial
#RUN mkdir '/data/sim/trial/1'
RUN mkdir /data/sim/agent
#RUN mkdir '/data/sim/agent/1'

#RUN touch '/data/sim/agent/1/weights.json'
#RUN echo '[1]' >> '/data/sim/agent/1/weights.json'


COPY config.json /data/sim/config.json
CMD "/pythonhostenv.sh"



