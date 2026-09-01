import matplotlib.pyplot as plt
import numpy as np

_s21 = []
with open('s21.txt', 'r') as f:
    _s21 = f.read().split()
s21_len = len(_s21)
s21 = []
for elem in _s21:
    s21.append(float(elem))


a = []
for i in range(s21_len): a.append(0.0)
for i in range(s21_len): a.append(1.0)
a = np.array(a)
A = np.fft.fft(a)
# A_abs = np.abs(A)
A_abs = A

for i in range(s21_len):
    A_abs[i] *= s21[i]
for i in range(s21_len):
    A_abs[s21_len+i] *= s21[s21_len-1-i]

plt.plot(a)
plt.plot(np.fft.ifft(A_abs))
plt.grid()
plt.show()