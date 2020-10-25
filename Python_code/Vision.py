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

        # Centroid
        self.ball_centroid = None
        self.basket_centroid = None
        self.orientation_range = 10

        # Depth stuff
        self.depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = self.depth_sensor.get_depth_scale()
        self.aligned_depth_frame = None
        self.color_frame = None

    def get_image(self):
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
            self.basket_mask = cv2.inRange(self.hsv, tuple(self.red_parameters['min']), tuple(self.red_parameters['max']))
        if self.color == 'blue':
            self.basket_mask = cv2.inRange(self.hsv, tuple(self.blue_parameters['min']), tuple(self.blue_parameters['max']))

    def get_basket_centroid(self):  # Purpose: distance debugging
        self.get_basket_color_mask()  # To update basket_mask

        basket_image, contours = cv2.findContours(self.basket_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
        self.get_image()
        self.ball_mask = cv2.inRange(self.hsv, tuple(self.green_parameters['min']), tuple(self.green_parameters['max']))

    def get_ball_centroid(self):
        self.get_ball_mask()
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(self.ball_mask, cv2.MORPH_CLOSE, kernel)
        center = None
        i = 0
        while True:
            i = i + i
            cnts = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 0:  # Check for something
                c = max(cnts, key=cv2.contourArea)
                ((cx, cy), r) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                if r > 10:  # Second validation
                    self.ball_centroid = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    break
                else:
                    continue
            elif i == 240:
                print('Could not get centroid after 240 frames')
                break
            else:
                continue

    def set_color_parameters(self):
        with open('color_parameters.json') as f:
            d = json.load(f)
        self.red_parameters = d['red']
        self.blue_parameters = d['blue']
        self.green_parameters = d['green']

    def stop_all(self):
        self.pipeline.stop()
        pass

    def rotate_to(self):
        self.get_ball_centroid()
        dif = self.ball_centroid[0] - (self.width / 2)
        return dif

    def return_basket_centroid(self):
        self.get_basket_centroid()
        return self.basket_centroid
