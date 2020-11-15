#! Python3

"""This is a test file for limit sensitivity method.
"""

from time import time, sleep

from pisat.calc import Navigator, Position
from pisat.model import cached_loggable, LinkedDataModelBase, linked_loggable
from pisat.sensor import SamM8Q, Bno055
from pisat.util.deco import cached_property
from pisat.actuator import BD62xx
from pisat.core.logger import RefQueue

import can09.parent.setting as setting
from can09.parent.util import PIDController


class RunningModel(LinkedDataModelBase):

    TEMP_GOAL = [0., 0.]
    
    longitude = linked_loggable(SamM8Q.DataModel.longitude, setting.NAME_GPS)
    latitude = linked_loggable(SamM8Q.DataModel.latitude, setting.NAME_GPS)
    mag = linked_loggable(Bno055.DataModel.mag, setting.NAME_BNO055)
    
    def setup(self) -> None:
        self._navi_goal_temp = Navigator(Position(*self.TEMP_GOAL))
        
    @cached_property
    def position(self):
        return Position(self.longitude, self.latitude, degree=True)
    
    def calc_heading(self, mag) -> float:
        pass
    
    @cached_loggable
    def offset_angle2goal(self):
        heading = self.calc_heading(self.mag)
        return self._navi_goal.delta_angle(self.position, heading)
    
    
class LimitSensitivityMethod:
    
    model = RunningModel
    
    def __init__(self, kp: float, ex_time: float) -> None:
        self._ref: RefQueue = self.manager.get_component(setting.NAME_DATA_LOGGER).refqueue
        self._right_motor: BD62xx = self.manager.get_component(setting.NAME_MOTOR_R)
        self._left_motor: BD62xx = self.manager.get_component(setting.NAME_MOTOR_L)
        self._first_time: float = time()
        self._last_time: float = self._first_time
        self._delta_time: float = 0.
        
        self._ex_time: float = ex_time
        
        self._pidcontroller = PIDController(kp=kp)
        
    def exec_p_ctrl(self) -> None:
        while self._delta_time < self._ex_time:
            current_time = time()
            if (current_time - self._last_time) < setting.SAMPLE_TIME:
                continue
            self._last_time = current_time
                     
            offset = self._ref.get()[0].offset_angle2child
            if offset is None:
                continue
            
            duty = self._pidcontroller.calc_input(offset)
                
            self._right_motor.ccw(duty)
            self._left_motor.cw(setting.DUTY_BASE)
            
            self._last_time = current_time
            self._delta_time = self._first_time - current_time
            
            sleep(setting.SAMPLE_TIME)
        
        self._right_motor.brake()
        self._left_motor.brake()

def main() -> None:
    kp = float(input('Enter Kp: '))
    ex_time = float(input('Enter experiment time [sec]: '))
    
    tunner = LimitSensitivityMethod(kp, ex_time)
    tunner.exec_p_ctrl()
    
if __name__ == '__main__':
    main()