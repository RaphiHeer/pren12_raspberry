import RPi.GPIO as GPIO

class ArduinoConnector:
    # Number PINS
    GPIO_NUMBER_0 = 0
    GPIO_NUMBER_1 = 20
    GPIO_NUMBER_2 = 21
    GPIO_NUMBER_3 = 26
    GPIO_NUMBER_4 = 0
    GPIO_NUMBER_5 = 0
    GPIO_NUMBER_6 = 0
    GPIO_NUMBER_7 = 0
    GPIO_NUMBER_8 = 0
    GPIO_NUMBER_9 = 0

    GPIO_START_DETECTED = 19
    GPIO_STOP_DETECTED = 13

    # Init Pins
    GPIO_PI_INI_DONE = 12
    GPIO_CAM_READY = 16
    GPIO_ARDUINO_INIT_DONE = 18

    # Train state
    GPIO_CUBE_STORED = 23
    GPIO_TRAIN_STOPPED = 24

    # Communication Pins
    GPIO_UART_TXD = 14
    GPIO_UART_RXT = 15

    def __init__(self):
        GPIO.setMode(GPIO.BCM)

        GPIO.setup(self.GPIO_NUMBER_1, GPIO.OUT)
        GPIO.setup(self.GPIO_NUMBER_2, GPIO.OUT)
        GPIO.setup(self.GPIO_NUMBER_3, GPIO.OUT)
        GPIO.setup(self.GPIO_NUMBER_4, GPIO.OUT)
        GPIO.setup(self.GPIO_START_DETECTED, GPIO.OUT)
        GPIO.setup(self.GPIO_STOP_DETECTED, GPIO.OUT)
        GPIO.setup(self.GPIO_PI_INI_DONE, GPIO.OUT)
        GPIO.setup(self.GPIO_CAM_READY, GPIO.OUT)
        GPIO.setup(self.GPIO_ARDUINO_INIT_DONE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.GPIO_CUBE_STORED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.GPIO_TRAIN_STOPPED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.GPIO_UART_TXD, GPIO.OUT)
        GPIO.setup(self.GPIO_UART_RXT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def numberDetected(self, number):
        self.resetNumberPins()

        if(number == 1):
            GPIO.output(self.GPIO_NUMBER_1, True)
        elif(number == 2):
            GPIO.output(self.GPIO_NUMBER_2, True)
        elif(number == 3):
            GPIO.output(self.GPIO_NUMBER_3, True)

    def resetNumberPins(self):
        GPIO.output(self.GPIO_NUMBER_1, False)
        GPIO.output(self.GPIO_NUMBER_2, False)
        GPIO.output(self.GPIO_NUMBER_3, False)
