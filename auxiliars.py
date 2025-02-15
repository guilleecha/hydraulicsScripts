import numpy as np

def calculate_CT(return_period):
    """Calculate CT(Tr) based on the given formula."""
    if return_period <= 1:
        raise ValueError("Return period must be greater than 1 year.")
    ln_term = np.log(return_period / (return_period - 1))
    return 0.5786 - 0.4312 * np.log10(ln_term)

def calculate_CD(duration):
    """Calculate CD(d) based on the given formula."""
    if duration <= 3:
        return (0.6208 * duration) / ((duration + 0.0137) ** 0.5639)
    else:
        return (1.0287 * duration) / ((duration + 1.0293) ** 0.8083)

def calculate_CA(area, duration):
    """Calculate CA(Ac,d) based on the given formula."""
    return 1.0 - (0.3549 * duration ** -0.4272) * (1.0 - np.exp(-0.005792 * area))
