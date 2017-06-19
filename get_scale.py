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

location = os.path.abspath(location) + "/20.gen"
scales = [round(0.5 + (0.01 * n), 2)for n in range(101)]
data = {}
for index, scale in enumerate(scales):
    data[scale] = {}
    d = dichro.run_dichro(
     username, password, location, "CONTIN", 1, 112.9, 0.0093, scale, epsilon=True, attempts=5
    )
    data[scale] = d
    with open("%s/scale.json" % "/".join(location.split("/")[:-1]), "w") as f:
        json.dump(data, f)
    if data[scale]["nrmsd"] is not None:
        charts.dichro_chart(
         scales,
         [data[scale]["nrmsd"] for scale in scales[:index + 1]],
         [data[scale]["helix_content"] for scale in scales[:index + 1]],
         "Scale Factor",
         "NRMSD",
         "Scale Probing",
         "%s/scale.png" % "/".join(location.split("/")[:-1]),
         y_max=0.1
        )
