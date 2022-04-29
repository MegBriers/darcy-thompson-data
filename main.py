import math
import matplotlib.pyplot as plt


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
    print(cur_vals)
    a1 = 2 * sum(cur_vals) / len(cur_vals)

    return a1


def f(A0, a1, b1, a2, b2):
    results = []
    for i in range(12):
        two_pi_value = math.radians(30 * i)
        four_pi_value = math.radians(60 * i)
        results.append(A0 + a1 * math.sin(two_pi_value) + b1 * math.cos(two_pi_value) + a2 * math.sin(
            four_pi_value) + b2 * math.cos(four_pi_value))
    return results


if __name__ == "__main__":
    file = open("current_data.txt", "r")
    data = []

    location_from = ""
    location_to = ""
    latitude = ""
    longitude = ""
    measuring = ""
    year = ""

    for i, line in enumerate(file):
        line = line.strip('\n')
        if i==0: measuring = line; continue
        if i==1: location_from = line; continue
        if i==2: location_to = line; continue
        if i==3: latitude = line; continue
        if i==4: longitude = line; continue
        if i==5: year = line; continue

        data.append(float(line))

    A0 = sum(data) / len(data)
    a1 = value_generator(30, math.sin, data)
    b1 = value_generator(30, math.cos, data)
    a2 = value_generator(60, math.sin, data)
    b2 = value_generator(60, math.cos, data)

    print("A0: ", A0)
    print("a1: ", a1)
    print("b1: ", b1)
    print("a2: ", a2)
    print("b2: ", b2)

    results = f(A0, a1, b1, a2, b2)

    plt.plot(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], results)
    plt.xlabel(measuring)
    plt.ylabel("months")
    plt.title(location_from + " to " + location_to + " " + year)
    plt.show()
