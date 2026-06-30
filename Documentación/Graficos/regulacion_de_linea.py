import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# =========================================
# Tension de alimentacion Vcc [V]
# =========================================

Vcc = np.array([4.28,5.03,5.31,5.69,6.01,7.03,8.08,9.2,10.19,12.2,13.62,14.33,15.94])

# =========================================
# Mediciones de Vo
# =========================================
Vo_fija = 5
# Multimetro
Vo_mult = np.array([Vo_fija-2.51,Vo_fija-0.570,Vo_fija-0.1992,Vo_fija-0.1954,Vo_fija-0.194,Vo_fija-0.1931,Vo_fija-0.1927,Vo_fija-0.1916,Vo_fija-0.1911,Vo_fija-0.1903,Vo_fija-0.1889,Vo_fija-0.1887,Vo_fija-0.1872])

#
# =========================================
# Interpolacion
# =========================================

Vcc_interp = np.linspace(Vcc.min(), Vcc.max(), 400)

f_mult = interp1d(Vcc, Vo_mult , kind='linear')

# =========================================
# Figura
# =========================================

plt.figure(figsize=(10,5))

# Curvas interpoladas
plt.plot(Vcc_interp, f_mult(Vcc_interp),linewidth=3, label='Vo Multimetro')

# Puntos medidos
plt.scatter(Vcc, Vo_mult)
# =========================================
# Etiquetas
# =========================================

plt.xlabel('Tension de alimentacion Vcc [V]')
plt.ylabel('Tension de salida Vo [V]')
plt.title('Regulacion de linea del LDO')

plt.grid(True)
plt.legend()

# =========================================
# Calculo regulacion de linea
# =========================================

Vo1_mult = Vo_mult[1]
Vo2_mult = Vo_mult[-1]


Vcc1 = Vcc[1]
Vcc2 = Vcc[-1]


Reg_mult = (Vo2_mult - Vo1_mult) / (Vcc2 - Vcc1)


# =========================================
# Cartel
# =========================================

texto = (
    'Regulacion de linea\n\n'

    f'Vcc1 = {Vcc1:.2f} V\n'
    f'Vcc2 = {Vcc2:.2f} V\n'

    f'Multimetro:\n'
    f'Vo1 = {Vo1_mult:.2f} V\n'
    f'Vo2 = {Vo2_mult:.2f} V\n'
    f'RL_mult = {Reg_mult:.5f} V/V\n\n'


)

plt.text(
    14, 4.64,
    texto,
    fontsize=9,
    bbox=dict(facecolor='white', alpha=0.9)
)

# Limites eje Y
plt.ylim(4.6, 5.1)

plt.show()