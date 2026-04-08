import numpy as np
import matplotlib.pyplot as plt
import os

# ruta del script
script_dir = os.path.dirname(os.path.abspath(__file__))

archivo = os.path.join(script_dir, "Datos de Ltspice/LDO/Vcc_Vo.txt")

data = np.loadtxt(archivo, skiprows=1)

t = data[:,0]
vcc = data[:,1]
vo = data[:,2]

plt.plot(t*1e6, vcc, label="Vcc",linewidth = 3)
plt.plot(t*1e6, vo, label="Vo",linewidth = 3)

plt.xlabel("Tiempo (µs)")
plt.ylabel("Voltaje (V)")
plt.title("LDO: Tensión de salida vs tensión de entrada")
plt.grid(True)
plt.legend()

plt.show()