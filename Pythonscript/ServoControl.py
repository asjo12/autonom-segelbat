import time
from adafruit_servokit import ServoKit

class servo_control:                #klass att anropa för att styra servon
    """Servo control klassen kan styra servon genom att skriva servo_control.FUNKTION
    Texten FUNKTION byts ut till vad som ska styras:
    1. servo_angle - För att sätta en vinkel på ett servo"""
    def __init__(self):
        pass
    
    def servo_angle (servo_number, set_angle, servo_channels=16):                     #set_angle = börvärde servo, servo_number = vilket servo, servo_channels = antal servon på kortet (default 16)
        """För att styra servo, anropa servo_control.servo_angle (1, 2) med två variabler: 
        1. Vilken vinkel servot ska till (Mellan 0 och 180 grader)
        2. Vilken numrering servot har på PCA9685 brädan, (0) är första servot på brädan."""
        servoboard = ServoKit(channels=servo_channels)
        servoboard.servo[servo_number].angle = set_angle
        return None
    
    def current_angle(servo_number, servo_channels=16):
        """För att få aktuell vinkel på servo"""
        servoboard = ServoKit(channels = servo_channels)
        currentangle = servoboard.servo[servo_number].angle
        return currentangle
