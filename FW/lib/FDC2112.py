#!/usr/bin/env python
#
# These are drivers for sensor TMP275 written by:
# - Repex97
# ...
#

import time
from machine import I2C

__version__ = '0.0.1'

class FDC2112:
    """ Class to handle FDC2112
        2-Ch, 12-bit, capacitance to digital converter
        Datasheet: https://www.ti.com/lit/gpn/fdc2112 """
    
    FDC2112_I2C_ADDR = const(0x2A)

    # Register addresses
    DATA_CH0_REG = const(0x00)
    DATA_CH0_LSB_REG = const(0x01)
    RCOUNT_CH0_REG = const(0x08)
    OFFSET_CH0_REG = const(0x0C)
    SETTLECOUNT_CH0_REG = const(0x10)
    CLOCK_DIVIDERS_CH0_REG = const(0x14)
    STATUS_REG = const(0x18)
    STATUS_CONFIG_REG = const(0x19)
    CONFIG_REG = const(0x1A)
    MUX_CONFIG_REG = const(0x1B)
    RESET_DEV_REG = const(0x1C)
    DRIVE_CURRENT_CH0_REG = const(0x1E)
    MANIFACTURER_ID_REG = const(0x7E)
    DEVICE_ID_REG = const(0x7F)
    
    # Register masks
    
    
    def __init__(self, sda = 'P22', scl = 'P21'):     
        self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl), baudrate=200000)
        # Set baudrate at 20kbauds
        # self.i2c.init(baudrate=20000)
        # Check device
        self.resetDev()
        self.printIds()

    def resetDev(self):
        status_reg = self.readReg(self.RESET_DEV_REG)
        status_reg |= 0x80 # Set reset pin high
        return self.i2c.writeReg(self.RESET_DEV_REG, status_reg)

    def printIds(self):
        print("Manifacturer ID: {:X}".format(self.readReg(self.MANIFACTURER_ID_REG)))
        print("Device ID: {:X}".format(self.readReg(self.DEVICE_ID_REG)))
        
    def readReg(self, addr):
        return int.from_bytes((self.i2c.readfrom_mem(self.FDC2112_I2C_ADDR, addr, 1)),"big")

    def writeReg(self, addr, byte):
        return self.i2c.writeto_mem(self.FDC2112_I2C_ADDR, addr, bytes(byte))