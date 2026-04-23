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


def find_0db_crossing(freq, mag_db):
    if len(freq) < 2:
        return None
    sign = np.sign(mag_db)
    crossing_indices = np.where(sign[:-1] * sign[1:] < 0)[0]
    if len(crossing_indices) > 0:
        i = crossing_indices[0]
        return np.interp(0.0, mag_db[i:i+2], freq[i:i+2])
    idx = np.argmin(np.abs(mag_db))
    return freq[idx]


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
fase_deg = np.unwrap(np.deg2rad(fase_deg)) * 180.0 / np.pi

f_0db = find_0db_crossing(freq, mag_db)

fig, axs = plt.subplots(2, 1, sharex=True, figsize=(8, 8))
axs[0].semilogx(freq, mag_db, linewidth=3, color="tab:blue", label="Magnitud")
axs[0].axhline(0, color="gray", linestyle=':', linewidth=1)
if f_0db is not None:
    axs[0].axvline(f_0db, color="tab:red", linestyle='--', linewidth=1.5,
                   label=f"|Av|=1 en {f_0db:.2f} Hz")
axs[0].set_ylabel("Magnitud (dB)")
axs[0].set_title("Diagrama de Bode - Lazo de Tensión")
axs[0].grid(True, which="both", alpha=0.3)
axs[0].legend(fontsize=10)

# Calcular margen de fase
phase_margin = None
if f_0db is not None:
    phase_margin = np.interp(f_0db, freq, fase_deg)
    phase_legend = f"Fase (Margen = {phase_margin:.2f}°)"
else:
    phase_legend = "Fase"

axs[1].semilogx(freq, fase_deg, linewidth=3, color="tab:green", label=phase_legend)
if f_0db is not None:
    axs[1].axvline(f_0db, color="tab:red", linestyle='--', linewidth=1.5)
axs[1].set_xlabel("Frecuencia (Hz)")
axs[1].set_ylabel("Fase (°)")
axs[1].grid(True, which="both", alpha=0.3)
axs[1].legend(fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(capturas_dir, "LDO_Bode_lazo_tension.png"), dpi=300)


# ---------- 3b Diagrama de Bode - Comparación Lazo de Tensión ----------

# Leer primer archivo Bode_lazo_tension
archivo1 = os.path.join(datos_dir, "Bode_lazo_tension.txt")
freq1 = []
mag_db1 = []
fase_deg1 = []

with open(archivo1, 'r') as f:
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            frequency = float(parts[0])
            complex_str = parts[1].replace('(', '').replace(')', '').replace('°', '').replace('dB', '')
            values = complex_str.split(',')
            magnitude_db = float(values[0])
            phase_deg = float(values[1])
            
            freq1.append(frequency)
            mag_db1.append(magnitude_db)
            fase_deg1.append(phase_deg)

freq1 = np.array(freq1)
mag_db1 = np.array(mag_db1)
fase_deg1 = np.unwrap(np.deg2rad(fase_deg1)) * 180.0 / np.pi

# Leer segundo archivo Bode_lazo_tension_2
archivo2 = os.path.join(datos_dir, "Bode_lazo_tension_2.txt")
freq2 = []
mag_db2 = []
fase_deg2 = []

with open(archivo2, 'r') as f:
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            frequency = float(parts[0])
            complex_str = parts[1].replace('(', '').replace(')', '').replace('°', '').replace('dB', '')
            values = complex_str.split(',')
            magnitude_db = float(values[0])
            phase_deg = float(values[1])
            
            freq2.append(frequency)
            mag_db2.append(magnitude_db)
            fase_deg2.append(phase_deg)

freq2 = np.array(freq2)
mag_db2 = np.array(mag_db2)
fase_deg2 = np.unwrap(np.deg2rad(fase_deg2)) * 180.0 / np.pi

f_0db1 = find_0db_crossing(freq1, mag_db1)
f_0db2 = find_0db_crossing(freq2, mag_db2)

fig, axs = plt.subplots(2, 1, sharex=True, figsize=(8, 8))

# Gráfico de magnitud
axs[0].semilogx(freq1, mag_db1, linewidth=3, color="tab:blue", label=r"$|T_v| \qquad R_L = 100 \Omega$")
axs[0].semilogx(freq2, mag_db2, linewidth=3, color="tab:orange", label=r"$|T_v| \qquad R_L = 100 k \Omega$")
axs[0].axhline(0, color="gray", linestyle=':', linewidth=1)
if f_0db1 is not None:
    axs[0].axvline(f_0db1, color="tab:blue", linestyle='--', linewidth=1.5, alpha=0.7,
                   label=f"|Av|=1 en {f_0db1:.2f} Hz (1)")
if f_0db2 is not None:
    axs[0].axvline(f_0db2, color="tab:orange", linestyle='--', linewidth=1.5, alpha=0.7,
                   label=f"|Av|=1 en {f_0db2:.2f} Hz (2)")
axs[0].set_ylabel("Magnitud (dB)")
axs[0].set_title("Diagrama de Bode - Comparación Lazo de Tensión")
axs[0].grid(True, which="both", alpha=0.3)
axs[0].legend(fontsize=9)

# Gráfico de fase
# Calcular márgenes de fase
phase_margin1 = None
phase_legend1 = r"$\angle T_v \qquad R_L = 100 \Omega$"
if f_0db1 is not None:
    phase_margin1 = np.interp(f_0db1, freq1, fase_deg1)
    phase_legend1 = f"(Margen = {phase_margin1:.2f}°)"

phase_margin2 = None
phase_legend2 = r"$\angle T_v \qquad R_L = 100 k \Omega$"
if f_0db2 is not None:
    phase_margin2 = np.interp(f_0db2, freq2, fase_deg2)
    phase_legend2 = f"(Margen = {phase_margin2:.2f}°)"

axs[1].semilogx(freq1, fase_deg1, linewidth=3, color="tab:blue", label=phase_legend1)
axs[1].semilogx(freq2, fase_deg2, linewidth=3, color="tab:orange", label=phase_legend2)
if f_0db1 is not None:
    axs[1].axvline(f_0db1, color="tab:blue", linestyle='--', linewidth=1.5, alpha=0.7)
if f_0db2 is not None:
    axs[1].axvline(f_0db2, color="tab:orange", linestyle='--', linewidth=1.5, alpha=0.7)
axs[1].set_xlabel("Frecuencia (Hz)")
axs[1].set_ylabel("Fase (°)")
axs[1].grid(True, which="both", alpha=0.3)
axs[1].legend(fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(capturas_dir, "LDO_Bode_lazo_tension_comparacion.png"), dpi=300)


# ---------- 4 Diagrama de Bode - Lazo de corriente ----------

archivo = os.path.join(datos_dir, "Bode_lazo_corriente.txt")

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
            phase_val = float(values[1])
            
            freq.append(frequency)
            mag_db.append(magnitude_db)
            fase_deg.append(phase_val)

freq = np.array(freq)
mag_db = np.array(mag_db)
fase_deg = np.unwrap(np.deg2rad(fase_deg)) * 180.0 / np.pi

f_0db = find_0db_crossing(freq, mag_db)

fig, axs = plt.subplots(2, 1, sharex=True, figsize=(8, 8))
axs[0].semilogx(freq, mag_db, linewidth=3, color="tab:green", label="Magnitud")
axs[0].axhline(0, color="gray", linestyle=':', linewidth=1)
if f_0db is not None:
    axs[0].axvline(f_0db, color="tab:red", linestyle='--', linewidth=1.5,
                   label=f"|Av|=1 en {f_0db:.2f} Hz")
axs[0].set_ylabel("Magnitud (dB)")
axs[0].set_title("Diagrama de Bode - Lazo de Corriente")
axs[0].grid(True, which="both", alpha=0.3)
axs[0].legend(fontsize=10)

# Calcular margen de fase
phase_margin = None
if f_0db is not None:
    phase_margin = np.interp(f_0db, freq, fase_deg)
    phase_legend = f"Fase (Margen = {phase_margin:.2f}°)"
else:
    phase_legend = "Fase"

axs[1].semilogx(freq, fase_deg, linewidth=3, color="tab:purple", label=phase_legend)
if f_0db is not None:
    axs[1].axvline(f_0db, color="tab:red", linestyle='--', linewidth=1.5)
axs[1].set_xlabel("Frecuencia (Hz)")
axs[1].set_ylabel("Fase (°)")
axs[1].grid(True, which="both", alpha=0.3)
axs[1].legend(fontsize=10)

plt.tight_layout()
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