###webScraping.py

import re
import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from pyorbital.orbital import Orbital
from tzlocal import get_localzone
import LETdec as dec
import sattracker
from init_port import *
ser = initSerialPort(COMPORT)

class Sat: #each satellite from the text file is stored as an object of class sat
    def __init__(self, tle = "", station = "", catalogNum = 0, checkSum1 = 0, checkSum2 = 0,pass_window = [], freq = 0):
        self.tle = tle #the web parsed TLE as a string
        self.station = station #satellite name
        self.pass_window = pass_window #Adjusted pass window + or - X minutes around TCA
        self.freq = freq #satellite downlink frequency in MHz

    def get_passes(self):  ##all pass times reported in UTC time (-4 hours for EST)

        time = datetime.utcnow()

        orb = Orbital(self.station.rstrip(), "best_file.txt")
        passes = orb.get_next_passes(time, 2, -75.15285, 39.98251, 0, tol=0.001, horizon=0)  # Temple radio room coords, longitude value is negative

        print(self.station.rstrip())
        if len(passes) != 0:

            for x in range(0, len(passes)):
                passes[x] = list(passes[x])

            new_passes = []
            for sublist in passes:
                for item in sublist:
                    new_passes.append(item)

            format = "%Y-%m-%d %H:%M:%S"
            now_local = []

            for y in range(0, len(new_passes)):
                now_local.append(new_passes[y].astimezone(get_localzone()))
                #now_local[y] = now_local[y].strftime(format)

            real_pass_window = now_local

            TCA_plus = real_pass_window[2] + timedelta(minutes=2)  # get the time 2 minutes after TCA
            TCA_minus = real_pass_window[2] + timedelta(minutes=-2)  # get the time 2 minutes before TCA

            sats[self.station.rstrip()].pass_window = [TCA_minus.strftime(format), TCA_plus.strftime(format)]  # trying to find the 'sweet spot' for best downlink around TCA

        else:
            sats[self.station.rstrip()].pass_window = None #pass_window is None if the sat does not pass within the alotted hours




    def calc_doppler(self):

        global doppler
        ground_coords = ("39.98251", "-75.15285", "0") #MAY NEED TO INCLUDE HEIGHT OF ANTENNAE ON THE ROOF FOR ACCURACY

        tle_split = self.tle.splitlines()
        tle_dict = {"name": tle_split[0],
                    "tle1": tle_split[1],
                    "tle2": tle_split[2]
                    }

        tracker = sattracker.Tracker(satellite=tle_dict, groundstation=ground_coords)



        while datetime.utcnow() < datetime.strptime(self.pass_window[1],"%Y-%m-%d %H:%M:%S" ): #loop runs until the end of satellite pass

            tracker.set_epoch(time.time()) ##sets the current time as the epoch (observation time), run this at the AOS

            #print("az         : %0.1f" % tracker.azimuth())
            #print("ele        : %0.1f" % tracker.elevation())
            #print("range      : %0.0f km" % (tracker.range() / 1000))
            #print("range rate : %0.3f km/s" % (tracker.satellite.range_velocity / 1000))
            doppler = tracker.doppler(self.freq*1e6)  ##send Doppler shifted freq in MHz to transceiver
            data = send_command(ser, 'FA' + str(doppler) + ';', 0)


            time.sleep(0.5)
        #ser.close()

        print("This pass for "+self.station.rstrip()+ " has ended. Select another satellite.")

    def to_transceiver(self):

        self.get_passes()

        if (self.pass_window != None): #if there is a pass within the alotted time

            print("Waiting for " +self.station.rstrip()+ " to enter your sky...\n")
            time.sleep(timedelta.total_seconds(datetime.strptime(self.pass_window[0],"%Y-%m-%d %H:%M:%S" ) - datetime.utcnow())) #suspend execution until the satellite pass begins

            print("Now downlinking from "+self.station.rstrip()+ "...\n")
            self.calc_doppler()

        else:
            print("This satellite does not pass within the alotted time frame. Select another satellite.")




def parser(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.find_all(text=True)

    lines = listToString(result)

    stringToFile(lines)

    station,lengthSt = dec.decode("kep_el.txt")##returns TLE's for all satellites listed

    satList = []

    for i in range(0, lengthSt):
        newSat = Sat("",station[i])
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
    for i in range(len(TLE_list)):
        u_list.append(TLE_list[i].upper()) #capitalize all strings in the text file for pyorbital to work
        best_file.write(u_list[i])

    best_file.close()

    ##Set satellite downlink frequencies in MHz
    sats['AO-07'].freq = 29.400
    sats['UO-11'].freq = 145.826
    sats['LO-19'].freq = 437.125
    sats['HUBBLE'].freq = 2255.5
    sats['MET-2/21'].freq = 137.85
    sats['AO-27'].freq = 436.795
    sats['IO-26'].freq = 435.822
    sats['FO-29'].freq = 435.900
    sats['NOAA-15'].freq = 137.620
    sats['GO-32'].freq = 435.225
    sats['ISS'].freq = 145.800
 '''sats['NO-44'].freq = 145.827
    sats['SO-50'].freq = 436.795
    sats['NOAA-18'].freq = 137.913
    sats['CO-55'].freq = 437.470
    sats['CO-57'].freq = 437.490
    sats['RS-22'].freq = 435.352
    sats['CO-58'].freq = 437.345
    sats['Falconsat-3'].freq = 435.103
    sats['CO-65'].freq = 437.475
    sats['AAUSAT2'].freq = 437.426
    sats['DO-64'].freq = 145.870
    sats['CO-66'].freq = 437.485
    sats['RS-30'].freq = 435.215
    sats['PRISM'].freq = 437.425
    sats['NOAA-19'].freq = 137.100
    sats['TISAT-1'].freq = 437.305
    sats['JUGNU'].freq = 437.505
    sats['SRMSAT'].freq = 437.500
    sats['AO-71'].freq = 437.475
    sats['HRBE'].freq = 437.502
    sats['HORYU-2'].freq = 437.375
    sats['RS-40'].freq = 435.365
    sats['BEESAT-3'].freq = 435.950
    sats['BEESAT-2'].freq = 435.950
    sats['ZACUBE-1'].freq = 437.355
    sats['TRITON-1'].freq = 145.818
    sats['GOMX-1'].freq = 437.250
    sats['LO-74'].freq = 437.445
    sats['AO-73'].freq = 145.970
    sats['SPROUT'].freq = 437.525
    sats['DUCHIFAT-1'].freq = 145.825
    sats['NANOSATCBR1'].freq = 145.865
    sats['DTUSAT-2'].freq = 2401.835
    sats['EO-80'].freq = 145.840
    sats['ANTELSAT'].freq = 437.575
    sats['VELOX-1'].freq = 145.980
    sats['DAURIA DX 1'].freq = 434.975
    sats['HODOYOSHI-1'].freq = 467.674
    sats['CHUBUSAT-1'].freq = 437.485
    sats['QSAT-EOS'].freq = 0 ##unknown frequency
    sats['FIREBIRD FU3'].freq = 437.405'''


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


#sats['AO-07'].to_transceiver()
