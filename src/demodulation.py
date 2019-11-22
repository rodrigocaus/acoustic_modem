'''
    Script for FSK demodulation
        Frequêncy modulation based on digital or binary information

'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile


def FSKdemod(wave, Fs=44100, f0=1400.0, df=500.0):
    low_freq = f0 - df
    high_freq = f0 + df
    # Criacao dos filtros de Butterworth (passa faixa em high\low_freq +\- 100Hz)
    filter_order = 5
    dev = 100
    sos_low = signal.butter(filter_order, [(
        low_freq - dev), (low_freq + dev)], btype='band', fs=Fs, output='sos')
    sos_high = signal.butter(filter_order, [(
        high_freq - dev), (high_freq + dev)], btype='band', fs=Fs, output='sos')
    # Filtragem da entrada
    low_wave = signal.sosfilt(sos_low, wave)
    high_wave = signal.sosfilt(sos_high, wave)
    # Deteccao de envelope
    low_wave = low_wave**2.0
    high_wave = high_wave**2.0
    # Subtracao dos sinais para comparacao
    return high_wave - low_wave


def bitwaveSample(bitwave, Fs=44100, baud=10):
    return 0


def sincronizeBits(bits, INIT_STREAM='2wLQTcNgiXyP<{', END_STREAM='}>ggIVZMbi09VM'):
    return 0


fs, audio = wavfile.read('hello.wav')
audio = np.float64(audio/(2**31 - 1))
level = FSKdemod(audio, Fs=fs)

plt.plot(level)
plt.xlim(604000, 605000)
plt.show()
