import RPi.GPIO as GPIO
from time import sleep

class RotaryEncoder:
    def __init__(self, enc_a=17, enc_b=27, index=22):
        self.counter = 1
        self.index_position = 0
        self.Enc_A = enc_a
        self.Enc_B = enc_b
        self.Index = index

        self.setup_gpio()

    def setup_gpio(self):
        #print("Rotary Encoder Test Program")
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Enc_A, GPIO.IN)
        GPIO.setup(self.Enc_B, GPIO.IN)
        GPIO.setup(self.Index, GPIO.IN)
        GPIO.add_event_detect(self.Enc_A, GPIO.RISING, callback=self.rotation_decode)
        #GPIO.add_event_detect(self.Index, GPIO.RISING, callback=self.index_detected)

    def rotation_decode(self, _):
        switch_A = GPIO.input(self.Enc_A)
        switch_B = GPIO.input(self.Enc_B)

        if (switch_A == 1) and (switch_B == 0):
            self.counter += 1
            #print("direction ->", self.counter)
            while switch_B == 0:
                switch_B = GPIO.input(self.Enc_B)
        elif (switch_A == 1) and (switch_B == 1):
            self.counter -= 1
            #print("direction <-", self.counter)
            while switch_A == 1:
                switch_A = GPIO.input(self.Enc_A)

    def index_detected(self, _):
        #print("Index detected")
        self.counter = self.index_position
    
    def get_counter(self):
        return self.counter

    def start_encoder(self):
        try:
            while True:
                if self.counter < 0:
                    self.counter = 359
                elif self.counter > 359:
                    self.counter = 0
                #sleep(1)

        except KeyboardInterrupt:
            GPIO.cleanup()

if __name__ == '__main__':
    encoder = RotaryEncoder(enc_a=17, enc_b=27, index=22)
    encoder.start_encoder()
