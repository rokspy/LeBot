# Description of LeBot MainBoard
Lebot MainBoard consists of two separate parts, the logic part, which consists of STM32G4 microcontroller and the motor control part which consists of motor driversand manages the current path to the motors attached to LeBot. Both the MCU part and the motor control part are electrically isolated from each other with digital isolators. These isolators carry PWM signals for the motor drivers. Microcontroller receives strings of data from the on-board PC, and converts these strings into corresponding signals for three wheel motors and one thrower motor.

Schematics for the LeBot MainBoard is in ![here](https://github.com/rokspy/LeBot/blob/master/Electronics/LeBot.pdf)

## Logic Part 
Logic part is powered by the incoming 5V over the USB, and is converted to 3.3V via a low-dropout regulator.
\
MCU firmware is available in ![here](https://github.com/rokspy/LeBot/blob/master/Electronics/STM32/LeBot_main/Core/Src/main.c) 
\
MCU recognises two types of strings coming from the on-board PC over USB.

One message is in form     s<x:y:z>    , where x,y,z and are numbers from -100 to 100 and sets the PWM pulse width for the motor driver. The string controls WheelMotor1, WheelMotor2, and WheelMotor3 respectively.

Other message form is  t<x>   , where x is number from 0 to 100 and corresponds to the thrower throttle value. 

There are three four connectors on the logic part of the MainBoard, three meant for wheel motor encoders and one other for the MCU debugger connection.
Three encoders have the same pinouit and have silk text that indicates for which motor it is meant. 

Encoder connectors J1(WheelMot1, WheelMot2, WheelMot3)\
Pin1. - GND\
Pin2. - 3V3\
Pin3. - ENCA\
Pin4. - ENCB

It is possible to upload code and debug the STM with SWD interface through the JP1 connector\
Pin1. - 3V3\
Pin2. - SWDIO\
Pin3. - GND\
Pin4. - SWCLK\
Pin5. - GND\
Pin6. - SWO\
Pin7. - NoConnection\
Pin8. - NoConnection\
Pin9. - GND\
Pin10. - RESET

## Motor Control Part

Motor Control part receives its power from the batteries.

Motor Control Part consists of three motor driver ICs, 5V switching regulator, and connectors for the thrower motor and servo motor(not implemented in the design). Motor drivers receive pwm signal from the MCU through the isolator, and then controls the corresponding wheel motor with this PWM.\
The switching regulator supplies the logic supply voltage for the motor drivers, and it was also meant for 5V supply for the servo motor, which was not implemented.\

The pinout for the Servo Motor connector (JP3):\
Pin1. - Serv_PWM_B\
Pin2. - 5V_B\
Pin3. - GND_B

The pinout for the Thrower Motor connector (JP2):\
Pin1. - THRW_PWM_B\
Pin2. - GND_B


