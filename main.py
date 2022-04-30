import math
import matplotlib.pyplot as plt
import os.path

months_axis = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def value_generator(period, trig_function, months):
    cur_vals = []
    t = 0
    for i, month in enumerate(months):
        # dealing with the reset for the later values
        if t == 6 and period == 60:
            t = 0
        # WEIRD FLOATING POINT ERRORS WILL MESS IT UP
        cur_vals.append(month * trig_function(math.radians(period * t)))
        t += 1
    return 2 * sum(cur_vals) / len(cur_vals)


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
    results = []
    for i in range(12):
        two_pi_value = math.radians(30 * i)
        four_pi_value = math.radians(60 * i)
        results.append(A0 - A1 * math.sin(two_pi_value + e1) + A2 * math.sin(four_pi_value + 32))
    return results


if __name__ == "__main__":
    for dirpath, dirnames, filenames in os.walk("./data"):
        for filename in [f for f in filenames if f.endswith(".txt")]:
            file = open(os.path.join(dirpath, filename), "r")

            print(filename)

            data = []

            location_from = ""
            location_to = ""
            latitude = ""
            longitude = ""
            measuring = ""
            year = ""
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
            # needs changed to new meta_info values
            fig.suptitle(location_from + " to " + location_to + " " + year + " " + latitude + " " + longitude)
            axes[1].set_title("Shifted")
            axes[0].set_title("Original")

            fig.tight_layout()
            plt.show()
