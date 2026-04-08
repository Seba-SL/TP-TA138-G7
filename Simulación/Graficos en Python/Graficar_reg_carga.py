import numpy as np
import matplotlib.pyplot as plt
import os

# carpeta donde está el script
script_dir = os.path.dirname(os.path.abspath(__file__))

archivo = os.path.join(script_dir,
                       "Datos de Ltspice/LDO/regulacion_carga_Vo_vsIL.txt")

# cargar datos
data = np.loadtxt(archivo, skiprows=1)

IL = data[:,0]
Vo = data[:,1]

plt.figure()
plt.plot(IL, Vo, marker='o', linewidth = 4)

plt.xlabel("Corriente de carga $I_L$ (A)")
plt.ylabel("Voltaje de salida $V_O$ (V)")
plt.title("Regulación de carga del LDO")
plt.grid(True)

plt.show()