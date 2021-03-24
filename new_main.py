# ПОДКЛЮЧЕНИЕ БИБЛИОТЕК
import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# 1. ПОЛУЧЕНИЕ ЧАСТОТЫ И МАССИВА ДАННЫХ ИЗ WAV ФАЙЛА
frequency, data = wav.read('signal.WAV')
length = len(data)
print("Frequency:  ", frequency, "   Length:   ", length)


# # 2. СОХРАНЕНИЕ В TXT ФАЙЛ - дополнительно
# # ТЕКУЩАЯ ДИРЕКТОРИЯ С ФАЙЛОМ ПРОГРАММЫ
# direction = os.getcwd()
#
# # ФУНКЦИЯ, СОХРАНЯЮЩАЯ МАССИВ В TXT ФАЙЛ В ДИРЕКТОРИЮ ВЫШЕ
# def save(data, name):
#     np.savetxt(direction + '\\' + name + ".txt", data, fmt='%3.0d')
#
# # ВЫЗОВ ФУНКЦИИ, СОХРАНЕНИЕ В ФАЙЛ
# save(data, "sheet")


# 3. ФУНКЦИЯ, ВОЗВРАЩАЮЩАЯ ОГИБАЮЩУЮ СИГНАЛА
def hilbert(data):
    analytical_signal = signal.hilbert(data)
    amplitude_envelope = np.abs(analytical_signal)
    return amplitude_envelope


# ОГИБАЮЩАЯ ВСЕГО СИГНАЛА
data_am = hilbert(data)


# 4. ДЕМОНСТРАЦИЯ
# ВЫДЕЛЕНИЕ ОТДЕЛЬНОГО УЧАСТКА ДЛЯ ДЕМОНСТРАЦИИ
data_1 = data[250 * frequency:251 * frequency]
# ОГИБАЮЩАЯ УЧАСТКА ДЛЯ ДЕМОНСТРАЦИИ
data_am_1 = hilbert(data_1)

# ВЫВОД ГРАФИКА НА ЭКРАН
plt.plot(data_1)
plt.plot(data_am_1)
plt.xlabel("Номер")
plt.ylabel("Амплитуда")
plt.title("Сигнал")
plt.show()


# 5. RESAMPLE
# НОВАЯ ЧАСТОТА ДЛЯ ИЗОБРАЖЕНИЯ
new_frequency = 2080
number_of_samples = round(len(data_am) * float(new_frequency) / frequency)
# ВЫЗОВ ФУНКЦИИ RESAMPLE ДЛЯ МАССИВА ОГИБАЮЩЕЙ ВСЕГО ГРАФИКА
data_resampled = signal.resample(data_am, number_of_samples)

# 6. ПОЛУЧЕНИЕ ИЗОБРАЖЕНИЯ:

# РАЗБИЕНИЕ НА УЧАСТКИ ДЛИНОЙ В ПОЛОВИНУ ЧАСТОТЫ
frame_width = int(0.5 * new_frequency)
# РАЗМЕРЫ ИЗОБРАЖЕНИЯ - ДЛИНА И ШИРИНА
w, h = frame_width, len(data_resampled) // frame_width
# СОЗДАНИЕ RGB ЗОБРАЖЕНИЯ
image = Image.new('RGB', (w, h))

# ЗАПИСЬ В ПИКСЕЛИ
px, py = 0, 0
for p in range(len(data_resampled)):
    lum = int(data_resampled[p] // 32 - 32)
    if lum < 0: lum = 0
    if lum > 255: lum = 255
    image.putpixel((px, py), (lum, lum, lum))
    px += 1
    if px >= w:
        px = 0
        py += 1
        if py >= h:
            break
# РАСТЯГИВАЕМ ИЗОБРАЖЕНИЕ ПО ДЛИНЕ В 2 РАЗА
image = image.resize((2 * w, h))
# СОХРАНЯЕМ
image.save('Sputnic.png')
