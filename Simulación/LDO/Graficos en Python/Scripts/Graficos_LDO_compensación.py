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


def find_0db_crossing(freq, mag_db):
    """Encuentra la frecuencia donde la magnitud cruza 0dB"""
    if len(freq) < 2:
        return None
    sign = np.sign(mag_db)
    crossing_indices = np.where(sign[:-1] * sign[1:] < 0)[0]
    if len(crossing_indices) > 0:
        i = crossing_indices[0]
        # Interpolar la frecuencia donde mag_db = 0
        f_crossing = np.interp(0.0, [mag_db[i], mag_db[i+1]], [freq[i], freq[i+1]])
        return f_crossing
    # Si no hay cruzamiento, retornar la frecuencia más cercana a 0dB
    idx = np.argmin(np.abs(mag_db))
    return freq[idx]


def read_bode_file(filepath):
    """Lee archivo de Bode en formato especial"""
    freq = []
    mag_db = []
    fase_deg = []
    
    with open(filepath, 'r') as f:
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
    
    return freq, mag_db, fase_deg


# ========== Diagrama de Bode - Lazo de tensión compensado ==========

# Leer archivos
archivo1 = os.path.join(datos_dir, "Bode_lazo_tension_compensado.txt")
freq1, mag_db1, fase_deg1 = read_bode_file(archivo1)

archivo2 = os.path.join(datos_dir, "Bode_lazo_tension_compensado_2.txt")
freq2, mag_db2, fase_deg2 = read_bode_file(archivo2)

# Encontrar cruzamientos de 0dB
f_0db1 = find_0db_crossing(freq1, mag_db1)
f_0db2 = find_0db_crossing(freq2, mag_db2)

# Calcular márgenes de fase
if f_0db1 is not None:
    phase_margin1 = np.interp(f_0db1, freq1, fase_deg1)
else:
    phase_margin1 = None

if f_0db2 is not None:
    phase_margin2 = np.interp(f_0db2, freq2, fase_deg2)
else:
    phase_margin2 = None


# ---------- Gráfico combinado: Magnitud y Fase ----------
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(10, 8))

# Subplot 1: Magnitud
axs[0].semilogx(freq1, mag_db1, linewidth=3, color="tab:blue", label=r"$|T_v| \qquad R_L = 100 \Omega$")
axs[0].semilogx(freq2, mag_db2, linewidth=3, color="tab:orange", label=r"$|T_v| \qquad R_L = 100 k \Omega$")

axs[0].axhline(0, color="gray", linestyle=':', linewidth=1.5, alpha=0.7)

# Marcar cruzamientos de 0dB
if f_0db1 is not None:
    axs[0].axvline(f_0db1, color="tab:blue", linestyle='--', linewidth=1.5, alpha=0.6)

if f_0db2 is not None:
    axs[0].axvline(f_0db2, color="tab:orange", linestyle='--', linewidth=1.5, alpha=0.6)

axs[0].set_ylabel("Magnitud (dB)", fontsize=12)
axs[0].set_title("Diagrama de Bode - Lazo de Tensión Compensado", fontsize=14)
axs[0].grid(True, which="both", alpha=0.3)
axs[0].legend(fontsize=10, loc="best")

# Subplot 2: Fase
# Leyendas con márgenes de fase
label1 = r"$\angle T_v \qquad R_L = 100 \Omega$"
label2 = r"$\angle T_v \qquad R_L = 100 k \Omega$"
if phase_margin1 is not None:
    label1 += f" (Margen = {phase_margin1:.2f}°)"
if phase_margin2 is not None:
    label2 += f" (Margen = {phase_margin2:.2f}°)"

axs[1].semilogx(freq1, fase_deg1, linewidth=3, color="tab:blue", label=label1)
axs[1].semilogx(freq2, fase_deg2, linewidth=3, color="tab:orange", label=label2)

# Marcar cruzamientos de 0dB
if f_0db1 is not None:
    axs[1].axvline(f_0db1, color="tab:blue", linestyle='--', linewidth=1.5, alpha=0.6)

if f_0db2 is not None:
    axs[1].axvline(f_0db2, color="tab:orange", linestyle='--', linewidth=1.5, alpha=0.6)

axs[1].set_xlabel("Frecuencia (Hz)", fontsize=12)
axs[1].set_ylabel("Fase (°)", fontsize=12)
axs[1].grid(True, which="both", alpha=0.3)
axs[1].legend(fontsize=10, loc="best")

plt.tight_layout()
plt.savefig(os.path.join(capturas_dir, "LDO_Bode_lazo_tension_compensado.png"), dpi=300)
plt.show()


# ========== Diagrama de Bode - Lazo de corriente compensado ==========

# Leer primer archivo
archivo_corriente1 = os.path.join(datos_dir, "Bode_lazo_corriente_compensado.txt")
freq_i1, mag_db_i1, fase_deg_i1 = read_bode_file(archivo_corriente1)

# Leer segundo archivo
archivo_corriente2 = os.path.join(datos_dir, "Bode_lazo_corriente_compensado2.txt")
freq_i2, mag_db_i2, fase_deg_i2 = read_bode_file(archivo_corriente2)

# Encontrar cruzamientos de 0dB
f_0db_i1 = find_0db_crossing(freq_i1, mag_db_i1)
f_0db_i2 = find_0db_crossing(freq_i2, mag_db_i2)

# Calcular márgenes de fase
if f_0db_i1 is not None:
    phase_margin_i1 = np.interp(f_0db_i1, freq_i1, fase_deg_i1)
else:
    phase_margin_i1 = None

if f_0db_i2 is not None:
    phase_margin_i2 = np.interp(f_0db_i2, freq_i2, fase_deg_i2)
else:
    phase_margin_i2 = None


# ---------- Gráfico combinado: Magnitud y Fase ----------
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(10, 8))

# Subplot 1: Magnitud
axs[0].semilogx(freq_i1, mag_db_i1, linewidth=3, color="tab:green", label=r"$|T_A| \qquad R_L = 2.5 \Omega$")
axs[0].semilogx(freq_i2, mag_db_i2, linewidth=3, color="tab:red", label=r"$|T_A| \qquad R_L = 1 \Omega$")

axs[0].axhline(0, color="gray", linestyle=':', linewidth=1.5, alpha=0.7)

# Marcar cruzamientos de 0dB
if f_0db_i1 is not None:
    axs[0].axvline(f_0db_i1, color="tab:green", linestyle='--', linewidth=1.5, alpha=0.6)

if f_0db_i2 is not None:
    axs[0].axvline(f_0db_i2, color="tab:red", linestyle='--', linewidth=1.5, alpha=0.6)

axs[0].set_ylabel("Magnitud (dB)", fontsize=12)
axs[0].set_title("Diagrama de Bode - Lazo de Corriente Compensado", fontsize=14)
axs[0].grid(True, which="both", alpha=0.3)
axs[0].legend(fontsize=10, loc="best")

# Subplot 2: Fase
# Leyendas con márgenes de fase
label_i1 = r"$\angle T_A \qquad R_L = 2.5 \Omega$"
if phase_margin_i1 is not None:
    label_i1 += f" (Margen = {phase_margin_i1:.2f}°)"

label_i2 = r"$\angle T_A \qquad R_L = 1 \Omega$"
if phase_margin_i2 is not None:
    label_i2 += f" (Margen = {phase_margin_i2:.2f}°)"

axs[1].semilogx(freq_i1, fase_deg_i1, linewidth=3, color="tab:green", label=label_i1)
axs[1].semilogx(freq_i2, fase_deg_i2, linewidth=3, color="tab:red", label=label_i2)

# Marcar cruzamientos de 0dB
if f_0db_i1 is not None:
    axs[1].axvline(f_0db_i1, color="tab:green", linestyle='--', linewidth=1.5, alpha=0.6)

if f_0db_i2 is not None:
    axs[1].axvline(f_0db_i2, color="tab:red", linestyle='--', linewidth=1.5, alpha=0.6)

axs[1].set_xlabel("Frecuencia (Hz)", fontsize=12)
axs[1].set_ylabel("Fase (°)", fontsize=12)
axs[1].grid(True, which="both", alpha=0.3)
axs[1].legend(fontsize=10, loc="best")

plt.tight_layout()
plt.savefig(os.path.join(capturas_dir, "LDO_Bode_lazo_corriente_compensado.png"), dpi=300)
plt.show()


# ========== Respuesta temporal Vcc vs Vo (compensado) ==========

archivo_temporal = os.path.join(datos_dir, "Vcc_Vo_compensado.txt")
data_temporal = np.loadtxt(archivo_temporal, skiprows=1)

t = data_temporal[:,0]
vcc = data_temporal[:,1]
vo = data_temporal[:,2]

vcc_mean = np.mean(vcc)
vo_mean = np.mean(vo)

vcc_ac = vcc - vcc_mean
vo_ac  = vo  - vo_mean

plt.figure(figsize=(10, 6))
plt.xlim(50, 100)
plt.ylim(-0.3, 0.3)

# Defino estilos explícitos
color_vcc = "tab:blue"
color_vo  = "tab:orange"

line_vcc, = plt.plot(t*1e6, vcc_ac, label="$V_{cc}$ (AC)", linewidth=3, linestyle="--", color=color_vcc)
line_vo,  = plt.plot(t*1e6, vo_ac, label="$V_O$ (AC)", linewidth=3, linestyle="-", color=color_vo)

plt.xlabel("Tiempo (µs)", fontsize=12)
plt.ylabel("Variación de tensión (V)", fontsize=12)
plt.title("Ripple en Vcc y Vo (componentes AC) - Compensado", fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

# Posición base
x0, y0 = 0.2, 0.95

# Línea Vcc
plt.text(x0, y0,
         f"■ $V_{{cc}}$ medio = {vcc_mean:.3f} V  (punteada)",
         transform=plt.gca().transAxes,
         fontsize=11,
         verticalalignment='top',
         color=color_vcc,
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

# Línea Vo (un poco más abajo)
plt.text(x0+0.2, y0-0.85,
         f"■ $V_O$ medio = {vo_mean:.3f} V  (continua)",
         transform=plt.gca().transAxes,
         fontsize=11,
         verticalalignment='top',
         color=color_vo, 
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

plt.savefig(os.path.join(capturas_dir, "LDO_Vcc_Vo_compensado.png"), dpi=300)
plt.show()


# ========== Respuesta dinámica - Lazo de tensión vs Lazo de corriente ==========

# Leer archivos de lazo dinámico
archivo_lazo_tension = os.path.join(datos_dir, "lazo_tension_dinamico.txt")
data_lazo_tension = np.loadtxt(archivo_lazo_tension, skiprows=1)

t_tension = data_lazo_tension[:, 0]
v_lazo_tension = data_lazo_tension[:, 1]

archivo_lazo_corriente = os.path.join(datos_dir, "lazo_corriente_dinamico.txt")
data_lazo_corriente = np.loadtxt(archivo_lazo_corriente, skiprows=1)

t_corriente = data_lazo_corriente[:, 0]
i_lazo_corriente = data_lazo_corriente[:, 1]

# Crear figura con dos subgráficos
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Gráfico 1: Lazo de Tensión Dinámico
axs[0].plot(t_tension * 1e6, v_lazo_tension, linewidth=2.5, color="tab:blue", label=r"$V_o$")
axs[0].set_xlabel("Tiempo (µs)", fontsize=12)
axs[0].set_ylabel("Voltaje (V)", fontsize=12)
axs[0].set_title("Respuesta Dinámica - Lazo de Tensión", fontsize=13, fontweight='bold')
axs[0].grid(True, alpha=0.3)
axs[0].legend(fontsize=11, loc="best")

# Gráfico 2: Lazo de Corriente Dinámico
axs[1].plot(t_corriente * 1e6, i_lazo_corriente, linewidth=2.5, color="tab:green", label=r"$I_o$")
axs[1].set_xlabel("Tiempo (µs)", fontsize=12)
axs[1].set_ylabel("Corriente (A)", fontsize=12)
axs[1].set_title("Respuesta Dinámica - Lazo de Corriente", fontsize=13, fontweight='bold')
axs[1].grid(True, alpha=0.3)
axs[1].legend(fontsize=11, loc="best")

plt.tight_layout()
plt.savefig(os.path.join(capturas_dir, "LDO_lazos_dinamicos.png"), dpi=300)
plt.show()
