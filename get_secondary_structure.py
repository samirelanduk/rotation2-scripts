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
    print("What is the scaling factor?\n")
    sys.exit()
scale = float(sys.argv[4])


def path_to_temperature(path):
    return int(path.split("/")[-1].split(".")[0])


data_files = sorted(
 [f for f in os.listdir(location) if f[-4:] == ".gen"]
)
data_files = [os.path.abspath(location + "/" + f) for f in data_files if "_" not in f]
data = {}
for index, data_file in enumerate(data_files):
    data[data_file] = {}
    for program in ("SELCON3", "CDSSTR", "CONTIN"):
        d = dichro.run_dichro(
         username, password, data_file, program, 1, 112.9, 0.0093, scale, epsilon=True
        )
        data[data_file][program] = d
        with open("%s/ss.json" % "/".join(location.split("/")[:-1]), "w") as f:
            json.dump(data, f)
        charts.dichro_chart(
         [path_to_temperature(path) for path in data_files],
         [data[data_file]["SELCON3"]["helix_content"] * 100 for data_file in data_files[:index + 1]],
         [data[data_file]["CONTIN"]["helix_content"] * 100 for data_file in data_files[:index + (1 if "CONTIN" in data[data_file] else 0)]],
         [data[data_file]["CDSSTR"]["helix_content"] * 100 for data_file in data_files[:index + (1 if "CDSSTR" in data[data_file] else 0)]],
         "Temperature (°C)",
         "Helical Content (%)",
         data_file.split("/")[-2],
         "%s/ss.png" % "/".join(location.split("/")[:-1]),
         y_max=100,
         average=True
        )
