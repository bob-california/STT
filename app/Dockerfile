FROM debian:bullseye-slim


RUN apt update -y && apt install -y sox libgomp1 libstdc++6 libpthread-stubs0-dev python3 python3-pip ffmpeg libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

RUN pip3 install --upgrade pip && pip3 install stt streamlit resampy wavio sounddevice

WORKDIR /app

ENTRYPOINT [ "streamlit", "run", "app.py" ]
