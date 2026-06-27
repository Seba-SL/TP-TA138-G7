import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# ======================================================
# DATOS
# ======================================================

# Tensión de entrada (ejemplo)
Vin = np.array([
    13.32,
    14.27,
    15.32,
    16.37,
    17.42,
    18.34,
    19.59,
    20.1,
    21.3,
    22.2,
    23.3,
    24.1
])

# Error medido respecto a 9.5 V (mV)
delta_mV = np.array([
     -78,
    -37.7,
    -32.5,
    -30.4,
    -22.3,
    -17.5,
    -17.7,
    -17.8,
    -15.2,
    -12,
    -12.2,
    -11.9
])

# ======================================================
# Conversión a tensión de salida
# ======================================================

Vo_ref = 9.5

Vo = Vo_ref + delta_mV/1000.0

# ======================================================
# Interpolación
# ======================================================

Vin_interp = np.linspace(Vin.min(), Vin.max(), 400)

spl = make_interp_spline(Vin, Vo, k=3)
Vo_interp = spl(Vin_interp)

# ======================================================
# Gráfico
# ======================================================

plt.figure(figsize=(8,5))

# Línea ideal
plt.plot(
    Vin_interp,
    np.full_like(Vin_interp, Vo_ref),
    '--',
    color='gray',
    linewidth=2,
    label='Salida ideal (9.5 V)'
)

# Curva interpolada
plt.plot(
    Vin_interp,
    Vo_interp,
    color='tab:blue',
    linewidth=2.5,
    label='Buck (interpolación)'
)

# Mediciones
plt.scatter(
    Vin,
    Vo,
    color='red',
    s=50,
    zorder=5,
    label='Mediciones'
)

plt.grid(True)

plt.xlabel(r'$V_{in}$ [V]')
plt.ylabel(r'$V_{out}$ [V]')

plt.title('Regulación de línea del convertidor Buck',fontsize = 15)

plt.legend(fontsize = 13)

# Zoom para apreciar variaciones pequeñas
plt.ylim(9.40, 9.55)

plt.tight_layout()
plt.show()