# Missing:
# - Mask of basket.
# - Exit cue :p (most probably need to modify while loop)
# - Terminate camera capture. Must disconnect on every debugging try ...


import pyrealsense2 as rs
import numpy as np
import time
import cv2

width = 1280
height = 720

pc = rs.pointcloud()
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, 30)

profile = pipeline.start(config)

align_to = rs.stream.color
align = rs.align(align_to)

while True:

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)


    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
    color_frame = aligned_frames.get_color_frame()

    try:
        vertex_array = np.asanyarray(pc.calculate(aligned_depth_frame).get_vertices())
    except Exception as e:
        count += 1
        print("Failed to get vertexes for {} frames".format(count))

        align_to = rs.stream.color
        align = rs.align(align_to)
        frames = pipeline.wait_for_frames()
        continue

    count = 0

    # Validate that both frames are valid
    if not aligned_depth_frame or not color_frame:
        continue

    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    pc.map_to(color_frame)

    x = 680
    y = 350
    w = 30
    h = 4

    cv2.rectangle(color_image, (x, y), (x + w, y + h), (255, 255, 0), 1)

    vertex_map = []

    vertex_map = np.array(vertex_array).reshape(height, width)

    dist = np.average(depth_image[y:y + w, x:x + h]) * depth_scale

    time.sleep(2)   # For ease on debugging. Can be much lower.
    print("Dist: ", dist)
