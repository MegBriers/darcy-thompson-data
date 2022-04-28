import math


def value_generator(period, trig_function, months):
    cur_vals = []
    for i, month in enumerate(months):
        # going to end up with weird floating point problems if not careful
        cur_vals.append(abs(month * trig_function(math.radians(period * i))))

    a1 = 2 * sum(cur_vals) / len(cur_vals)

    return a1


def f(t, A0, a1, b1, a2, b2):
    return (A0 + a1 * x + b1 * y + a2 * z + b2 * p)


if __name__ == "__main__":
    file = open("current_data.txt", "r")
    data = []

    for month in file:
        data.append(float(month))

    A0 = sum(data) / len(data)
    a1 = value_generator(30, math.sin, data)
    b1 = value_generator(30, math.cos, data)
    a2 = value_generator(60, math.sin, data)
    b2 = value_generator(60, math.cos, data)
