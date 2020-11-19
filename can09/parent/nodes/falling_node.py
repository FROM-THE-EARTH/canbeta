
from collections import deque
import statistics
from typing import List

from pisat.core.nav import Node

from can09.parent.model import FallingModel
import can09.parent.setting as setting


class FallingNode(Node):
    
    model = FallingModel
    
    LENGTH_JUDGING_DATA = 10
    
    THRESHOLD_RISING_DETECT = 30        # [m]
    THRESHOLD_LANDING_DETECT = 10       # [m]
    THRESHOLD_COUNT_GOOD_JUDGED = 10

    def enter(self):        
        # for judging
        self.que = deque(maxlen=self.LENGTH_JUDGING_DATA)
        self.is_falling: bool = False
        self.count_good_judged_rising: int = 0
        self.count_good_judged_falling: int = 0
        self.value_good_judged_rising: List[float] = []
        self.value_good_judged_falling: List[float] = []

    def judge(self, data: FallingModel) -> bool:

        # getting data
        if data.press is None or data.temp is None:
            return False
        
        # median filter
        self.que.appendleft(data.altitude)
        if len(self.que) < self.LENGTH_JUDGING_DATA:
            return False
        median = statistics.median(self.que)
        
        # Rising Assessment
        # 1. Judging if data through median filter is bigger than the rising threshold.
        # 2. Judging if 'good' data comes THRESHOLD_COUNT_GOOD_JUDGED times in a row.
        # NOTE This assessment always returns False because the true purpose of this Node
        #      is to judge falling the body.
        if not self.is_falling:
            if median < self.THRESHOLD_RISING_DETECT:
                self.value_good_judged_rising.append(median)
                self.count_good_judged_rising += 1
                
                if self.count_good_judged_rising >= self.THRESHOLD_COUNT_GOOD_JUDGED:
                    self.is_falling = True
            else:
                # Reset counted data
                if self.count_good_judged_rising:
                    self.count_good_judged_rising = 0
                    self.value_good_judged_rising.clear()
                    
            return False

        # Falling Assessment
        # 1. Judging if data through median filter is smaller than the falling threshold.
        # 2. Judging if 'good' data comes THRESHOLD_COUNT_GOOD_JUDGED times in a row.
        if self.is_falling:
            if median < self.THRESHOLD_LANDING_DETECT:
                self.value_good_judged_falling.append(median)
                self.count_good_judged_falling += 1
                
                if self.count_good_judged_falling >= self.THRESHOLD_COUNT_GOOD_JUDGED:
                    return True
                else:
                    return False
            else:
                # Reset counted data
                if self.count_good_judged_falling:
                    self.count_good_judged_falling = 0
                    self.value_good_judged_falling.clear()
                return False

    def exit(self) -> None:
        slogger = self.manager.get_component(setting.NAME_SYSTEM_LOGGER)
        values_rising = [round(n, 2) for n in self.value_good_judged_rising]
        values_falling = [round(n, 2) for n in self.value_good_judged_falling]
        slogger.info(f"Landing detected, rising data: {values_rising}, falling data: {values_falling}")
