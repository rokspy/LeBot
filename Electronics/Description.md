# Description of LeBot MainBoard
Lebot MainBoard consists of two separate parts, the logic part, which consists of STM32G4 microcontroller and the motor control part which consists of motor driversand manages the current path to the motors attached to LeBot. Both the MCU part and the motor control part are electrically isolated from each other with digital isolators. These isolators carry PWM signals for the motor drivers. Microcontroller receives strings of data from the on-board PC, and converts these strings into corresponding signals for three wheel motors and one thrower motor. 

