
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
        '''
        自分の緯度，経度がそれぞれ第一目標地点の5m以内ならTrueを返す．それ以外はFalseを返す．
        '''
        pass
            
    def control(self):
        
        self._duty_base = setting.FAR_DUTY_RATIO
        
        while not self.event.is_set():
            
            que = self.ref.get()
            self.offset = que[0].get(dname.OFFSET_ANGLE)
            if self.offset is None:
                continue
            
            if abs(self.offset) > setting.THRESHOLD_PID_START:
                self._pid_control()
            else:
                self.motor_R.ccw(self._duty_base)
                self.motor_L.cw(self._duty_base)
            
    def _pid_control(self):
        self._clear()
        
        if self.offset > 0:
            while self.offset > setting.THRESHOLD_PID_FINISH:
                self._update()
                self.motor_R.ccw(self._duty_updated)
                self.motor_L.cw(self._duty_base)
                sleep(1)
            
        else:
            while self.offset < -setting.THRESHOLD_PID_FINISH:
                self._update()
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

    def _update(self):
        que = self.ref.get()
        temp_offset = abs(que[0].get(dname.OFFSET_ANGLE))
        if temp_offset is not None:
            self._offset = temp_offset
        elif self._offset < 0:
            self._offset = - self._offset
        
        current_time = time()
        delta_time = current_time - self._last_time
        
        delta_error = self._offset - self._last_offset
        
        self._p_term = self._offset
        
        i_term_temp = self._offset * delta_time
        if self._offset > setting.THRESHOLD_I_TERM:
            i_term_temp = 0
        self._i_term += i_term_temp
        if self._i_term > setting.MAX_I_TERM:
            self._i_term = setting.MAX_I_TERM
        elif self._i_term < setting.MIN_I_TERM:
           self._i_term = setting.MIN_I_TERM
           
        self._d_term = delta_error / delta_time
        
        self._last_time = current_time
        self._last_error = self._offset
        
        output = (setting.KP * self._p_term) + (setting.KI * self._i_term) + (setting.KD * self._d_term)
        if output < 0:
            output = 0
        
        self._duty_updated = self._duty_base - output
        if self._duty_updated < setting.MIN_DUTY_RATIO:
            self._duty_updated = setting.MIN_DUTY_RATIO