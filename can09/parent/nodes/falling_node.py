
from typing import Dict, Any

import pisat.config.dname as dname
from pisat.core.nav import Node

import can09.parent.setting as setting


class FallingNode(Node):
    
    def judge(self, data: Dict[str, Any]) -> bool:
        if data[dname.ALTITUDE_SEALEVEL] < setting.THRESHOLD_LANDING_DETECT:
            return True
        else:
            return False
        