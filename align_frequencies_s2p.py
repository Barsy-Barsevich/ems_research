import numpy as np

# --- НАСТРОЙКИ ---
input_file = "channel_model.s2p"   # Имя вашего исходного s2p файла
output_file = "AAA.s2p" # Имя исправленного файла для PyBERT

print("Чтение исходного файла .s2p...")
frequencies = []
s_data = []

# Читаем файл, игнорируя комментарии и строку параметров
with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('!') or line.startswith('#'):
            continue
        parts = list(map(float, line.split()))
        # В файле s2p в строке должно быть 1 число частоты + 4 числа для S11 и S21 
        # (либо 9 чисел, если S11, S21, S12, S22 записаны в одну строку)
        if len(parts) >= 5: 
            frequencies.append(parts[0])
            s_data.append(parts[1:9] if len(parts) == 9 else parts[1:5])

freq_old = np.array(frequencies)
data_old = np.array(s_data)

# Проверяем, сколько параметров в строке. Если s2p записан в сокращенном виде (только S11 и S21), 
# дублируем их для симметричного канала (S12=S21, S22=S11), так как PyBERT требует полную матрицу.
if data_old.shape[1] == 4:
    print("Обнаружено 2 параметра (S11, S21). Достраиваем до полной матрицы (S12, S22)...")
    full_data = np.zeros((data_old.shape[0], 8))
    full_data[:, 0:2] = data_old[:, 0:2] # S11
    full_data[:, 2:4] = data_old[:, 2:4] # S21
    full_data[:, 4:6] = data_old[:, 2:4] # S12 = S21
    full_data[:, 6:8] = data_old[:, 0:2] # S22 = S11
    data_old = full_data

# Переводим Magnitude/Angle (MA) в Real/Imaginary (RI) для точной интерполяции
data_ri = np.zeros_like(data_old)
for i in range(4): # 4 параметра: S11, S21, S12, S22
    mag = data_old[:, i*2]
    ang_rad = np.radians(data_old[:, i*2 + 1])
    real = mag * np.cos(ang_rad)
    imag = mag * np.sin(ang_rad)
    data_ri[:, i*2] = real
    data_ri[:, i*2 + 1] = imag

# Строим ИДЕАЛЬНО ЛИНЕЙНУЮ сетку частот от 0 ГГц (DC) до 10 ГГц с шагом 5 МГц
freq_new = np.arange(0.0, 10.005, 0.005) 
data_new_ri = np.zeros((len(freq_new), 8))

print("Интерполяция и выравнивание сетки...")
for i in range(8):
    # На краях диапазона (DC и выше 6 ГГц) используем крайние известные точки (left/right)
    data_new_ri[:, i] = np.interp(freq_new, freq_old, data_ri[:, i], left=data_ri[0, i], right=data_ri[-1, i])

# Переводим обратно в формат MA (Magnitude/Angle)
data_new_ma = np.zeros_like(data_new_ri)
for i in range(4):
    real = data_new_ri[:, i*2]
    imag = data_new_ri[:, i*2 + 1]
    mag = np.sqrt(real**2 + imag**2)
    ang = np.degrees(np.arctan2(imag, real))
    data_new_ma[:, i*2] = mag
    data_new_ma[:, i*2 + 1] = ang

print(f"Запись исправленного файла: {output_file}...")
with open(output_file, 'w') as f:
    f.write("! Fixed Touchstone file for PyBERT\n")
    f.write("! Linear frequency sweep from 0 to 10 GHz with 5 MHz step\n")
    f.write("# GHz S MA R 50.0\n")
    for f_val, d_row in zip(freq_new, data_new_ma):
        # Для файлов .s2p стандарт Touchstone требует запись всех 4 параметров в одну строку 
        # (Частота S11_mag S11_ang S21_mag S21_ang S12_mag S12_ang S22_mag S22_ang)
        data_str = " ".join([f"{x:e}" for x in d_row])
        f.write(f"{f_val:e} {data_str}\n")

print("Готово! Файл .s2p успешно адаптирован для PyBERT.")

