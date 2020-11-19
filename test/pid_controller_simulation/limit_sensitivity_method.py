#! Python3

"""This is a test file for limit sensitivity method.
"""

import time

import pigpio
from pisat.actuator import BD62xx
from pisat.calc import Navigator, Position
from pisat.core.logger import SensorController
from pisat.handler import PigpioI2CHandler, PyserialSerialHandler, PigpioPWMHandler
from pisat.model import (
    loggable, cached_loggable, LinkedDataModelBase, linked_loggable
)
from pisat.sensor import SamM8Q, Bno055
from pisat.util.deco import cached_property

import can09.parent.setting as setting
from can09.parent.util import PIDController


class RunningModel(LinkedDataModelBase):

    TEMP_GOAL = [0., 0.]
    
    longitude = linked_loggable(SamM8Q.DataModel.longitude, setting.NAME_GPS)
    latitude = linked_loggable(SamM8Q.DataModel.latitude, setting.NAME_GPS)
    euler = linked_loggable(Bno055.DataModel.euler, setting.NAME_BNO055, logging=False)
    
    def setup(self) -> None:
        self._navi_goal_temp = Navigator(Position(*self.TEMP_GOAL))
        
    @cached_property
    def position(self):
        return Position(self.longitude, self.latitude, degree=True)

    @loggable
    def heading(self):
        return self.euler[0]
    
    @cached_loggable
    def offset_angle2goal(self):
        return self._navi_goal.delta_angle(self.position, self.heading)


def main():
    
    kp = float(input('Enter Kp: '))
    ex_time = float(input('Enter experiment time [sec]: '))
    
    # device setting
    pi = pigpio.pi()    
    handler_bno055 = PigpioI2CHandler(pi, setting.I2C_ADDRESS_BNO055)
    handler_gps = PyserialSerialHandler(setting.SERIAL_PORT_GPS, baudrate=9600)
    handler_motor_l_fin = PigpioPWMHandler(pi, setting.GPIO_MOTOR_L_FIN, setting.MOTOR_PWM_FREQ)
    handler_motor_l_rin = PigpioPWMHandler(pi, setting.GPIO_MOTOR_L_RIN, setting.MOTOR_PWM_FREQ)
    handler_motor_r_fin = PigpioPWMHandler(pi, setting.GPIO_MOTOR_R_FIN, setting.MOTOR_PWM_FREQ)
    handler_motor_r_rin = PigpioPWMHandler(pi, setting.GPIO_MOTOR_R_RIN, setting.MOTOR_PWM_FREQ)
    bno055 = Bno055(handler_bno055, name=setting.NAME_BNO055)
    gps = SamM8Q(handler_gps, name=setting.NAME_GPS)
    sencon = SensorController(RunningModel, bno055, gps)
    motor_l = BD62xx(handler_motor_l_fin, handler_motor_l_rin, name=setting.NAME_MOTOR_L)
    motor_r = BD62xx(handler_motor_r_fin, handler_motor_r_rin, name=setting.NAME_MOTOR_R)
    
    # testing
    data = sencon.read()
    pidcontroller = PIDController(kp=kp)
    first_time = time.time()
    last_time = first_time
    delta_time = 0.
    
    while delta_time < ex_time:
        current_time = time.time()
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
            
        time.sleep(setting.SAMPLE_TIME)
        
    motor_r.brake()
    motor_l.brake()
    

if __name__ == '__main__':
    main()