import re
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

base_dir = Path(__file__).resolve().parent
input_path = base_dir / "bode_descompensado.txt"
input_path2 = base_dir / "bode_descompensado10.txt"
compensated_input_path = base_dir / "bode_compensado.txt"
compensated_input_path2 = base_dir / "bode_compensado6.txt"
response_path = base_dir / "respuesta_descompensado.txt"
response_compensated_path = base_dir / "respuesta_compensado.txt"
out_dir = base_dir.parent.parent.parent / "Checkpoints" / "Checkpoint 5" / "Informe CHK 5" / "img" / "BUCK"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "bode_descompensado.png"
out_path_response = out_dir / "respuesta_descompensado.png"
out_path_compensated = out_dir / "bode_compensado.png"
out_path_response_compensated = out_dir / "respuesta_compensado.png"


def parse_bode_file(path):
    freqs = []
    mags = []
    phs = []
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("Freq"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                freq = float(parts[0])
            except ValueError:
                continue
            values = re.findall(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", parts[1])
            if len(values) >= 2:
                freqs.append(freq)
                mags.append(float(values[0]))
                phs.append(float(values[1]))
    return freqs, mags, phs


def parse_response_file(path):
    times = []
    values = []
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("time"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                t = float(parts[0])
                v = float(parts[1])
            except ValueError:
                continue
            times.append(t)
            values.append(v)
    return times, values

frequencies, magnitudes, phases = parse_bode_file(input_path)
frequencies2, magnitudes2, phases2 = parse_bode_file(input_path2)
comp_frequencies, comp_magnitudes, comp_phases = parse_bode_file(compensated_input_path)
comp_frequencies2, comp_magnitudes2, comp_phases2 = parse_bode_file(compensated_input_path2)
response_times, response_values = parse_response_file(response_path)
response_comp_times, response_comp_values = parse_response_file(response_compensated_path)

phases = np.unwrap(np.deg2rad(phases), discont=np.pi)
phases = np.rad2deg(phases)
phases2 = np.unwrap(np.deg2rad(phases2), discont=np.pi)
phases2 = np.rad2deg(phases2)

phase_cross_freq = None
for i in range(1, len(phases)):
    if (phases[i - 1] >= -180 and phases[i] <= -180) or (phases[i - 1] <= -180 and phases[i] >= -180):
        x1, x2 = frequencies[i - 1], frequencies[i]
        y1, y2 = phases[i - 1], phases[i]
        phase_cross_freq = x1 + (-180 - y1) * (x2 - x1) / (y2 - y1) if y2 != y1 else x1
        break

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
if phase_cross_freq is not None:
    for ax in (ax1, ax2):
        ax.axvline(phase_cross_freq, color="gray", linestyle=(0, (5, 5)), linewidth=1.2, alpha=0.8)

ax1.semilogx(frequencies, magnitudes, color="tab:blue", linewidth=1.8, label=r"$R = 100\Omega$")
ax1.semilogx(frequencies2, magnitudes2, color="tab:orange", linewidth=1.8, label=r"$R = 6\Omega$")
ax1.set_ylabel("Magnitud (dB)")
ax1.tick_params(axis="y")
ax1.set_title("Ganancia de lazo - Descompensado")
ax1.grid(True, which="both", linestyle="--", alpha=0.4)
ax1.legend(loc="best")

ax2.semilogx(frequencies, phases, color="tab:blue", linewidth=1.8)
ax2.semilogx(frequencies2, phases2, color="tab:orange", linewidth=1.8)
ax2.set_xlabel("Frecuencia (Hz)")
ax2.set_ylabel("Fase (°)")
ax2.tick_params(axis="y")
ax2.grid(True, which="both", linestyle="--", alpha=0.4)
ax2.legend(loc="best")

fig.tight_layout()
fig.savefig(out_path, dpi=300, bbox_inches="tight")
plt.show()
plt.close(fig)

# Compensado
phases_comp = np.unwrap(np.deg2rad(comp_phases), discont=np.pi)
phases_comp = np.rad2deg(phases_comp)
phases_comp2 = np.unwrap(np.deg2rad(comp_phases2), discont=np.pi)
phases_comp2 = np.rad2deg(phases_comp2)

phase_cross_freq_comp = None
for i in range(1, len(phases_comp)):
    if (phases_comp[i - 1] >= -180 and phases_comp[i] <= -180) or (phases_comp[i - 1] <= -180 and phases_comp[i] >= -180):
        x1, x2 = comp_frequencies[i - 1], comp_frequencies[i]
        y1, y2 = phases_comp[i - 1], phases_comp[i]
        phase_cross_freq_comp = x1 + (-180 - y1) * (x2 - x1) / (y2 - y1) if y2 != y1 else x1
        break

fig_comp, (ax4, ax5) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
if phase_cross_freq_comp is not None:
    for ax in (ax4, ax5):
        ax.axvline(phase_cross_freq_comp, color="gray", linestyle=(0, (5, 5)), linewidth=1.2, alpha=0.8)

ax4.semilogx(comp_frequencies, comp_magnitudes, color="tab:blue", linewidth=1.8, label=r"$R = 100\Omega$")
ax4.semilogx(comp_frequencies2, comp_magnitudes2, color="tab:orange", linewidth=1.8, label=r"$R = 6\Omega$")
ax4.set_ylabel("Magnitud (dB)")
ax4.tick_params(axis="y")
ax4.set_title("Ganancia de lazo - Compensado")
ax4.grid(True, which="both", linestyle="--", alpha=0.4)
ax4.legend(loc="best")

ax5.semilogx(comp_frequencies, phases_comp, color="tab:blue", linewidth=1.8)
ax5.semilogx(comp_frequencies2, phases_comp2, color="tab:orange", linewidth=1.8)
ax5.set_xlabel("Frecuencia (Hz)")
ax5.set_ylabel("Fase (°)")
ax5.tick_params(axis="y")
ax5.grid(True, which="both", linestyle="--", alpha=0.4)
ax5.legend(loc="best")

fig_comp.tight_layout()
fig_comp.savefig(out_path_compensated, dpi=300, bbox_inches="tight")
plt.show()
plt.close(fig_comp)

# Respuesta en el tiempo hasta 2 ms - descompensado
max_time = 2e-3
response_times_limited = [t for t in response_times if t <= max_time]
response_values_limited = response_values[: len(response_times_limited)]
response_times_ms = [t * 1e3 for t in response_times_limited]

fig2, ax3 = plt.subplots(figsize=(9, 4.5))
ax3.plot(response_times_ms, response_values_limited, color="tab:green", linewidth=1.8)
ax3.set_xlabel("Tiempo (ms)")
ax3.set_ylabel("V(vo)")
ax3.set_title("Respuesta descompensada")
ax3.grid(True, linestyle="--", alpha=0.4)
fig2.tight_layout()
fig2.savefig(out_path_response, dpi=300, bbox_inches="tight")
plt.show()
plt.close(fig2)

# Respuesta en el tiempo hasta 2 ms - compensado
response_comp_times_limited = [t for t in response_comp_times if t <= max_time]
response_comp_values_limited = response_comp_values[: len(response_comp_times_limited)]
response_comp_times_ms = [t * 1e3 for t in response_comp_times_limited]

fig3, ax4 = plt.subplots(figsize=(9, 4.5))
ax4.plot(response_comp_times_ms, response_comp_values_limited, color="tab:purple", linewidth=1.8)
ax4.set_xlabel("Tiempo (ms)")
ax4.set_ylabel("V(vo)")
ax4.set_title("Respuesta compensada")
ax4.grid(True, linestyle="--", alpha=0.4)
fig3.tight_layout()
fig3.savefig(out_path_response_compensated, dpi=300, bbox_inches="tight")
plt.show()
plt.close(fig3)

print(f"Gráfico de Bode descompensado guardado en: {out_path}")
print(f"Respuesta descompensada guardada en: {out_path_response}")
print(f"Gráfico de Bode compensado guardado en: {out_path_compensated}")
print(f"Respuesta compensada guardada en: {out_path_response_compensated}")
