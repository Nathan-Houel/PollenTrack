import RPi.GPIO as GPIO
import time


class Fan():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)    
        
        self.PWM_FREQ = 3853   
        self.duty_cycle = 5.04
        self.duty_cycle_start = 100                                                  
        self.pwm = GPIO.PWM(pin, self.PWM_FREQ)
        self.pwm.start(0)
        print("Initialisation of the Fan : done")
        
    def start_on(self) :
        self.pwm.ChangeDutyCycle(self.duty_cycle_start) # Start strong to give momentum to the fan
        time.sleep(1)

    def on(self) :   
        self.pwm.ChangeDutyCycle(self.duty_cycle) # Then set the wanted duty cycle
    
    def on_for(self, duration):
        """ Turn on the fan during the time given in parameters

        Args:
            duration (_float_): in seconds
        """
        self.start_on()
        self.on()
        time.sleep(duration)
        self.pwm.stop()

    def off(self):
        """ Turn off the fan
        """
        self.pwm.stop()
        GPIO.cleanup(self.pin)

if __name__ == "__main__" :
    fan = Fan(9)
    fan.on_for(10)
    fan.off()