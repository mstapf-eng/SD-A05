import sys
import time
import datetime
from math import *
from pygeodesy import ecef
import ephem

class Tracker():

    def __init__(self, satellite, groundstation=("59.4000", "24.8170", "0")):
        self.groundstation = ephem.Observer()
        self.groundstation.lat = groundstation[0]
        self.groundstation.lon = groundstation[1]
        self.groundstation.elevation = int(groundstation[2])

        self.satellite = ephem.readtle(satellite["name"], satellite["tle1"], satellite["tle2"])

    def set_epoch(self, epoch=time.time()):
        ''' sets epoch when parameters are observed '''

        self.groundstation.date = datetime.datetime.utcfromtimestamp(epoch)
        self.satellite.compute(self.groundstation)

    def azimuth(self):
        ''' returns satellite azimuth in degrees '''
        return degrees(self.satellite.az)

    def elevation(self):
        ''' returns satellite elevation in degrees '''
        return degrees(self.satellite.alt)

    def latitude(self):
        ''' returns satellite latitude in degrees '''
        return degrees(self.satellite.sublat)

    def longitude(self):
        ''' returns satellite longitude in degrees '''
        return degrees(self.satellite.sublong)

    def range(self):
        ''' returns satellite range in meters '''
        return self.satellite.range

    def doppler(self, frequency_hz=0): #modified to return doppler shifted frequency
        ''' returns doppler shifted frequency in 11-digit format for transceiver '''
        calc_doppler = ((-self.satellite.range_velocity / 299792458. * frequency_hz) + frequency_hz)  # calcs doppler shifted freq in Hz
        temp_calc = str(round(calc_doppler, 1)).replace('.', '')  #round calculation to 1 decimal point, make it a string, and remove decimal point
        if len(temp_calc) == 9:
            calc_doppler = temp_calc.zfill(2)  # add 2 leading zeros
        elif len(temp_calc) == 10:
            calc_doppler = temp_calc.zfill(1)
        elif len(temp_calc) == 11:
            calc_doppler = temp_calc
        return (calc_doppler)
    
    def ecef_coordinates(self):
        ''' returns satellite earth centered cartesian coordinates
            https://en.wikipedia.org/wiki/ECEF
        '''
        x, y, z = self._aer2ecef(self.azimuth(), self.elevation(), self.range(), float(self.groundstation.lat), float(self.groundstation.lon), self.groundstation.elevation)
        return x, y, z

    def _aer2ecef(self, azimuthDeg, elevationDeg, slantRange, obs_lat, obs_long, obs_alt):

        #site ecef in meters
        sitex, sitey, sitez = ecef.EcefKarney.forward(self,obs_lat,obs_long,obs_alt) ##Had to edit this line myself, obs_alt must be meters if not 0

        #some needed calculations
        slat = sin(radians(obs_lat))
        slon = sin(radians(obs_long))
        clat = cos(radians(obs_lat))
        clon = cos(radians(obs_long))

        azRad = radians(azimuthDeg)
        elRad = radians(elevationDeg)

        # az,el,range to sez convertion
        south  = -slantRange * cos(elRad) * cos(azRad)
        east   =  slantRange * cos(elRad) * sin(azRad)
        zenith =  slantRange * sin(elRad)

        x = ( slat * clon * south) + (-slon * east) + (clat * clon * zenith) + sitex
        y = ( slat * slon * south) + ( clon * east) + (clat * slon * zenith) + sitey
        z = (-clat *        south) + ( slat * zenith) + sitez

        return x, y, z

'''
if __name__ == "__main__":
    # taken from: http://celestrak.com/NORAD/elements/cubesat.txt
    ec1_tle = { "name": "ESTCUBE 1", \
                "tle1": "1 39161U 13021C   14364.09038846  .00002738  00000-0  45761-3 0  7997", \
                "tle2": "2 39161  98.0855  83.4746 0010705 128.9405 231.2717 14.70651844 88381"}
    # http://www.gpscoordinates.eu/show-gps-coordinates.php
    tallinn = ("59.4000", "24.8170", "0")
    tracker = Tracker(satellite=ec1_tle, groundstation=tallinn)
    while 1:
        tracker.set_epoch(time.time())
        print("az         : %0.1f" % tracker.azimuth())
        print("ele        : %0.1f" % tracker.elevation())
        print("range      : %0.0f km" % (tracker.range()/1000))
        print("range rate : %0.3f km/s" % (tracker.satellite.range_velocity/1000))
        print("doppler    : %0.0f Hz" % (tracker.doppler(100e6)))
        time.sleep(0.5)
'''
