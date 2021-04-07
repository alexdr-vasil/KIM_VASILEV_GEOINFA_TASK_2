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
print("\nFrequency:  ", frequency, "   Length:   ", length, "\n")

if frequency % 2 == 1:
    frequency += 1


# # 2. СОХРАНЕНИЕ В TXT ФАЙЛ - дополнительно (много времени)
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
data_1 = data[250 * frequency:(250 * frequency + frequency // 2)]
# ОГИБАЮЩАЯ УЧАСТКА ДЛЯ ДЕМОНСТРАЦИИ
data_am_1 = hilbert(data_1)

# ВЫВОД ГРАФИКА НА ЭКРАН
plt.plot(data_1)
plt.plot(data_am_1, "-o")
plt.xlabel("Номер")
plt.ylabel("Амплитуда")
plt.title("Сигнал")
plt.show()

# # 5. RESAMPLE
# # НОВАЯ ЧАСТОТА ДЛЯ ИЗОБРАЖЕНИЯ
# new_frequency = 2080
# number_of_samples = round(len(data_am) * float(new_frequency) / frequency)
# # ВЫЗОВ ФУНКЦИИ RESAMPLE ДЛЯ МАССИВА ОГИБАЮЩЕЙ ВСЕГО ГРАФИКА
# data_resampled = signal.resample(data_am, number_of_samples)

new_frequency = frequency
data_resampled = data_am

# 6. ПОЛУЧЕНИЕ ИЗОБРАЖЕНИЯ:

# РАЗБИЕНИЕ НА УЧАСТКИ ДЛИНОЙ В ПОЛОВИНУ ЧАСТОТЫ
frame_width = int(0.5 * new_frequency)
# РАЗМЕРЫ ИЗОБРАЖЕНИЯ - ШИРИНА И ВЫСОТА
w, h = frame_width, len(data_resampled) // frame_width
# СОЗДАНИЕ RGB ИЗОБРАЖЕНИЯ
image = Image.new('RGB', (w, h))

# ЗАПИСЬ В ПИКСЕЛИ
px, py = 0, 0
max = np.max(data_resampled)
min = np.min(data_resampled)
for p in range(len(data_resampled)):
    lum = int((data_resampled[p] - min) / (max - min) * 255)
    # проверка попадания в диапазон 0...255
    if lum < 0: lum = 0
    if lum > 255: lum = 255
    image.putpixel((px, py), (lum, lum, lum))
    # продвижение дальше по ширине картинки
    px += 1
    # переход на следующую строку, если вышли за пределы ширины
    if px >= w:
        if (py % 50) == 0:
            print(f"Line saved {py} of {h}")
        px = 0
        py += 1
        # выход из цикла, если превышена выстота
        if py >= h:
            break
# РАСТЯГИВАЕМ ИЗОБРАЖЕНИЕ ПО ДЛИНЕ В 2 РАЗА
image = image.resize((w, 3 * h))
# СОХРАНЯЕМ
image.save('Sputnic.png')
print("Successfully saved image 'Sputnic.png'")

# СЧИТАЕМ ВРУЧНУЮ С ГРАФИКА РАЗМЕР СИНХРОИМПУЛЬСА И РАССТОЯНИЕ МЕЖДУ МАКСИМУМАМИ
impulse_length = 84
delta = 14


def find_impulse(data, first_it):
    id = first_it
    for i in range(first_it, len(data) - 91, 1):
        counter = 0
        for j in range(0, impulse_length, delta):
            if data[i + j] > 0.3 * max or abs(data[i + j + 7] - data[i + j]) > max * 0.7 or abs(data[i + j + 7] - data[i + j]) < 0.3 * max:
                counter += 1
        if counter <= 2:
            id = i
            break
    return id


# пересохранение правильного массива
new_data = np.zeros((len(data_resampled), 1))
elem = int(0)
it = find_impulse(data_resampled, 0)
while it <= len(data_resampled) - int(new_frequency * 0.5):
    for j in range(it, it + int(new_frequency * 0.5), 1):
        new_data[elem] = data_resampled[j]
        elem += 1
    k = it + int(new_frequency * 0.5) - 500
    it = find_impulse(data_resampled, k)



w, h = frame_width, len(new_data) // frame_width
image = Image.new('RGB', (w, h))

px, py = 0, 0
for p in range(new_data.shape[0]):
    light = int((new_data[p]-min)/(max-min) * 255)
    if light < 0: light = 0
    image.putpixel((px, py), (light, light, light))
    px += 1
    if px >= w:
        if (py % 50) == 0:
            print(f"Line saved {py} of {h}")
        px = 0
        py += 1
        if py >= h:
            break
image = image.resize((w, 4*h))
image.save('Straight_picture.png')
print("Successfully saved image 'Straight_picture.png'")