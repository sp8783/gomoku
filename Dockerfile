FROM continuumio/miniconda3:latest

WORKDIR /app

RUN conda update -n base -c defaults conda && conda install -y python=3.13 numpy pandas jupyter && conda clean -afy

# Install tkinter for GUI
RUN apt-get update && apt-get install -y python3-tk && rm -rf /var/lib/apt/lists/*
