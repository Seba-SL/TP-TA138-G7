import numpy as np
import matplotlib.pyplot as plt
import os

# directorio donde está el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# rutas
datos_dir = os.path.join(script_dir, "..", "Datos de Ltspice", "LDO")
capturas_dir = os.path.join(script_dir, "..", "Capturas")

# normalizar rutas
datos_dir = os.path.normpath(datos_dir)
capturas_dir = os.path.normpath(capturas_dir)

# ---------- 1 Respuesta temporal Vcc vs Vo ----------

archivo = os.path.join(datos_dir, "Vcc_Vo.txt")
data = np.loadtxt(archivo, skiprows=1)

t = data[:,0]
vcc = data[:,1]
vo = data[:,2]

plt.figure()
plt.plot(t*1e6, vcc, label="Vcc")
plt.plot(t*1e6, vo, label="Vo")

plt.xlabel("Tiempo (µs)")
plt.ylabel("Tensión (V)")
plt.title("Respuesta temporal del LDO")
plt.grid(True)
plt.legend()

plt.savefig(os.path.join(capturas_dir, "LDO_Vcc_Vo.png"), dpi=300)


# ---------- 2 Regulación de carga ----------

archivo = os.path.join(datos_dir, "regulacion_carga_Vo_vsIL.txt")
data = np.loadtxt(archivo, skiprows=1)

IL = data[:,0]
Vo = data[:,1]

plt.figure()
plt.plot(IL, Vo, linewidth = 2)

plt.xlabel("Corriente de carga $I_L$ (A)")
plt.ylabel("Voltaje de salida $V_O$ (V)")
plt.title("Regulación de carga del LDO")
plt.grid(True)

plt.savefig(os.path.join(capturas_dir, "LDO_regulacion_carga.png"), dpi=300)


# ---------- 3 Regulación de línea ----------

archivo = os.path.join(datos_dir, "regulaciondeLinea_Vo_vs_Vc.txt")
data = np.loadtxt(archivo, skiprows=1)

Vcc = data[:,1]
Vo = data[:,2]

plt.figure()
plt.plot(Vcc, Vo, linewidth = 2, color = "blue")
plt.plot(Vcc, Vcc, linewidth = 2, color = "red")


plt.xlabel("Tensión de entrada $V_{cc}$ (V)")
plt.ylabel("Tensión de salida $V_O$ (V)")
plt.title("Regulación de línea del LDO")
plt.grid(True)

plt.savefig(os.path.join(capturas_dir, "LDO_regulacion_linea.png"), dpi=300)

plt.show()