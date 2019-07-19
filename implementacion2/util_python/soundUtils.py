import numpy as np
import simpleaudio as sa
from pydub import AudioSegment
from scipy.io.wavfile import read,write


#IMPORTANTE!
#Primero bajar FMMPEG desde https://ffmpeg.org/download.html
#Hay que agregar C:\FFMPEG\bin  al path de variables de entorno
#link de como hacerlo: https://www.youtube.com/watch?v=pHR3ttH5t-w

#Link que hizo todo andar
# https://stackoverflow.com/questions/51219531/pydub-unable-to-locte-ffprobe



FFMPEGLoc = "C:\\FFMPEG\\bin\\"

AudioSegment.converter = "ffmpeg.exe"
AudioSegment.ffmpeg = "ffmpeg.exe"
AudioSegment.ffprobe = "ffprobe.exe"


def playSound(arr, fs=44100, volume=100,runWhenEnd = None):
    arr *= 32767 / max(abs(arr))* (volume/100)
    arr = arr.astype(np.int16)
    play_obj = sa.play_buffer(arr, 1, 2, fs)
    play_obj.wait_done()
    if runWhenEnd:
        runWhenEnd()


# def read(f, normalized=False):
#     """MP3 to numpy array"""
#     a = AudioSegment.from_mp3(f)
#     y = np.array(a.get_array_of_samples())
#     if a.channels == 2:
#         y = y.reshape((-1, 2))
#     if normalized:
#         return a.frame_rate, np.float32(y) / 2**15
#     else:
#         return a.frame_rate, y
#
#
# def write(f, sr, x, normalized=False):
#     """numpy array to MP3"""
#     channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
#     if normalized:  # normalized array - each item should be a float in [-1, 1)
#         y = np.int16(x * 2 ** 15)
#     else:
#         y = np.int16(x)
#     song = AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
#     song.export(f, format="mp3", bitrate="320k")


def reescale(sound, volume):
    sound *= volume / 100

