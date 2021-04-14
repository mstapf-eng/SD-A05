##LETdec.py

import itertools


def decode(txtfile):
    # empty arrays for different keplerian elements
    station = []

    # interpreting text files 3 lines at a time using itertools toolbox
    # Each group of three lines represents information for different satellites
    with open(txtfile) as f:
        for line1, line2, line3 in itertools.zip_longest(*[f] * 3):
            station.append(line1)  # Creating station name array
            

    lengthSt = len(station)

    return station,lengthSt


