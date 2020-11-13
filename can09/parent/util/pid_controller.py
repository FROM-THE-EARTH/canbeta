from time import time

class PIDController:

    def __init__(self,
                 kp: float,
                 ki: float,
                 kd: float,
                 max_input: float,
                 min_input: float,
                 acceptable_moe: float,
                 threshold_i_ctrlr: int) -> None:
        
        # TODO; The integral controller's limitation should be selectable.
        
        """Initializes the instance variables"""
        # Setting constants
        self._kp: float = kp
        self._ki: float = ki
        self._kd: float = kd
        self._max_input: float = max_input
        self._min_input: float = min_input
        self._acceptable_moe: float = acceptable_moe
        self._threshold_i_ctrlr: int = threshold_i_ctrlr

        # Initializing variables
        self._last_time: float = time()
        self._last_i_term: float = 0.
        self._last_error: float = 0.
        self._moe: float = 0.
        self._counter: int = 0
        self._i_counter: int = 0

    def calc_input(self, error: float) -> float:
        """Calculates an input using PID controller"""
        # Activating this if-statement only once
        if self._counter == 0:
            # Done in order to make the first dalta_error 0
            self._last_error = error
            
            # Calculating the value for the margin of error (moe), used in the integral controller
            self._moe = error * self._acceptable_moe
            
            # Making the counter non 0 so that it will not be activated from the next time
            self._counter += 1
        
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
        if input < self._min_input:
            input = self._min_input
        elif input > self._max_input:
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
        """Calcultes an i_term using trapezoidal rule or returns 0
        
        Note:
        -----
        This integral controller is activated only for eliminating steady-state error.
        """
        
        # Increasing self._i_counter by 1 when the error is within the margin of error (moe)
        if self._last_error - self._moe < error < self._last_error + self._moe:
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