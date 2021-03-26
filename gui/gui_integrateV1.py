import tkinter as tk
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
#ser = initSerialPort(COMPORT)

class Sat: #each satellite from the text file is stored as an object of class sat
    def __init__(self, tle = "", station = "", catalogNum = 0, checkSum1 = 0, checkSum2 = 0,pass_window = [], freq = 0):
        self.tle = tle #the web parsed TLE as a string
        self.station = station #satellite name
        self.catalogNum = catalogNum #satellite ID number used to lookup satellites
        self.checkSum1 = checkSum1
        self.checkSum2 = checkSum2
        self.pass_window = pass_window #Adjusted pass window + or - X minutes around TCA
        self.freq = freq #satellite downlink frequency in MHz

    def get_passes(self):  ##all pass times reported in UTC time (-4 hours for EST)

        time = datetime.utcnow()

        orb = Orbital(self.station.rstrip(), "best_file.txt")
        passes = orb.get_next_passes(time, 4, 75.15285, 39.98251, 0, tol=0.001, horizon=0)  # Temple radio room coords, longitude value is actually negative
                                        #  ^ time in hours to look for sats
                                        # can set a input box for user

        print(self.station.rstrip())
        if len(passes) != 0:

            for x in range(0, len(passes)):
                passes[x] = list(passes[x])

            new_passes = []
            for sublist in passes:
                for item in sublist:
                    new_passes.append(item)

            format = "%Y-%m-%d   %H:%M:%S"
            now_local = []

            for y in range(0, len(new_passes)):
                now_local.append(new_passes[y].astimezone(get_localzone()))
                #now_local[y] = now_local[y].strftime(format)

            real_pass_window = now_local

            TCA_plus = real_pass_window[2] + timedelta(minutes=2)  # get the time 2 minutes after TCA
            TCA_minus = real_pass_window[2] + timedelta(minutes=-2)  # get the time 2 minutes before TCA
            TCA_peak = real_pass_window[2]

            sats[self.station.rstrip()].pass_window = [TCA_minus.strftime(format), TCA_plus.strftime(format),TCA_peak.strftime(format)]  # trying to find the 'sweet spot' for best downlink around TCA

        else:
            sats[self.station.rstrip()].pass_window = None #pass_window is None if the sat does not pass within the alotted hours

    def calc_doppler(self):

        global doppler
        ground_coords = ("39.98251", "75.15285", "0") #MAY NEED TO INCLUDE HEIGHT OF ANTENNAE ON THE ROOF FOR ACCURACY

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

            ##SET an update label here to display the

            time.sleep(0.5)
        ser.close()

        print("This pass for "+self.station.rstrip()+ " has ended. Select another satellite.")

    def to_transceiver(self):

        self.get_passes()

        if (self.pass_window != None): #if there is a pass within the alotted time

            print("Waiting for " +self.station.rstrip()+ " to enter your sky...\n")
            pg2_label_status.config(text="Waiting for " +self.station.rstrip()+ " to enter your sky...")
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
    print(lines)  #error checking

    stringToFile(lines)

    station,catalogNumber,checkSum1,checkSum2,lengthSt = dec.decode("kep_el.txt")##returns TLE's for all satellites listed

    global satList
    satList= []

    for i in range(0, lengthSt):
        newSat = Sat("",station[i], catalogNumber[i],checkSum1[i], checkSum2[i])
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
    sats['NO-44'].freq = 145.827
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
    sats['FIREBIRD FU3'].freq = 437.405

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

## END OF WEB SCRAPING ####

def are_you_sure():
    #Pop up declarations
    newWindow = tk.Toplevel(root)
    newWindow.title("Terminate?")
    newWindow.geometry("400x150+50+50")

    #Window widget declarations
    window_label = tk.Label(newWindow, text="Are you sure?", font="Verdana 10 bold")
    window_button_yes = tk.Button(newWindow, text="Yes", command=root.destroy, padx=20, pady=0.5)
    window_button_no = tk.Button(newWindow, text="No", command=newWindow.destroy, padx=20, pady=0.5)

    #Widget placements
    window_label.place(relx=0.4, rely=0.15, anchor='nw')
    window_button_yes.place(relx=0.3, rely=0.5, anchor='nw')
    window_button_no.place(relx=0.6, rely=0.5, anchor='nw')
    return

def start_tracking():
    selected_sat.to_transceiver()

def start_to_idle():
    #Wipe start screen
    pg1_label_title.place_forget()
    pg1_label_back.place_forget()
    pg1_button.place_forget()

    # Satellite functions
    parser("https://www.amsat.org/tle/current/nasabare.txt")

    #Place the idle screen widgets
    pg2_label_1.place(relx=0.005, rely=0.005, anchor='nw')
    pg2_label_2.place(relx=0.05, rely=0.105, anchor='nw')

    pg2_button_end.place(relx=0.8, rely=0.95, anchor='nw')
    pg2_button_begin_tracking.place(relx=0.05, rely=0.45, anchor='nw')
    pg2_label_opening.place(relx=0.05, rely=0.27, anchor='nw')
    pg2_label_peak.place(relx=0.05, rely=0.30, anchor='nw')
    pg2_label_closing.place(relx=0.05, rely=0.33, anchor='nw')
    pg2_label_confirm.place(relx=0.05, rely=0.15, anchor='nw')
    pg2_label_status.place(relx=0.05, rely=0.50, anchor='nw')
    pg2_label_sat_freq.place(relx=0.05, rely=0.18, anchor='nw')
    return

def selection_listbox( ):

    #can add search bar

    #Window initialization
    newWindow = tk.Toplevel(root)
    newWindow.title("Satellite Selection")
    newWindow.geometry("300x500+50+50")
    newWindow.resizable(width=False, height=False)
    selection_flag = 0

    #window widgets
    newWindow_listbox = tk.Listbox(newWindow, width=46, height=27, selectmode=tk.SINGLE)
    newWindow_button = tk.Button(newWindow, text="Input Selection", padx=15, pady=2.5,
                                 command=lambda: set_selected_sat(newWindow_listbox, newWindow))
    newWindow_listbox.place(relx=0.005, rely=0.005, anchor='nw')
    newWindow_button.place(relx=0.3, rely=0.9, anchor='nw')

    #for loop to populate listbox
    for i in range(len(satList)):
        newWindow_listbox.insert(i, satList[i].station.rstrip())
    return

def set_selected_sat(listbox,window):
    global selected_sat
    selected_sat = listbox.get(listbox.curselection())  #Gets the string from the menu
    selected_sat = sats[selected_sat]                   #Searches dict for string and gets obejct
    selected_sat.get_passes()

    pg2_label_confirm.config(text="Selected satellite: " + str(selected_sat.station.rstrip()))
    pg2_label_sat_freq.config(text="Down-link frequency: " + str(selected_sat.freq) + " Mhz")

    if(selected_sat.pass_window != None):
        pg2_label_opening.config(text="Pass window opening: " + str(selected_sat.pass_window[0]))
        pg2_label_peak.config(text="Pass window opening: " + str(selected_sat.pass_window[2]))
        pg2_label_closing.config(text="Pass window closing: " + str(selected_sat.pass_window[1]))

        pg2_label_opening.place(relx=0.05, rely=0.27, anchor='nw')
        pg2_label_peak.place(relx=0.05, rely=0.30, anchor='nw')
        pg2_label_closing.place(relx=0.05, rely=0.33, anchor='nw')
        pg2_label_window_error.place_forget()
    else:
        pg2_label_opening.place_forget()
        pg2_label_peak.place_forget()
        pg2_label_closing.place_forget()
        pg2_label_window_error.place(relx=0.05, rely=0.27, anchor='nw')


    window.destroy()
    #Add update labels here for pass times, and so forth from global list
    #Add a frequncy label too

    return


#Root stuff
root = tk.Tk(className="Temple Satellite Tracker")
root.geometry("750x600+10+10")
root.resizable(width=False, height=False)

#Background image
background = tk.PhotoImage(file="backer.ppm")
background = background.zoom(3, 3)

#Start Screen widget creation
pg1_label_title = tk.Label(root, text="Temple 3-in-1 AMSAT Special", fg="white", bg="black", font="Verdana 20 bold")
pg1_label_back = tk.Label(root, image=background)
pg1_button = tk.Button(root, text="Start", font="Verdana 12", padx=55, pady=5, command=start_to_idle)

#Start Screen placing commands
pg1_label_title.place(relx=0.40, rely=0.075, anchor='nw')
pg1_label_title.lift()
pg1_label_back.place(x=0.0, y=0.0, relwidth=1.0, relheight=1.0)
pg1_button.place(relx=0.40, rely=0.95, anchor='sw')

#Idle Screen widget creation
pg2_label_1 = tk.Label(root, text="Tracking Idle Page", font="Verdana 10 bold")
pg2_label_2 = tk.Button(root, text="Select a satellite", command=selection_listbox)
pg2_button_end = tk.Button(root, text="End Program and Tracking", command=are_you_sure)
pg2_button_begin_tracking = tk.Button(text="Begin Tracking",command=start_tracking)
pg2_label_confirm = tk.Label(root, text="Selected satellite: None", font="Verdana 10")
pg2_label_status = tk.Label(root, text="Program status: Test", font="Verdana 10")
pg2_label_window_error = tk.Label(root, text="Satellite does not pass over in inputted window, "
                                             "please adjust timme window length",font="Verdana 10")

#Pass Labels
pg2_label_opening = tk.Label(root, text="Pass window opening:None", font="Verdana 10")
pg2_label_peak = tk.Label(root, text="Pass window peak: None", font="Verdana 10")
pg2_label_closing = tk.Label(root, text="Pass window closing: None", font="Verdana 10")
pg2_label_sat_freq = tk.Label(root, text="Down-link frequency: None",font="Verdana 10")

root.mainloop()

