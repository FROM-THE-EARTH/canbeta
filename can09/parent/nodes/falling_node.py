
from typing import Dict, Any
from collections import deque

import pisat.config.dname as dname
from pisat.core.logger.systemlogger import SystemLogger
from pisat.core.nav import Node
from pisat.core.logger import DataLogger

import can09.parent.setting as setting

class FallingNode(Node):

    def enter(self):
        self.dlogger: DataLogger = self.manager.get_component("DataLogger")
        self.slogger: SystemLogger = self.manager.get_component("SystemLogger")
        self.que = deque(maxlen=100)
        
        self.value_good_judged = 0

    def judge(self, data: Dict[str, Any]) -> bool:

        # getting data
        sealevel = data.get(dname.ALTITUDE_SEALEVEL)
        if sealevel is None:
            return False

        # prevent outliers
        self.que.appendleft(sealevel)

        length = len(self.que)
        if length < 50:
            return False
    
        quater_1st = length // 4
        quater_3rd = quater_1st * 3
        dataset = sorted(self.que)
        sum_data = sum(dataset[quater_1st:quater_3rd])
        average = sum_data / (quater_3rd - quater_1st)

        # assessment
        if abs(setting.THRESHOLD_LANDING_DETECT - average) < 1:
            self.value_good_judged = average
            return True
        else:
            return False

    def control(self):
        pass
    
    def exit(self) -> None:
        self.slogger.info(f"Landing, data: {self.value_good_judged}")
