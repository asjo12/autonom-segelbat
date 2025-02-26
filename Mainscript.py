import os
import sys
import time
import smbus
import math
import RPi.GPIO as GPIO
import threading


from ServoControl import servo_control			#Importerar programkoden för att styra servon, via PCA9685
from Z_angle import IMUReader					#Importerar programkoden för att läsa av IMU-sensor (MPU 9250)
from PID_control import PIDController			#Importerar progarm för att reglera utsignal (roder) med PID-regulator
from Wind_angle import RotaryEncoder			#Importerar progamkoden för att läsa av vinkel på encoder


############################################# Definiera GPIO-pins ##################################################
GPIO.setmode(GPIO.BCM) #Vilken numrering som används, = GPIO numrering
GPIO.setwarnings(False) #Gör att felkoder inte stör programmet

#Bestämmer om GPIO pinnar ska vara IN-put eller OUT-put
GPIO.setup(5, GPIO.OUT) #Grön lampa
GPIO.setup(6, GPIO.OUT) #Röd lampa
############################################# Startar avläsningar av sensorer #########################################
imu_reader = IMUReader() #Definierar IMU-avläsningen
imu_reader.start() #Startar IMU-avläsningen

encoder = RotaryEncoder() #Definierar encodern
encoder_thread = threading.Thread(target=encoder.start_encoder) #Skapar en separat tråd av encodern
encoder_thread.start() #Startar avläsningen av encodern i en separat tråd

###########################################HUVUDPROGRAM###############################################################

pid_controller = PIDController() #Skapar PID-kontrollern

riktning = 0 #Börvärde för båten (0 = rakt fram)

try:
    GPIO.output(5, GPIO.LOW) #Släcker grön lampa när programmet körs
    GPIO.output(6, GPIO.LOW) #Släcker röd lampa när programmet körs
    time.sleep(2)	#Väntar 2 sekunder innan grön lampa tänds igen
    GPIO.output(5, GPIO.HIGH) #Tänder grön lampa när programmet körs

    while True:
        """Roderstyrning efter signal från IMU
        """
        Zangle = imu_reader.Zangle #Hämtar värdet för Z-angle från IMU

        control_output = pid_controller.update(riktning, Zangle) #PID reglering för roder, beräknar värde med invärdet (börvärde för båten) och aktuell Z-vinkel från IMU.
        print("Zangle:", Zangle)

        if control_output >100:
            servo_control.servo_angle(0, 28)
        elif control_output <-100:
            servo_control.servo_angle(0, 152)
        else:
            servo_control.servo_angle(0, 90-control_output*0.623) #Output*0.623
        
        current_angle0 = servo_control.current_angle(0) #Hämtar aktuellt värde för servovinkeln

        print("Roder:", current_angle0)

                
        
        """Segelstyrning efter signal från encoder
        """
        counter_value = encoder.get_counter() #Hämtar in värde från encodern    
        windangle = counter_value			#Encoderns värde är vår vindriktning
        
        #print("Wind_angle:", windangle)
        
        """If sats som räknar ut servovinkel för servot som styr seglet
        Vinkeln på seglet ska vara hälften av windens vinkel relativt båten
        """
        if windangle > 180:
            sailangle = (windangle-180)*0.5
        elif windangle < 180:
            sailangle = (windangle+180)*0.5
        
        """If sats som sätter fasta ändlägen för segelvinkel (+- 45 grader)
        """
        if sailangle > 135:
            sailangle = 135
        elif sailangle < 45:
            sailangle = 45
        
        servo_control.servo_angle(4, sailangle) #Sätter vinkel på segel efter bestämt värde (segelservo = 1)
        #print("sail:", sailangle)
        
        time.sleep(0.1) #Uppdateringsfrekvens för styrning av servon
        
except:
    GPIO.output(5, GPIO.LOW) #Släcker grön lampa vid fel i programmet
    GPIO.output(6, GPIO.HIGH) #Tänder röd lampa vid fel i programmet

    print("Fel i loopen")
    
