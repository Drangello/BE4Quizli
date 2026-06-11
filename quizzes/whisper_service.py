import whisper


def transcribe_audio(audio_path):
    """
    Transcribe audio file with Whisper.
    """

    model = whisper.load_model("base")
    result = model.transcribe(str(audio_path))

    return result["text"]