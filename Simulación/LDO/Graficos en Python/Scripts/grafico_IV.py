import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Leer los archivos

# directorio donde está el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# rutas
datos_dir = os.path.join(script_dir, "..", "Datos de Ltspice", "LDO")
capturas_dir = os.path.join(script_dir, "..", "Capturas")

# normalizar rutas
datos_dir = os.path.normpath(datos_dir)
capturas_dir = os.path.normpath(capturas_dir)

archivo = os.path.join(datos_dir, "VvsI.txt")

df1 = pd.read_csv(archivo, sep='\t')
df1.columns = ['R', 'V', 'I']

# Crear el gráfico
plt.figure(figsize=(10, 6))

# Scatter plot para Prueba1
plt.scatter(df1['I'], df1['V'], color='blue', s=30, alpha=0.7, edgecolors='black', linewidth=0.5 )


# Etiquetas de los ejes
plt.xlabel(r'$I_o$ (A)', fontsize=12)
plt.ylabel(r'$V_o$ (V)', fontsize=12)
plt.title(r'Gráfico V vs I para $5\Omega > R_L > 0,5\Omega$', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

# Línea vertical punteada en I = 1.5A
plt.axvline(x=1.5, linestyle='--', color='black', linewidth=1, label=r'$I_o$ = 1.5A')

# Mostrar el gráfico
plt.tight_layout()
plt.savefig(os.path.join(capturas_dir, "V vs I.png"), dpi=300)
