from typing import float
from time import time

class PIDController:

    def __init__(self, kp: float, ki: float, kd: float, duty_base: float):
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self._duty_base = duty_base
        
    def reset(self, offset: float) -> None:
        self._last_offset = offset
        self._last_time = time()
        self._last_i_term = 0.

    def calc_duty(self, offset: float) -> float:
        """Calculates a duty ratio using PID controller"""
        # Preparating parameters
        delta_offset = offset - self._last_offset
        current_time = time()
        delta_time = current_time - self._last_time

        # Calculating each term
        p_term = offset
        i_term = self._calc_i_term(offset, delta_time)
        d_term = self._calc_d_term(delta_offset, delta_time)

        # Calculating an output
        duty = (self._kp * p_term) + (self._ki * i_term) + (self._kd * d_term)
        if duty < 0:
            duty = 0
        elif duty > 100:
            duty = 100

        # Saving parameters
        self._last_offset = offset
        self._last_time = current_time
        self._last_i_term = i_term

        return duty

    def _calc_i_term(self, offset: float, delta_time: float) -> float:
        """Calcultes an i_term using trapezoidal rule"""
        delta_i_term = ((self._last_offset + offset) / 2) * delta_time
        return (self._last_i_term + delta_i_term)

    def _calc_d_term(self, delta_offset: float, delta_time: float) -> float:
        """Calculates a d_term using approximation"""
        return delta_offset / delta_time