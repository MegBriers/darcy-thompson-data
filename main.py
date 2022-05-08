import math
import matplotlib.pyplot as plt
import os.path
import re
import coordinate_mapping

months_axis = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def value_generator(period, trig_function, months):
    """

    Function that performs the calculations to retrieve the
    ai/bi values

    :param period: the period of the trig function for the given value (i.e 2pi/t values for a1 = 30, 4pi/t values for a2 = 60)
    :param trig_function: which trig function is invoked for the parameter
    :param months: the actual data value
    :return: the corresponding parameter value given the above arguments
    """
    cur_vals = []
    # have to keep a separate loop variable so we don't restart the calculations but we can also reset at the right part
    t = 0
    for i, month in enumerate(months):
        # dealing with the reset for the later values (loops back round before 4pi/t reaches 360)
        if t == 6 and period == 60:
            t = 0
        # WEIRD FLOATING POINT ERRORS WILL COMPOUND
        # includes conversion to radians
        cur_vals.append(month * trig_function(math.radians(period * t)))
        t += 1
    return 2 * sum(cur_vals) / len(cur_vals)


def shift_terms(a1, b1, a2, b2):
    """

    A function to perform stage (2) of the calculations and get the new
    parameters for a reduced trig equation

    :param a1: a1 value from stage (1)
    :param b1: b1 value from stage (1)
    :param a2: a2 value from stage (1)
    :param b2: b2 value from stage (1)
    :return: an array of the new parameters from the calculations
    """

    # the following lines just perform the calculations as laid out for stage (2) in the investigations calculation
    A1 = math.sqrt(a1 ** 2 + b1 ** 2)
    A2 = math.sqrt(a2 ** 2 + b2 ** 2)
    e1 = math.degrees(math.atan(b1 / a1))
    e2 = math.degrees(math.atan(b2 / a2))
    return [A1, A2, e1, e2]


def f(A0, a1, b1, a2, b2):
    """

    A function (in a programming sense) to find the values that the original function (in a maths sense)
    produced by the calculations would be for each of the months

    :param A0: A0 value from stage (1)
    :param a1: a1 value from stage (1)
    :param b1: b1 value from stage (1)
    :param a2: a2 value from stage (1)
    :param b2: b2 value from stage (1)
    :return: an array containing the values the function would output
    """
    results = []
    # loop for each of the months
    for i in range(12):
        # getting the 2pi/t and 4pi/t values
        two_pi_value = math.radians(30 * i)
        four_pi_value = math.radians(60 * i)
        # following the equation of the function calculated in stage (1)
        results.append(A0 + a1 * math.sin(two_pi_value) + b1 * math.cos(two_pi_value) + a2 * math.sin(
            four_pi_value) + b2 * math.cos(four_pi_value))
    return results


def f_shifted(A0, A1, e1, A2, e2):
    """

    A function (in a programming sense) to find the values that the shrunk/shifted function (in a maths sense)
    produced by the calculations would be for each of the months

    Similar to f but with the maths for the second equation

    :param A0: A0 value from stage (1)
    :param A1: A1 value from stage (2)
    :param e1: e1 value from stage (2)
    :param A2: A2 value from stage (2)
    :param e2: e2 value from stage (2)
    :return: an array containing the values the function would output
    """
    # for easy checking that the functions are performing correctly
    print(A0, A1, e1, A2, e2)
    results = []
    for i in range(12):
        two_pi_value = math.radians(30 * i)
        four_pi_value = math.radians(60 * i)
        results.append(A0 - A1 * math.sin(two_pi_value + math.radians(e1)) + A2 * math.sin(four_pi_value + math.radians(e2)))
    return results


if __name__ == "__main__":
    # will store the longitude and latitude values for all the trips taken present in the data folder
    coords = []

    # finds all the files in the data folder
    for dirpath, dirnames, filenames in os.walk("./data"):
        # files must have .txt extension
        for filename in [f for f in filenames if f.endswith(".txt")]:
            file = open(os.path.join(dirpath, filename), "r", encoding="utf-8")

            # for debugging/make it easier to match up values with given files
            print(filename)

            # stores the actual data points for the trip
            data = []
            # stores the meta information (location, date etc) about the trip
            meta_info = []

            for i, line in enumerate(file):
                # removing new lines
                line = line.strip('\n')
                # structure of file is given in github repo, but meta information is stored in first five lines of file
                if i < 6: meta_info.append(line); continue
                data.append(float(line))

            # finding the average value across the months
            A0 = sum(data) / len(data)
            # generating each of the data points for the function
            a1 = value_generator(30, math.sin, data)
            b1 = value_generator(30, math.cos, data)
            a2 = value_generator(60, math.sin, data)
            b2 = value_generator(60, math.cos, data)

            # getting the output for each month from the original function with the calculated parameters
            results = f(A0, a1, b1, a2, b2)

            # getting the modified parameters (completing stage 2 of the calculations)
            A1, A2, e1, e2 = shift_terms(a1, b1, a2, b2)

            # getting the output for each month from the modified function with the newly calculated parameters
            results_shifted = f_shifted(A0, A1, e1, A2, e2)

            # allowing the graphs to be plotted side by side
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
            # plotting the values from the original function on the first plot
            axes[0].plot(months_axis, results)
            # plotting the original points on the first plot
            axes[0].plot(months_axis, data, 'o', linestyle='None', markerfacecolor = 'r')
            # plotting the values from the modified function on the second plot
            axes[1].plot(months_axis, results_shifted)
            # plotting the original points on the second plot
            axes[1].plot(months_axis, data, 'o', linestyle='None', markerfacecolor = 'r')

            # adding the axis labels
            fig.supxlabel("months")
            fig.supylabel(meta_info[0])
            # adding the titles to the plot
            fig.suptitle(meta_info[1] + " to " + meta_info[2] + " " + meta_info[5] + " " + meta_info[3] + " " + meta_info[4])
            axes[1].set_title("Shifted")
            axes[0].set_title("Original")

            # extracting the right information to convert the latitude values into degree versions
            deg, minutes, direction = re.split('[°\']', meta_info[3])
            # converting the latitude values from their form to degree values
            lat_dec = (float(deg) + float(minutes)/60) * (-1 if direction in ['W', 'S'] else 1)

            # same process followed for longitude
            deg, minutes, direction = re.split('[°\']', meta_info[4])
            lon_dec = (float(deg) + float(minutes)/60) * (-1 if direction in ['W', 'S'] else 1)

            # append them to the coords array along with what file they came from
            coords.append([lat_dec,lon_dec,filename])

            fig.tight_layout()
            # showing the files
            plt.show()

    # plots the coordinates of where the ship took the measurements
    coordinate_mapping.plot(coords)
