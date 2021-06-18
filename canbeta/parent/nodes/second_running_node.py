

from time import sleep, time

from pisat.core.nav import Node
from pisat.core.logger.refque import RefQueue
from pisat.actuator.bd62xx import BD62xx

from can09.parent.model import RunningModel
import can09.parent.setting as setting
from can09.parent.util import PIDController


class SencondRunningNode(Node):
    
    
    def enter(self) -> None:
        """Sets up the instance variables"""
        
        self._ref: RefQueue = self.manager.get_component(setting.NAME_DATA_LOGGER).refqueue
        self._right_motor: BD62xx = self.manager.get_component(setting.NAME_MOTOR_R)
        self._left_motor: BD62xx = self.manager.get_component(setting.NAME_MOTOR_L)
        self._last_time: float = 0.
        
        self._pidcontroller = PIDController(kp=setting.KP,
                                            ki=setting.KI,
                                            kd=setting.KD,
                                            max_input=setting.MAX_DUTY,
                                            min_input=setting.MIN_DUTY,
                                            sse_ratio=setting.SSE_RATIO,
                                            threshold_i_ctrlr=setting.THRESHOLD_I_CTRLR)
    
    def judge(self, data: RunningModel) -> bool:
        """Returns 'True' if the first goal is reached"""
        distance = data.distance2goal
        if distance is None:
            return False
        
        if distance < setting.THRESHOLD_CAMERA_DETECTION:
            return True
        else:
            return False
            
    def control(self) -> None:
        """Controls the direction, in which CanSat moves
        
        Note:
        -----
        If OFFSET_ANGLE is positive, CanSat has to turn right by first decreasing the rotational velocity of the right tyre.
        If OFFSET_ANGLE is negative, CanSat has to turn left by first decreasing the rotational velocity of the left tyre.
        
        1. By obtaining OFFSET_ANGLE, a motor, to be controlled, is determined.
        2. When OFFSET_ANGLE is negative, the sign is inverted for simplification purposes.
        3. The moter is PID-Controlled until the first goal is reached.
        4. When the first goal is reached, CanSat stops moving.
        """
        while not self.event.is_set():
            offset = self._ref.get()[0].offset_angle2goal
            
            self._last_time = time()
            
            if offset is None or offset == 0:
                continue
            elif offset > 0:
                self._exec_pid_ctrl_right()
            elif offset < 0:
                self._exec_pid_ctrl_left()
                
        self._right_motor.brake()
        self._left_motor.brake()
            
    def _exec_pid_ctrl_right(self) -> None:
        """Executes PID controller on the right motor"""
        while not self.event.is_set():
            current_time = time()
            if (current_time - self._last_time) < setting.SAMPLE_TIME:
                continue
            self._last_time = current_time
                     
            offset = self._ref.get()[0].offset_angle2goal
            if offset is None:
                continue
            
            duty = self._pidcontroller.calc_input(offset)
                
            self._right_motor.ccw(duty)
            self._left_motor.cw(setting.DUTY_BASE)
                        
            sleep(setting.SAMPLE_TIME)
            
    def _exec_pid_ctrl_left(self) -> None:
        """Executes PID controller on the left motor"""
        while not self.event.is_set():
            current_time = time()
            if (current_time - self._last_time) < setting.SAMPLE_TIME:
                continue
            self._last_time = current_time
            
            offset = -self._ref.get()[0].offset_angle2goal
            if offset is None:
                continue
            
            duty = self._pidcontroller.calc_input(offset)
                
            self._right_motor.ccw(setting.DUTY_BASE)
            self._left_motor.cw(duty)
            
            sleep(setting.SAMPLE_TIME)