FROM debian:bullseye-slim


RUN apt update -y && apt install -y sox libgomp1 libstdc++6 libpthread-stubs0-dev python3 python3-pip

RUN pip3 install --upgrade pip && pip3 install stt streamlit resampy

COPY coqui-stt-0.9.3-models.pbmm coqui-stt-0.9.3-models.pbmm
COPY coqui-stt-0.9.3-models.scorer coqui-stt-0.9.3-models.scorer

