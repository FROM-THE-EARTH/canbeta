
from typing import Dict, Any

import pisat.config.dname as dname
from pisat.core.nav import Node

import can09.parent.setting as setting


class SencondRunningNode(Node):
    
    
    def enter(self):
        '''
        第二目的地が正面を向くようにその場で回転．
        '''
    
    
    def judge(self, data: Dict[str, Any]) -> bool:
        '''
        自分の緯度，経度がそれぞれ第二目標地点の5m以内ならTrueを返す．それ以外はFalseを返す．
        '''
    
    
    def control(self):
        '''
        遠走行サイクルを実行．
        '''