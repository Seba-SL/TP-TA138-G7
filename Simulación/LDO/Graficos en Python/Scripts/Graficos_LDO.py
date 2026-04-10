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

vcc_mean = np.mean(vcc)
vo_mean = np.mean(vo)

vcc_ac = vcc - np.mean(vcc)
vo_ac  = vo  - np.mean(vo)

plt.figure()
plt.plot(t*1e6, vcc_ac, label="Vcc (AC)", linewidth = 3)
plt.plot(t*1e6, vo_ac, label="Vo (AC)", linewidth = 3)

plt.xlabel("Tiempo (µs)")
plt.ylabel("Variación de tensión (V)")
plt.title("Ripple en Vcc y Vo (componentes AC)")
plt.grid(True)
plt.legend(fontsize=12)


# Texto en el gráfico
texto = f"Vcc medio = {vcc_mean:.3f} V\nVo medio = {vo_mean:.3f} V"
plt.text(0.4, 0.95, texto,
         transform=plt.gca().transAxes,
         fontsize=12,
         verticalalignment='top',
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

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

v_reg = 6.0

plt.figure()
plt.plot(Vcc, Vo, linewidth=3, label="Vo")
plt.plot(Vcc, Vcc, linewidth=3, label="Vcc")

plt.axvline(x=v_reg, linestyle='--', linewidth=2, label=f"Inicio regulación ≈ {v_reg} V")

plt.xlabel("Tensión de entrada $V_{cc}$ (V)")
plt.ylabel("Tensión de salida $V_O$ (V)")
plt.title("Regulación de línea del LDO")

 
#plt.yticks(np.arange(0, 10, 0.2))  

plt.grid(True)
plt.legend(fontsize=12)

plt.savefig(os.path.join(capturas_dir, "LDO_regulacion_linea.png"), dpi=300)
plt.show()