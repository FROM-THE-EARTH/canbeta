
from typing import Dict, Any
from collections import deque

import pisat.config.dname as dname
from pisat.core.nav import Node
from pisat.core.logger import DataLogger

import can09.parent.setting as setting

class FallingNode(Node):

    def enter(self):
        self.dlogger: DataLogger = self.manager.get_component("DataLogger")
        self.que = deque(maxlen=100)

    def judge(self, data: Dict[str, Any]) -> bool:

        sealevel = data.get(dname.ALTITUDE_SEALEVEL)
        if sealevel is None:
            return False

        self.que.appendleft(sealevel)

        length = len(self.que)
        if length < 50:
            return False

        dataset = sorted(self.que)
        for i in range(length/2):
            sum += dataset(length/4 + i)

        average = sum / length

        if abs(setting.THRESHOLD_LANDING_DETECT - average) < 1:
            return True
        else:
            print("Landin'!")
            return False

    def control(self):
