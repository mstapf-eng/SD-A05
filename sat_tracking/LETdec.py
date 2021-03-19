##LETdec.py

import itertools


def decode(txtfile):
    # empty arrays for different keplerian elements
    station, catalogNumber, classification, desigYR = [], [], [], []
    desigNU, desigP, epochYR, epochDY, firstDer, secDer = [], [], [], [], [], []
    drag, ephType, elNum, checkSum1, checkSum2, inclination = [], [], [], [], [], []
    rightAsc, ecc, Per, Anom, Mot, revNum = [], [], [], [], [], []

    # interpreting text files 3 lines at a time using itertools toolbox
    # Each group of three lines represents information for different satellites
    with open(txtfile) as f:
        for line1, line2, line3 in itertools.zip_longest(*[f] * 3):
            station.append(line1)  # Creating station name array
            if (line2 != None):  # fix on 2/9/21 (it was appending NoneType)
                catalogNumber.append(line2[2:7])  # Creating satellite number array
                classification.append(line2[7])  # Satellite calssification array
                desigYR.append(line2[9:11])  # Last 2 digits of launch Year array
                desigNU.append(line2[11:14])  # Launch number of the year array
                desigP.append(line2[14])  # Launch piece array
                epochYR.append(line2[18:20])  # Epoch Year  last two digits of year array
                epochDY.append(line2[20:32])  # Epoch Day with fractional part of day array
                firstDer.append(line2[33:43])  # First time derivative of the mean motion array
                secDer.append(line2[44:52])  # Second derivative of the mean motion array
                drag.append(line2[53:61])  # BSTAR drag term array
                ephType.append(line2[62])  # Ephermis type array
                elNum.append(line2[64:68])  # Ephermis number array
                checkSum1.append(line2[68])  # Check sum Modulus 10 array
                inclination.append(line3[8:16])  # Inclination array
                rightAsc.append(line3[17:25])  # Right ascension of the ascending node array
                ecc.append(line3[26:33])  # Eccentricity array
                Per.append(line3[34:42])  # Argument of Perigee array
                Anom.append(line3[43:51])  # Mean anomoly array
                Mot.append(line3[52:63])  # Mean motion array
                revNum.append(line3[63:68])  # Revolution number at epoch
                checkSum2.append(line3[68])  # Checksum modulus 10 array

    lengthSt = len(station)

    return station, catalogNumber, checkSum1,checkSum2, lengthSt


