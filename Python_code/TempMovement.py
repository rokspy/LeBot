import serial
from time import sleep


class MainBoardMovement:
    def __init__(self):
        self.ser = serial.Serial("/dev/xxxx", timeout=0.03, baudrate=115200)
        self.wheels = [0, 0, 0]

    def update_wheel_speed(self, w1, w2, w3):
        self.wheels = [w1, w2, w3]

    def wheel_speed_zero(self):
        self.wheels = [0, 0, 0]

    def ser_stop(self):
        self.ser.close()

    def ser_write_wheel(self):
        sot = ("sd:{0}:{1}:{2}\n".format(str(self.wheels[0]), str(self.wheels[1]), str(self.wheels[2])))
        self.ser.write(sot.encode('utf-8'))
        print("Output text ---> ")
        print(sot)

    def sleep(self, t):
        sleep(t)

    # Movement functions
    def move_forward(self, t):
        self.update_wheel_speed(10, -10, 0)
        self.ser_write_wheel()
        self.sleep(t)
        self.wheel_speed_zero()
        self.ser_write_wheel()

    def move_backward(self, t):
        self.update_wheel_speed(-10, 10, 0)
        self.ser_write_wheel()
        self.sleep(t)
        self.wheel_speed_zero()
        self.ser_write_wheel()

    def rotate_left(self, t):
        self.update_wheel_speed(10, 0, 0)
        self.ser_write_wheel()
        self.sleep(t)
        self.wheel_speed_zero()
        self.ser_write_wheel()

    def rotate_right(self, t):
        self.update_wheel_speed(0, 10, 0)
        self.ser_write_wheel()
        self.sleep(t)
        self.wheel_speed_zero()
        self.ser_write_wheel()


# Debugging Section.
LeBot = MainBoardMovement()

# Manual movement
LeBot.update_wheel_speed(20, -20, 0)
LeBot.ser_write_wheel()
LeBot.sleep(0.3)
LeBot.wheel_speed_zero()
LeBot.ser_write_wheel()

# Semi automatic movement
LeBot.move_forward(1)
LeBot.move_backward(1)
LeBot.rotate_right(1)
LeBot.rotate_left(1)
