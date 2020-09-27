import numpy as np
import cv2
import pyrealsense2 as rs


class ImageProcessing:

    def __init__(self,color):
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

        self.basketColor = "blue"
        self.basketCoord = [0, 0, 0, 0]

    def find_basket(self):
        area = 0
        if self.basketColor == "blue":
            while area < 40:    # Placeholder value
                hl, sl, vl = 10, 10, 10
                hu, su, vu = 20, 20, 20

                l_blue = np.array([hl, sl, vl])
                u_blue = np.array([hu, su, vu])

                blue_mask = cv2.inRange(self.hsv, l_blue, u_blue)

                b_basket_contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                b_cnt = b_basket_contours[0]
                area = cv2.contourArea(b_cnt)
                x1, y1, w, h = cv2.boundingRect(b_cnt)
                x2, y2 = x1 + w, y1 + h

        if self.basketColor == "red":
            while area < 40:
                hl, sl, vl = 100, 10, 10
                hu, su, vu = 209, 20, 20

                l_red = np.array([hl, sl, vl])
                u_red = np.array([hu, su, vu])

                red_mask = cv2.inRange(self.hsv, l_red, u_red)

                r_basket_contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                r_cnt = r_basket_contours[0]
                area = cv2.contourArea(r_cnt)
                x1, y1, w, h = cv2.boundingRect(r_cnt)
                x2, y2 = x1 + w, y1 + h
        else:
            print("Problem assigning basket")
            x1, y1, x2, y2 = None, None, None, None

        self.basketCoord = np.array([x1, x2, y1, y2])

    def is_ball_biggest(self):   #Might be better to avoid masking once again if I do mask beforehand.
        %

        l_green = np.array([130, 30, 100])
        u_green = np.array([125, 255, 200])
        green_mask = cv2.inRange(self.hsv, l_green, u_green)

        #Should return location or mask with biggest blob.

    def getArea(self):    #Might be useless. Better to add in isBallBiggest




    def getImage(self):

        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)

        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        depth_image_array = np.asanyarray(aligned_depth_frame.get_data())
        frame_array = np.asanyarray(color_frame.get_data())

        self.hsv = cv2.cvtColor(frame_array, cv2.COLOR_BGR2HSV)     #Maybe not ideal as will have to update each usage and can forget to update.

    def getDepth(self, x, y, w, h):
        depth_sensor = self.profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()

    def maskImage(self, array):
        m_color_frame = self.hsv.copy()




        dist = np.average(depth_image[y:y + w, x:x + h]) * depth_scale
