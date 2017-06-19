import dichro
import charts
import os
import sys
import json

# Get arguments
if len(sys.argv) < 2:
    print("What is your username?\n")
    sys.exit()
username = sys.argv[1]
if len(sys.argv) < 3:
    print("What is your password?\n")
    sys.exit()
password = sys.argv[2]
if len(sys.argv) < 4:
    print("Where is the melt data?\n")
    sys.exit()
location = sys.argv[3]
if len(sys.argv) < 5:
    print("What is the rough concentration in mg/ml?\n")
    sys.exit()
concentration = float(sys.argv[4])
if len(sys.argv) < 6:
    print("What is the mean residue mass in Da?\n")
    sys.exit()
residue_mass = float(sys.argv[5])
if len(sys.argv) < 7:
    print("What is the pathlength in cm?\n")
    sys.exit()

location = os.path.abspath(location)
concentrations = [(concentration - 0.05) + (0.01 * n) for n in range(11)]
data = {}
for index, conc in enumerate(concentrations):
    data[conc] = {}
    for program in ("SELCON3", "CDSSTR", "CONTIN"):
        d = dichro.run_dichro(
         username, password, location, program, conc, residue_mass, 0.0093, 1
        )
        data[conc][program] = d
        with open("%s/conc.json" % "/".join(location.split("/")[:-1]), "w") as f:
            json.dump(data, f)
        charts.dichro_chart(
         concentrations,
         [data[conc]["SELCON3"]["nrmsd"] for conc in concentrations[:index + 1]],
         [data[conc]["CONTIN"]["nrmsd"] for conc in concentrations[:index + (1 if "CONTIN" in data[conc] else 0)]],
         [data[conc]["CDSSTR"]["nrmsd"] for conc in concentrations[:index + (1 if "CDSSTR" in data[conc] else 0)]],
         "Concentration (mg/ml)",
         "NRMSD",
         "Concentration Probing",
         "%s/conc.png" % "/".join(location.split("/")[:-1]),
         y_max=0.2
        )
