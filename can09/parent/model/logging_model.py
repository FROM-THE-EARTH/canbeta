
import time

from pisat.calc import press2alti
from pisat.model import (
    cached_loggable, LinkedDataModelBase, linked_loggable, loggable
)
from pisat.sensor import (
    Bme280, Bno055, SamM8Q
)

import can09.parent.setting as setting


class LoggingModel(LinkedDataModelBase):
    press = linked_loggable(Bme280.DataModel.press, setting.NAME_BME280)
    temp = linked_loggable(Bme280.DataModel.temp, setting.NAME_BME280)
    acc = linked_loggable(Bno055.DataModel.acc_lin, setting.NAME_BNO055, logging=False)
    gravity = linked_loggable(Bno055.DataModel.acc_gra, setting.NAME_BNO055, logging=False)
    euler = linked_loggable(Bno055.DataModel.euler, setting.NAME_BNO055, logging=False)
    altitude_gps = linked_loggable(SamM8Q.DataModel.altitude, setting.NAME_GPS)
    longitude = linked_loggable(SamM8Q.DataModel.longitude, setting.NAME_GPS)
    latitude = linked_loggable(SamM8Q.DataModel.latitude, setting.NAME_GPS)
    
    @cached_loggable
    def altitude(self):
        return press2alti(self.press, self.temp)
    
    @loggable
    def acc_x(self):
        return self.acc[0]
    
    @loggable
    def acc_y(self):
        return self.acc[1]
    
    @loggable
    def acc_z(self):
        return self.acc[2]
    
    @loggable
    def gra_x(self):
        return self.gravity[0]
    
    @loggable
    def gra_y(self):
        return self.gravity[1]
    
    @loggable
    def gra_z(self):
        return self.gravity[2]
    
    @loggable
    def heading(self):
        return self.euler[0]
    
    @loggable
    def pitch(self):
        return self.euler[1]
    
    @loggable
    def roll(self):
        return self.euler[2]
