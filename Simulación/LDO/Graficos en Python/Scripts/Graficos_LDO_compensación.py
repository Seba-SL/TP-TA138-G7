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
    if len(freq) < 2:
        return None
    sign = np.sign(mag_db)
    crossing_indices = np.where(sign[:-1] * sign[1:] < 0)[0]
    if len(crossing_indices) > 0:
        i = crossing_indices[0]
        return np.interp(0.0, mag_db[i:i+2], freq[i:i+2])
    idx = np.argmin(np.abs(mag_db))
    return freq[idx]


# ---------- Diagrama de Bode - Lazo de tensión compensado ----------

# Función auxiliar para leer archivo de Bode
def read_bode_file(filepath):
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

# Leer Bode compensado
archivo_compensado = os.path.join(datos_dir, "Bode_lazo_tension_compensado.txt")
freq, mag_db, fase_deg = read_bode_file(archivo_compensado)

# Leer Bode descompensado
archivo_descompensado = os.path.join(datos_dir, "Bode_lazo_tension.txt")
freq_desc, mag_db_desc, fase_deg_desc = read_bode_file(archivo_descompensado)

f_0db = find_0db_crossing(freq, mag_db)

fig, axs = plt.subplots(2, 1, sharex=True, figsize=(8, 8))

# Gráfico de magnitud
axs[0].semilogx(freq, mag_db, linewidth=3, color="tab:blue", label="Magnitud (Compensado)")
axs[0].semilogx(freq_desc, mag_db_desc, linewidth=2, color="gray", linestyle=':', label="Magnitud (Descompensado)")
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

# Gráfico de fase
axs[1].semilogx(freq, fase_deg, linewidth=3, color="tab:green", label=phase_legend)
axs[1].semilogx(freq_desc, fase_deg_desc, linewidth=2, color="gray", linestyle=':', label="Fase (Descompensado)")
if f_0db is not None:
    axs[1].axvline(f_0db, color="tab:red", linestyle='--', linewidth=1.5)
axs[1].set_xlabel("Frecuencia (Hz)")
axs[1].set_ylabel("Fase (°)")
axs[1].grid(True, which="both", alpha=0.3)
axs[1].legend(fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(capturas_dir, "LDO_Bode_lazo_tension_compensado.png"), dpi=300)
plt.show()
