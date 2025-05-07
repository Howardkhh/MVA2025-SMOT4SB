FROM nvcr.io/nvidia/cuda:11.6.1-devel-ubuntu20.04
LABEL org.opencontainers.image.authors="Howardkhh"

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
ENV OMP_NUM_THREADS=4
ENV MKL_NUM_THREADS=4

ENV DEBIAN_FRONTEND noninteractive
RUN apt update -y
RUN apt-get install -y tzdata && ln -fs /usr/share/zoneinfo/Asia/Taiwan /etc/localtime && dpkg-reconfigure -f noninteractive tzdata \
    && apt install -y sudo vim wget gcc libgl1-mesa-glx libglib2.0-0 zip openmpi-bin tree \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /root/MVA2025-SMOT4SB/requirements.txt

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && echo "Running $(conda --version)" \
    && conda init bash \
    && . /root/.bashrc \
    && conda create -n mva_team1 -c conda-forge -y python==3.8 \
    && conda activate mva_team1 \
    && pip install -r /root/MVA2025-SMOT4SB/requirements.txt

RUN echo "conda activate mva_team1" >> /root/.bashrc

WORKDIR /root/MVA2025-SMOT4SB

CMD ["/bin/bash"]