import ffmpeg

import numpy as np

from common.models import load_tts, load_whisper


def speechToText(speech: bytes) -> str:
    stream = ffmpeg.input('pipe:', threads=0)
    stream = ffmpeg.output(
        stream, "-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000
    )
    out, _ = ffmpeg.run(
        stream,
        cmd=["ffmpeg", "-nostdin"],
        capture_stdout=True,
        capture_stderr=True,
        input=speech,
    )

    arr = (
        (
            np.frombuffer(out, np.int16).flatten().astype(np.float32)
        ) / pow(2, 15)
    )

    w = load_whisper('tiny')

    result = w.transcribe(arr)
    text = w.extract_text(result)

    return ''.join(text)


def textToSpeech(text: str, reference_voice_path: str, output_path: str):
    tts = load_tts()

    tts.tts_to_file(
        text,
        speaker_wav=reference_voice_path,
        language="en",
        file_path=output_path,
    )
