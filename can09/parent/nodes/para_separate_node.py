
from pisat.core.nav import Node
from collections import deque

import pisat.config.dname as dname
from pisat.core.nav import Node
from pisat.core.logger import DataLogger
from pisat.handler import PigpioDigitalOutputHandler

import can09.parent.setting as setting



class ParaSeparateNode(Node):

    def enter(self):
        self.dlogger: DataLogger = self.manager.get_component("DataLogger")
        self.que = deque(maxlen=100)
        self.fethandler: PigpioDigitalOutputHandler = self.manager.get_component("PigpioDigitalOutputHandler")

    def judge(self, data: Dict[str, Any]) -> bool:
        advance = data.get(dname.ACCELERATION_X)
        if advance is None:
            return False

        self.que.appendleft(advance)
        if 

    def control(self):
        self.fethander.set_high()

    def exit(self):
        self.fethander.set_low()