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
    
    # Register modes
    ACTIVE_CHAN_CH0_MODE = const(0b00)

    # Register offsets
    ACTIVE_CHAN_OFFSET = const(0xE)
    CHX_FREF_DIVIDER_OFFSET = const(0x0)
    CHX_FIN_DIVIDER_OFFSET = const(0xC)
    DEGLITCH_OFFSET = const(0x0)

    # Register masks
    DATA_MSB_MASK = const(0x0FFF)
    RESET_DEV_PIN_bp = const(0x8000)
    HIGH_CURRENT_DRV_bp = const(0x0040)
    ACTIVE_CHAN_MASK = const(0xC000)
    CHX_FREF_DIVIDER_MASK = const(0x03FF)
    CHX_FIN_DIVIDER_MASK = const(0x3000)
    DEGLITCH_MASK = const(0x7)
    SLEEP_MODE_EN_bp = const(0x2000)
    
    def __init__(self, sda = 'P22', scl = 'P21'):     
        self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl), baudrate=200000)
        # Set baudrate at 20kbauds
        # self.i2c.init(baudrate=20000)
        # Check device
        self.resetDev()
        self.printIds()
        # Set right frequencies prescalers
        self.setFRef(2, 0)
        self.setFIn(3, 0)
        # Set analog multiplexer on CH0
        self.setMux(self.ACTIVE_CHAN_CH0_MODE)
        # Set settlecount to 128
        self.setSettleCount(128, 0)
        # Set rcount to 256
        self.setRCount(256, 0)
        # Set high current mode
        self.setHighCurrentMode(True)
        # Set deglitch filter
        self.setDeglitchFilter(0b111)

    def readRawData(self):
        self.setSleepMode(False)
        time.sleep(0.010)
        data=bytearray([self.readReg(self.DATA_CH0_REG)&(self.DATA_MSB_MASK)])
        data.append(self.readReg(self.DATA_CH0_LSB_REG))
        self.setSleepMode(True)
        return data

    def resetDev(self):
        reset_dev_reg = self.readReg(self.RESET_DEV_REG)
        reset_dev_reg |= self.RESET_DEV_PIN_bp # Set reset pin high
        return self.writeReg(self.RESET_DEV_REG, reset_dev_reg)

    def printIds(self):
        print("\nFDC2112:")
        print("\tManifacturer ID: 0x{:X}".format(self.readReg(self.MANIFACTURER_ID_REG)))
        print("\tDevice ID: 0x{:X}\n".format(self.readReg(self.DEVICE_ID_REG)))

    def setFRef(self, fref, channel):
        address = self.CLOCK_DIVIDERS_CH0_REG+(channel&0x3)
        clock_dividers_reg = self.readReg(address)
        clock_dividers_reg = (clock_dividers_reg&(~self.CHX_FREF_DIVIDER_MASK)) | ((fref << self.CHX_FREF_DIVIDER_OFFSET)&(self.CHX_FREF_DIVIDER_MASK))
        return self.writeReg(address, clock_dividers_reg)

    def setFIn(self, fin, channel):
        address = self.CLOCK_DIVIDERS_CH0_REG+(channel&0x3)
        clock_dividers_reg = self.readReg(address)
        clock_dividers_reg = (clock_dividers_reg&(~self.CHX_FIN_DIVIDER_MASK)) | ((fin << self.CHX_FIN_DIVIDER_OFFSET)&(self.CHX_FIN_DIVIDER_MASK))
        return self.writeReg(address, clock_dividers_reg)

    def setMux(self, mode):
        config_reg = self.readReg(self.CONFIG_REG)
        config_reg = (config_reg&(~self.ACTIVE_CHAN_MASK)) | ((mode << self.ACTIVE_CHAN_OFFSET)&(self.ACTIVE_CHAN_MASK))  
        return self.writeReg(self.CONFIG_REG, config_reg)

    def setHighCurrentMode(self, bit):
        config_reg = self.readReg(self.CONFIG_REG)
        config_reg = (config_reg&(~self.HIGH_CURRENT_DRV_bp)) | (bit*self.HIGH_CURRENT_DRV_bp)

    def setSettleCount(self, count, channel):
        address = self.SETTLECOUNT_CH0_REG+(channel&0x3)
        return self.writeReg(address, count&0xFFFF)

    def setRCount(self, count, channel):
        address = self.RCOUNT_CH0_REG+(channel&0x3)
        return self.writeReg(address, count&0xFFFF)

    def setDeglitchFilter(self, value):
        mux_config = self.readReg(self.MUX_CONFIG_REG)
        mux_config = (mux_config&(~self.DEGLITCH_MASK)) | ((value<<self.DEGLITCH_OFFSET)&(self.DEGLITCH_MASK))
        return self.writeReg(self.MUX_CONFIG_REG, mux_config)

    def setSleepMode(self, bit):
        config_reg = self.readReg(self.CONFIG_REG)
        config_reg = (config_reg&(~self.SLEEP_MODE_EN_bp)) | (bit*self.SLEEP_MODE_EN_bp)
        return self.writeReg(self.CONFIG_REG, config_reg)

    
    # Basic IO members

    def readReg(self, addr):
        return int.from_bytes((self.i2c.readfrom_mem(self.FDC2112_I2C_ADDR, addr, 2)),"big")

    def readRegBytes(self, addr, n_bytes):
        return int.from_bytes((self.i2c.readfrom_mem(self.FDC2112_I2C_ADDR, addr, n_bytes)),"big")

    def writeReg(self, addr, value):
        return self.i2c.writeto_mem(self.FDC2112_I2C_ADDR, addr, int.to_bytes(value, 2, "big"))