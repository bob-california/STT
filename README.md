# Speech to Text

![app frontend](./images/STT_app.png)

Small app for Speech To Text model development.

- Easy to upload audio file
- Execute model seamlessly on input
- Output clear and nice for user

Technologies used:

- [Coqui STT](https://github.com/coqui-ai/STT)
- [streamlit)](https://github.com/streamlit/streamlit)

Download the model from coqui before starting:

```bash
wget https://github.com/coqui-ai/STT/releases/download/v0.9.3/coqui-stt-0.9.3-models.pbmm
wget https://github.com/coqui-ai/STT/releases/download/v0.9.3/coqui-stt-0.9.3-models.scorer
```

Run following command to start app:

```bash
docker-compose up -d
```

You can then access the app at http://localhost:8501.

Some test audio files are in the `audio` folder.
