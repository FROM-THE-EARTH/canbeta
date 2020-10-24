
from typing import Dict, Any
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
        self.motors = self.manager.get_component("TwoWheels")
        self.ave
        self.gap = false

    def judge(self, data: Dict[str, Any]) -> bool:
        advance = data.get(dname.ACCELERATION_X)
        if advance is None:
            return False

        self.que.appendleft(advance)

        length = len(self.que)
        if length < 50:
            return False

        if(!self.ave and queue_ave(self.que) - self.ave > 1):
            return True
        else:
            self.ave = queue_ave(self.que)
            return False

    def control(self):
        self.motors.straight()
        self.fethander.set_high()

    def exit(self):
        self.fethander.set_low()

    def queue_ave(self, q):
        queue_list = []
        while not q.empty():
            queue_list.append(q.get())
        for value in queue_list:  # stackの場合はreversed(queue_list)に変更
            q.put(value)
        return sum(queue_list) / len(queue_list)