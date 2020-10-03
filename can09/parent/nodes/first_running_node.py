
from typing import Dict, Deque
from time import time, sleep

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
        self.ref = dlogger.refqueue
        self.motors = self.manager.get_component("TwoWheels")
    
    def judge(self, data: Dict[str, Logable]) -> bool:
        '''
        自分の緯度，経度がそれぞれ第一目標地点の5m以内ならTrueを返す．それ以外はFalseを返す．
        '''
        pass
            
    def control(self):
        while not self.event.is_set():
            que = self.ref.get()
            self.offset = que[0].get(dname.OFFSET_ANGLE)
            if self.offset is None:
                continue
            
            if self.offset > setting.THRESHOLD_PID_START or self.offset < -setting.THRESHOOD_PID_START :
                self._pid_control()
            else:
                self.motors.straight()
            
    def _pid_control(self):
        self._clear()
        
        if self.offset > 0:
            while self.offset > setting.THRESHOLD_PID_FINISH:
                self._update()
                
                sleep(1)
            
        else:
            while self.offset < -setting.THRESHOLD_PID_FINISH:
                self._update()
                
                sleep(1)
            
    def _clear(self):
        self._p_term = 0.0
        self._i_term = 0.0
        self._d_term = 0.0
        self._last_offset = 0.0
        self._current_time = time()
        self._last_time = self._current_time
        
        self.output = 0.0

    def _update(self):
        que = self.ref.get()
        self.offset = que[0].get(dname.OFFSET_ANGLE)
        
        self._current_time = time()
        delta_time = self._current_time - self._last_time
        delta_error = self.offset - self._last_offset
        
        self._p_term = setting.KP * self.offset
        self._i_term += self.offset * self.delta_time

        if self._i_term > setting.MAX_I_TERM:
            self._i_term = setting.MAX_I_TERM
        if self._i_term < -setting.MAX_I_TERM:
           self._i_term = -setting.MAX_I_TERM
           
        self._d_term = delta_error / delta_time
        
        self._last_time = self._current_time
        self._last_error = self.offset
        
        self.output = self._p_term + (setting.KI * self._i_term) + (setting.KD * self._d_term)