import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos
pwm = pd.read_csv('pwm.txt', sep='\t')
pwm2 = pd.read_csv('pwm2.txt', sep='\t')

# Convertir la columna de tiempo a microsegundos para mejor legibilidad
pwm['time_us'] = pwm['time'] * 1e6
pwm2['time_us'] = pwm2['time'] * 1e6

# Encontrar el punto medio
mid_index = len(pwm) // 2
mid_time = pwm.iloc[mid_index]['time_us']

# Definir la ventana de 20 microsegundos alrededor del punto medio
window_width = 20  # microsegundos
t_min = mid_time - window_width / 2
t_max = mid_time + window_width / 2

# Filtrar datos dentro de la ventana
pwm_window = pwm[(pwm['time_us'] >= t_min) & (pwm['time_us'] <= t_max)]
pwm2_window = pwm2[(pwm2['time_us'] >= t_min) & (pwm2['time_us'] <= t_max)]

# Crear figura con subgráficos
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Gráfico 1: PWM - V(v_cuad) y V(v_triag)
ax1 = axes[0]
ax1.plot(pwm_window['time_us'], pwm_window['V(v_cuad)'], 'b-', linewidth=1.5, label='V(v_cuad)')
ax1.plot(pwm_window['time_us'], pwm_window['V(v_triag)'], 'r-', linewidth=1.5, label='V(v_triag)')
ax1.set_xlabel('Tiempo (µs)')
ax1.set_ylabel('Voltaje (V)')
ax1.set_title('Oscilador triangular')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Gráfico 2: PWM2 - V(pwm), V(v_triag), V(vmed), V(n003)
pwm2_filtered = pwm2[(pwm2['time_us'] >= 200) & (pwm2['time_us'] <= 300)]
ax2 = axes[1]
ax2.plot(pwm2_filtered['time_us'], pwm2_filtered['V(pwm)'], 'b-', linewidth=1.5, label='V(pwm)')
ax2.plot(pwm2_filtered['time_us'], pwm2_filtered['V(v_triag)'], 'r-', linewidth=1.5, label='V(v_triag)')
ax2.plot(pwm2_filtered['time_us'], pwm2_filtered['V(vmed)'], 'g-', linewidth=1.5, label='V(vmed)')
ax2.plot(pwm2_filtered['time_us'], pwm2_filtered['V(n003)'], 'm-', linewidth=1.5, label='V(Av*v_sense)')
ax2.set_xlabel('Tiempo (µs)')
ax2.set_ylabel('Voltaje (V)')
ax2.set_title('PWM2 - Múltiples Señales')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()

# Guardar gráficos
fig1 = plt.figure(figsize=(12, 5))
ax_pwm = fig1.add_subplot(111)
ax_pwm.plot(pwm_window['time_us'], pwm_window['V(v_cuad)'], 'b-', linewidth=1.5, label='V(v_cuad)')
ax_pwm.plot(pwm_window['time_us'], pwm_window['V(v_triag)'], 'r-', linewidth=1.5, label='V(v_triag)')
ax_pwm.set_xlabel('Tiempo (µs)')
ax_pwm.set_ylabel('Voltaje (V)')
ax_pwm.set_title('PWM - Señales de PWM y Triangular')
ax_pwm.grid(True, alpha=0.3)
ax_pwm.legend()
fig1.savefig('grafico_pwm.png', dpi=150, bbox_inches='tight')
plt.close(fig1)

fig2 = plt.figure(figsize=(12, 5))
ax_pwm2 = fig2.add_subplot(111)
ax_pwm2.plot(pwm2_filtered['time_us'], pwm2_filtered['V(pwm)'], 'b-', linewidth=1.5, label='V(pwm)')
ax_pwm2.plot(pwm2_filtered['time_us'], pwm2_filtered['V(v_triag)'], 'r-', linewidth=1.5, label='V(v_triag)')
ax_pwm2.plot(pwm2_filtered['time_us'], pwm2_filtered['V(vmed)'], 'g-', linewidth=1.5, label='V(vmed)')
ax_pwm2.plot(pwm2_filtered['time_us'], pwm2_filtered['V(n003)'], 'm-', linewidth=1.5, label='V(Av*v_sense)')
ax_pwm2.set_xlabel('Tiempo (µs)')
ax_pwm2.set_ylabel('Voltaje (V)')
ax_pwm2.set_title('Señal de salida PWM')
ax_pwm2.grid(True, alpha=0.3)
ax_pwm2.legend()
fig2.savefig('grafico_pwm2.png', dpi=150, bbox_inches='tight')
plt.close(fig2)

# Imprimir información
print(f"Datos cargados correctamente:")
print(f"  PWM: {len(pwm)} puntos, tiempo total: {pwm['time_us'].min():.2f} - {pwm['time_us'].max():.2f} µs")
print(f"  PWM2: {len(pwm2)} puntos, tiempo total: {pwm2['time_us'].min():.2f} - {pwm2['time_us'].max():.2f} µs")
print(f"\nVentana mostrada:")
print(f"  PWM: {t_min:.2f} - {t_max:.2f} µs (punto medio: {mid_time:.2f} µs) - {len(pwm_window)} puntos")
print(f"  PWM2: 200.00 - 300.00 µs - {len(pwm2_filtered)} puntos")
print(f"\nGráficos guardados:")
print(f"  - grafico_pwm.png")
print(f"  - grafico_pwm2.png")
