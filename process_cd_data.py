import sys
import re
print("")

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
