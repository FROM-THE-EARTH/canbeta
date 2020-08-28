
import pigpio

from pisat.core.cansat import CanSat
from pisat.core.nav import Context
from pisat.core.manager import ComponentManager
from pisat.core.logger import (
    DataLogger, SensorController, LogQueue, SystemLogger
)
from pisat.actuator.motor import MotorBase, TwoWheelsBase
from pisat.sensor.handler import HandlerI2C, HandlerSerial
from pisat.sensor.sensor import Mpu9250, Gyfsdmaxb, SensorGroup
from pisat.adapter import GpsAdapter, AdapterGroup

from can09.parent.nodes import *
from can09.parent.setting import *


def run_parent():

    # device setting
    pi = pigpio.pi()
    handler_i2c = HandlerI2C(pi, I2C_ADDRESS_MPU9250)
    handler_serial = HandlerSerial(port=SERIAL_PORT_GPS)

    motor_L = MotorBase(pi, PIN_MOTOR_L_FIN, PIN_MOTOR_L_RIN)
    motor_R = MotorBase(pi, PIN_MOTOR_R_FIN, PIN_MOTOR_R_RIN)
    wheels = TwoWheelsBase(motor_L, motor_R)

    mpu9250 = Mpu9250(handler_i2c)
    gps = Gyfsdmaxb(handler_serial)
    sgroup = SensorGroup(mpu9250, gps)

    gps_adapter = GpsAdapter(POSITION_GOAL)
    agroup = AdapterGroup(gps_adapter)
    
    con = SensorController(sgroup, agroup)
    que = LogQueue(maxlen=500, dnames=con.dnames)
    dlogger = DataLogger(con, que)

    slogger = SystemLogger()
    slogger.setFileHandler()

    manager = ComponentManager(wheels, dlogger, slogger, recursive=True)

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
    cansat = CanSat(context, manager, dlogger=dlogger, slogger=slogger)
    cansat.run()


if __name__ == "__main__":
    run_parent()
