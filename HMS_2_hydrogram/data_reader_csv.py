import pandas as pd

def load_csv_data(file_path):
    """
    Loads a CSV file containing hydrograph data with columns: Date, Time, Total Flow (M3/S)
    and processes it into a structured format.
    
    Parameters:
    - file_path: Path to the input CSV file.
    
    Returns:
    - df: DataFrame containing columns ["Date", "Time", "Q_outflow", "Time_h"].
    """
    df = pd.read_csv(file_path, delimiter=",", dtype=str, index_col=False, engine="python")
    
    # Trim excessive columns if necessary
    df = df.iloc[:, :3]
    
    # Ensure the file has at least 3 columns
    if df.shape[1] < 3:
        raise ValueError("The CSV file does not contain enough columns. Check the delimiter and file format.")
    
    # Assign correct column names
    df.columns = ["Date", "Time", "Q_outflow"]
    
    # Convert Q_outflow to float
    df["Q_outflow"] = df["Q_outflow"].astype(float)
    
    # Convert time to hours (assuming format hh:mm)
    df["Time_h"] = df["Time"].apply(lambda x: int(x.split(":")[0]) + int(x.split(":")[1]) / 60.0)
    
    return df