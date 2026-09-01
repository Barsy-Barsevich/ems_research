import matplotlib.pyplot as plt
import numpy as np

a = []
for i in range(250*2): a.append(0.0)
for i in range(500*2): a.append(1.0)
for i in range(251*2): a.append(0.0)

e = np.fft.fft(a)

# e = e[:len(e)//2]

with open('data_i.txt', 'w') as f:
    for elem in e:
        f.write(str(float(elem)) + '\n')

plt.plot(np.fft.ifft(e))
plt.grid()
plt.show()