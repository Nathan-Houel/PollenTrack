import RPi.GPIO as GPIO
import time

class MotorMicroscope():
    def __init__(self, motor_pins):
        in1, in2, in3, in4 = motor_pins
        self.step_sleep = 0.002
        self.step_sequence = [[1,0,0,1],
                            [1,0,0,0],
                            [1,1,0,0],
                            [0,1,0,0],
                            [0,1,1,0],
                            [0,0,1,0],
                            [0,0,1,1],
                            [0,0,0,1]]

        GPIO.setmode( GPIO.BCM )
        GPIO.setup( in1, GPIO.OUT )
        GPIO.setup( in2, GPIO.OUT )
        GPIO.setup( in3, GPIO.OUT )
        GPIO.setup( in4, GPIO.OUT )

        GPIO.output( in1, GPIO.LOW )
        GPIO.output( in2, GPIO.LOW )
        GPIO.output( in3, GPIO.LOW )
        GPIO.output( in4, GPIO.LOW )

        self.motor_pins = motor_pins
        self.motor_step_counter = 0 
        print("Initialisation of the microscope's motor : done")


    def off(self):
        """Clean up the pins used
        """
        GPIO.output( self.motor_pins[1], GPIO.LOW )
        GPIO.output( self.motor_pins[2], GPIO.LOW )
        GPIO.output( self.motor_pins[3], GPIO.LOW )
        GPIO.output( self.motor_pins[0], GPIO.LOW )
        GPIO.cleanup()

    def move(self, steps, direction):
        """Rotate the motor according to the number of steps and the direction given in parameters

        Args:
            steps (_int_):
            direction (_bool_): 
        """
        for _ in range(steps):
            for pin in range(len(self.motor_pins)):
                GPIO.output(self.motor_pins[pin], self.step_sequence[self.motor_step_counter][pin])

            if direction:
                self.motor_step_counter = (self.motor_step_counter - 1) % 8
            else:
                self.motor_step_counter = (self.motor_step_counter + 1) % 8

            time.sleep(self.step_sleep)

if __name__ == "__main__":
    in1 = 17
    in2 = 18
    in3 = 27
    in4 = 22
    pins_list = [in1, in2, in3, in4]
    motor = MotorMicroscope(pins_list, True)
    motor.move(500, False)
    time.sleep(2)
    motor.move(500, True)
    motor.off()