from picamera2 import Picamera2, Preview
from MotorMicroscope import *
from Led import *
import cv2
import numpy as np
from camera_utilities import blurriness, pollenDetection

class Camera(Picamera2):
    def __init__(self, camera_motor_pins) :
        super().__init__()
        self.motor = MotorMicroscope(camera_motor_pins)
        print("Initialisation of the Camera : done")


    def take_picture(self, image_path, image_name):
        """ Take an image and save it to image_path with the label image_name

        Args:
            image_path (_string_):
            image_name (_string_): 
        """
        self.start_preview(Preview.QTGL)
        self.start()
        self.capture_file(image_path+"/"+image_name) 
        self.stop_preview()
        self.stop()

    def take_3_pictures(self, image_path, image_name):
        """ Acquire 3 pictures with a slight difference in focus and save it to image_path with the label image_name

        Args:
            image_path (string): 
            image_name (string): 
        """
        self.focus()
        for i in range(3):
            
            if i == 1:
                self.zoom(100,False)
            elif i == 2:
                self.zoom(200,True)

            self.take_picture(image_path, f"{image_name}_{i+1}.jpg")
        self.zoom(100,False)


    # def calibrage(self):
    #     state = True
    #     def set_state_false():
    #         state = False
    #     keyboard.add_hotkey('z', lambda : self.zoom(True))
    #     keyboard.add_hotkey('s', lambda : self.zoom(False))
    #     keyboard.add_hotkey('a', set_state_false)
    #     self.start_preview(Preview.QTGL)
    #     self.start()
    #     while state :
    #         pass
    #     self.stop_preview()

    def zoom(self, step, direction):
        """activate the motor for x steps to the direction given in parameters

        Args:
            step (_int_): Number of steps to rotate
            direction (_bool_): True if clock-wise and False in the opposite case
        """
        self.motor.move(step, direction)

    def focus(self):
        """Activate the motor to get the image sharp using pollen detection and blurriness measurement
        """
        self.start_preview(Preview.QTGL)
        self.start()
        image = self.capture_array()
        x, y, w, h = pollenDetection.pollen_detection(image)
        cpt = 0
        while x==0 & y==0 & w==0 & h==0 :
            if cpt < 20 :
                self.zoom(100,True)
                time.sleep(0.5)
                cpt+=1
                image = self.capture_array()
                x, y, w, h = pollenDetection.pollen_detection(image)
            if cpt == 20 :
                for _ in range(20):
                    self.zoom(100, False)
                    time.sleep(0.3)
                cpt+=1
            if (cpt > 20 and cpt <= 40) :
                self.zoom(100, False)
                time.sleep(0.5)
                cpt+=1
                image = self.capture_array()
                x, y, w, h = pollenDetection.pollen_detection(image)
            if cpt > 40 :
                for _ in range(20):
                    self.zoom(100,True)
                    time.sleep(0.3)
                x=1
                
        comp = [x,y,w,h]
        if comp != [1,0,0,0]:
            cropped_image = image[y:y+h, x:x+w]

            def get_direction(step, img):
                """Indicate if it's better to zoom in, zoom out or stay in position
                """
                time.sleep(1)
                sharp =  blurriness.measure_blurriness(img)
                self.zoom(step,True)
                time.sleep(1)
                sharp_true = blurriness.measure_blurriness(img)
                self.zoom(2*step, False)
                time.sleep(1)
                sharp_false = blurriness.measure_blurriness(img)
                self.zoom(step,True)

                if (sharp_false > sharp) & (sharp_false > sharp_true):
                    return False
                elif (sharp_true > sharp) & (sharp_true > sharp_false):
                    return True
                else:
                    return -1

            
            step = 150    
            direction = get_direction(step, cropped_image)
            if direction != -1 :
                self.zoom(step,direction)

            while step > 80 :
                step -= 10
                I = self.capture_array()
                cropped_image = I[y:y+h, x:x+w]
                direction = get_direction(step, cropped_image)
                if direction != -1 :
                    self.zoom(step,direction)
        self.stop_preview()
        self.stop()
            

    def off(self) :
        self.motor.off()

if __name__ == "__main__":
    in1 = 2
    in2 = 3
    in3 = 17
    in4 = 27
    pins_list = [in1, in2, in3, in4]
    cam = Camera(pins_list)
    cam.focus()
    cam.off()