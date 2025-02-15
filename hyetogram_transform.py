import numpy as np
import pandas as pd

def transform_hyetogram(time_intervals, hyetogram, new_time_step):
    """
    Transforma el hietograma a un nuevo intervalo de tiempo.
    :param time_intervals: Array de intervalos de tiempo originales.
    :param hyetogram: Array de valores de precipitación originales (mm).
    :param new_time_step: Nuevo intervalo de tiempo para el hietograma (en las mismas unidades).
    :return: DataFrame con el hietograma transformado.
    """

    # Calcular el número de intervalos para el nuevo tiempo
    num_intervals = int((time_intervals[-1] - time_intervals[0]) / new_time_step)

    # Crear los nuevos intervalos de tiempo
    new_time_intervals = np.linspace(time_intervals[0], time_intervals[-1], num_intervals + 1)

    # Interpolar los valores del hietograma
    new_precipitation = np.interp(new_time_intervals, time_intervals, hyetogram)

    # Ajustar la precipitación para conservar el volumen total de lluvia
    scale_factor = np.sum(hyetogram) / np.sum(new_precipitation)
    new_precipitation *= scale_factor

    # Crear un DataFrame para visualizar el nuevo hietograma
    transformed_hyetogram = pd.DataFrame({
        "Time (hours)": new_time_intervals,
        "Precipitation (mm)": new_precipitation
    })

    return transformed_hyetogram
