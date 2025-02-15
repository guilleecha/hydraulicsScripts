import pandas as pd

def load_data(file_path):
    """
    Loads a CSV file containing hydrograph data and processes it into a structured format.
    
    Parameters:
    - file_path: Path to the input CSV file.
    
    Returns:
    - df: DataFrame containing columns ["Date", "Time", "Q_inflow", "Q_outflow", "Time_h"].
    """
    # Read first row to detect if it's a 4-column header
    df_check = pd.read_csv(file_path, delimiter=",", dtype=str, nrows=1, engine="python")
    
    if df_check.shape[1] == 4:
        # Read again, skipping the first row
        df = pd.read_csv(file_path, delimiter=",", dtype=str, skiprows=1, index_col=False, engine="python")
    else:
        df = pd.read_csv(file_path, delimiter=",", dtype=str, index_col=False, engine="python")
    
    # Ensure the file has at least 6 columns in data rows (to handle decimal separator issue)
    if df.shape[1] < 6:
        raise ValueError("The CSV file does not contain enough columns. Check the delimiter and file format.")
    
    # Assign correct column names
    df.columns = ["Date", "Time", "Q1", "Q2", "Q3", "Q4"]
    
    # Convert Q_inflow and Q_outflow correctly by merging decimal-separated columns
    df["Q_inflow"] = (df["Q1"].str.replace(",", ".") + "." + df["Q2"].str.replace(",", ".")).astype(float)
    df["Q_outflow"] = (df["Q3"].str.replace(",", ".") + "." + df["Q4"].str.replace(",", ".")).astype(float)
    
    # Keep only relevant columns
    df = df[["Date", "Time", "Q_inflow", "Q_outflow"]].copy()
    
    # Convert the time to hours (assuming the index represents minutes)
    df["Time_h"] = df.index / 60
    
    return df