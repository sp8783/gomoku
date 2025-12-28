FROM python:3.13-slim

WORKDIR /app

# Install tkinter, locale support, and Japanese fonts for GUI
RUN apt-get update && \
    apt-get install -y \
        python3-tk \
        locales \
        fonts-noto-cjk \
        fonts-noto-cjk-extra \
        fontconfig \
    && echo "ja_JP.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen ja_JP.UTF-8 \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir numpy pandas jupyter

ENV LANG=ja_JP.UTF-8
ENV LC_ALL=ja_JP.UTF-8
