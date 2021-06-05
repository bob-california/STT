import wave
import numpy as np
import streamlit as st
from stt import Model
import resampy

MODEL_PATH = "./coqui-stt-0.9.3-models.pbmm"
SCORER_PATH = "./coqui-stt-0.9.3-models.scorer"

model = Model(MODEL_PATH)
model.enableExternalScorer(SCORER_PATH)

st.title("Speech To Text")

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

    with st.spinner("Transcripting ..."):
        transcript = model.stt(audio)

    st.title("Transcript:")
    st.code(transcript)
