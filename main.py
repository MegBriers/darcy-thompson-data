import math
import matplotlib.pyplot as plt
import os.path
import numpy as np
from mpl_toolkits.basemap import Basemap
from itertools import chain
import re

months_axis = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def value_generator(period, trig_function, months):
    cur_vals = []
    t = 0
    for i, month in enumerate(months):
        # dealing with the reset for the later values
        if t == 6 and period == 60:
            t = 0
        # WEIRD FLOATING POINT ERRORS WILL COMPOUND
        cur_vals.append(month * trig_function(math.radians(period * t)))
        t += 1
    return 2 * sum(cur_vals) / len(cur_vals)


def draw_map(m, scale=0.2):
    # draw a shaded-relief image
    m.shadedrelief(scale=scale)

    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)

    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')
    plt.show()


def shift_terms(a1, b1, a2, b2):
    A1 = math.sqrt(a1 ** 2 + b1 ** 2)
    A2 = math.sqrt(a2 ** 2 + b2 ** 2)
    e1 = math.degrees(math.atan(b1 / a1))
    e2 = math.degrees(math.atan(b2 / a2))
    return [A1, A2, e1, e2]


def f(A0, a1, b1, a2, b2):
    results = []
    for i in range(12):
        two_pi_value = math.radians(30 * i)
        four_pi_value = math.radians(60 * i)
        results.append(A0 + a1 * math.sin(two_pi_value) + b1 * math.cos(two_pi_value) + a2 * math.sin(
            four_pi_value) + b2 * math.cos(four_pi_value))
    return results


def f_shifted(A0, A1, e1, A2, e2):
    print(A0, A1, e1, A2, e2)
    results = []
    for i in range(12):
        two_pi_value = math.radians(30 * i)
        four_pi_value = math.radians(60 * i)
        results.append(A0 - A1 * math.sin(two_pi_value + math.radians(e1)) + A2 * math.sin(four_pi_value + math.radians(e2)))
    return results


if __name__ == "__main__":

    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='lcc', resolution=None,
                lon_0=0, lat_0=50, lat_1=45, lat_2=55,
                width=1.6E7, height=1.2E7)

    coords = []

    for dirpath, dirnames, filenames in os.walk("./data"):
        for filename in [f for f in filenames if f.endswith(".txt")]:
            file = open(os.path.join(dirpath, filename), "r", encoding="utf-8")

            print(filename)

            data = []
            meta_info = []

            for i, line in enumerate(file):
                line = line.strip('\n')
                if i < 6: meta_info.append(line); continue
                data.append(float(line))

            A0 = sum(data) / len(data)
            a1 = value_generator(30, math.sin, data)
            b1 = value_generator(30, math.cos, data)
            a2 = value_generator(60, math.sin, data)
            b2 = value_generator(60, math.cos, data)

            results = f(A0, a1, b1, a2, b2)

            A1, A2, e1, e2 = shift_terms(a1, b1, a2, b2)

            results_shifted = f_shifted(A0, A1, e1, A2, e2)

            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
            axes[0].plot(months_axis, results)
            axes[1].plot(months_axis, results_shifted)

            fig.supxlabel("months")
            fig.supylabel(meta_info[0])
            fig.suptitle(meta_info[1] + " to " + meta_info[2] + " " + meta_info[5] + " " + meta_info[3] + " " + meta_info[4])
            axes[1].set_title("Shifted")
            axes[0].set_title("Original")

            deg, minutes, direction = re.split('[°\']', meta_info[3])
            lat_dec = (float(deg) + float(minutes)  / 60) * (-1 if direction in ['W', 'S'] else 1)

            deg, minutes, direction = re.split('[°\']', meta_info[4])
            lon_dec = (float(deg) + float(minutes)  / 60) * (-1 if direction in ['W', 'S'] else 1)

            coords.append([lat_dec,lon_dec])
            print(lat_dec, lon_dec)

            fig.tight_layout()
            plt.show()
