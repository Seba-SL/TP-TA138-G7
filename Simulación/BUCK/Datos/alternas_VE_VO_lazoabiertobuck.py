import numpy as np
import matplotlib.pyplot as plt

# Cargar datos
datos = np.loadtxt(
    "buck_lazoabierto_ve_vo2.txt",
    skiprows=1
)

# Extraer columnas
t = datos[:, 0]      # tiempo [s]
vo = datos[:, 1]     # tensión de salida

# Convertir tiempo a microsegundos
t_us = t * 1e6

# Graficar
plt.figure(figsize=(10, 5))


# Línea horizontal en 9.5 V
plt.axhline(
    y=9.5,
    linestyle='--',
    linewidth=2,
    color ="black",
    label='Referencia 9.5 V'
)


plt.plot(t_us, vo, label=r'$V_o$', linewidth=3)

plt.xlabel('Tiempo [$\mu$s]')
plt.ylabel('Tensión [V]')
plt.title('Convertidor Buck en Lazo Abierto')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()