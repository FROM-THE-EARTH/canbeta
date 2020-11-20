

from pisat.calc import press2alti
from pisat.model import LinkedDataModelBase, linked_loggable, cached_loggable
from pisat.sensor import Bme280, Opt3002, SamM8Q

import can09.setting as whole_setting
import can09.child.setting as child_setting


class ChildLoggingModel(LinkedDataModelBase):
    press = linked_loggable(Bme280.DataModel.press, child_setting.NAME_BME280)
    temp = linked_loggable(Bme280.DataModel.temp, child_setting.NAME_BME280)
    irradiance = linked_loggable(Opt3002.DataModel.irradiance, child_setting.NAME_OPT3002)
    longitude = linked_loggable(SamM8Q.DataModel.longitude, child_setting.NAME_GPS)
    latitude = linked_loggable(SamM8Q.DataModel.latitude, child_setting.NAME_GPS)
    
    @cached_loggable
    def altitude(self):
        return press2alti(self.press, self.temp) - whole_setting.ALTITUDE_GROUND
