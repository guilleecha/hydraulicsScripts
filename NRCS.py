# %% Step 0: Loading
import numpy as np
import pandas as pd
from auxiliars import calculate_CT, calculate_CA, calculate_CD
from hyetogram_transform import transform_hyetogram

# %% Step 1: Precipitation NRCS
def generate_precipitation_nrcs(tc, P3_10, return_period, area, NC, I_min, d):
    """
    Generates the hyetograph using the NRCS methodology.
    :param tc: Time of concentration in hours.
    :param P3_10: Maximum precipitation in 3 hours with a 10-year return period.
    :param return_period: Return period in years.
    :param area: Basin area in km².
    :param NC: Curve number.
    :param I_min: Minimum infiltration rate in mm/h.
    :return: Hyetograph (precipitation as a function of time).
    """

    D = tc / 7 * 12  # Total storm duration in hours
    intervals = np.ceil(D / d).astype(int)
    durations = [(i + 1) * d for i in range(intervals)]
    P_max_values = []

    CT = calculate_CT(return_period)

    for duration in durations:
        CA = calculate_CA(area, duration)
        CD = calculate_CD(duration)
        P_max = P3_10 * CT * CA * CD
        P_max_values.append(P_max)

    INCP = np.diff([0] + P_max_values)
    
    alternating_precipitation = distribute_precipitation_alternating(INCP)

    precipitation = alternating_precipitation

    effective_precipitation = correct_precipitation_infiltration(precipitation, NC, d, I_min)

    precipitation_nrcs = pd.DataFrame({
        "Time (hours)": durations,
        "Precipitation (mm)": precipitation,
        "Infiltration (mm)": precipitation - effective_precipitation,
        "Effective Precipitation (mm)": effective_precipitation
    })


    return precipitation_nrcs


def distribute_precipitation_alternating(INCP):
    """
    Distribute precipitation increments (INCP) using the alternating block method.

    Args:
        INCP (array): Array of incremental precipitation values.

    Returns:
        array: Array of precipitation values distributed using the alternating block method.
    """
    n = len(INCP)
    INCP_sorted = np.sort(INCP)[::-1]  # Sort increments in descending order
    alternating_block = np.zeros_like(INCP_sorted)

    # Place the maximum value in the center
    mid_index = n // 2
    alternating_block[mid_index] = INCP_sorted[0]

    # Alternate remaining values left and right
    left, right = mid_index - 1, mid_index + 1
    for i in range(1, n):
        if i % 2 == 0:  # Odd index: place to the right
            if right < n:  # Ensure within bounds
                print(i, "right",right, INCP_sorted[i])
                alternating_block[right] = INCP_sorted[i]
                right += 1
        else:  # Even index: place to the left
            if left >= 0:  # Ensure within bounds
                print(i, "left",left, INCP_sorted[i])
                alternating_block[left] = INCP_sorted[i]
                left -= 1

    return alternating_block


def correct_precipitation_infiltration(precipitation, curve_number, d, I_min):
    """
    Corrects precipitation for infiltration using the curve number.
    :param precipitation: Array of precipitation values (hyetograph).
    :param curve_number: Curve number (CN).
    :param d: Duration increment.
    :param I_min: Minimum infiltration rate in mm/h.
    :return: Array of corrected precipitation values.
    """
    S = (25400 / curve_number) - 254  # Maximum retention capacity
    Ia = 0.2 * S  # Initial abstraction

    # Calculate cumulative precipitation
    cumulative_precipitation = np.cumsum(precipitation)

    # Correct cumulative precipitation
    runoff_accumulated = np.zeros_like(cumulative_precipitation)

    for i, P in enumerate(cumulative_precipitation):
        if P > Ia:
            runoff_accumulated[i] = ((P - Ia) ** 2) / (P + 0.8 * S)
        else:
            runoff_accumulated[i] = 0

    # Calculate incremental runoff
    incremental_runoff = np.diff([0] + runoff_accumulated.tolist())

    # Calculate deficit (storage)
    deficit = precipitation - incremental_runoff

    # Correct deficit for minimum infiltration rate
    corrected_deficit = np.maximum(deficit, I_min * d)

    effective_precipitation = precipitation - corrected_deficit

    return effective_precipitation

def convolve_hydrograph(precipitation, unit_hydrograph):
    """
    Generates the convolution between the unit hydrograph and the precipitation.
    :param precipitation: Array of precipitation values.
    :param unit_hydrograph: Array of unit hydrograph values.
    :return: Array of convoluted hydrograph values.
    """
    return np.convolve(unit_hydrograph, precipitation, )[:len(precipitation)]

# %% Step 1: Hydrograph

def generate_unit_hydrograph_nrcs(tc, area):
    """
    Generates the hydrograph using the NRCS methodology.
    :param tc: Time of concentration in hours.
    :param area: Basin area in km².
    :return: Hydrograph (flow as a function of time).
    """
    X = 1.67  # Factor for calculating the base time of the NRCS
    d = tc / 7
    D = d * 12  # Total storm duration in hours
    
    Tp = (d / 2) + (0.6 * tc)  # Time to peak
    Tb = (1 + X) * Tp  # Total base time of the hydrograph
    qp = 0.208 * (area / Tp)  # Peak flow

    time_steps = np.linspace(0, Tb, 100)  # 100 time steps for the hydrograph
    hydrograph = np.zeros_like(time_steps)

    # Rising limb (from 0 to Tp)
    hydrograph[time_steps <= Tp] = (qp / Tp) * time_steps[time_steps <= Tp]
    # Falling limb (from Tp to Tb)
    hydrograph[time_steps > Tp] = qp * (1 - (time_steps[time_steps > Tp] - Tp) / (Tb - Tp))

    return time_steps, hydrograph