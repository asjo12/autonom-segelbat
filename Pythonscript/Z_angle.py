import time
import smbus
import math
from threading import Thread 

from imusensor.MPU9250 import MPU9250


class IMUReader(Thread):
    """Definierar IMU med address och bus samt läser in data från IMU.
    Läser av värdet för z-angle och integerar för att få fram vinkel i z-led.
    För att starta läsningen skriv följande i ditt huvudprogram:
    imu_reader = IMUReader()
    imu_reader.start()
    För att få det senaste z-angle kan följande skrivas:
    imu_reader.Zangle"""
    def __init__ (self):
        Thread.__init__(self)
        self.Zangle = 0 #Startvärde för beräkning av Z-angle (vanligast 0)
        address = 0x68 #Adress för IMU-enhet
        bus = smbus.SMBus(1) 
        self.imu = MPU9250.MPU9250(bus, address)
        self.imu.begin()
        
    def run(self):
        drift = 0
        varv = 0
        tdrift = 0
        starttime = time.time()
        nowtime = time.time() #deffinerar start och now -time 
        previoustime = time.monotonic()
        Zgyro = 0
        while True:
            ts = 0.05
            t0 = time.monotonic() #sparar starttid
            
            self.imu.readSensor() # läser in sensor
            
            dt = t0 - previoustime
            self.Zangle = self.Zangle + Zgyro * dt - drift #integrerar numeriskt och tar bort driftvärdet varje gång
            
            Zgyro = self.imu.GyroVals[2] * 180 / math.pi #sparar vinkelhastigheten i grader/s
            
            previoustime = t0 #tiden då loopen började loggas som previous time
            
            """if satsen körs de 2 första sekunderna och mätter den genomsnittliga driften på gyrot..
            Upprepas vid varje start. """
            
            passedtime = nowtime-starttime #
            if passedtime < 2: # kör endast under de första 2 sekunderna
                varv = varv + 1 # räknar antal varv
                tdrift = tdrift + self.Zangle #total drift
                drift = tdrift / varv  # genomsnittlig drift
                nowtime = time.time() # tid efter loop
        
            time.sleep (ts) # kort stopp för att minska processorns belastning
