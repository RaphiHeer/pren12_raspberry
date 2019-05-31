try:
    import RPi.GPIO as GPIO
    GPIOsImported = True
except ImportError:
    print("RPi.GPIO not installed")
    GPIOsImported = False

from multiprocessing import Lock

class ArduinoConnector:

    def __init__(self):
        if GPIOsImported:
            self.setGPIOPins()
            self.initGPIOPins()

        self.sendLock = Lock()

    def setGPIOPins(self):
        # Number PINS
        self.GPIO_SIGN_INTERRUPT = 20

        self.GPIO_IS_INFO_SIGN = 21

        self.GPIO_NUMBER_BIT_0 = 26
        self.GPIO_NUMBER_BIT_1 = 19
        self.GPIO_NUMBER_BIT_2 = 13
        self.GPIO_NUMBER_BIT_3 = 6

        # Init Pins
        self.GPIO_PI_INI_DONE = 12
        self.GPIO_CAM_READY = 16
        self.GPIO_ARDUINO_INIT_DONE = 18

        # Train state
        self.GPIO_CUBE_STORED = 23
        self.GPIO_TRAIN_STOPPED = 24

        # Communication Pins
        self.GPIO_UART_TXD = 14
        self.GPIO_UART_RXT = 15

    def initGPIOPins(self):
        GPIO.setMode(GPIO.BCM)

        GPIO.setup(self.GPIO_NUMBER_BIT_0, GPIO.OUT)
        GPIO.setup(self.GPIO_NUMBER_BIT_1, GPIO.OUT)
        GPIO.setup(self.GPIO_NUMBER_BIT_2, GPIO.OUT)
        GPIO.setup(self.GPIO_NUMBER_BIT_3, GPIO.OUT)
        GPIO.setup(self.GPIO_IS_INFO_SIGN, GPIO.OUT)
        GPIO.setup(self.GPIO_SIGN_INTERRUPT, GPIO.OUT)
        GPIO.setup(self.GPIO_PI_INI_DONE, GPIO.OUT)
        GPIO.setup(self.GPIO_CAM_READY, GPIO.OUT)
        GPIO.setup(self.GPIO_ARDUINO_INIT_DONE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.GPIO_CUBE_STORED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.GPIO_TRAIN_STOPPED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.GPIO_UART_TXD, GPIO.OUT)
        GPIO.setup(self.GPIO_UART_RXT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def numberDetected(self, number, isInfoSign):

        if GPIOsImported is not True:
            print("No signal sended since GPIO library is not imported")
            return

        self.sendLock.acquire()

        self.resetNumberPins()

        # Calculate bits
        bit0 = (number % 2) == 1
        number /= 2
        bit1 = (number % 2) == 1
        number /= 2
        bit2 = (number % 4) == 1
        number /= 2
        bit3 = (number % 8) == 1

        print("Sending following bit combination: %d%d%d%d - Is Info Sign: %d" % (bit3, bit2, bit1, bit0, isInfoSign))

        # Send interrupt
        GPIO.output(self.GPIO_NUMBER_BIT_0, bit0)
        GPIO.output(self.GPIO_NUMBER_BIT_1, bit1)
        GPIO.output(self.GPIO_NUMBER_BIT_2, bit2)
        GPIO.output(self.GPIO_NUMBER_BIT_3, bit3)
        GPIO.output(self.GPIO_IS_INFO_SIGN, isInfoSign)
        GPIO.output(self.GPIO_SIGN_INTERRUPT, True)

        self.sendLock.release()

    def resetNumberPins(self):
        GPIO.output(self.GPIO_NUMBER_BIT_0, False)
        GPIO.output(self.GPIO_NUMBER_BIT_1, False)
        GPIO.output(self.GPIO_NUMBER_BIT_2, False)
        GPIO.output(self.GPIO_NUMBER_BIT_3, False)
        GPIO.output(self.GPIO_IS_INFO_SIGN, False)
        GPIO.output(self.GPIO_SIGN_INTERRUPT, False)
