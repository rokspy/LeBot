import numpy as np
import cv2
import pyrealsense2 as rs
import json


class ImageProcessing:

    def __init__(self, basket_color):
        self.width = 1280
        self.height = 720
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, 30)
        self.profile = self.pipeline.start(self.config)

        self.align_to = rs.stream.color
        self.align = rs.align(self.align_to)

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

        # Depth stuff
        self.depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = self.depth_sensor.get_depth_scale()
        self.aligned_depth_frame = None
        self.color_frame = None

    def get_image(self):  # Purpose: get hsv image
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        frame_array = np.asanyarray(color_frame.get_data())
        self.aligned_depth_frame = aligned_frames.get_depth_frame()

        self.hsv = cv2.cvtColor(frame_array, cv2.COLOR_BGR2HSV)

    def get_depth_from_mask(self, obj_mask):
        self.get_image()

        depth_image = np.asanyarray(self.aligned_depth_frame.get_data())
        mask_array_mask = depth_image[obj_mask > 0]

        dist = np.average(mask_array_mask) * self.depth_scale
        return dist

    def get_basket_color_mask(self):  # Purpose: get color mask (pre image processing)
        self.get_image()  # To update hsv

        if self.color == 'red':
            self.basket_mask = cv2.inRange(self.hsv, self.red_parameters['min'], self.red_parameters['max'])
        if self.color == 'blue':
            self.basket_mask = cv2.inRange(self.hsv, self.blue_parameters['min'], self.blue_parameters['max'])

    def get_basket_centroid(self):  # Purpose: distance debugging
        self.get_basket_color_mask()  # To update basket_mask

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

    def stop_all(self):
        self.pipeline.stop()
        pass
