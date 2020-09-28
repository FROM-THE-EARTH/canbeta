
from typing import Dict, Any
from time import sleep

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
        self.motors = self.manager.get_component("TwoWheels")
    
    def judge(self, data: Dict[str, Any]) -> bool:
        '''
        自分の緯度，経度がそれぞれ第一目標地点の5m以内ならTrueを返す．それ以外はFalseを返す．
        '''
        if data[dname.ALTITUDE_]
            
    def control(self):
        '''
        走行サイクルを実行．
        '''
        while not self.event.is_set():
            ref = self.dlogger.get_ref()
            longi = ref[0][dname.GPS_LONGITUDE]
            lati = ref[0][dname.GPS_LATITUDE]
            
            self.motors.pwm(self.calc_pwm(longi, lati))
            time.sleep(0.5)
            
        if self.event.package:
            print("Hoge")
            
    def calc_pwm(self, longi, lati) -> float:
        print("HogeHoge")
        pass