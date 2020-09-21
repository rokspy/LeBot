import numpy as np
import cv2
import pyrealsense2 as rs


class ImageProcessing():

    def __init__(self):
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

    def findBasket(self, color):  # Find way way to pass color basket.

        # if color == "blue":
        if True:
            l_blue = np.array([100, 230, 100])
            u_blue = np.array([125, 255, 200])
            blue_mask = cv2.inRange(self.hsv, l_blue, u_blue)  # Need erosion and dilution filter to reduce noise?

            # Chain_approx only uses 4 points
            # Retr_external gets outermost; need very strict first mask?
            b_basket_contours = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # [] check for proper hierarchy
            if len(b_basket_contours) == 4:
                c = max(b_basket_contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)
            else:
                print('Need more points')
                x, y, w, h = None, None, None, None

        # Do same for other basket.


        return (x, y, w, h)


    def getImage(self):

        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)

        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        depth_image_array = np.asanyarray(aligned_depth_frame.get_data())
        frame_array = np.asanyarray(color_frame.get_data())

        self.hsv = cv2.cvtColor(frame_array, cv2.COLOR_BGR2HSV)     #Maybe not ideal as will have to update each usage and can forget to update.

    def getDepth(self):
        depth_sensor = self.profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()

        # Missing
        
        dist = np.average(depth_image[y:y + w, x:x + h]) * depth_scale
