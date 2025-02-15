def calculate_tc_kirpich(length, slope):
    # Kirpich method: Tc = 0.01947 * L^0.77 * S^-0.385
    return 0.066 * (length ** 0.77) * (slope ** -0.385)

def calculate_tc_uruguay(area, slope, runoff_coefficient):
    # Uruguay method: Tc = To + 6.625 * A^0.3 * P^-0.38 * C^-0.45
    return 6.625 * (area ** 0.3) * (slope ** -0.38) * (runoff_coefficient ** -0.45)