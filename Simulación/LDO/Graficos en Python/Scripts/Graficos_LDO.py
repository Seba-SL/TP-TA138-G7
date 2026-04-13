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

vcc_ac = vcc - vcc_mean
vo_ac  = vo  - vo_mean

plt.figure()
plt.xlim(1000, 1030)
plt.ylim(-0.3, 0.3)

# Defino estilos explícitos
color_vcc = "tab:blue"
color_vo  = "tab:orange"

line_vcc, = plt.plot(t*1e6, vcc_ac, label="Vcc (AC)",linewidth=3, linestyle="--", color=color_vcc)

line_vo,  = plt.plot(t*1e6, vo_ac, label="Vo (AC)",linewidth=3, linestyle="-", color=color_vo)

plt.xlabel("Tiempo (µs)")
plt.ylabel("Variación de tensión (V)")
plt.title("Ripple en Vcc y Vo (componentes AC) ")
plt.grid(True)
plt.legend(fontsize=12)

# Posición base
x0, y0 = 0.2, 0.95

# Línea Vcc
plt.text(x0, y0,
         f"■ Vcc medio = {vcc_mean:.3f} V  (punteada)",
         transform=plt.gca().transAxes,
         fontsize=12,
         verticalalignment='top',
         color=color_vcc,
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

# Línea Vo (un poco más abajo)
plt.text(x0+0.2, y0-0.85,
         f"■ Vo medio = {vo_mean:.3f} V  (continua)",
         transform=plt.gca().transAxes,
         fontsize=12,
         verticalalignment='top',
         color=color_vo, 
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))


plt.savefig(os.path.join(capturas_dir, "LDO_Vcc_Vo.png"), dpi=300)






# ---------- 2 Regulación de carga ----------

archivo = os.path.join(datos_dir, "regulacion_carga_Vo_vsIL.txt")
data = np.loadtxt(archivo, skiprows=1)

IL = data[:,0]
Vo = data[:,1]

plt.figure()
plt.plot(IL, Vo, linewidth = 3)

plt.ylim(0, 6)
plt.xlim(0, 2.5)

plt.xlabel("Corriente de carga $I_L$ (A)")
plt.ylabel("Voltaje de salida $V_O$ (V)")
plt.title("Regulación de carga del LDO")
plt.grid(True)



plt.savefig(os.path.join(capturas_dir, "LDO_regulacion_carga.png"), dpi=300)




# ---------- 3 Diagrama de Bode - Lazo de tensión ----------

archivo = os.path.join(datos_dir, "Bode_lazo_tension.txt")

# Leer archivo con formato especial
freq = []
mag_db = []
fase_deg = []

with open(archivo, 'r') as f:
    # Saltar encabezado
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            frequency = float(parts[0])
            # Parse formato complejo: (magnitud dB, fase°)
            complex_str = parts[1].replace('(', '').replace(')', '').replace('°', '').replace('dB', '')
            values = complex_str.split(',')
            magnitude_db = float(values[0])
            phase_deg = float(values[1])
            
            freq.append(frequency)
            mag_db.append(magnitude_db)
            fase_deg.append(phase_deg)

freq = np.array(freq)
mag_db = np.array(mag_db)

# Gráfico de magnitud
plt.figure()
plt.semilogx(freq, mag_db, linewidth=3, color="tab:blue")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud (dB)")
plt.title("Diagrama de Bode - Lazo de Tensión")
plt.grid(True, which="both", alpha=0.3)

plt.savefig(os.path.join(capturas_dir, "LDO_Bode_lazo_tension.png"), dpi=300)


# ---------- 4 Diagrama de Bode - Lazo de corriente ----------

archivo = os.path.join(datos_dir, "Bode_lazo_corriente.txt")

# Leer archivo con formato especial
freq = []
mag_db = []

with open(archivo, 'r') as f:
    # Saltar encabezado
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            frequency = float(parts[0])
            # Parse formato complejo: (magnitud dB, fase°)
            complex_str = parts[1].replace('(', '').replace(')', '').replace('°', '').replace('dB', '')
            values = complex_str.split(',')
            magnitude_db = float(values[0])
            
            freq.append(frequency)
            mag_db.append(magnitude_db)

freq = np.array(freq)
mag_db = np.array(mag_db)

# Gráfico de magnitud
plt.figure()
plt.semilogx(freq, mag_db, linewidth=3, color="tab:green")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud (dB)")
plt.title("Diagrama de Bode - Lazo de Corriente")
plt.grid(True, which="both", alpha=0.3)

plt.savefig(os.path.join(capturas_dir, "LDO_Bode_lazo_corriente.png"), dpi=300)


# ---------- 5 Regulación de línea ----------

archivo = os.path.join(datos_dir, "regulaciondeLinea_Vo_vs_Vc.txt")
data = np.loadtxt(archivo, skiprows=1)

Vcc = data[:,1]
Vo = data[:,2]

v_reg = 5.25

plt.figure()
plt.plot(Vcc, Vo, linewidth=2, label="Vo")
plt.plot(Vcc, Vcc, linewidth=2,linestyle='--', label="Vcc")

plt.axvline(x=v_reg, linestyle='--', linewidth=1, label=f"Inicio regulación ≈ {v_reg} V")

plt.xlabel("Tensión de entrada $V_{cc}$ (V)")
plt.ylabel("Tensión de salida $V_O$ (V)")
plt.title("Regulación de línea del LDO")

#plt.yticks(np.arange(0, 10, 0.2))  

plt.grid(True)
plt.legend(fontsize=12)

plt.savefig(os.path.join(capturas_dir, "LDO_regulacion_linea.png"), dpi=300)

plt.figure()
plt.plot(Vcc, Vo, linewidth=2, label="Vo")
plt.plot(Vcc, Vcc, linewidth=2,linestyle='--', label="Vcc")
plt.axvline(x=v_reg, linestyle='--', linewidth=1, label=f"Inicio regulación ≈ {v_reg} V")

plt.xlim(3.5, 5.5)
plt.ylim(0, 5.5)

plt.xlabel("Tensión de entrada $V_{cc}$ (V)")
plt.ylabel("Tensión de salida $V_O$ (V)")
plt.title("Regulación de línea del LDO (zoom 3.5–5.5 V)")

plt.grid(True)
plt.legend(fontsize=12)

plt.savefig(os.path.join(capturas_dir, "LDO_regulacion_linea_zoom.png"), dpi=300)
plt.show()

# ---------- 6 Eficiencia ----------

archivo = os.path.join(datos_dir, "eficiencia.txt")
data = np.loadtxt(archivo, skiprows=1)

V = data[:,0]
ef = data[:,1]

plt.figure()
plt.plot(V, ef, linewidth=3, alpha = 0.85, color='red')
plt.xlim(0, 24)
plt.ylim(0, 90)

plt.xlabel("Tensión de entrada $V_{cc}$ [V]")
plt.ylabel("Eficiencia [%]")
plt.title("Eficiencia del LDO")
plt.grid(True)

plt.savefig(os.path.join(capturas_dir, "LDO_eficiencia.png"), dpi=300)
plt.show()

# ---------- 7 V_vs_I ----------
archivo = os.path.join(datos_dir, "VvsI.txt")

data = np.loadtxt(archivo, skiprows=1)

# Crear el gráfico
plt.figure(figsize=(10, 6))

V = data[:,1]
I = data[:,2]
# Scatter plot para Prueba1
plt.scatter(I, V, color='blue', s=30, alpha=0.7, edgecolors='black', linewidth=0.5 )


# Etiquetas de los ejes
plt.xlabel(r'$I_o$ (A)', fontsize=12)
plt.ylabel(r'$V_o$ (V)', fontsize=12)
plt.title(r'Gráfico V vs I para $100\Omega > R_L > 0,5\Omega$', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

# Línea vertical punteada en I = 1.5A
plt.axvline(x=1.5, linestyle='--', color='black', linewidth=1, label=r'$I_o$ = 1.5A')

# Mostrar el gráfico
plt.tight_layout()
plt.savefig(os.path.join(capturas_dir, "V vs I.png"), dpi=300)
plt.show()