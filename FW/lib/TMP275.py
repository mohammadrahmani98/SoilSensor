#!/usr/bin/env python
#
# These are drivers for sensor TMP275 written by:
# - Repex97
# ...
#

import time
from machine import I2C

__version__ = '0.0.1'

class TMP275:
    """ Class to handle the temperature sensor TMP275
        +/- 0.5°C from -20°C to 100°C
        Datasheet: https://www.ti.com/lit/ds/symlink/tmp275.pdf?ts=1653874616684 """
    
    TMP275_I2C_ADDR = const(0x48)

    # Register addresses
    TEMP_REG    = const(0x0) # 16-bits data register
    CONF_REG    = const(0x1) # 8-bits conf-register
    T_LOW_REG   = const(0x2) # 8-bits low boundary trigger for alert pin
    T_HIGH_REG  = const(0x3) # 8-bits high boundary trigger for alert pin

    # Register masks
    SD_MODE     = const(0b00000001) # Turns off internal circuitry, when '0' continous running mode
    TM_MODE     = const(0b00000010) # Turns on thermostat mode
    POL_MODE    = const(0b00000100) # Set polarity of ALERT pin
    FQ_MASK     = const(0b00011000) # Set number of faults to catch the fault over the trigger
    FQ_OFFSET   = const(0x3)
    CRES_MASK   = const(0b01100000) # Set resolution of the conversion
    CRES_OFFSET = const(0x5)
    OS_MODE     = const(0b10000000) # Set One-Shot mode

    def __init__(self, pysense = None, sda = 'P22', scl = 'P21'):
        if pysense is not None:
            self.i2c = pysense.i2c
        else:
            self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl))
        # Set baudrate at 20kbauds
        self.i2c.init(baudrate=20000)
        # Set resolution at 12 bits
        self.setResolution(12)
        # Set shutdown mode
        self.setShutdownMode()


    def __getTempData(self, high, low):
        return ((high<<4) + (low>>4))

    def temp(self):
        """ Obtaining the temperatrue by the sensor """
        self.setOneShotMode()
        time.sleep(0.3)
        data = self.readTempReg()
        # Shift by 4 position to the left
        data = self.__getTempData(data[0], data[1])
        self.temperature = data
        return data

    def setResolution(self, res = 12):
        """ Setting resolution of the sensor """
        conf_reg = self.readConfReg() # register pointer still points to conf reg
        if res == 9:
            conf_reg &= ~(self.CRES_MASK)   # Clears the right position
            conf_reg |= 0b00 << self.CRES_OFFSET    # 27.5ms
        if res == 10:
            conf_reg &= ~(self.CRES_MASK)   # Clears the right position
            conf_reg |= 0b01 << self.CRES_OFFSET    # 55ms
        if res == 11:
            conf_reg &= ~(self.CRES_MASK)   # Clears the right position
            conf_reg |= 0b10 << self.CRES_OFFSET    # 110ms
        if res == 12:
            conf_reg &= ~(self.CRES_MASK)   # Clears the right position
            conf_reg |= 0b11 << self.CRES_OFFSET    # 220ms
        self.i2c.writeto(self.TMP275_I2C_ADDR, bytearray([conf_reg]))

    def setShutdownMode(self):
        " Setting shutdown mode "
        conf_reg = self.readConfReg()
        conf_reg |= self.SD_MODE
        self.i2c.writeto(self.TMP275_I2C_ADDR, bytearray([conf_reg])) 

    def setOneShotMode(self):
        """ Setting one-shot mode """
        conf_reg = self.readConfReg()
        conf_reg |= self.OS_MODE
        self.i2c.writeto(self.TMP275_I2C_ADDR, bytearray([conf_reg]))

    def readTempReg(self):
        # Set register pointer to ConfReg
        self.i2c.writeto(self.TMP275_I2C_ADDR, bytearray([self.TEMP_REG]))
        return self.i2c.readfrom(self.TMP275_I2C_ADDR, 2)

    def readConfReg(self):
        # Set register pointer to ConfReg
        self.i2c.writeto(self.TMP275_I2C_ADDR, bytearray([self.CONF_REG]))
        return self.i2c.readfrom(self.TMP275_I2C_ADDR, 1)

