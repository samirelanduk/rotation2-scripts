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
