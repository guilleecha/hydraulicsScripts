import matplotlib.pyplot as plt
import pandas as pd

def plot_hydrographs(datasets, labels, times, time_min=None, time_max=None, marker_density=1.0, label_max_point=False, max_times=None, max_flows=None):
    """
    Generates a plot with Matplotlib to visualize multiple hydrographs with optional time filtering and marker density control.
    
    Parameters:
    - datasets: List of lists with flow rate data.
    - labels: List of labels for each dataset.
    - times: List of lists with time values corresponding to each dataset.
    - time_min: Minimum time (in hours) to display in the plot.
    - time_max: Maximum time (in hours) to display in the plot.
    - marker_density: Value between 0 and 1 determining how many points have markers.
    - label_max_point: If True, marks the maximum flow point with a label.
    - max_times: List of max time values for each dataset.
    - max_flows: List of max flow values for each dataset.
    """
    plt.figure(figsize=(10, 6))  # Increased figure height to avoid label overlap
    
    for i, (data, label, time) in enumerate(zip(datasets, labels, times)):
        df = pd.DataFrame({"Time": time, "Flow": data})
        
        # Apply time filtering if limits are provided
        if time_min is not None:
            df = df[df["Time"] >= time_min]
        if time_max is not None:
            df = df[df["Time"] <= time_max]
        
        plt.plot(df["Time"], df["Flow"], label=label, linewidth=2)
        
        # Apply marker density
        num_points = len(df)
        mark_repeat = max(1, int(1 / marker_density)) if marker_density > 0 else num_points + 1
        marker_indices = list(range(0, num_points, mark_repeat))
        plt.scatter(df.iloc[marker_indices]["Time"], df.iloc[marker_indices]["Flow"], label=f"Markers ({label})")
        
        # Highlight max flow points
        if label_max_point and max_times is not None and max_flows is not None:
            max_time = max_times[i] if i < len(max_times) else None
            max_flow = max_flows[i] if i < len(max_flows) else None
            if max_time is not None and max_flow is not None:
                plt.scatter([max_time], [max_flow], color='blue', marker='o', s=100, label=f"Max {label}")
                plt.annotate(f"Max: {max_flow:.2f} m³/s", (max_time, max_flow),
                             textcoords="offset points", xytext=(10, 15), ha='center', fontsize=10, 
                             color='blue', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.3'))
    
    all_times = [t for sublist in times for t in sublist]  # Flatten list of lists
    plt.xlabel("Time (h)")
    plt.ylabel("Flow rate (m³/s)")
    plt.xlim(left=time_min if time_min is not None else min(all_times),
             right=time_max if time_max is not None else max(all_times))
    plt.ylim(bottom=0, top=max(max_flows) * 1.3 if max_flows is not None else None)  # Expanding Y-axis
    plt.legend()
    plt.grid()
    plt.title("Hydrograph Output - Multiple Datasets")
    plt.show()
