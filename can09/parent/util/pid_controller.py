#! python 3


"""pid_controller.py
    
    Requires:
        kp                  - proportional gain (default is None)
                                -> If given, the proportional controller is used.
        ki                  - integral gain (default is None)
                                -> If given, the integral controller is used.
        kd                  - derivative gain (default is None)
                                -> If given, the derivative controller is used.
        max_input           - maximum desired input if any (default is None)
        min_input           - minimum desired input if any (default is None)
        sse_ratio           - steady-state error ratio (default is None)
                                -> Set this if you want to use the integral controller only for
                                   eliminating steady-state error (0.1 < sse_dtctr < 0.3 recommended).
        threshold_i_ctrlr   - threshold intergral controller (default is None)
                                -> Each time it is detected that it is in the range of steady-state error,
                                   self._i_counter is incresed by 1, and when it exceeds threshold_i_cntrlr,
                                   steady-state error is detected, and the integral controller is activated.

    Returns:
        input: float
        
    Notes:
        If you put a limitation on the integral controller, you MUST give BOTH sse_ratio AND threshold_i_ctrlr.
"""


from time import time
from typing import Optional

class PIDController:

    def __init__(self,
                 kp: Optional[float] = None,
                 ki: Optional[float] = None,
                 kd: Optional[float] = None,
                 max_input: Optional[float] = None,
                 min_input: Optional[float] = None,
                 sse_ratio: Optional[float] = None,
                 threshold_i_ctrlr: Optional[int] = None) -> None:
                
        """Initializes the instance variables"""
        # Setting constants
        self._kp: Optional[float] = kp
        self._ki: Optional[float] = ki
        self._kd: Optional[float] = kd
        self._max_input: Optional[float] = max_input
        self._min_input: Optional[float] = min_input
        self._sse_ratio: Optional[float] = sse_ratio
        self._threshold_i_ctrlr: Optional[int] = threshold_i_ctrlr

        # Initializing variables
        self._last_time: float = time()
        self._last_i_term: float = 0.
        self._last_error: float = 0.
        self._sse_range: float = 0.
        self._counter: int = 0
        self._i_counter: int = 0

    def calc_input(self, error: float) -> float:
        """Calculates an input using PID controller"""
        # Activating this if-statement only once
        if self._counter == 0:
            # Done in order to make the first dalta_error 0
            self._last_error = error
            
            # Calculating the steady-state error range, used in the integral controller
            if self._sse_ratio is not None:
                self._sse_range = error * self._sse_ratio
            
            # Making the counter non 0 so that it will not be activated from the next time
            self._counter += 1
        
        # Preparating parameters
        delta_error = error - self._last_error
        current_time = time()
        delta_time = current_time - self._last_time

        # Calculating each term
        if self._kp is not None:
            p_term = self._calc_p_term(error)
        else:
            p_term = 0.
        
        if self._ki is not None:
            if self._sse_ratio is not None & self._threshold_i_ctrlr is not None:
                i_term = self._calc_i_term_sse(error, delta_time)
            else:
                i_term = self._calc_i_term
        else:
            i_term = 0.
            
        if self._kd is not None:
            d_term = self._calc_d_term(delta_error, delta_time)
        else:
            d_term = 0.

        # Calculating an input
        input = p_term + i_term + d_term
        if self._min_input is not None:
            if input < self._min_input:
                input = self._min_input
        if self._max_input is not None:
            if input > self._max_input:
                input = self._max_input

        # Saving parameters
        self._last_error = error
        self._last_time = current_time
        self._last_i_term = i_term

        return input
    
    def _calc_p_term(self, error: float) -> float:
        """Calculates a p_term"""
        return self._kp * error
    
    def _calc_i_term(self, error: float, delta_time: float) -> float:
        """Calculates an i_term using trapezoidal rule"""
        delta_i_term = ((self._last_error + error) / 2) * delta_time   
        return self._ki * (self._last_i_term + delta_i_term)

    def _calc_i_term_sse(self, error: float, delta_time: float) -> float:
        """Calculates an i_term using trapezoidal rule or returns 0
        
        Note:
        -----
        This integral controller is activated only for eliminating steady-state error.
        """
        
        # Increasing self._i_counter by 1 when the error is within the margin of error (moe)
        if -self._sse_range < error < self._sse_range:
            self._i_counter += 1
        else:
            self._last_i_term = 0
            self._i_counter = 0
        
        # Activating the integral controller when the steady-state error is detected
        if self._i_counter > self._threshold_i_ctrlr:
            delta_i_term = ((self._last_error + error) / 2) * delta_time   
            return self._ki * (self._last_i_term + delta_i_term)
        else:
            return 0

    def _calc_d_term(self, delta_error: float, delta_time: float) -> float:
        """Calculates a d_term using approximation"""
        return self._kd * (delta_error / delta_time)