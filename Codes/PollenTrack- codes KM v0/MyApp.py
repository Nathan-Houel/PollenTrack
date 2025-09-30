from Camera import *
from Fan import *
from Led import *
from Button import *
from MotorTransport import *
from datetime import datetime
import os

class MyApp():

    def __init__(self, fan_pin, led_pins, motor_pins, camera_motor_pins, button_pin):
        self.TRANSPORT_DISTANCE = 110 #in mm 
        self.MINI_DEPLACEMENT = 5 #in mm
        self.path = "/home/pollentrack/Documents/PollenTrack"
        self.run = True
        self.fan = Fan(fan_pin)
        self.date = datetime.today().strftime("%Y-%m-%d")
        self.led = Led(led_pins)
        self.transportMotor = MotorTransport(motor_pins)
        self.camera = Camera(camera_motor_pins)
        self.button = Button(button_pin)
        self.button.set_callback_single(self.button_single_click)
        self.button.set_callback_double(self.button_double_click)
        self.button.start()
        self.init_storage()
        self.transportMotor.move(500,True)
        self.camera.zoom(200,True)
        self.camera.zoom(200,False)

    def routine(self):
        self.run = True
        start_time = time.time()
        self.fan.start_on()
        while self.run :
            current_time = time.time()
            t = current_time - start_time
            if t < (6*3600) :       # 6 hrs of pollen trapping
                self.led.on(0,1,1) 
                self.fan.on()
                time.sleep(0.1)
            else :
                self.led(0,0,1)
                self.transportMotor.move_mm(self.TRANSPORT_DISTANCE)
                for i in range(4):
                    self.camera.take_3_pictures(self.path + "/Image/" + self.date,self.date+ f"_{i}")
                    self.transportMotor.move_mm(self.MINI_DEPLACEMENT)
                self.run = False
        self.led.on_for(0,1,0, 10)

    def routine_test(self):
        self.run = True
        start_time = time.time()
        self.fan.start_on()
        self.fan.on()
        self.led.on(0,1,0)
        while self.run :
            current_time = time.time()
            t = current_time - start_time
            time.sleep(0.5)
            if t > 5 :
                self.button.stop()
                self.fan.off()
                time.sleep(0.1)
                self.led.on(1,0,1)
                time.sleep(0.1)
                self.transportMotor.move_mm(self.TRANSPORT_DISTANCE)
                time.sleep(0.1)
                for i in range(2):
                    self.camera.take_3_pictures(self.path+"/Image/" + self.date,self.date+ f"_{i}")
                    time.sleep(0.1)
                    self.transportMotor.move_mm(self.MINI_DEPLACEMENT)
                    time.sleep(0.1)
                self.run = False
        self.led.on(0,1,0) 
        self.off()

    def routine_test_sans_button(self):
        self.led.on(0,1,0)
        self.fan.on_for(10)
        self.button.stop()
        self.led.on(1,0,0)
        self.transportMotor.move_mm(self.TRANSPORT_DISTANCE)
        self.led.on(0,0,1)
        for i in range(2):
                    self.camera.take_3_pictures(self.path+"/Image/" + self.date,self.date+ f"_{i}")
                    self.transportMotor.move_mm(self.MINI_DEPLACEMENT)
        self.off()

    def init_storage(self):
        folder_path = self.path+"/Image/" + self.date

        if not os.path.exists(folder_path):
            try:
                os.mkdir(folder_path)
                print(f"Dossier créé : {folder_path}")
            except OSError as e:
                print(f"Erreur lors de la création du dossier : {e}")
        else:
            print(f"Le dossier {folder_path} existe déjà.")

    def button_single_click(self):
        print("bouton simple")
        self.run = False

    def button_double_click(self):
        print("bouton double")
        self.transportMotor.erase_log()
    
    def off(self):
        self.button.stop()  # stop button listening's thread
        self.button.join() 
        GPIO.cleanup()