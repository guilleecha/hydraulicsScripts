#%%
import os
from data_reader import load_data
from data_reader_csv import load_csv_data
from data_writer import write_tikz
from hydrograph_plotter import plot_hydrographs
import numpy as np
#%%
# ==========================
# CONFIGURATION
# ==========================
INPUT_FILES = [
        "./_test/cuencaoeste_tr25_hydrogram.csv",
        "./_test/cuencaoeste_tr100_hydrogram.csv"

]

OUTPUT_FILE = "./_test/hydrograph_tikz.tex"

# Visualization parameters
TIME_MIN = 0.5  # Set lower time limit (e.g., 1.5 for 1h30min)
TIME_MAX = 3  # Set upper time limit
NUM_POINTS = 150  # Number of points to sample in the final output
MARKER_DENSITY = 0.30  # Fraction of points with markers
LABEL_MAX_POINT = True  # Label max flow points
WRAP_TIKZ = True  # Wrap TikZ in figure structure
TABLE_NAME = "hydrograph_data"

def resample_data(times, flows, num_points):
    if len(times) > num_points:
        indices = np.linspace(0, len(times) - 1, num_points, dtype=int)
        return np.array(times)[indices].tolist(), np.array(flows)[indices].tolist()
    return times, flows

def main():
    datasets = []
    labels = []
    times_list = []
    max_times = []
    max_flows = []

    for file in INPUT_FILES:
        if os.path.exists(file):
            df = load_data(file)
            times = df["Time_h"].tolist()
            q_outflows = df["Q_outflow"].tolist()
            
            # Apply time filtering before resampling
            filtered_indices = [i for i, t in enumerate(times) if (TIME_MIN is None or t >= TIME_MIN) and (TIME_MAX is None or t <= TIME_MAX)]
            times = [times[i] for i in filtered_indices]
            q_outflows = [q_outflows[i] for i in filtered_indices]

            # Resample data to reduce number of points
            times, q_outflows = resample_data(times, q_outflows, NUM_POINTS)

            datasets.append(q_outflows)
            labels.append(os.path.splitext(os.path.basename(file))[0])
            times_list.append(times)

            # Get max flow and corresponding time
            max_idx = q_outflows.index(max(q_outflows))
            max_times.append(times[max_idx])
            max_flows.append(q_outflows[max_idx])
        else:
            print(f"Warning: File {file} not found.")

    # Generate plot in Jupyter
    if datasets:
        plot_hydrographs(datasets, labels, times_list, time_min=TIME_MIN, time_max=TIME_MAX, 
                         marker_density=MARKER_DENSITY, label_max_point=LABEL_MAX_POINT, 
                         max_times=max_times, max_flows=max_flows)
    
    # Save TikZ code
    write_tikz(OUTPUT_FILE, datasets, labels, times_list, wrap=WRAP_TIKZ, table_name=TABLE_NAME, 
               time_min=TIME_MIN, time_max=TIME_MAX, marker_density=MARKER_DENSITY, 
               label_max_point=LABEL_MAX_POINT, max_times=max_times, max_flows=max_flows)

    print(f"TikZ file generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
