import numpy as np
import cv2
import json


class ProcessingFromPicture:

    def __init__(self, basket_color):
        self.hsv = None

        # Store the mask from functions
        self.basket_mask = None
        self.ball_mask = None

        # Assign color value
        self.color = basket_color
        self.red_parameters = None
        self.blue_parameters = None
        self.green_parameters = None
        self.set_color_parameters()  # To forget about it :)

        # Store ball centroid
        self.ball_centroid = None

        # Store basket centroid
        self.basket_centroid = None

    def get_image(self, img_location):  # Purpose: get hsv image
        img = cv2.imread(img_location)
        self.hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def get_basket_color_mask(self):
        self.get_image()

        if self.color == 'red':
            self.basket_mask = cv2.inRange(self.hsv, self.red_parameters['min'], self.red_parameters['max'])
        if self.color == 'blue':
            self.basket_mask = cv2.inRange(self.hsv, self.blue_parameters['min'], self.blue_parameters['max'])

    def get_basket_centroid(self):
        self.get_basket_color_mask()

        basket_image, contours, hrchy = cv2.findContours(self.basket_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        biggest_cnt = 0
        points = None

        for cnt in contours:
            cnt_size = cv2.contourArea(cnt)
            if cnt_size > biggest_cnt:
                points = cnt_size

        M = cv2.moments(points)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        self.basket_centroid = [cX, cY]

    def get_ball_mask(self):
        self.get_image()  # To update hsv

        self.ball_mask = cv2.inRange(self.hsv, self.green_parameters['min'], self.green_parameters['max'])

    def get_ball_centroid(self):
        self.get_ball_mask()

        ball_image, contours, hierarchy = cv2.findContours(self.ball_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        biggest_cnt = 0
        points = None

        for cnt in contours:
            cnt_size = cv2.contourArea(cnt)
            if cnt_size > biggest_cnt:
                points = cnt_size

        M = cv2.moments(points)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        self.ball_centroid = [cX, cY]

    def set_color_parameters(self):
        with open('color_parameters.json') as f:
            d = json.load(f)
        self.red_parameters = d['red']
        self.blue_parameters = d['blue']
        self.green_parameters = d['green']

    def show_ball_mask(self):
        self.get_ball_mask()
        cv2.namedWindow('ball_mask', cv2.WINDOW_NORMAL)
        cv2.imshow(self.ball_mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show_basket_mask(self):
        self.get_basket_color_mask()
        cv2.namedWindow('basket_mask', cv2.WINDOW_NORMAL)
        cv2.imshow(self.basket_mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def print_ball_centroid(self):
        self.get_ball_centroid()
        print(self.ball_centroid)
        
    def print_basket_centroid(self):
        self.get_basket_centroid()
        print(self.basket_centroid)


# Reminder to set color.
# Not yet running exceptions for not found.
debug = ProcessingFromPicture('red')
debug.get_image("./images/image1.jpg")
debug.show_basket_mask()


