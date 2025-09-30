import RPi.GPIO as GPIO
import time
from numpy import pi

radius_min = 33/2 #in mm
i_m = 1.8/16
full_rotation_step = 3200 # 16 microstep x 200 
scotch_thickness = 28e-6 #in mm

class MotorTransport():
    def __init__(self, motor_pins):
        self.dirPin, self.stepPin = motor_pins
        self.speed = 0.004

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dirPin, GPIO.OUT)
        GPIO.setup(self.stepPin, GPIO.OUT)
        print("Initialisation of the transport's motor : done")


    def off(self):
        """Turn off the motor and clean the pins
        """
        GPIO.cleanup()

    def move(self, steps, direction):
        """ Make the motor rotate steps in the direction given in parameters

        Args:
            steps (_int_): Number of steps to rotate the motor
            direction (_bool_):
        """
        if direction:
            self.refresh_log(steps)
            GPIO.output(self.dirPin, GPIO.LOW)
        else:
            GPIO.output(self.dirPin, GPIO.HIGH)

        for _ in range(steps):
            GPIO.output(self.stepPin, GPIO.HIGH)
            time.sleep(self.speed) 
            GPIO.output(self.stepPin, GPIO.LOW)
            time.sleep(self.speed)

    def move_mm(self,distance):  
        """ Make the motor reel in distance in mm of scotch

        Args:
            distance (_int_): Distance to reel in in millimeter
        """
        total_steps = self.get_total_step()
        radius = radius_min + (total_steps % full_rotation_step)*scotch_thickness
        angle = (distance*i_m)/radius
        step = int(angle*full_rotation_step/(2*pi))
        self.refresh_log(step)
        self.move(step, True)

    def refresh_log(self,steps):
        """ Update the number of steps rotated from the initiation of the spool until now in a text file

        Args:
            steps (_int_): 
        """
        total_steps = self.get_total_step()
        with open("/home/pollentrack/Documents/PollenTrack/motor_utilities/log.txt", "w") as file:
            file.write(str(steps + total_steps))

    def erase_log(self):
        """ Erase the log file to change the spool and put the number of step to 0
        """
        with open("/home/pollentrack/Documents/PollenTrack/motor_utilities/log.txt", "w") as file:
            file.write(str(0))

    def get_total_step(self):
        """ Get the number of steps rotated from the initiation of the spool until now

        Returns:
            _int_:
        """
        with open("/home/pollentrack/Documents/PollenTrack/motor_utilities/log.txt", "r") as file:
                total_steps = int(file.read())
        return total_steps
                

if __name__ == "__main__":
    in1 = 26
    in2 = 19
    pins_list = [in1, in2]
    motor = MotorTransport(pins_list)
    motor.move(300, True)
    print(motor.get_total_step())
    time.sleep(0.1)
    motor.move_mm(100)
    print(motor.get_total_step())
    motor.erase_log()
    motor.off()