'''
    Script for FSK modulation
        Frequêncy modulation based on digital or binary information

'''

import numpy as np
import matplotlib.pyplot as plt

def stringToBits(string: str)->np.array:
    narray = np.array(list(map(ord,string)),dtype="uint8") # Transforma a string num array de uint8
    return np.unpackbits(narray) # converte todos os bytes em bits (array de 1's e 0's)

def randomBitArray(n):
    return np.random.randint(0,2,n)

def bitsToWave(bits, Fs=44100, baud=10):
    sample_bit = int(Fs/baud)
    wave = np.repeat(bits, sample_bit)
    wave = 2.0 * wave - 1.0
    return wave

def FSKMod(bitwave, Fs = 44100, f0 = 1500.0, df = 500.0):
    time_end = len(bitwave)/Fs
    t = np.linspace(0.0, time_end, len(bitwave))
    fsk = np.sin(2.0*np.pi*(f0 + df*bitwave)*t)
    return [t, fsk]

bits = randomBitArray(10)
mb = bitsToWave(bits)
t, x = FSKMod(mb, f0=30.0, df=10.0)

## Plotting Data ##
ax_bit = plt.subplot(211)
ax_bit.plot(t, mb)
ax_bit.set_ylabel('Mensagem binária')
ax_bit.grid(True)

ax_mod = plt.subplot(212)
ax_mod.plot(t, x)
ax_mod.set_ylabel('Mensagem modulada')
ax_mod.set_xlabel('Tempo (s)')
ax_mod.grid(True)

plt.show()
