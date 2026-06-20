import numpy as np
import matplotlib.pyplot as plt

# Cargar datos
datos = np.loadtxt(
    "tensiones_vctrl_vs_ve_vo.txt",
    skiprows=1
)

# Extraer columnas
t     = datos[:, 0]
vctrl = datos[:, 1]
ve    = datos[:, 2]
vo    = datos[:, 3]
vs    = datos[:, 4]

# Convertir tiempo a microsegundos
t_us = t * 1e6

# Graficar
plt.figure(figsize=(12, 6))

plt.plot(t_us, vctrl, label=r'$V_{ctrl}$', linewidth=4)
plt.plot(t_us, ve,    label=r'$V_e$', linewidth=4)
plt.plot(t_us, vo,    label=r'$V_o$', linewidth=4)
plt.plot(t_us, vs,    label=r'$V_s$', linewidth=4)

plt.xlabel('Tiempo [$\mu$s]')
plt.ylabel('Tensión [V]')
plt.title('Tensiones del Convertidor Buck')
plt.grid(True)
plt.legend(fontsize=18)

plt.tight_layout()
plt.show()