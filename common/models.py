from functools import cache

from TTS.api import TTS
from whispercpp import Whisper


@cache
def load_whisper(size: str):

    return Whisper(size)


@cache
def load_tts():

    return TTS("tts_models/multilingual/multi-dataset/xtts_v2").to('cpu')
