import sys
import re
import os
from omnicanvas.color import hsl_to_rgb
import matplotlib.pyplot as plt
print("")

# Define function for opening data file and getting relevant data
def open_data_file(path):
    with open(path) as f:
        lines = [line.rstrip() for line in f.readlines() if line.rstrip()]
    runs, run, in_data = [], [], False
    for line in lines:
        if in_data:
            values = line.split()
            try:
                run.append({
                 "wavelength": float(values[0]),
                 "signal": float(values[1]),
                 "error": float(values[2]),
                })
            except ValueError:
                pass
        if line == "$DATA": in_data = True
        if line == "$ENDDATA": in_data = False
        if line.startswith("$MDCNAME") and run:
            runs.append(run)
            run = []
    runs.append(run)
    return runs

# Define function for averaging a series of runs
def average_runs(runs):
    wavelengths = [datum["wavelength"] for datum in runs[0]]
    run_average = []
    for wavelength in wavelengths:
        scans = [[
         datum for datum in run if datum["wavelength"] == wavelength][0
        ] for run in runs]
        run_average.append({
         "wavelength": wavelength,
         "signal": sum([scan["signal"] for scan in scans]) / len(scans),
         "error": sum([scan["error"] for scan in scans]) / len(scans)
        })
    return run_average

# Define function for subtracting blank curve from sample curve
def subtract_blank_curve(blank_run, sample_run):
    run_average = []
    for index, blank_scan in enumerate(blank_run):
        sample_scan = sample_run[index]
        run_average.append({
         "wavelength": blank_scan["wavelength"],
         "signal": sample_scan["signal"] - blank_scan["signal"],
         "error": sample_scan["error"] + blank_scan["error"]
        })
    return run_average

if __name__ == "__main__":
    # Get arguments
    if len(sys.argv) <= 1:
        print("Please provide a path to the sample data\n")
        sys.exit()
    sample_path = sys.argv[1]
    if len(sys.argv) <= 2:
        print("Please provide a path to the blank data\n")
        sys.exit()
    blank_path = sys.argv[2]
    if len(sys.argv) <= 3:
        print("Where should the output .dat be saved?\n")
        sys.exit()
    output_path = sys.argv[3]
    if len(sys.argv) > 4:
        output_chart_path = sys.argv[4]
    else:
        output_chart_path = None
    if len(sys.argv) > 5:
        chart_title = sys.argv[5]
    else:
        chart_title = output_chart_path

    # Get data files
    blank_data_files = sorted([
     f for f in os.listdir(blank_path) if f.endswith(".dat")
    ])
    sample_data_files = sorted([
     f for f in os.listdir(sample_path) if f.endswith(".dat")
    ])
    assert blank_data_files == sample_data_files

    # Get temperatures and wavelengths
    temperatures = [f.split(".")[0] for f in blank_data_files]
    wavelengths = [
     run["wavelength"] for run in open_data_file("%s/20.dat" % blank_path)[0]
    ]

    # Create header line
    head = " ".join(["%s_signal %s_error" % (temp, temp) for temp in temperatures])
    head = "wavelength " + head
    lines = [head]

    # Open up all the data files
    blank_data_files = [average_runs(
     open_data_file("%s/%s" % (blank_path, data))
    ) for data in blank_data_files]
    sample_data_files = [average_runs(
     open_data_file("%s/%s" % (sample_path, data))
    ) for data in sample_data_files]
    data_files = zip(blank_data_files, sample_data_files)
    data = [subtract_blank_curve(
     blank_run, sample_run
    ) for blank_run, sample_run in data_files]

    # Build up data lines
    for wavelength in wavelengths:
        line = [str(wavelength)]
        for temperature_run in data:
            scan = [
             s for s in temperature_run if s["wavelength"] == wavelength
            ][0]
            line.append(str(scan["signal"]))
            line.append(str(scan["error"]))
        lines.append(" ".join(line))

    # Write to file
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    # Make chart
    if output_chart_path:
        max_temp = int(temperatures[-2])
        min_temp = int(temperatures[0])
        relative_temps = [
         1 - ((int(temp) - min_temp) / (max_temp - min_temp)) for temp in temperatures[:-1]
        ]
        color_scale = [
         hsl_to_rgb(0.45 * 360 * temp, 100, 50) for temp in relative_temps
        ] + ["#0000FF"]
        for index, temp in enumerate(temperatures):
            y = [line.split(" ")[(index * 2) + 1] for line in lines[1:]]
            y_error = [line.split(" ")[(index * 2) + 2] for line in lines[1:]]
            plt.plot(wavelengths, y, color=color_scale[index], label=temp + "°C")
            plt.fill_between(
             wavelengths,
             [float(val) - (float(y_error[index])) for index, val in enumerate(y)],
             [float(val) + (float(y_error[index])) for index, val in enumerate(y)],
             color=color_scale[index], alpha=0.1
            )
        plt.grid(True)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("CD (AU)")
        plt.legend(prop={'size':7})
        plt.title(chart_title)
        plt.savefig(output_chart_path, dpi=500)
