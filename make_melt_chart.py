import sys
import os
import matplotlib.pyplot as plt
from omnicanvas import hsl_to_rgb
print("")

if len(sys.argv) <= 1:
    print("Please provide a path to the processed data\n")
    sys.exit()
data_path = sys.argv[1]
if len(sys.argv) <= 2:
    print("Please provide a label in the form Agent,Sample\n")
    sys.exit()
agent, sample = sys.argv[2].split(",") if "," in sys.argv[2] else sys.argv[2], None
if len(sys.argv) <= 3:
    print("Please provide a chart filename\n")
    sys.exit()
chart_file_name = sys.argv[3]

# What are the files here?
data_files = sorted([f for f in os.listdir(data_path) if f[-4:] == ".gen" and "90" not in f and "85" not in f])

# Open up the files and extract the delicious data
all_series = []
for data_file in data_files:
    with open("%s/%s" % (data_path, data_file)) as f:
        lines = f.readlines()
    lines = [line.split() for line in lines]
    lines = [line for line in lines if line[0][:3].isdigit()]
    series = [[
     float(line[0]),
     float(line[3]),
     float(line[3]) - float(line[5]),
     float(line[3]) + float(line[5]),
     data_file.split(".")[0]
    ] for line in lines]
    all_series.append(series)

# Make chart of data
for series in all_series:
    # What temperature is this?
    label = series[0][4]
    color = "#000000"
    if "20" not in label:
        temp = int(label)
        relative_temp = 1 - ((temp - 20) / 70)
        color = hsl_to_rgb(0.45 * 360 * relative_temp, 100, 50)

    # Make label prettier
    if "_" in label:
        label = "20°C (cooled)"
    else:
        label += "°C"

    wavelengths = [line[0] for line in series]
    absorbance = [line[1] for line in series]
    if "cooled" in label:
        plt.plot(wavelengths, absorbance, "--", color=color, label=label, linewidth=0.5)
    elif "20" in label:
        plt.plot(wavelengths, absorbance, color=color, label=label, linewidth=0.5, zorder=100)
    else:
        plt.plot(wavelengths, absorbance, color=color, label=label, linewidth=0.5)
    '''plt.fill_between(
     wavelengths,
     [line[2] for line in series],
     [line[3] for line in series],
     color=color, alpha=0.05
    )'''

plt.xlabel("Wavelength (nm)")
plt.ylabel("Delta Epsilon")
plt.xlim([190, 280])
plt.xticks([190, 200, 210, 220, 230, 240, 250, 260, 270, 280])
plt.ylim(-10, 20)
#plt.legend(prop={'size':7}, framealpha=1)
plt.savefig("../charts/melts/%s.pdf" % chart_file_name, dpi=1000)
plt.savefig("../charts/melts/%s.eps" % chart_file_name, dpi=1000)
