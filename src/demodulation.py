'''
    Script for FSK demodulation
        Frequêncy modulation based on digital or binary information

'''

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

from modulation import stringToBits, bitsToString, bitsToWave


sd.default.samplerate = 44100
sd.default.channels = 1


def getAudio(duration=15, fs=44100):
    print("Start recording..")
    audio = sd.rec(int(duration * fs))
    sd.wait()  # espera a gravação ser finalizada
    print("Record ended")
    return audio


def FSKdemod(wave, Fs=44100, f0=1400.0, df=500.0, verbose=False):
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
    if verbose:
        plt.subplot(211)
        plt.plot(low_wave)
        plt.subplot(212)
        plt.plot(high_wave)
    # Deteccao de envelope
    low_wave = np.abs(signal.hilbert(low_wave))
    high_wave = np.abs(signal.hilbert(high_wave))
    if verbose:
        plt.subplot(211)
        plt.plot(low_wave)
        plt.subplot(212)
        plt.plot(high_wave)
    # Subtracao dos sinais para comparacao
    bitwave = high_wave/max(high_wave) - low_wave/max(low_wave)
    bitwave[bitwave > 0.0] = 1.0
    bitwave[bitwave <= 0.0] = 0.0
    # Retorna uma bitwave de 0's e 1's
    return bitwave


def bitwaveSample(bitwave, Fs=44100, baud=10):
    sample_bit = int(Fs/baud)

    # Subamostra dez amostras e faz a media
    bits = np.zeros((int(len(bitwave)/sample_bit), ), dtype=np.int32)
    for i in range(len(bits)):
        center = int((2*i+1)*(sample_bit/2))
        dev = 5
        bits[i] = np.rint(np.mean(bitwave[center-dev:center+dev]))

    return bits


def sincronizeBits(bits, INIT_STREAM='2wLQTcNgiXyP<{', END_STREAM='}>ggIVZMbi09VM', Fs=44100, baud=10, verbose=True):
    sync_init = stringToBits(INIT_STREAM)
    sync_end = stringToBits(END_STREAM)
    c_init = np.correlate(bits, sync_init)
    c_end = np.correlate(bits, sync_end)
    begin = np.where(c_init == np.amax(c_init))[0][0]+len(sync_init)
    end = np.where(c_end == np.amax(c_end))[0][0]
    if verbose:
        plt.subplot(211)
        plt.plot(c_init)
        plt.subplot(212)
        plt.plot(c_end)

    return bits[begin: end]


def bitErrorRate(original_bits: np.array, received_bits: np.array):
    # Ambos os vetores devem ter o mesmo tamanho
    diff = np.sum((original_bits - received_bits)**2.0)
    return diff/float(len(original_bits))


if __name__ == '__main__':
    fs = 44100
    audio = getAudio(duration=30)[:,0]
    print(audio)
    print(audio.shape)
    audio = np.float64(audio/(2**31 - 1))
    bitwave = FSKdemod(audio, Fs=fs, verbose=True)
    bits = bitwaveSample(bitwave,baud=25)
    bits = sincronizeBits(bits, verbose=True)
    try:
        print(bitErrorRate(stringToBits("LJlqRK0sLItJH3dzgpoYb0g79fXs7u2dr67lxY2GYhTiiwyH7y"), bits))
        print(bits)
        print("LJlqRK0sLItJH3dzgpoYb0g79fXs7u2dr67lxY2GYhTiiwyH7y")
    except:
        print("nao leu")
    plt.figure()
    plt.plot(bitwave)
    plt.xlim(420000, 470000)
    plt.show()

