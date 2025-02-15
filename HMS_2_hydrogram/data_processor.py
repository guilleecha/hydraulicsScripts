def time_to_decimal(time_str):
    """
    Convierte una hora en formato HH:MM a horas en formato decimal.
    Ejemplo: '01:30' -> 1.50
    """
    try:
        h, m = map(int, time_str.split(':'))
        return h + m / 60
    except Exception as e:
        print(f"Error en la conversión del tiempo '{time_str}': {e}")
        return None

def procesar_linea(line):
    """
    Procesa una línea del archivo y retorna (tiempo_decimal, Q_inflow, Q_outflow).

    Se asume que la línea tiene 6 tokens:
      - Token 0: Fecha
      - Token 1: Hora (HH:MM)
      - Tokens 2 y 3: Juntos forman Q_inflow (ejemplo: '0' y '0' para 0,0)
      - Tokens 4 y 5: Juntos forman Q_outflow
    """
    line = line.strip()
    if not line:
        return None
    tokens = line.split(",")
    
    if len(tokens) == 6:
        time_str = tokens[1]
        t_decimal = time_to_decimal(time_str)
        if t_decimal is None:
            return None
        
        # Combinar tokens para Q_inflow y Q_outflow
        q_in_str = tokens[2] + "," + tokens[3]
        q_out_str = tokens[4] + "," + tokens[5]
        
        try:
            q_inflow = float(q_in_str.replace(",", "."))
            q_outflow = float(q_out_str.replace(",", "."))
        except Exception as e:
            print(f"Error al convertir los valores '{q_in_str}' o '{q_out_str}': {e}")
            return None
        
        return t_decimal, q_inflow, q_outflow

    elif len(tokens) == 4:
        # Caso alternativo si la línea ya viene con 4 tokens (sin problemas de separadores decimales)
        time_str = tokens[1]
        t_decimal = time_to_decimal(time_str)
        if t_decimal is None:
            return None
        try:
            q_inflow = float(tokens[2].replace(",", "."))
            q_outflow = float(tokens[3].replace(",", "."))
        except Exception as e:
            print(f"Error al convertir los valores en línea: {e}")
            return None
        return t_decimal, q_inflow, q_outflow
    else:
        print(f"Línea con número inesperado de tokens ({len(tokens)}): {tokens}")
        return None
