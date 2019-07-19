from scipy.fftpack import fft
import numpy as np
from scipy.signal import butter, lfilter
from scipy.signal import freqs
from util_python import Senial

def butter_lowpass(cutOff, fs, order=5):
    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = butter(order, normalCutoff, btype='low', analog = False)
    return b, a

def butter_lowpass_filter(data, cutOff, fs, order=4):
    b, a = butter_lowpass(cutOff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def fourierTransform(senial):
    # Hacemos una aproximacion discreta muy buena de la transformada de fourier bilateral de la senial

    frecuencyStep = 1 / ((len(senial.xvar)-1) * senial.separation)#la senial debe estar mostrada de manera equiespaciada

    fftOutput = 1/len(senial.values) * abs(fft(senial.values))

    iValsPositive = []
    ampPositive = []
    iValsNegative = []
    ampNegative = []

    for i in range(len(fftOutput)//4):
        iValsPositive.append(i)
        ampPositive.append(fftOutput[i])

    i = -1
    while len(iValsNegative) + len(iValsPositive) < len(fftOutput)//2:
        iValsNegative.append(i)
        ampNegative.append(fftOutput[i])
        i = i - 1

    iValsNegative.reverse()
    ampNegative.reverse()

    iVals = iValsNegative + iValsPositive
    amplitud = ampNegative + ampPositive

    frecuencies = [frecuencyStep * i for i in iVals]

    final_freq = []
    final_amp = []

    for i in range(len(frecuencies)):
        #if abs(frecuencies[i]) < 10*1e3:
        final_freq.append(frecuencies[i])
        final_amp.append(amplitud[i])

    senial = Senial.Senial(final_freq, final_amp)

    return senial


    # precise_freq = []
    # precise_amp = []
    #
    # index = 0
    # for i in np.linspace(-10*1e3, 10*1e3, 200000):
    #     precise_freq.append(i)
    #     if index < len(final_freq) and abs(i - final_freq[index]) < Globals.EPS_freq:
    #         precise_amp.append(final_amp[index])
    #         index += 1
    #     else:
    #         precise_amp.append(0)
    # print(frecuencyStep)
    # precise_amp = butter_lowpass_filter(
    #     data=precise_amp,
    #     cutOff=2/frecuencyStep,
    #     fs=1/(precise_freq[1] - precise_freq[0]),
    #     order=6
    # )
    # precise_amp = [abs(i)*200 for i in precise_amp]

    #return Senial.Senial(final_freq, final_amp)
