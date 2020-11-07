from can09.parent.util.pid_controller import PIDController
from typing import Dict
from time import sleep
from numpy import abs

import pisat.config.dname as dname
from pisat.config.type import Logable
from pisat.core.nav import Node
from pisat.core.logger import DataLogger

import can09.parent.setting as setting
from can09.parent.util.pid_controller import PIDController


class FirstRunningNode(Node):
    
    
    def enter(self):
        '''
        第一目的地が正面を向くようにその場で回転．
        '''
        self._ref = self.manager.get_component("DataLogger").refqueue
        self._motor_R = self.manager.get_component("SimplePWMMotorDriver")
        self._motor_L = self.manager.get_component("SimolePWMMotorDriver")
        
        self._pidcontroller = PIDController(setting.KP, setting.KI, setting.KD, setting.DUTY_BASE)
    
    def judge(self, data: Dict[str, Logable]) -> bool:
        distance = data.get(dname.DISTANCE_FIRST_GOAL)
        if distance is None:
            return False
        
        if distance < setting.THRESHOLD_CHILD_RELEASE:
            return True
            
    def control(self) -> None:
        while not self.event.is_set():
            
            offset = self._ref.get()[0].get(dname.OFFSET_ANGLE)
            if offset is None:
                continue
            
            if abs(offset) > setting.THRESHOLD_PID_START:
                self._pidcontroller.reset(offset)
                self._excecute_pid_control()
            else:
                self._motor_R.ccw(setting.DUTY_BASE)
                self._motor_L.cw(setting.DUTY_BASE)
                
    def _excecute_pid_control(self) -> None:        
        while True:
            sleep(1)
            
            offset = self._ref.get()[0].get(dname.OFFSET_ANGLE)
            if offset is None:
                continue

            duty = self._pidcontroller.calc_duty(abs(offset))
            
            if offset > setting.THRESHOLD_PID_FINISH:
                self._motor_R.ccw(duty)
                self._motor_L.cw(setting.DUTY_BASE)
            elif offset < - setting.THRESHOLD_PID_FINISH:
                self._motor_R.ccw(setting.DUTY_BASE)
                self._motor_L.cw(duty)
            else:
                break