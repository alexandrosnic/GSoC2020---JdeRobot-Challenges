#!/usr/bin/python
#-*- coding: utf-8 -*-
import threading
import time
from datetime import datetime

import math
import cv2
import numpy as np

time_cycle = 80

class MyAlgorithm(threading.Thread):

    def __init__(self, camera, motors):
        self.camera = camera
        self.motors = motors
        self.threshold_image = np.zeros((640,360,3), np.uint8)
        self.color_image = np.zeros((640,360,3), np.uint8)
        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.threshold_image_lock = threading.Lock()
        self.color_image_lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)
        self.error = 0
        self.last_error = 0
        self.integral = 0
        self.derivative = 0
    
    def getImage(self):
        self.lock.acquire()
        img = self.camera.getImage().data
        self.lock.release()
        return img

    def set_color_image (self, image):
        img  = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.color_image_lock.acquire()
        self.color_image = img
        self.color_image_lock.release()
        
    def get_color_image (self):
        self.color_image_lock.acquire()
        img = np.copy(self.color_image)
        self.color_image_lock.release()
        return img
        
    def set_threshold_image (self, image):
        img = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.threshold_image_lock.acquire()
        self.threshold_image = img
        self.threshold_image_lock.release()
        
    def get_threshold_image (self):
        self.threshold_image_lock.acquire()
        img  = np.copy(self.threshold_image)
        self.threshold_image_lock.release()
        return img

    def run (self):

        while (not self.kill_event.is_set()):
            start_time = datetime.now()
            if not self.stop_event.is_set():
                self.algorithm()
            finish_Time = datetime.now()
            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def stop (self):
        self.stop_event.set()

    def play (self):
        if self.is_alive():
            self.stop_event.clear()
        else:
            self.start()

    def kill (self):
        self.kill_event.set()

    def algorithm(self):
        #GETTING THE IMAGES
        image = self.getImage()

        # Gains
        # kp = 0.0002 
        # ki = 0.0015
        # kd = 0.02
        kp = 0.005
        ki = 0.001
        kd = 0.015 

        # Define range of black color in HSV
        lower_black = np.array([20,0,0])
        upper_black = np.array([100,30,10])

        # Create the mask
        mask = cv2.inRange(image, lower_black, upper_black)

        # Get the center of the width dimension
        width = mask.shape[1]
        center_width = width / 2

        # Create threshold for binary result (black or white, 1 or 0)
        ret, thresh = cv2.threshold(mask, 127, 255, 0)

        # Find the contours of the thresholded image
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the center of the biggest contour
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            try:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
            except:
                cx = center_width
                cy = 0

            # Draw the lines and contour onto the initial image    
            cv2.line(image,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(image,(0,cy),(1280,cy),(255,0,0),1)
            cv2.drawContours(image, contours, -1, (0,255,0), 1)
            
            # Convert to RGB
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            cv2.drawContours(mask, contours, -1, (255,0,0), 2)
            
            # Update controller
            self.error = center_width - cx
            self.integral = (2 / 3) * self.integral + self.error
            self.derivative = self.error - self.last_error
            self.last_error = self.error
            
            angular = kp*self.error + ki*self.integral + kd*self.derivative
            
            print self.error
        
        else:
            angular = 0   


        print "Running"

        #EXAMPLE OF HOW TO SEND INFORMATION TO THE ROBOT ACTUATORS
        self.motors.sendV(10)
        self.motors.sendW(angular)

        #SHOW THE FILTERED IMAGE ON THE GUI
        self.set_threshold_image(mask)
