# ПОДКЛЮЧЕНИЕ БИБЛИОТЕК
import wave, struct
import numpy as np
import matplotlib.pyplot as plt
import os

# УКАЗАНИЕ НА ТЕКУЩУЮ ДИРЕКТОРИЮ ПАПКИ С ФАЙЛОМ MAIN
direction = os.getcwd()


# ФУНКЦИЯ, СОХРАНЯЮЩАЯ В ТЕКУЩУЮ ДИРЕКТОРИЮ(ВЫШЕ) TXT ФАЙЛ
def save(data, name):
    np.savetxt(direction + '\\' + name + ".txt", data, fmt='%3.0d')


# ОТКРЫТИЕ СЧИТЫВАНИЯ WAV ФАЙЛА
wavefile = wave.open('signal.WAV', 'r')

# НАХОЖДЕНИЕ ЧАСТОТЫ ДИСКРЕТЕЗАЦИИ И ДЛИНЫ МАССИВА ФАЙЛОВ
frequency = wave.Wave_read.getframerate(wavefile)
length = wavefile.getnframes()

# ВЫВОД ЧАСТОТЫ И ДЛИНЫ НА ЭКРАН
print("Frequency:  ", frequency, "    Length:  ", length)

# СОЗДАНИЕ МАССИВА ПОД ПОЛУЧЕННУЮ ДЛИНУ
sheet = np.arange(length)

# ПОЛУЧЕНИЕ ДАННЫХ МАССИВА
for i in range(0, length):
    wavedata = wavefile.readframes(1)
    data = struct.unpack("<h", wavedata)
    sheet[i] = int(data[0])

# СОХРАНЕНИЕ В ФАЙЛ
save(sheet, "sheet")

# ПОЛОВИНА ЧАСТОТЫ, ПУСТОЙ ОБЩИЙ("ДВУМЕРНЫЙ") МАССИВ, ОДИНАРНЫЙ МАССИВ ДЛЯ РАЗБИЕНИЯ НА УЧАСТКИ
l = frequency // 2
total = []
single = []

# РАЗБИЕНИЕ НА УЧАСТКИ ДЛИНОЙ В ПОЛОВИНУ ЧАСТОТЫ
for j in range(0, length // l):
    for i in range(0, l):
        single.append(sheet[i + l * j])
    total.append(single)
    single = []

# ВЫВОД ГРАФИКОВ(БЕСКОНЕЧНЫЙ)
print("Enter number:")
n = int(input())
while n != -1:
    current_array = []
    T = []
    for i in range(l * (n - 1), l * n):
        current_array.append(sheet[i])
        T.append(i)

    fig = plt.figure()
    plt.plot(T, current_array)
    plt.show()
    print("Enter number:")
    n = int(input())
