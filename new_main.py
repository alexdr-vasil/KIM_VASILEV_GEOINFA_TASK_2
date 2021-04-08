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


# # 2. СОХРАНЕНИЕ В TXT ФАЙЛ - дополнительно (занимает много времени)
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

# 4. ДЕМОНСТРАЦИЯ, ПО КОТОРОЙ МЫ НАХОДИМ РАССТОЯНИЕ МЕЖДУ МАКСИМУМОМ И МИНИМУМОМ
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

new_frequency = frequency
data_resampled = data_am

# # 5. RESAMPLE (ПРИМ. ТЕРЯЕТСЯ КАЧЕСТВО! ДОПОЛНИТЕЛЬНЫЙ ПУНКТ)
# # НОВАЯ ЧАСТОТА ДЛЯ ИЗОБРАЖЕНИЯ
# new_frequency = 2080
# number_of_samples = round(len(data_am) * float(new_frequency) / frequency)
# # ВЫЗОВ ФУНКЦИИ RESAMPLE ДЛЯ МАССИВА ОГИБАЮЩЕЙ ВСЕГО ГРАФИКА
# data_resampled = signal.resample(data_am, number_of_samples)


# 6. ПОЛУЧЕНИЕ ИЗОБРАЖЕНИЯ(НЕ ПРЯМОЕ):

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
            # ПО СТРОКЕ ОЧЕНЬ УДОБНО ОТСЛЕЖИВАТЬ, РАБОТАЕТ ЛИ ПРОГРАММА ВООБЩЕ
            print(f"Saved {py} of {h}")
        px = 0
        py += 1
        # выход из цикла, если превышена выстота
        if py >= h:
            break
# РАСТЯГИВАЕМ ИЗОБРАЖЕНИЕ ПО ДЛИНЕ В 3 РАЗА
image = image.resize((w, 3 * h))
# СОХРАНЯЕМ
image.save('Sputnic.png')
print("Successfully saved image 'Sputnic.png'")

# ТЕПЕРЬ МЫ МОЖЕМ НАЙТИ КОЛИЧЕСТВО ПОЛОС В СИНХРОИМПУЛЬСЕ, А ЗАТЕМ РАЗМЕР ПО ГРАФИКУ ВЫШЕ

# 7. ПОЛУЧЕНИЕ ИЗОБРАЖЕНИЯ(ПРЯМОЕ):

# СЧИТАЕМ ВРУЧНУЮ С ГРАФИКА РАЗМЕР СИНХРОИМПУЛЬСА И РАССТОЯНИЕ МЕЖДУ МАКСИМУМАМИ
impulse_length = 84  # РАЗМЕР ИМПУЛЬСА, 7 ПОЛОС - 6 ПЕРЕПАДОВ, МЕЖДУ КОТОРЫМИ 14, ИТОГО 84
delta = 7  # ТОЧКИ МЕЖДУ МАКС. И МИН., МЕЖДУ ДВУМЯ МАКС. И ДВУМЯ МИН. В 2 РАЗА БОЛЬШЕ (14)


# НАХОЖДЕНИЕ НАЧАЛЬНОГО ЭЛЕМЕНТА СИНХРОИМПУЛЬСА
def impulse(data_resampled, k):
    # ПУСТЬ ПЕРЕДАННЫЙ НОМЕР _ НАЧАЛО ИМПУЛЬСА
    n = k
    for i in range(k, len(data_resampled) - 91):
        # СЧЁТЧИК НЕПРАВИЛЬНЫХ ПЕРЕПАДОВ
        wrong = 0
        # ПРОХОД ПО МИНИМУМАМ
        for j in range(0, impulse_length, 2 * delta):
            # ПРОВЕРКА НА МИНИМУМ И ПЕРЕПАД
            if data_resampled[i + j] > 0.3 * max or abs(
                    data_resampled[i + j + delta] - data_resampled[i + j]) > max * 0.7 or abs(
                    data_resampled[i + j + delta] - data_resampled[i + j]) < 0.3 * max:
                wrong += 1
        # НЕКОТОРЫЕ МОГУТ НЕ СОЙТИСЬ - ТАМ ПРОМЕЖУТОК, НАПРИМЕР, НЕ 7, А 6 ТОЧЕК (ГРАФИК)
        # ИЗ-ЗА ЭТОГО В НЕКОТОРЫХ МЕСТАХ ЧБ ПОЛОСКИ РАЗМЫВАЮТСЯ
        if wrong <= 2:
            n = i
            break
    return n


# СОЗДАЕМ МАССИВ (ИЗНАЧАЛЬНО НУЛЕЙ) ДЛЯ ПРЯМОГО ИЗОБРАЖЕНИЯ
data_straight = np.zeros((len(data_resampled), 1))

# НАЧИНАЕМ ПРОВЕРКУ С НАЧАЛА
num = 0
current = impulse(data_am, 0)

while current <= len(data_resampled) - new_frequency // 2:
    # ЗАПИСЫВАЕМ СТРОКУ В НОВЫЙ МАССИВ
    for j in range(current, current + new_frequency // 2):
        # ЗАПИСЫВАЕМ ЗНАЧЕНИЯ В НАШ МАССИВ
        data_straight[num] = data_resampled[j + 32]
        # "+ 32"  - ПОДГОНКА ИЗОБРАЖЕНИЯ, ЧТОБЫ НАЧИНАЛОСЬ С ПОЛОС
        num += 1

    # СДВИГАЕМ ГДЕ-ТО НА 500 МЕНЬШЕ, ЧТОБЫ СЛУЧАЙНО НЕ ПРОПУСТИТЬ
    k = current + new_frequency // 2 - 500
    current = impulse(data_resampled, k)


# РАЗМЕРЫ ПРЯМОГО ИЗОБРАЖЕНИЯ - ШИРИНА И ВЫСОТА
w, h = frame_width, len(data_straight) // frame_width
# СОЗДАНИЕ RGB ИЗОБРАЖЕНИЯ
image = Image.new('RGB', (w, h))
# ЗАПИСЬ В ПИКСЕЛИ
px, py = 0, 0
max = np.max(data_straight)
min = np.min(data_straight)
for p in range(len(data_straight)):
    lum = int((data_straight[p] - min) / (max - min) * 255)
    # проверка попадания в диапазон 0...255
    if lum < 0: lum = 0
    if lum > 255: lum = 255
    image.putpixel((px, py), (lum, lum, lum))
    # продвижение дальше по ширине картинки
    px += 1
    # переход на следующую строку, если вышли за пределы ширины
    if px >= w:
        if (py % 50) == 0:
            # ПО СТРОКЕ ОЧЕНЬ УДОБНО ОТСЛЕЖИВАТЬ, РАБОТАЕТ ЛИ ПРОГРАММА ВООБЩЕ
            print(f"Saved {py} of {h}")
        px = 0
        py += 1
        # выход из цикла, если превышена выстота
        if py >= h:
            break
# РАСТЯГИВАЕМ ИЗОБРАЖЕНИЕ В 3 РАЗА
image = image.resize((w, 3 * h))
# СОХРАНЯЕМ
image.save('Straight_picture.png')
print("Successfully saved image 'Straight_picture.png'")
