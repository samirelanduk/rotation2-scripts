import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

colors = ["#3498db", "#c0392b", "#27ae60", "#8e44ad"]

# SVD
with open("pca.dat") as f:
    lines = f.readlines()
svd_data = [[float(x) for x in line.strip().split()] for line in lines[1:]]
temperatures = [line[0] for line in svd_data]
ys = [[line[n] for line in svd_data] for n in range(1, 5)]
for y, color in zip(ys, colors):
    xnew = np.linspace(20,80,104)
    power_smooth = spline(temperatures,y,xnew)
    plt.plot(xnew, power_smooth, color=color)
    plt.plot(temperatures, y, linewidth=0, color=color, marker="o", markerfacecolor="#000000", markeredgecolor="#000000", markersize=3)
plt.ylabel("Proportion of Principal Component 1 (Normalised)")
plt.xlabel("Temperature (°C)")
plt.xlim([20, 80])
plt.ylim([0, 1.2])
plt.savefig("../charts/melts/pca.pdf", dpi=1000)
plt.savefig("../charts/melts/pca.eps", dpi=1000)
plt.clf()

# Helix
with open("helix.dat") as f:
    lines = f.readlines()
svd_data = [[float(x) for x in line.strip().split()] for line in lines[1:]]
temperatures = [line[0] for line in svd_data]
ys = [[line[n] for line in svd_data] for n in range(1, 5)]
for y, color in zip(ys, colors):
    xnew = np.linspace(20,80,104)
    power_smooth = spline(temperatures,y,xnew)
    plt.plot(xnew, power_smooth, color=color)
    plt.plot(temperatures, y, linewidth=0, color=color, marker="o", markerfacecolor="#000000", markeredgecolor="#000000", markersize=3)
plt.ylabel("Helix Content (%)")
plt.xlabel("Temperature (°C)")
plt.xlim([20, 80])
plt.ylim([0, 100])
plt.savefig("../charts/melts/helix.pdf", dpi=1000)
plt.savefig("../charts/melts/helix.eps", dpi=1000)
plt.clf()

ys = ys[:2]
colors = colors[:2]
for y, color in zip(ys, colors):
    xnew = np.linspace(20,80,104)
    power_smooth = spline(temperatures,y,xnew)
    plt.plot(xnew, power_smooth, color=color)
    plt.plot(temperatures, y, linewidth=0, color=color, marker="o", markerfacecolor="#000000", markeredgecolor="#000000", markersize=3)
plt.ylabel("Helix Content (%)")
plt.xlabel("Temperature (°C)")
plt.xlim([20, 80])
plt.ylim([0, 100])
plt.savefig("../charts/melts/helix2.pdf", dpi=1000)
plt.savefig("../charts/melts/helix2.eps", dpi=1000)
plt.clf()

# Basis
with open("basis.dat") as f:
    lines = f.readlines()
basis1 = [float(x) for x in lines[0].strip().split()[1:]]
basis2 = [float(x) for x in lines[1].strip().split()[1:]]
temperatures += [85, 90]
xnew = np.linspace(20,80,104)
smooth1 = spline(temperatures,basis1,xnew)
smooth2 = spline(temperatures,basis2,xnew)
plt.plot(temperatures, basis1, color="#2980b9")
plt.plot(temperatures, basis2, color="#e74c3c")
plt.plot(temperatures, basis1, linewidth=0, color=color, marker="o", markerfacecolor="#000000", markeredgecolor="#000000", markersize=3)
plt.plot(temperatures, basis2, linewidth=0, color=color, marker="o", markerfacecolor="#000000", markeredgecolor="#000000", markersize=3)
plt.xlim([20, 90])
plt.ylabel("PCA Component Magnitude)")
plt.xlabel("Temperature (°C)")
plt.savefig("../charts/melts/basis.pdf", dpi=1000)
plt.savefig("../charts/melts/basis.eps", dpi=1000)
