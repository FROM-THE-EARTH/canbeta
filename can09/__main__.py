
from pisat.core.cansat import CanSat
from pisat.core.nav import Context
from pisat.core.manager import ComponentManager
from pisat.core.logger import DataLogger, SensorController, LogQueue
from pisat.sensor.handler import HandlerSerial
from pisat.sensor.sensor import Mpu9250, Gyfsdmaxb, SensorGroup
from pisat.adapter import GpsAdapter, AdapterGroup

from can09.nodes import *
import can09.setting as setting


def main():
    
    # device setting
    handler_serial      = HandlerSerial(port=setting.SERIAL_PORT_GPS)
    mpu9250             = Mpu9250()
    gps                 = Gyfsdmaxb(handler_serial)
    gps_adapter         = GpsAdapter(setting.POSITION_GOAL)
    con                 = SensorController(SensorGroup(mpu9250, gps), AdapterGroup(gps_adapter))
    que                 = LogQueue(maxlen=500, dnames=con.dnames)
    dlogger             = DataLogger(con, que)
    manager             = ComponentManager(dlogger, recursive=True)
    
    # context setting
    context = Context({
                    FallingNode:        {True: ParaSeparateNode,    False: FallingNode},
                    ParaSeparateNode:   {True: FirstRunningNode,    False: ParaSeparateNode},
                    FirstRunningNode:   {True: ChildSeparateNode,   False: FirstRunningNode},
                    ChildSeparateNode:  {True: SencondRunningNode,  False: ChildSeparateNode},
                    SencondRunningNode: {True: GoalDetectNode,      False: SencondRunningNode},
                    GoalDetectNode:     {True: None,                False: GoalDetectNode}
                },
                start=FallingNode)
    
    # build a cansat
    cansat = CanSat(context, manager)
    cansat.run()


if __name__ == "__main__":
    main()
