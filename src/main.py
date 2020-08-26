
from pisat.core.cansat import CanSat
from pisat.core.nav import Context
from pisat.core.logger import *
from pisat.sensor.sensor import Mpu9250, SensorGroup

from .nodes import *


def main():
    
    # device setting
    mpu9250 =   Mpu9250()
    con     =   SensorController(SensorGroup(mpu9250))
    que     =   LogQueue(maxlen=500, dnames=con.dnames)
    dlogger =   DataLogger(con, que)
    
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
    cansat = CanSat(context, dlogger)
    cansat.run()


if __name__ == "__main__":
    main()    
