import numpy as np
import matplotlib.pyplot as plt

# =========================================
# MEDICIONES (12 puntos)
# =========================================

Vcc = np.array([
    3.48, 4.57, 4.81, 4.99,
    5.37, 5.62, 6.25, 7.18,
    8.2, 11.04, 13.13, 15.27
])

Icc = np.array([
    0.02, 0.034, 0.041, 0.047,
    0.059, 0.063, 0.064, 0.064,
    0.065, 0.067, 0.068, 0.070
])

Vo = np.array([
    0.0203, 2.63, 3.18, 3.63,
    4.63, 4.99, 4.99, 4.99,
    4.99, 4.99, 5, 5
])

Io = np.array([
    0.2*1e-6, 26.3*1e-3, 31.8*1e-3, 36.3*1e-3,
    46.3*1e-3, 49.9*1e-3, 49.9*1e-3, 49.9*1e-3,
   49.9*1e-3,49.9*1e-3, 49.99*1e-3,50*1e-3
])



# =========================================
# POTENCIAS
# =========================================
Po = Vo * Io
Pe = Vcc * Icc

eta = Po / Pe

# =========================================
# GRAFICO
# =========================================
plt.figure(figsize=(9,5))

plt.plot(Vcc, eta * 100, 'o-', linewidth=3, color = "red", label='Eficiencia medida')

# =========================================
# FORMATO
# =========================================
plt.xlabel('Tensión de entrada $V_{CC}$ [V]')
plt.ylabel('Eficiencia [%]')
plt.title('Eficiencia de un LDO en función de $V_{CC}$')

plt.grid(True)
plt.legend(fontsize=12, loc='best')
plt.ylim(0, 100)

plt.show()