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
plt.show()
