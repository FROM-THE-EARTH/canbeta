
from typing import Dict, Any

import pisat.config.dname as dname
from pisat.core.nav import Node

import can09.setting as setting


class FirstRunningNode(Node):
    
    
    def judge(self, data: Dict[str, Any]) -> bool:
        pass
