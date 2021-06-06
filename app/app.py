import os
import wave

import numpy as np
import resampy
import sounddevice as sd
import streamlit as st
import wavio
from stt import Model

WAVE_OUTPUT_FILE = "recorded.wav"


def main():
    st.header("Speech To Text")

    app_mode = st.sidebar.selectbox("Choose app mode", ["File upload", "Mic recording"])

    st.subheader(app_mode)

    model_path, scorer_path = choose_model()
    model = Model(model_path)
    model.enableExternalScorer(scorer_path)
    if app_mode == "File upload":
        app_file_upload(model)
    else:
        app_mic(model)


def choose_model():
    model_choice = st.sidebar.selectbox(
        "Choose model for transcription", os.listdir("/models")
    )
    model_folder = os.path.join("/models", model_choice)
    scorer_file = next(
        filter(lambda file: file.endswith(".scorer"), os.listdir(model_folder))
    )
    model_file = next(
        filter(lambda file: file.endswith(".pbmm"), os.listdir(model_folder))
    )
    return os.path.join(model_folder, model_file), os.path.join(
        model_folder, scorer_file
    )


def app_file_upload(model):
    audio_file = st.file_uploader("Upload a WAVE file to generate transcript", "wav")

    if audio_file is not None:
        st.audio(audio_file, format="audio/wav")

        raw = wave.open(audio_file)

        sample_rate = raw.getframerate()
        audio = np.frombuffer(raw.readframes(raw.getnframes()), np.int16)
        if sample_rate != model.sampleRate():
            st.warning(
                f"Warning: original sample rate ({sample_rate}) is different than {model.sampleRate()}hz. Resampling might produce erratic speech recognition."
            )
            audio = resampy.resample(audio, sample_rate, model.sampleRate())

        with st.spinner("Transcribing ..."):
            transcript = model.stt(audio)

        st.title("Transcript:")
        st.code(transcript)


def record(duration=5, fs=16000):
    sd.default.samplerate = fs
    sd.default.channels = 1
    audio = sd.rec(int(duration * fs), dtype=np.int16)
    sd.wait(duration)
    return audio


def app_mic(model):
    duration = st.slider(
        "Select record duration (in seconds)", min_value=3, max_value=10
    )
    if st.button("Record"):
        fs = 44100
        with st.spinner(f"Recording for {duration} seconds"):
            audio = record(duration, fs)
        wavio.write(WAVE_OUTPUT_FILE, audio, fs, sampwidth=2)
        st.audio(WAVE_OUTPUT_FILE)
        audio = np.frombuffer(audio, dtype=np.int16)
        audio = resampy.resample(audio, fs, model.sampleRate())
        with st.spinner("Transcribing ..."):
            transcript = model.stt(audio)
        st.title("Transcript:")
        st.code(transcript)


if __name__ == "__main__":
    main()
