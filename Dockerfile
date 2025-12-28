FROM continuumio/miniconda3:latest

WORKDIR /app

RUN conda update -n base -c defaults conda && conda install -y python=3.13 numpy pandas jupyter && conda clean -afy
