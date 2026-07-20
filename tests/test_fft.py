import numpy as np

from fftn.fft import compute_fft


# Señal de prueba
days = 100

x = np.arange(days)

signal = np.sin(2 * np.pi * x / 10)


freq, amp, phase = compute_fft(signal)


index = np.argmax(amp[1:]) + 1


print("Dominant frequency:")
print(freq[index])

print("Expected period:")
print(1 / abs(freq[index]))