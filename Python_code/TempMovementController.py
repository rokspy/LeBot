import serial
from time import sleep
import re
from math import atan2, sqrt, cos
import getch
import cv2
from pyPS4Controller.controller import Controller


# "/dev/cu.usbmodem01234567891"
# "/dev/ttyACM0"


class MainBoardMovement:
    def __init__(self):  # Initiate connection
        self.ser = serial.Serial("/dev/ttyACM0", timeout=0.03, baudrate=115200,
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        self.wheels = [0, 0, 0]

        # Omnidirectional Movement
        self.wheelSpeedToMainboardUnits = None  # Must calculate from gearboxReductionRatio * encoderEdgesPerMotorRevolution / (2 * PI * wheelRadius * pidControlFrequency)
        self.wheelAngle = [0, 120, 240]
        self.robotSpeed = 0
        self.wheelDistanceFromCenter = None
        self.robotAngularVelocity = None
        self.wheelLinearVelocity = [None, None, None]
        self.wheelAngularSpeedMainboardUnits = [None, None, None]

    def set_wheel_speed(self, w1, w2, w3):  # Does not send command.    Has range of -250 and 250
        self.wheels = [w1, w2, w3]

    def wheel_speed_zero(self):  # Does not send command
        self.wheels = [0, 0, 0]

    def ser_stop(self):
        self.ser.close()

    def ser_write_wheel(self):  # This does send the command.
        sot = ("sd:{0}:{1}:{2}\n".format(str(self.wheels[0]), str(self.wheels[1]), str(self.wheels[2])))
        self.ser.write(sot.encode('utf-8'))
        print("Output text ---> ")
        print(sot)

    def sleep(self, t):  # Will need to change this once we start threading.
        sleep(t)

    def get_current_speed(self):
        sot = "gs\n"
        current_speed = self.ser.write(sot.encode('utf-8'))
        values = re.findall(r"\d+?", current_speed)
        self.wheels[0], self.wheels[0], self.wheels[0], = int(values[0]), int(values[1]), int(values[2])

    def set_thrower_speed(self, speed):  # Between 1000 and 2000
        sot = "d:{0}\n".format(str(speed))
        self.ser.write(sot.encode('utf-8'))

    def set_thrower_position(self, pos):
        sot = "sv:{0}\n".format(str(pos))
        self.ser.write(sot.encode('utf-8'))

    # Movement functions
    def move_forward(self, t):
        self.set_wheel_speed(t, -t, 0)
        self.ser_write_wheel()

    def move_backward(self, t):
        self.set_wheel_speed(-t, t, 0)
        self.ser_write_wheel()

    def rotate_left(self, t):
        self.set_wheel_speed(-t, -t, -t)
        self.ser_write_wheel()

    def rotate_right(self, t):
        self.set_wheel_speed(t, t, t)
        self.ser_write_wheel()

    def move_wheel_0(self, t):
        self.set_wheel_speed(t, 0, 0)
        self.ser_write_wheel()

    def move_wheel_1(self, t):
        self.set_wheel_speed(0, t, 0)
        self.ser_write_wheel()

    def move_wheel_2(self, t):
        self.set_wheel_speed(0, 0, t)
        self.ser_write_wheel()

    def send_string(self, text):
        sot = "rf:{0}\n".format(str(text))
        self.ser.write(sot.encode('utf-8'))

    def ser_write_omni(self):
        sot = ("sd:{0}:{1}:{2}\n".format(str(self.wheelLinearVelocity[0]), str(self.wheelLinearVelocity[1]),
                                         str(self.wheelLinearVelocity[2])))
        self.ser.write(sot.encode('utf-8'))

    def calculate_omni(self, robotSpeedX, robotSpeedY):
        try:
            robotDirectionAngle = atan2(robotSpeedY, robotSpeedX)
        except:
            robotDirectionAngle = 0.01

        robotSpeed = sqrt(robotSpeedX * robotSpeedX + robotSpeedY * robotSpeedY)

        for i in range(3):
            self.wheelLinearVelocity[i] = robotSpeed * cos(robotDirectionAngle - self.wheelAngle[i]) \
                                          + self.wheelDistanceFromCenter * self.robotAngularVelocity

            self.wheelAngularSpeedMainboardUnits[i] = self.wheelLinearVelocity[i] * self.wheelSpeedToMainboardUnits

    def pycharm_keyboard_input(self):
        char = '1'
        spd = 10
        while char != 'q':
            char = getch.getch()
            if char == 'w':
                self.move_forward(20)
            elif char == 's':
                self.move_backward(20)
            elif char == 'd':
                self.rotate_right(20)
            elif char == 'a':
                self.rotate_left(20)
            elif char == 'z':  # Motor 0
                self.move_wheel_0(20)
            elif char == 'x':  # Motor 1
                self.move_wheel_1(20)
            elif char == 'c':  # Motor 2
                self.move_wheel_2(20)

    def cv2_keyboard_input(self):
        cv2.namedWindow("Movement")
        spd = 10
        while True:
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(0) & 0xFF == ord('a'):
                self.rotate_left(spd)
            elif cv2.waitKey(0) & 0xFF == ord('d'):
                self.rotate_right(spd)
            elif cv2.waitKey(0) & 0xFF == ord('w'):
                self.move_forward(spd)
            elif cv2.waitKey(0) & 0xFF == ord('s'):
                self.move_backward(spd)
            elif cv2.waitKey(0) & 0xFF == ord('z'):
                self.move_wheel_0(spd)
            elif cv2.waitKey(0) & 0xFF == ord('x'):
                self.move_wheel_1(spd)
            elif cv2.waitKey(0) & 0xFF == ord('c'):
                self.move_wheel_2(spd)


class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.speed = 20

    def on_x_press(self):
        self.speed = self.speed - 5

    def on_square_press(self):
        self.speed = self.speed + 5

    def on_up_arrow_press(self):
        LeBot.move_forward(self.speed)

    def on_down_arrow_press(self):
        LeBot.move_backward(self.speed)

    def on_left_arrow_press(self):
        LeBot.rotate_left(self.speed)

    def on_right_arrow_press(self):
        LeBot.rotate_right(self.speed)

    def on_options_press(self):
        exit()



LeBot = MainBoardMovement()

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen(timeout=10)
# LeBot.cv2_keyboard_input()
# LeBot.pycharm_keyboard_input()
