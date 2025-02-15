from hecdss import HecDss
import pandas as pd
import re
from collections import defaultdict

# Ruta del archivo de catálogo externo
CATALOG_FILE_PATH = "./_test/Tr25_NRCS_catalog"

# Lista de archivos DSS de entrada
INPUT_FILES = [
    "./_test/TR25.dss"]

def load_catalog_from_file():
    """
    Carga los pathnames desde el archivo de catálogo externo y los organiza en categorías.
    """
    try:
        with open(CATALOG_FILE_PATH, "r", encoding="utf-8") as file:
            catalog_paths = [line.strip() for line in file.readlines()]
        print(f"✅ Catálogo cargado con {len(catalog_paths)} registros.")
        
        # Organizar pathnames por elemento (Part B) y variable (Part C)
        categorized_paths = defaultdict(lambda: defaultdict(list))
        for path in catalog_paths:
            parts = path.split("/")
            if len(parts) > 2:
                categorized_paths[parts[1]][parts[2]].append(path)
        
        return categorized_paths
    except Exception as e:
        print(f"❌ Error al cargar el catálogo: {e}")
        return {}

def select_pathname():
    """
    Permite al usuario seleccionar un pathname desde el catálogo externo organizado por elementos y variables.
    """
    categorized_paths = load_catalog_from_file()
    if not categorized_paths:
        print("❌ No se encontraron pathnames en el catálogo.")
        return None
    
    # Mostrar los elementos disponibles (Part B) con opciones numeradas
    elements = list(categorized_paths.keys())
    print("\n🔹 Elementos disponibles:")
    element_mapping = {i: element for i, element in enumerate(elements)}
    for i, element in element_mapping.items():
        print(f"{i}: {element}")
    
    while True:
        try:
            element_choice = int(input("Ingrese el número del elemento deseado: "))
            if element_choice in element_mapping:
                selected_element = element_mapping[element_choice]
                break
            else:
                print("❌ Opción fuera de rango. Intente de nuevo.")
        except ValueError:
            print("❌ Entrada inválida. Ingrese un número válido.")
    
    # Mostrar las variables disponibles (Part C) dentro del elemento seleccionado
    variables = list(categorized_paths[selected_element].keys())
    print("\n🔹 Variables disponibles para el elemento seleccionado:")
    variable_mapping = {i: variable for i, variable in enumerate(variables)}
    for i, variable in variable_mapping.items():
        print(f"{i}: {variable}")
    
    while True:
        try:
            variable_choice = int(input("Ingrese el número de la variable deseada: "))
            if variable_choice in variable_mapping:
                selected_variable = variable_mapping[variable_choice]
                break
            else:
                print("❌ Opción fuera de rango. Intente de nuevo.")
        except ValueError:
            print("❌ Entrada inválida. Ingrese un número válido.")
    
    # Mostrar los pathnames dentro de la categoría seleccionada con opciones numeradas
    pathnames = categorized_paths[selected_element][selected_variable]
    print("\n🔹 Pathnames disponibles en la variable seleccionada:")
    path_mapping = {i: path for i, path in enumerate(pathnames)}
    for i, path in path_mapping.items():
        print(f"{i}: {path}")
    
    while True:
        try:
            choice = int(input("Ingrese el número del pathname deseado: "))
            if choice in path_mapping:
                return path_mapping[choice]
            else:
                print("❌ Opción fuera de rango. Intente de nuevo.")
        except ValueError:
            print("❌ Entrada inválida. Ingrese un número válido.")

def load_dss_data(file_paths):
    """
    Reads time-series data from multiple DSS files using HecDss, allowing the user to select the dataset.

    Parameters:
    - file_paths (list of str): List of paths to DSS files.

    Returns:
    - df (pd.DataFrame): DataFrame containing time and flow data from all files.
    """
    data_list = []
    
    for file_path in file_paths:
        print(f"\n📂 Procesando archivo DSS: {file_path}")
        pathname = select_pathname()
        if not pathname:
            print(f"⚠ Saltando archivo {file_path} debido a errores en la selección del pathname.")
            continue
        
        # Abrir el archivo DSS y leer los datos
        with HecDss(file_path) as dss:
            try:
                print("📥 Leyendo datos del DSS...")
                data = dss.get(pathname)
                print("✅ Datos obtenidos correctamente.")
                
                if not hasattr(data, "times") or not hasattr(data, "values"):
                    print(f"⚠ Advertencia: No se pudieron extraer datos válidos de {file_path} en {pathname}")
                    continue
            except Exception as e:
                print(f"❌ Error al leer datos de {file_path} en {pathname}: {e}")
                continue
        
        # Manejar TS-PATTERN y rangos de fechas para evitar errores
        part_D = pathname.split("/")[3]
        if "TS-PATTERN" in part_D or "-" in part_D:
            print(f"⚠ Advertencia: El pathname '{pathname}' usa un rango de fechas o TS-PATTERN. Se omitirá la conversión de fecha.")
            df_time = pd.Series(range(len(data.values)))  # Crear índice numérico
        else:
            df_time = pd.to_datetime(data.times, errors='coerce')
        
        print("🛠 Construyendo DataFrame...")
        df = pd.DataFrame({
            "Time": df_time,  
            "Q_outflow": data.values,  
            "Source_File": file_path,  
            "Pathname": pathname  
        })
        
        if "TS-PATTERN" not in part_D and "-" not in part_D:
            df = df.dropna(subset=["Time"])
        
        if df.empty:
            print(f"⚠ Advertencia: No hay datos válidos en {file_path} ({pathname}).")
            continue
        
        if "TS-PATTERN" not in part_D and "-" not in part_D:
            df["Time_h"] = (df["Time"] - df["Time"].iloc[0]).dt.total_seconds() / 3600
        else:
            df["Time_h"] = df.index.astype(float)
        
        print(f"✅ DataFrame creado con {len(df)} filas.")
        data_list.append(df)
    
    if not data_list:
        raise ValueError("❌ No se pudieron extraer datos válidos de ningún archivo DSS.")
    
    return pd.concat(data_list, ignore_index=True)
