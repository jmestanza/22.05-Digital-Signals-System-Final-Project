import simpleaudio as sa
import numpy as np


def playSound(arr, fs=44100):
    arr *= 32767 / max(abs(arr))
    arr = arr.astype(np.int16)
    play_obj = sa.play_buffer(arr, 1, 2, fs)
    play_obj.wait_done()