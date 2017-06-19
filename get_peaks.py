import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
from omnicanvas import hsl_to_rgb
print("")

if len(sys.argv) <= 1:
    print("Please provide a path to the processed data\n")
    sys.exit()
data_path = sys.argv[1]

agents = ["A835", "Pmal-C8", "DDM", "Cymal5"]
#agents = ["Pmal-C8"]
wavelengths = [223, 194]
colors = ["#3498db", "#c0392b", "#27ae60", "#8e44ad"]
#colors = ["#c0392b"]

files = {agent: sorted(
 [f for f in os.listdir(data_path + "/" + agent) if f[-4:] == ".gen" and "9" not in f and "85" not in f]
)[:-1] for agent in agents}
temperatures = {
 agent: [20 + (n * 5) for n in range(len(files[agent]))] for agent in agents
}
data = {wav: {agent: [] for agent in agents} for wav in wavelengths}
for wav in data:
    for agent in data[wav]:
        for path in files[agent]:
            with open("%s/%s/%s" % (data_path, agent, path)) as f:
                lines = f.readlines()
            line = [l for l in lines if l[:3] == str(wav)][0]
            value, error = line.split()[1:6:4]
            data[wav][agent].append((float(value), float(value) - float(error), float(value) + float(error)))

for wavelength in (223, 194):
    for agent, color in zip(agents, colors):
        temp = temperatures[agent][:]
        absorbance = [l[0] for l in data[wavelength][agent][:]]
        xnew = np.linspace(20,80,13)
        power_smooth = spline(temp,absorbance,xnew)
        plt.plot(xnew, power_smooth, color=color, label=agent)
        plt.plot(temp, absorbance, linewidth=0, color=color, label=agent, marker="o", markerfacecolor="#000000", markeredgecolor="#000000", markersize=3)
        '''plt.fill_between(
         temperatures[agent],
         [l[1] for l in data[wavelength][agent]],
         [l[2] for l in data[wavelength][agent]],
         color=color, alpha=0.05
        )'''
    plt.ylabel("Delta Epsilon")
    plt.xlabel("Temperature (°C)")
    plt.xlim([20, 80])
    #plt.legend(prop={'size':7}, framealpha=1)
    plt.savefig("../charts/melts/%i.pdf" % (wavelength), dpi=1000)
    plt.savefig("../charts/melts/%i.eps" % (wavelength), dpi=1000)
    plt.clf()

for color, agent in zip(colors, agents):
    with open("%s/%s/20.gen" % (data_path, agent)) as f:
        lines = f.readlines()
    lines = [line.split() for line in lines]
    lines = [line for line in lines if line[0][:3].isdigit()]
    series = [[
     float(line[0]),
     float(line[3]),
     float(line[5])
    ] for line in lines]
    wavelengths = [line[0] for line in series]
    absorbance = [line[1] for line in series]
    wavelengths.reverse()
    absorbance.reverse()
    xnew = np.linspace(190,280,180)
    power_smooth = spline(wavelengths,absorbance,xnew)
    waverror = [280, 270, 260, 250, 240, 224, 209, 194]
    error = [[line[2] for line in series if line[0] == wav][0] if wav in waverror else 0 for wav in wavelengths]

    plt.errorbar(wavelengths, absorbance, yerr=error, color=color, label=agent, linewidth=1)

    #plt.errorbar(waverror, abserror, yerr=error, linewidth=0)
    '''plt.fill_between(
     wavelengths,
     [line[2] for line in series],
     [line[3] for line in series],
     color=color, alpha=0.1
    )'''
plt.ylabel("Delta Epsilon")
plt.xlabel("Wavelength (nm)")
# plt.legend(prop={'size':7}, framealpha=1)
plt.xlim([190, 280])
plt.savefig("../charts/melts/20.pdf", dpi=1000)
plt.savefig("../charts/melts/20.eps", dpi=1000)
plt.clf()

with open(data_path + "/A835/20.gen") as f:
    lines = f.readlines()
lines = [line.split() for line in lines]
lines = [line for line in lines if line[0][:3].isdigit()]
series20 = [[
 float(line[0]),
 float(line[3]),
 float(line[3]) - float(line[5]),
 float(line[3]) + float(line[5]),
 float(line[2])
] for line in lines]
with open(data_path + "/A835/cool_20.gen") as f:
    lines = f.readlines()
lines = [line.split() for line in lines]
lines = [line for line in lines if line[0][:3].isdigit()]
seriescool = [[
 float(line[0]),
 float(line[3]),
 float(line[3]) - float(line[5]),
 float(line[3]) + float(line[5]),
 float(line[2])
] for line in lines]
wavelengths = [line[0] for line in series20]
absorbance20 = [line[1] for line in series20]
absorbancecool = [line[1] for line in seriescool]
ht20 = [line[4] for line in series20]
htcool = [line[4] for line in seriescool]
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
l1 = ax1.plot(wavelengths, absorbance20, color="#00FF00", label="20 °C", linewidth=1)
l2 = ax1.plot(wavelengths, absorbancecool, color="#0000FF", label="cooled 20 °C", linewidth=1)
'''ax1.fill_between(
 wavelengths,
 [line[2] for line in series20],
 [line[3] for line in series20],
 color="#00FF00", alpha=0.1
)
ax1.fill_between(
 wavelengths,
 [line[2] for line in seriescool],
 [line[3] for line in seriescool],
 color="#0000FF", alpha=0.1
)'''

l3 = ax2.plot(wavelengths, ht20, "--", color="#00FF00", label="20 °C HT", linewidth=1)
l4 = ax2.plot(wavelengths, htcool, "--", color="#0000FF", label="cooled 20 °C HT", linewidth=1)
ax1.set_ylabel("Delta Epsilon")
ax2.set_ylabel("High tension (mV)")
ax2.set_ylim([0, 600])
plt.xlim([190, 280])
ax1.set_xlabel("Wavelength (nm)")
lns = l1 + l2 + l3 + l4
labels = [l.get_label() for l in lns]
#plt.legend(lns, labels, prop={'size':7}, framealpha=1)
plt.xticks([190, 200, 210, 220, 230, 240, 250, 260, 270, 280])
plt.savefig("../charts/melts/20COOL.pdf", dpi=1000)
plt.savefig("../charts/melts/20COOL.eps", dpi=1000)
plt.clf()
