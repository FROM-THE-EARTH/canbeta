
from pisat.calc import press2alti
from pisat.model import cached_loggable, LinkedDataModelBase, linked_loggable
from pisat.sensor import Bme280, SamM8Q

import can09.parent.setting as setting


class FallingModel(LinkedDataModelBase):
    
    press = linked_loggable(Bme280.DataModel.press, setting.NAME_BME280)
    temp = linked_loggable(Bme280.DataModel.temp, setting.NAME_BME280)
    longitude = linked_loggable(SamM8Q.DataModel.longitude, setting.NAME_GPS)
    latitude = linked_loggable(SamM8Q.DataModel.latitude, setting.NAME_GPS)
    
    @cached_loggable
    def altitude(self) -> float:
        return press2alti(self.press, self.temp) - setting.ALTITUDE_GROUND
