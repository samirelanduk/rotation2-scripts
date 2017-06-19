import matplotlib.pyplot as plt
import inferi

def dichro_chart(x, selcon, contin, cdsstr, x_label, y_label, title, path, y_max=100, average=False):
    plt.scatter(x[:len(selcon)], selcon, color="#FF0000", marker="o", s=8, label="SELCON3")
    plt.scatter(x[:len(contin)], contin, color="#00FF00", marker="o", s=8, label="CONTIN")
    plt.scatter(x[:len(cdsstr)], cdsstr, color="#0000FF", marker="o", s=8, label="CDSSTR")
    if average:
        data = [[selcon[n], contin[n], cdsstr[n]] for n in range(len(contin))]
        means = [sum(d) / len(d) for d in data]
        errors = [inferi.Series(*d, sample=False).standard_deviation() for d in data]
        plt.errorbar(x[:len(means)], means, yerr=errors[:len(means)], fmt="o", color="#000000", label="Average")
    plt.grid(True, lw=0.5, ls=":")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    gap = x[1] - x[0] if len(x) > 1 else 1
    plt.xlim(x[0] - gap, x[-1] + gap)
    plt.ylim(0, y_max)
    plt.title(title)
    if len(contin) > 1: plt.legend(prop={'size':8}, framealpha=1)
    plt.savefig(path)
    plt.clf()


'''def dichro_chart(x, contin, second, x_label, y_label, title, path, y_max=100, average=False):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax2.set_ylabel("Helix content")
    s1 = ax1.scatter(x[:len(contin)], contin, color="#4A9586", marker="o", s=8, label="CONTIN")
    s2 = ax2.scatter(x[:len(contin)], second, color="#0000BB", marker="x", s=16, label="CONTIN")
    if average:
        data = [[selcon[n], contin[n], cdsstr[n]] for n in range(len(contin))]
        means = [sum(d) / len(d) for d in data]
        errors = [inferi.Series(*d, sample=False).standard_deviation() for d in data]
        plt.errorbar(x[:len(means)], means, yerr=errors[:len(means)], fmt="o", color="#000000", label="Average")
    ax1.grid(True, lw=0.5, ls=":")
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    gap = x[1] - x[0] if len(x) > 1 else 1
    ax1.set_xlim(x[0] - gap, x[-1] + gap)
    ax2.set_ylim(0.4, 0.9)
    ax1.set_ylim(0, y_max)
    ax1.set_title(title)
    if len(contin) > 1: fig.legend((s1, s2), ("NRMSD", "Helix"), prop={'size':8}, framealpha=1)
    plt.savefig(path)
    plt.clf()
'''
