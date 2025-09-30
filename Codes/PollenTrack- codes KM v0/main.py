from MyApp import *

if __name__ == "__main__":

    #== insert pin numbers ==#
    fan_pin = 9 
    led_pins = [23, 24, 8] 
    camera_pins = [2, 3, 17, 27]
    motor_pins = [26, 19] 
    button_pin = 5 

    cycle = MyApp(fan_pin, led_pins, motor_pins, camera_pins, button_pin)
    cycle.routine()
    cycle.off()
     