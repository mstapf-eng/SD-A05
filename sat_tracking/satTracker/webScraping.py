###webScraping.py

import requests
from bs4 import BeautifulSoup
import LETdec as dec
import re
from pyorbital.orbital import Orbital
from datetime import datetime, timedelta
from pytz import timezone
from tzlocal import get_localzone
import numpy as np



# Standard Gravitational parameter in km^3 / s^2 of Earth
GM = 398600.4418


class Sat: #each satellite from the text file is stored as an object of class sat
    def __init__(self, tle = "", station = "", catalogNum = 0, classification = "", desigYR = 0, desigNU = 0, desigP = "", epochYR = 0, epochDY = 0, firstDer = 0, secDer = 0, drag = 0, ephType = 0, elNum = 0, checkSum1 = 0, checkSum2 = 0, inclination = 0, rightAsc = 0, ecc = 0, Per = 0, Anom = 0, Mot = 0, revNum = 0, pass_window = []):
        self.tle = tle
        self.station = station
        self.catalogNum = catalogNum
        self.classification = classification
        self.desigYR = desigYR
        self.desigNU = desigNU
        self.desigP = desigP
        self.epochYR = epochYR
        self.epochDY = epochDY
        self.firstDer = firstDer
        self.secDer = secDer
        self.drag = drag
        self.ephType = ephType
        self.elNum = elNum
        self.checkSum1 = checkSum1
        self.checkSum2 = checkSum2
        self.inclination = inclination
        self.rightAsc = rightAsc
        self.ecc = ecc
        self.Per = Per
        self.Anom = Anom
        self.Mot = Mot
        self.revNum = revNum
        self.pass_window = pass_window

    def get_passes(self):  ##all pass times reported in UTC time

        time = datetime.utcnow()

        orb = Orbital(self.station.rstrip(), "best_file.txt")
        passes = orb.get_next_passes(time, 5, 75.15285, 39.98251, 0, tol=0.001, horizon=0)  # Temple radio room coords, longitude value is really negative

        print(self.station.rstrip())
        if len(passes) != 0:

            for x in range(0, len(passes)):
                passes[x] = list(passes[x])

            new_passes = []
            for sublist in passes:
                for item in sublist:
                    new_passes.append(item)

            format = "%Y-%m-%d %H:%M:%S %Z%z"
            now_local = []

            for y in range(0, len(new_passes)):
                now_local.append(new_passes[y].astimezone(get_localzone()))
                now_local[y] = now_local[y].strftime(format)

            sats[self.station.rstrip()].pass_window = now_local

        else:
            sats[self.station.rstrip()].pass_window = None #pass_window is None if the sat does not pass within the alotted hours


def parser(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.find_all(text=True)

    lines = listToString(result)
    print(lines)

    stringToFile(lines)

    station,catalogNumber,classification,desigYR,desigNU,desigP,epochYR,epochDY,firstDer,secDer,drag,ephType,elNum,checkSum1,inclination,rightAsc,ecc,Per,Anom,Mot,revNum,checkSum2,lengthSt = dec.decode("kep_el.txt")##returns TLE's for all satellites listed

    satList = []

    for i in range(0, lengthSt):
        newSat = Sat("",station[i], catalogNumber[i], classification[i], desigYR[i], desigNU[i], desigP[i], epochYR[i],
                     epochDY[i], firstDer[i], secDer[i], drag[i], ephType[i], elNum[i], checkSum1[i], checkSum2[i],
                     inclination[i], rightAsc[i], ecc[i], Per[i], Anom[i], Mot[i], revNum[i])
        satList.append(newSat)

    k = open("kep_el.txt", "r")
    TLE_list = k.readlines()

    j = 0
    for i in range(0, len(TLE_list)):
        if i == len(TLE_list)-1:
            satList[len(satList)-1].tle = "".join(tuple(TLE_list[-3:]))  # store each TLE (every 3 lines) for its respective satellite
            satList[len(satList)-1].tle = satList[len(satList)-1].tle[:-1]  # remove final "/n" from TLE string

        elif (i + 1) % 3 == 0:

            satList[j].tle = "".join(tuple(TLE_list[(i - 2):i + 1]))  # store each TLE (every 3 lines) for its respective satellite
            satList[j].tle = satList[j].tle[:-1] #remove final "/n" from TLE string
            j = j + 1

    k.close()

    global new_stat

    new_stat = []
    for sub in station: #remove all line breaks from station list
        new_stat.append(re.sub('\n', '',sub))

    global sats

    sats = dict(zip(new_stat, satList)) #create dictionary with sat names as keys for each satellite object

    u_list = []
    best_file = open("best_file.txt", "w")
    for i in range(0,621):
        u_list.append(TLE_list[i].upper()) #capitalize all strings in the text file for pyorbital to work
        best_file.write(u_list[i])

    best_file.close()



def listToString(list):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in list:
        str1 += ele

        # return string
    return str1

def stringToFile(string):
    text_file = open("kep_el.txt", "w")
    text_file.write(string)
    text_file.close()

def decode(txtfile):
    dec.decode(txtfile)



parser("https://www.amsat.org/tle/current/nasabare.txt")

#get_passes()
#print(sats['ISS'].pass_window)

sats['ISS'].get_passes() #edit satellite string to choose a satellite

print(sats['ISS'].pass_window) #display the upcoming pass windows in groups of 3 reported times

