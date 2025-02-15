#%% Packages
import pandas as pd
import numpy as np

#%%
# Parámetros configurables
archivo_entrada = "./_test/cuencaOeste_Tr100.csv"  # Nombre del archivo de entrada
num_valores_salida = 100  # Número de puntos deseados en la salida
archivo_salida = "._/test/hidrograma_tikz.dat"  # Nombre del archivo de salida

def time_to_decimal(time_str):
    """Convierte una hora en formato HH:MM a formato decimal."""
    h, m = map(int, time_str.split(':'))
    return h + m / 60

# Cargar el archivo
try:
    df = pd.read_csv(archivo_entrada, delimiter=",", decimal=".", index_col=False)
    df["TimeDecimal"] = df["Time"].apply(time_to_decimal)
    
    # Seleccionar columnas relevantes
    tiempo = df["TimeDecimal"].values
    caudal = df["Outflow (M3/S)"].values  # Cambiar a "Inflow (M3/S)" si se desea
    
    # Seleccionar valores equidistantes
    indices_seleccionados = np.linspace(0, len(tiempo) - 1, num_valores_salida, dtype=int)
    tiempo_reducido = tiempo[indices_seleccionados]
    caudal_reducido = caudal[indices_seleccionados]
    
    # Guardar en formato TikZ
    with open(archivo_salida, "w") as f:
        f.write("% Tiempo (h)   Caudal (m3/s)\n")
        for t, q in zip(tiempo_reducido, caudal_reducido):
            f.write(f"{t:.2f} {q:.2f}\n")
    
    print(f"Archivo generado correctamente: {archivo_salida}")
except Exception as e:
    print(f"Error al procesar el archivo: {e}")

# %%
a = 2