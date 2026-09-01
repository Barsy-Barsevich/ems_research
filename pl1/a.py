import numpy as np
import matplotlib.pyplot as plt

a_i = []
with open('data_i.txt', 'r') as f:
    a_i = f.read().split()

s21 = []
with open('s21.txt', 'r') as f:
    s21 = f.read().split()
s21_len = len(s21)
for i in range(s21_len):
    s21.append(s21[s21_len-1-i])

X_i = []
for elem in a_i:
    X_i.append(float(elem))

X_o = []
for i in range(len(s21)):
    X_o.append(float(s21[i]) * X_i[i])

x_o = np.fft.ifft(X_o)
x_i = np.fft.ifft(X_i)

x_o_avg = x_o[0] - 0

for i in range(len(x_o)):
    x_o[i] -= x_o_avg

plt.plot(x_i)
plt.plot(x_o)
plt.grid()
plt.show()