
from typing import Dict, Any

import pisat.config.dname as dname
from pisat.core.nav import Node
from pisat.core.logger import DataLogger

import can09.parent.setting as setting


class FirstRunningNode(Node):
    
    
    def enter(self):
        '''
        第一目的地が正面を向くようにその場で回転．
        '''
        self.dlogger: DataLogger = self.manager.get_component("DataLogger")
    
    def judge(self, data: Dict[str, Any]) -> bool:
        '''
        自分の緯度，経度がそれぞれ第一目標地点の5m以内ならTrueを返す．それ以外はFalseを返す．
        '''
        if data[dname.ALTITUDE] < 10:
            print("hogehoge")
            raise HogeHogeError(
                "HogeHoge detected."
            )
        else:
            raise HogeHogeError(
                "HogeHoge not detected."
            )
    
    
    def control(self):
        '''
        走行サイクルを実行．
        '''
        while not self.event.is_set():
            ref = self.dlogger.get_ref()
            ref[0][dname.]