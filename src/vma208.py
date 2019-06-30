# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MMA8452Q
# This code is designed to work with the MMA8452Q_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=MMA8452Q_I2CS#tabs-0-product_tabset-2

import random
try:
    import smbus
    smbusImported = True
except ImportError:
    print("SMBus.GPIO not installed")
    smbusImported = False
import time
from logging import getLogger

def initBus():

    # Get I2C bus
    bus = smbus.SMBus(1)

    # MMA8452Q address, 0x1C(28)
    # Select Control register, 0x2A(42)
    #               0x00(00)        StandBy mode
    bus.write_byte_data(0x1D, 0x2A, 0x00)
    # MMA8452Q address, 0x1C(28)
    # Select Control register, 0x2A(42)
    #               0x01(01)        Active mode
    bus.write_byte_data(0x1D, 0x2A, 0x01)
    # MMA8452Q address, 0x1C(28)
    # Select Configuration register, 0x0E(14)
    #               0x00(00)        Set range to +/- 2g
    bus.write_byte_data(0x1D, 0x0E, 0x00)

def getDataFromBus(bus):

    # Read data back from 0x00(0), 7 bytes
    # Status register, X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
    data = bus.read_i2c_block_data(0x1D, 0x00, 7)

    # Convert the data
    xAccl = (data[1] * 256 + data[2]) / 16

    yAccl = (data[3] * 256 + data[4]) / 16

    zAccl = (data[5] * 256 + data[6]) / 16

    return xAccl, yAccl, zAccl

def logDrivingData(filename):

    if not smbusImported:
        print("SMBUS not installed, therefor i")
        return

    logger = getLogger()
    logger.info("Init vma208 sensor")

    bus = initBus()

    with open(filename, "w") as f:
        logger.info("Start logging to the vma208 sensor")
        while True:
            try:

                time.sleep(0.1)

                xAccl, yAccl, zAccl = getDataFromBus(bus)

                # Output data to screen
                logger.debug("Acceleration in X-Axis : %d" %xAccl)
                logger.debug("Acceleration in Y-Axis : %d" %yAccl)
                logger.debug("Acceleration in Z-Axis : %d" %zAccl)

                f.write(str(xAccl)+";"+str(yAccl)+";"+str(zAccl)+"\n")
            except Exception:
                break
        f.close()
