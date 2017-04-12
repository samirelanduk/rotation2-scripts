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
agent, sample = sys.argv[2].split(",")

# What are the files here?
data_files = sorted([f for f in os.listdir(data_path) if f[-4:] == ".gen"])

# Open up the files and extract the delicious data
all_series = []
for data_file in data_files:
    with open("%s/%s" % (data_path, data_file)) as f:
        lines = f.readlines()
    lines = [line.split() for line in lines]
    lines = [line for line in lines if line[0][:3].isdigit()]
    series = [[float(line[0]), float(line[3]), data_file.split(".")[0]] for line in lines]
    all_series.append(series)

# Make chart of data
for series in all_series:
    # What temperature is this?
    label = series[0][2]
    color = "#0000FF"
    if "_" not in label:
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
    plt.plot(wavelengths, absorbance, color=color, label=label)

plt.grid(True)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Circular Dichroism")
plt.title("%s: Sample %s" % (agent, sample))
plt.xlim(all_series[0][-1][0], all_series[0][0][0])
plt.ylim(-20, 40)
plt.legend(prop={'size':7})
plt.savefig(data_path + "/melt.png", dpi=500)

'''
# Open up the files and extract the delicious data
all_series = []
min_temp = start_temp
max_temp = 90
for index, data_file in enumerate(data_files):
    # What temperature is this?
    temp = start_temp + (index * temp_interval)
    color = "#0000FF"
    if temp > 90:
        temp = "20°C (cooled)"
    else:
        relative_temp = 1 - ((temp - min_temp) / (max_temp - min_temp))
        color = hsl_to_rgb(0.45 * 360 * relative_temp, 100, 50)
        temp = "%i°C" % temp

    # Get the data series
    with open("%s/%s" % (data_path, data_file)) as f:
        lines = f.readlines()
    lines = [line.split() for line in lines]
    lines = [line for line in lines if line[0][:3].isdigit()]
    series = [[float(line[0]), float(line[1]), temp, color] for line in lines]
    all_series.append(series)

# Make chart of data
for series in all_series:
    wavelengths = [line[0] for line in series]
    absorbance = [line[1] for line in series]
    plt.plot(wavelengths, absorbance, color=series[0][3], label=series[0][2])
plt.grid(True)
plt.xlabel("Wavelength (nm)")
plt.ylabel("CD (AU)")
plt.title("%s: Run %s, Sample %s" % (agent, run, sample))
plt.xlim(all_series[0][-1][0], all_series[0][0][0])
plt.ylim(-20, 40)
plt.legend(prop={'size':7})
plt.savefig(data_path + "/melt.png", dpi=500)'''
