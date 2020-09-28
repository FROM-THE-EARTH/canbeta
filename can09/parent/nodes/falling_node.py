
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

        if len(self.que) < 50:
            return False

        

        if self.SEALEVEL - setting.THRESHOLD_LANDING_DETECT \
            and data[dname.ALTITUDE_SEALEVEL] < self.SEALEVEL + setting.THRESHOLD_LANDING_DETECT:
            print("This isn't flying, this is falling with style!")
            return True
        else:
            print("Landin'!")
            return False

    def control(self):
        print("This isn't flying, this is falling with style!")
