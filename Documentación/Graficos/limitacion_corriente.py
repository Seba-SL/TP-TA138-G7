import numpy as np
import matplotlib.pyplot as plt

# =========================================
# SIMULACIÓN (ideal LTspice)
# =========================================
Io_sim_1 = np.linspace(0, 1.5, 200)
Vo_sim_1 = np.full_like(Io_sim_1, 5.0)

Io_sim_2 = np.linspace(1.5, 0.4, 200)
Vo_sim_2 = np.linspace(5.0, 0.0, 200)

# =========================================
# MODELO EXPERIMENTAL (consistente con medición)
# =========================================
Io_lab = np.array([0.4, 0.4, 0.41, 0.67, 0.98, 0.98])
Vo_lab = np.array([0.0, 0.6, 1.025, 2.345, 4.41, 4.99])

Io_med_2 = np.linspace(0, 0.980, 200)
Vo_med_reg = np.full_like(Io_sim_1, 4.99)

# =========================================
# GRAFICO
# =========================================
plt.figure(figsize=(9,5))

# Simulación
plt.plot(Io_sim_1, Vo_sim_1, 'b', linewidth=3, label='Simulación LTspice')
plt.plot(Io_sim_2, Vo_sim_2, 'b', linewidth=3)

# Medición real (curva real)
plt.plot(Io_med_2, Vo_med_reg, 'r', linewidth=3)
plt.plot(Io_lab, Vo_lab, 'r-o', linewidth=3, label='Medición laboratorio')

# Puntos
plt.scatter(Io_lab, Vo_lab, color='black', s=70)

# =========================================
# FORMATO
# =========================================
plt.xlabel('Corriente de salida $I_O$ [A]')
plt.ylabel('Tensión de salida $V_O$ [V]')
plt.title('Limitación de corriente foldback en LDO')

plt.grid(True)

plt.legend(fontsize=12, loc='best')
plt.xlim(0, 1.6)
plt.ylim(0, 5.5)

plt.show()
