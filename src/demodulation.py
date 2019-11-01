'''
    Script for FSK demodulation
        Frequêncy modulation based on digital or binary information

'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

b, a = signal.butter(5, [800, 1600], btype='band', analog=True)
w, h = signal.freqs(b, a)
b, a = signal.butter(7, [800, 1600], btype='band', analog=True)
w2, h2 = signal.freqs(b, a)
b, a = signal.butter(9, [800, 1600], btype='band', analog=True)
w3, h3 = signal.freqs(b, a)

plt.semilogx(w, 20 * np.log10(abs(h)), label='ordem 5')
plt.semilogx(w2, 20 * np.log10(abs(h2)), label='ordem 7')
plt.semilogx(w3, 20 * np.log10(abs(h3)), label='ordem 9', color='red')

plt.xlabel('Frequência (Hz)')
plt.ylabel('Amplitude (dB)')
plt.grid(which='both', axis='both')
plt.axvline(800, color='green', linestyle='--', linewidth='1') # cutoff frequency
plt.axvline(1600, color='green', linestyle='--', linewidth='1') # cutoff frequency
plt.xlim((100, 10000))
plt.ylim((-100,10))

plt.legend()
plt.show()