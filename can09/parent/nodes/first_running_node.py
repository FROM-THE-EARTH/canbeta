
from typing import Dict, Deque
from time import time, sleep
from numpy import abs

import pisat.config.dname as dname
from pisat.config.type import Logable
from pisat.core.nav import Node
from pisat.core.logger import DataLogger

import can09.parent.setting as setting


class FirstRunningNode(Node):
    
    
    def enter(self):
        '''
        第一目的地が正面を向くようにその場で回転．
        '''
        dlogger = self.manager.get_component("DataLogger")
        self.ref: DataLogger = dlogger.refqueue
        self.motor_R = self.manager.get_component("SimplePWMMotorDriver")
        self.motor_L = self.manager.get_component("SimolePWMMotorDriver")
    
    def judge(self, data: Dict[str, Logable]) -> bool:
        
        distance = data.get(dname.DISTANCE_FIRST_GOAL)
        if distance is None:
            return False
        
        if distance < setting.THRESHOLD_CHILD_RELEASE:
            return True
            
    def control(self):
        
        self._duty_base = setting.DUTY_RATIO_FAR
        
        while not self.event.is_set():
            
            que = self.ref.get()
            self.offset = que[0].get(dname.OFFSET_ANGLE)
            if self.offset is None:
                continue
            
            if abs(self.offset) > setting.THRESHOLD_PID_START:
                self._running_cycle()
            else:
                self.motor_R.ccw(self._duty_base)
                self.motor_L.cw(self._duty_base)
            
    def _running_cycle(self):
        self._clear()
        
        if self.offset > 0:
            while self.offset > setting.THRESHOLD_PID_FINISH:
                self._pid_controller()
                self.motor_R.ccw(self._duty_updated)
                self.motor_L.cw(self._duty_base)
                sleep(1)
            
        else:
            while self.offset < -setting.THRESHOLD_PID_FINISH:
                self._pid_controller()
                self.motor_R.ccw(self._duty_base)
                self.motor_L.cw(self._duty_updated)
                sleep(1)
            
    def _clear(self):
        self._p_term = 0.0
        self._i_term = 0.0
        self._d_term = 0.0
        self._last_offset = 0.0
        self._current_time = time()
        self._last_time = self._current_time
        
    def _set_up_parameters(self):
        que = self.ref.get()
        temp_offset = abs(que[0].get(dname.OFFSET_ANGLE))
        if temp_offset is not None:
            self._offset = temp_offset
        elif self._offset < 0:
            self._offset = - self._offset
        
        self._current_time = time()
        self._delta_time = self._current_time - self._last_time
        
        self._delta_error = self._offset - self._last_offset
        
    def _update_p(self):
        self._p_term = self._offset
        
    def _update_i(self):
        i_term_temp = self._offset * self._delta_time
        if self._offset > setting.THRESHOLD_I_TERM:
            i_term_temp = 0
        self._i_term += i_term_temp
        if self._i_term > setting.MAX_I_TERM:
            self._i_term = setting.MAX_I_TERM
        elif self._i_term < setting.MIN_I_TERM:
           self._i_term = setting.MIN_I_TERM
           
    def _update_d(self):
        self._d_term = self._delta_error / self._delta_time
        
    def _save_parameters(self):
        self._last_time = self._current_time
        self._last_error = self._offset
        
    def _update_duty_ratio(self):
        output = (setting.KP * self._p_term) + (setting.KI * self._i_term) + (setting.KD * self._d_term)
        if output < 0:
            output = 0
        
        self._duty_updated = self._duty_base - output
        if self._duty_updated < setting.MIN_DUTY_RATIO:
            self._duty_updated = setting.MIN_DUTY_RATIO

    def _pid_controller(self):
        
        self._set_up_parameters()
        
        self._update_p()
        self._update_i()
        self._update_d()
        
        self._save_parameters()
        
        self._update_duty_ratio()