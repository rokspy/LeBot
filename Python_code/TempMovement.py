import serial
from time import sleep
import re
from math import atan2, sqrt, cos


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
        self.set_wheel_speed(t, -t, -t)
        self.ser_write_wheel()

    def rotate_right(self, t):
        self.set_wheel_speed(-t, t, t)
        self.ser_write_wheel()

    def send_string(self, text):
        sot = "rf:{0}\n".format(str(text))
        self.ser.write(sot.encode('utf-8'))

    def send_omni(self):
        sot = ("sd:{0}:{1}:{2}\n".format(str(self.wheelLinearVelocity[0]), str(self.wheelLinearVelocity[1]), 
                                         str(self.wheelLinearVelocity[2])))
        self.ser.write(sot.encode('utf-8'))

    def calculate_omni(self, robotSpeedX, robotSpeedY):
        try:
            robotDirectionAngle = atan2(robotSpeedY, robotSpeedX)
        except:
            robotDirectionAngle = 0.01

        robotSpeed = sqrt(robotSpeedX * robotSpeedX + robotSpeedY * robotSpeedY)
        wheelLinearVelocity = [None, None, None]

        for i in range(3):
            self.wheelLinearVelocity[i] = robotSpeed * cos(robotDirectionAngle - self.wheelAngle[i]) \
                                     + self.wheelDistanceFromCenter * self.robotAngularVelocity

            self.wheelAngularSpeedMainboardUnits[i] = wheelLinearVelocity[i] * self.wheelSpeedToMainboardUnits
