def write_tikz(file_path, datasets, labels, times, wrap=False, table_name="datatable", time_min=None, time_max=None, marker_density=1.0, label_max_point=False, max_times=None, max_flows=None):
    """
    Writes multiple hydrographs to TikZ format with structured hydrograph data.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        if wrap:
            f.write("\\begin{figure}[H]\n")
            f.write("    \\centering\n")
            f.write("    \\begin{tikzpicture}\n")
            f.write("        \\begin{axis}[")
            f.write("width=14cm, height=8cm, ")
            f.write(f"xmin={time_min if time_min is not None else min(min(t) for t in times):.2f}, xmax={time_max if time_max is not None else max(max(t) for t in times):.2f}, ")
            f.write("ymin=0, ")
            f.write(f"ymax={max(max_flows) * 1.3 if max_flows is not None else 10:.2f}, ")
            f.write("xlabel={Time (h)}, ylabel={Flow rate (m³/s)}, ")
            f.write("grid=major, legend pos=north east, title={Hydrograph Output - Multiple Datasets}, smooth]\n")
        
        markers = ["triangle*", "square*", "circle*", "diamond*"]
        legend_entries = []  # Store legend entries
        
        for i, (data, label, time) in enumerate(zip(datasets, labels, times)):
            mark_repeat = max(1, round(1 / marker_density))  # Ensure a valid mark repeat value
            f.write(f"        \\addplot[black, thick, mark={markers[i % len(markers)]}, mark repeat={mark_repeat}] coordinates {{\n")
            for t, q in zip(time, data):
                if t is not None and q is not None and q >= 0:  # Ensure valid non-negative values
                    f.write(f"            ({t:.2f}, {q:.2f})\n")
            f.write("        };")
            legend_entries.append(label.replace("_", "\\_"))  # Store legend safely
        
        # Add combined legend
        if legend_entries:
            f.write(f"        \\legend{{{', '.join(legend_entries)}}}\n")
        
        # Highlight max flow points
        if label_max_point and max_times is not None and max_flows is not None:
            for i, (max_time, max_flow) in enumerate(zip(max_times, max_flows)):
                if max_time is not None and max_flow is not None:
                    f.write(f"        \\node[above=8pt, draw=blue, fill=white, rounded corners] at (axis cs:{max_time:.2f},{max_flow:.2f}) {{Max: {max_flow:.2f} m³/s}};\n")
                    f.write(f"        \\addplot[only marks, mark=*, mark options={{color=blue, scale=1.5}}] coordinates {{({max_time:.2f},{max_flow:.2f})}};\n")
        
        if wrap:
            f.write("        \\end{axis}\n")
            f.write("    \\end{tikzpicture}\n")
            f.write("    \\caption{Hydrograph Output - Multiple Datasets}\n")
            f.write("    \\label{fig:hydrograph}\n")
            f.write("\\end{figure}\n")
    
    print(f"TikZ file generated: {file_path}")
