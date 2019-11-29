'''
    Script for FSK modulation
        Frequency modulation based on digital or binary information

'''

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io import wavfile


def stringToBits(string: str) -> np.array:
    # Transforma a string num array de uint8
    narray = np.array(list(map(ord, string)), dtype="uint8")
    # converte todos os bytes em bits (array de 1's e 0's)
    return np.unpackbits(narray)


def bitsToString(bits: np.array) -> str:
    # Transforma o array de bits em um array de uint8
    packed = np.packbits(bits)
    # Converte o array de uint8 em caracteres e concatena em uma string
    return str("".join(map(chr, packed)))


def randomBitArray(n):
    return np.random.randint(0, 2, n)


def bitsToWave(bits, Fs=44100, baud=10):
    sample_bit = int(Fs/baud)
    wave = np.repeat(bits, sample_bit)
    wave = 2.0 * wave - 1.0
    return wave


def FSKMod(bitwave, Fs=44100, f0=1400.0, df=500.0):
    time_end = len(bitwave)/Fs
    t = np.linspace(0.0, time_end, len(bitwave))
    fsk = np.sin(2.0*np.pi*(f0 + df*bitwave)*t)
    return [t, fsk]


def playSound(t, Fs=44100):
    sd.play(t, Fs)


def sincronizeMessage(s: str, INIT_STREAM='2wLQTcNgiXyP<{', END_STREAM='}>ggIVZMbi09VM') -> str:
    # coloca um caractere de inicio e de final na string
    return str(INIT_STREAM) + s + str(END_STREAM)


if __name__ == '__main__':

    bits = stringToBits(sincronizeMessage("LJlqRK0sLItJH3dzgpoYb0g79fXs7u2dr67lxY2GYhTiiwyH7y"))
    mb = bitsToWave(bits,baud=25)
    t, x = FSKMod(mb)

    playSound(x)
    # Espera o som acabar para continuar o script
    sd.wait()

    
#    wavfile.write('hello.wav', 44100, np.int32((2**31 - 1) * x))
#
#    ## Plotting Data ##
#    ax_bit = plt.subplot(211)
#    ax_bit.plot(t, mb)
#    ax_bit.set_ylabel('Mensagem binária')
#    ax_bit.grid(True)
#
#    ax_mod = plt.subplot(212)
#    ax_mod.plot(t, x)
#    ax_mod.set_ylabel('Mensagem modulada')
#    ax_mod.set_xlabel('Tempo (s)')
#    ax_mod.grid(True)
#
#    plt.show()
