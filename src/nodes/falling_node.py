
from typing import Dict, Any

import pisat.sensor.const as const
from pisat.core.nav import Node

from .setting import *


class FallingNode(Node):
    
    # 
    #
    #
    
    def judge(self, data: Dict[str, Any]) -> bool:
        if data[const.DATA_ALTITUDE] < THRESHOLD_LANDING_DETECT:
            return True
        else:
            return False
        