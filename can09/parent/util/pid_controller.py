from time import time

class PIDController:

    def __init__(self, kp: float, ki: float, kd: float, max: float, min: float) -> None:
        """Initializes the instance variables"""
        self._kp: float = kp
        self._ki: float = ki
        self._kd: float = kd
        self._max: float = max
        self._min: float = min
        
    def reset(self, error: float) -> None:
        """Resets parameters"""
        # Saving the first error in order to limit the i_term
        self._first_error = error
        
        self._last_error = error
        self._last_time = time()
        self._last_i_term = 0.

    def calc_input(self, error: float) -> float:
        """Calculates an input using PID controller"""
        # Preparating parameters
        delta_error = error - self._last_error
        current_time = time()
        delta_time = current_time - self._last_time

        # Calculating each term
        p_term = self._calc_p_term(error)
        i_term = self._calc_i_term(error, delta_time)
        d_term = self._calc_d_term(delta_error, delta_time)

        # Calculating an input
        input = p_term + i_term + d_term
        if input < self._min:
            input = self._min
        elif input > self._max:
            input = self._max

        # Saving parameters
        self._last_error = error
        self._last_time = current_time
        self._last_i_term = i_term

        return input
    
    def _calc_p_term(self, error: float) -> float:
        """Calculates a p_term"""
        return self._kp * error

    def _calc_i_term(self, error: float, delta_time: float) -> float:
        """Calcultes an i_term using trapezoidal rule"""
        delta_i_term = ((self._last_error + error) / 2) * delta_time
        
        # Using the integral controller only when eliminating steady-state error
        if error < self._first_error / 5:
            return self._ki * (self._last_i_term + delta_i_term)
        else:
            return self._ki * self._last_i_term

    def _calc_d_term(self, delta_error: float, delta_time: float) -> float:
        """Calculates a d_term using approximation"""
        return self._kd * (delta_error / delta_time)