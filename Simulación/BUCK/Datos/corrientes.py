import numpy as np
import matplotlib.pyplot as plt

# Cargar datos
datos = np.loadtxt(
    "corrientes_iL_io2.txt",
    skiprows=1
)

# Extraer columnas
t = datos[:, 0]      # tiempo [s]
iL = datos[:, 1]     # corriente del inductor
io = datos[:, 2]     # corriente de salida (carga)

# Convertir tiempo a microsegundos
t_us = t * 1e6

# Graficar
plt.figure(figsize=(10, 5))

plt.plot(t_us, iL, linewidth=3, label=r'$i_L$')
plt.plot(t_us, io, linewidth=3, label=r'$i_o$')

plt.xlabel('Tiempo [$\mu$s]')
plt.xlim([3000 , 3100])
plt.ylim([0 , 0.3])
plt.ylabel('Corriente [A]')
plt.title('Corriente del Inductor y Corriente de Salida')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()