#! Python3

"""This is a test file for limit sensitivity method.
"""

from time import time, sleep
import pigpio

from pisat.core.logger import SensorController
from pisat.handler import PigpioI2CHandler, PyserialSerialHandler, PigpioPWMHandler
from pisat.calc import Navigator, Position
from pisat.model import cached_loggable, LinkedDataModelBase, linked_loggable
from pisat.sensor import SamM8Q, Bno055
from pisat.util.deco import cached_property
from pisat.actuator import PWMDCMotorDriver
import can09.parent.setting as setting
from can09.parent.util import PIDController

NAME_BNO055 = "bno055"
NAME_GPS = "gps"

class RunningModel(LinkedDataModelBase):

    TEMP_GOAL = [0., 0.]
    
    longitude = linked_loggable(SamM8Q.DataModel.longitude, NAME_GPS)
    latitude = linked_loggable(SamM8Q.DataModel.latitude, NAME_GPS)
    mag = linked_loggable(Bno055.DataModel.mag, NAME_BNO055)
    
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


def main() -> None:
    kp = float(input('Enter Kp: '))
    ex_time = float(input('Enter experiment time [sec]: '))
    
    pi = pigpio.pi()
    
    handler_bno055 = PigpioI2CHandler(pi, 0x28)
    handler_gps = PyserialSerialHandler("/dev/serial0", baudrate=9600)
    handler_motor_l_fin = PigpioPWMHandler(pi, 12, 40000)
    handler_motor_l_rin = PigpioPWMHandler(pi, 18, 40000)
    handler_motor_r_fin = PigpioPWMHandler(pi, 13, 40000)
    handler_motor_r_rin = PigpioPWMHandler(pi, 19, 40000)

    bno055 = Bno055(handler_bno055, name=NAME_BNO055)
    gps = SamM8Q(handler_gps, name=NAME_GPS)
    sencon = SensorController(RunningModel, bno055, gps)
    data = sencon.read()
    motor_l = PWMDCMotorDriver(handler_motor_l_fin, handler_motor_l_rin)
    motor_r = PWMDCMotorDriver(handler_motor_r_fin, handler_motor_r_rin)
    
    pidcontroller = PIDController(kp=kp)
    first_time = time()
    last_time = first_time
    delta_time = 0.
    
    while delta_time < ex_time:
        current_time = time()
        if (current_time - last_time) < setting.SAMPLE_TIME:
            continue
        last_time = current_time
                     
        offset = data.offset_angle2goal
        if offset is None:
            continue
            
        duty = pidcontroller.calc_input(offset)
                
        motor_r.ccw(duty)
        motor_l.cw(setting.DUTY_BASE)
            
        last_time = current_time
        delta_time = first_time - current_time
            
        sleep(setting.SAMPLE_TIME)
        
    motor_r.brake()
    motor_l.brake()
    
if __name__ == '__main__':
    main()