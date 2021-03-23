# ПОДКЛЮЧЕНИЕ БИБЛИОТЕК
import wave, struct
import numpy as np
import matplotlib.pyplot as plt
import os

direction = os.getcwd()


def save(data, name):
    np.savetxt(direction + '\\' + name + ".txt", data, fmt='%3.0d')


wavefile = wave.open('signal.WAV', 'r')

frequency = wave.Wave_read.getframerate(wavefile)

length = wavefile.getnframes()

print(frequency, length)
sheet = np.arange(length)
array = []
for i in range(0, length):
    wavedata = wavefile.readframes(1)
    data = struct.unpack("<h", wavedata)
    sheet[i] = int(data[0])
    array.append(int(data[0]))

save(sheet, "sheet")

current_array = []
T = []
for i in range(1000000, 1000000+frequency*20):
    current_array.append(array[i])
    T.append(i)

fig = plt.figure()
plt.plot(T, current_array)
plt.show()
