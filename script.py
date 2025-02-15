# %% Step 0: Loading
import numpy as np
import pandas as pd
from NRCS import generate_precipitation_nrcs, convolve_hydrograph, generate_unit_hydrograph_nrcs
from concentration_time import calculate_tc_kirpich
from hyetogram_transform import transform_hyetogram
import matplotlib.pyplot as plt

# %% Step 1: Generate precipitation hietogram
# Step 2: Define inputs and constants
length_cauce = 58.75  # Longitud del cauce en Km
basin_area = 546 # Área de la cuenca en Km²
h_max = 310  # Altura máxima en la cuenca en m
h_min = 5  # Altura mínima en la cuenca en m
P_3_10 = 79  # Precipitación máxima en 3 horas con un periodo de retorno de 10 años
Tr = 100  # Periodo de retorno en años
NC = 60 # Número de curva
I_min = 2.4  # Infiltración mínima del en mm/h 

slope = (h_max - h_min) / 1000 / length_cauce  # Pendiente del cauce en m/m

tc = calculate_tc_kirpich(length_cauce, slope)
d=5/60
precipitation_nrcs = generate_precipitation_nrcs(tc,P_3_10, Tr, basin_area, NC, I_min,d)

time_intervals = np.array(precipitation_nrcs["Time (hours)"])
hyetogram = np.array(precipitation_nrcs["Precipitation (mm)"])
effective_precipitation = np.array(precipitation_nrcs["Effective Precipitation (mm)"])

transformed_hyetogram = transform_hyetogram(time_intervals, hyetogram, 5/60)

# %% Step 2: Plotting the hietogram and effective precipitation
plt.bar(time_intervals, hyetogram, width=0.1, align='center', label='Total Precipitation')
plt.bar(time_intervals, effective_precipitation, width=0.1, align='center', label='Effective Precipitation', alpha=0.7)
plt.xlabel('Duration (hours)')
plt.ylabel('Precipitation (mm)')
plt.title('Precipitation Hietogram')
plt.legend()
plt.show()

# Imprimir durations y hietogram en forma de columnas con 2 decimales
print("Durations (hours) | Precipitation (mm) | Effective Precipitation (mm)")
for duration, precipitation, effective in zip(time_intervals, hyetogram, effective_precipitation):
    print(f"{duration:<17.2f} | {precipitation:.2f} | {effective:.2f}")

# %% Generar y plotear el hidrograma unitario
time_steps, unit_hydrograph = generate_unit_hydrograph_nrcs(tc, basin_area)

plt.plot(time_steps, unit_hydrograph)
plt.xlabel('Time (hours)')
plt.ylabel('Flow (m³/s)')
plt.title('NRCS Unit Hydrograph')
plt.show()


# Generar la convolución entre el hidrograma unitario y la precipitación corregida
hydrograph = convolve_hydrograph(unit_hydrograph, effective_precipitation)

# Plotear el hidrograma convolucionado
plt.plot(time_steps[:len(hydrograph)], hydrograph)
plt.xlabel('Time (hours)')
plt.ylabel('Flow (m³/s)')
plt.title('Convoluted Hydrograph')
plt.show()

# %%

