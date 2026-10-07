import pandas as pd
import numpy as np

# 1. Загружаем CSV (проверь, что разделитель - табуляция или запятая. 
# Если файл разделен табуляцией, используй sep='\t', если запятой - sep=',')
df = pd.read_csv('ems/results/Port_0_data.csv', sep=',') # Попробуй sep=',' если возникнет ошибка

# 2. Извлекаем и конвертируем данные
# Частота: из МГц в ГГц
freq_ghz = df['Frequency [MHz]'] / 1000.0

# S11 (отражение на порту 1): берем модуль и переводим фазу из радиан в градусы
s11_mag = df['|S0-0| [-]']
s11_ang = np.degrees(df['Arg(S0-0) [rad]'])

# S21 (передача от порта 0 к порту 1): модуль и фаза в градусах
s21_mag = df['|S1-0| [-]']
s21_ang = np.degrees(df['Arg(S1-0) [rad]'])

# 3. Применяем допущение о симметрии и взаимности для пассивного канала
s22_mag = s11_mag.copy()
s22_ang = s11_ang.copy()
s12_mag = s21_mag.copy()
s12_ang = s21_ang.copy()

# 4. Собираем в новый DataFrame в строгом порядке для Touchstone:
# Freq, S11, S21, S12, S22
touchstone_df = pd.DataFrame({
    'freq': freq_ghz,
    's11_mag': s11_mag, 's11_ang': s11_ang,
    's21_mag': s21_mag, 's21_ang': s21_ang,
    's12_mag': s12_mag, 's12_ang': s12_ang,
    's22_mag': s22_mag, 's22_ang': s22_ang
})

# 5. Сохраняем в формат Touchstone (.s2p)
output_file = 'channel_model.s2p'
with open(output_file, 'w') as f:
    f.write("! Touchstone file converted from gerber2ems Port_0_data.csv\n")
    f.write("! Assumption: Channel is reciprocal and symmetric (S11=S22, S21=S12)\n")
    f.write("# GHz S MA R 50.0\n") # MA = Magnitude/Angle, R 50.0 = 50 Ом
    
    # Записываем строки данных
    for index, row in touchstone_df.iterrows():
        f.write(f"{row['freq']:.6e} "
                f"{row['s11_mag']:.6e} {row['s11_ang']:.6f} "
                f"{row['s21_mag']:.6e} {row['s21_ang']:.6f} "
                f"{row['s12_mag']:.6e} {row['s12_ang']:.6f} "
                f"{row['s22_mag']:.6e} {row['s22_ang']:.6f}\n")

print(f"✅ Файл успешно сохранен как {output_file}")
print("Не забудь проверить в PyBERT галочку 'Enforce Passivity' при загрузке!")
