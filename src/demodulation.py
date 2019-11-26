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

def getAudio(duration=15, fs = 44100):
    print("Start recording..")
    audio = sd.rec(int(duration * fs))
    sd.wait() # espera a gravação ser finalizada
    print("Record ended")
    return audio

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
    low_wave = np.abs(signal.hilbert(low_wave))
    high_wave = np.abs(signal.hilbert(high_wave))
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


def sincronizeBits(bits, INIT_STREAM='2wLQTcNgiXyP<{', END_STREAM='}>ggIVZMbi09VM', Fs=44100, baud=10):
    #sample=int(Fs/baud)
    #sync_init = bitsToWave(stringToBits(INIT_STREAM))
    #sync_end = bitsToWave(stringToBits(END_STREAM))
    #c_init = np.correlate(bits[:int(len(bits)/2)], sync_init)
    #c_end =  np.correlate(bits[int(len(bits)/2):], sync_end)
    #begin = np.where(c_init == np.amax(c_init))[0][0]+len(sync_init)
    #end = np.where(c_end == np.amax(c_end))[0][0]+int(len(bits)/2)
    #sync_bits = bits[begin:end+ int((8 - ((end-begin)/sample)%8)*sample)]
    #return sync_bits
    sync_init = stringToBits(INIT_STREAM)
    sync_end = stringToBits(END_STREAM)
    c_init = np.correlate(bits, sync_init)
    c_end = np.correlate(bits, sync_end)
    begin = np.where(c_init == np.amax(c_init))[0][0]+len(sync_init)
    end = np.where(c_end == np.amax(c_end))[0][0]
    plt.plot(c_init)
    plt.show()
    plt.plot(c_end)
    plt.show()

    return bits[begin: end]


if __name__ == '__main__':
    #fs, audio = wavfile.read('hello.wav')
    fs = 44100
    audio = getAudio(duration=200)[:,0]
    audio = np.float64(audio/(2**31 - 1))
    bitwave = FSKdemod(audio, Fs=fs)
    bits = bitwaveSample(bitwave)
    bits = sincronizeBits(bits)
    print(bitsToString(bits))
    plt.figure()
    plt.plot(bitwave)
    plt.xlim(420000, 470000)
    plt.show()

