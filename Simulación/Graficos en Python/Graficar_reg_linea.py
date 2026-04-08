import numpy as np
import matplotlib.pyplot as plt
import os

# directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))

archivo = os.path.join(
    script_dir,
    "Datos de Ltspice/LDO/regulaciondeLinea_Vo_vs_Vc.txt"
)

# cargar datos
data = np.loadtxt(archivo, skiprows=1)

Vcc = data[:,1]   # V(vcc)
Vo  = data[:,2]   # V(vo)

plt.figure()

plt.plot(Vcc, Vo, marker='o', color = "blue",alpha = 0.85, linewidth =  2)

plt.plot(Vcc, Vcc, marker='o', color = "red",alpha = 0.85, linewidth =  2)


plt.xlabel("Voltaje de entrada $V_{cc}$ (V)")
plt.ylabel("Voltaje de salida $V_O$ (V)")
plt.title("Regulación de línea del LDO")

plt.grid(True)

plt.show()