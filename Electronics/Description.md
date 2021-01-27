# Description of LeBot MainBoard
Lebot MainBoard consists of two separate parts, the logic part, which consists of STM32G4 microcontroller and the motor control part which consists of motor driversand manages the current path to the motors attached to LeBot. Both the MCU part and the motor control part are electrically isolated from each other with digital isolators. These isolators carry PWM signals for the motor drivers. Microcontroller receives strings of data from the on-board PC, and converts these strings into corresponding signals for three wheel motors and one thrower motor. 

## Logic Part 

MCU firmware is available in ![here](https://github.com/rokspy/LeBot/blob/master/Electronics/STM32/LeBot_main/Core/Src/main.c) 

Schematics for the LeBot MainBoard is in ![here](https://github.com/rokspy/LeBot/blob/master/Electronics/LeBot.pdf)

There are three four connectors on the logic part of the MainBoard, three meant for wheel motor encoders and one other for the MCU debugger connection.
Three encoders have the same pinouit and have silk text that indicates for which motor it is meant. 

Encoder connectors J1(WheelMot1, WheelMot2, WheelMot3)
Pin1. - GND
Pin2. - 3V3
Pin3. - ENCA
Pin4. - ENCB

It is possible to upload code and debug the STM with SWD interface through the JP1 connector
Pin1. - 3V3
Pin2. - SWDIO
Pin3. - GND
Pin4. - SWCLK
Pin5. - GND
Pin6. - SWO
Pin7. - NoConnection
Pin8. - NoConnection
Pin9. - GND
Pin10. - RESET

