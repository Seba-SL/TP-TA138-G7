import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# =========================================
# MEDICIONES REALES
# =========================================

# Resistencias de carga [ohm]
R = np.array([100000,10000,4700,1000, 560, 220,100, 47, 23.5, 10])

Vo_ideal = 5
# Mediciones de Vo
Vo_mult = np.array([Vo_ideal- 0.1814 ,Vo_ideal-0.1921,Vo_ideal-0.1929,Vo_ideal- 0.1962,Vo_ideal - 0.1975,Vo_ideal -0.205,Vo_ideal - 0.217 , Vo_ideal-0.237,Vo_ideal-0.235,Vo_ideal - 0.373])


# =========================================
# INTERPOLACION
# =========================================

R_interp = np.linspace(R.min(), R.max(), 400)

f_mult = interp1d(R, Vo_mult, kind='linear')


# =========================================
# DATOS LTSPICE
# =========================================

archivo = "/home/sebastian/FIUBA-2do Cuatrimestre/Taller de Diseño Electrónico TA138/TP_Taller_de_Diseño_ TA138_G7/Simulación/LDO/Graficos en Python/Datos de Ltspice/LDO/regulacion_carga_Vo_vsIL.txt"

# Cargar archivo
datos = np.loadtxt(archivo, skiprows=1)

IL = datos[:,0]      # Corriente [A]
Vo_lt = datos[:,1]   # Tension [V]

# =========================================
# CONVERSION A RESISTENCIA
# RL = Vo / IL
# =========================================

# Evitar division por cero
mask = IL > 0

IL = IL[mask]
Vo_lt = Vo_lt[mask]

RL_lt = Vo_lt / IL

# Filtrar valores invalidos
mask_valid = Vo_lt > 0

RL_lt = RL_lt[mask_valid]
Vo_lt = Vo_lt[mask_valid]

# =========================================
# GRAFICO
# =========================================

plt.figure(figsize=(9,5))

# Curvas interpoladas medidas
plt.plot(   R_interp,f_mult(R_interp),label='Vo Multimetro',linewidth=3.5)


# Puntos medidos
plt.scatter(R, Vo_mult, s=80)

# Curva LTspice
#plt.plot(RL_lt,Vo_lt,'--',linewidth=3,label='Simulación LTspice')

# =========================================
# TEXTOS
# =========================================

plt.xlabel('Resistencia de carga RL [Ω]')
plt.ylabel('Tension de salida Vo [V]')
plt.title('Regulacion de carga del LDO')

plt.grid(True)
plt.legend( fontsize=12)

# =========================================
# CALCULO Rt
# =========================================

V1_mult = Vo_mult[5]
R1_mult = R[5]

V2_mult = Vo_mult[3]
R2_mult = R[3]

print("Vo1 = "+ str(V1_mult) , "R_1: " + str(R1_mult) +"\n")
print("Vo1 = "+ str(V2_mult) , "R_2: " + str(R2_mult))


RT_mult = (
    ((1 - (V1_mult/V2_mult))*R2_mult) /
    (((V1_mult/V2_mult)*(R2_mult/R1_mult)) - 1)
)


texto = (
    f'Rt_mult = {RT_mult:.2f} Ω'
)

plt.text(
    0.88, 0.02,
    texto,
    fontsize=12,
    ha='right',
    va='bottom',
    transform=plt.gca().transAxes,
    bbox=dict(facecolor='white', alpha=0.85)
)

# =========================================
# CARTEL MEDICIONES
# =========================================

texto = (
    'Valores medidos:\n\n'
    f'RL = {R[0]:.1f} Ω  |  Vo_mult = {Vo_mult[0]:.2f} V   \n'
    f'RL = {R[1]:.1f} Ω  |  Vo_mult = {Vo_mult[1]:.2f} V  \n'
    f'RL = {R[2]:.1f} Ω  |  Vo_mult = {Vo_mult[2]:.2f} V   \n'
    f'RL = {R[3]:.1f} Ω  |  Vo_mult = {Vo_mult[3]:.2f} V  \n'
    f'RL = {R[4]:.1f} Ω  |  Vo_mult = {Vo_mult[4]:.2f} V \n'
    f'RL = {R[5]:.1f} Ω  |  Vo_mult = {Vo_mult[5]:.2f} V'
)

plt.text(
    0.88, 0.6,
    texto,
    fontsize=12,
    ha='right',
    va='top',
    transform=plt.gca().transAxes,
    bbox=dict(facecolor='white', alpha=0.9)
)

# =========================================
# MOSTRAR
# =========================================

plt.show()