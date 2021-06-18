
import pigpio
from pisat.actuator import BD62xx, TwoWheels
from pisat.comm.transceiver import Im920, SocketTransceiver
from pisat.core.cansat import CanSat
from pisat.core.nav import Context
from pisat.core.manager import ComponentManager
from pisat.core.logger import (
    DataLogger, LogQueue, SystemLogger
)
from pisat.handler import (
    PigpioI2CHandler, PyserialSerialHandler,
    PigpioDigitalInputHandler, PigpioDigitalOutputHandler,
    PigpioPWMHandler
)
from pisat.sensor import Bno055, Bme280, SamM8Q, HcSr04

from can09.parent.model import LoggingModel
from can09.parent.nodes import *
from can09.parent.setting import *


def run_parent():

    # device setting
    pi = pigpio.pi()
    
    handler_bno055 = PigpioI2CHandler(pi, I2C_ADDRESS_BNO055)
    handler_bme280 = PigpioI2CHandler(pi, I2C_ADDRESS_BME280)
    handler_gps = PyserialSerialHandler(SERIAL_PORT_GPS, baudrate=BAUDRATE_GPS)
    handler_im920 = PyserialSerialHandler(SERIAL_PORT_IM920, baudrate=BAUDRATE_IM920)
    
    handler_motor_L_fin = PigpioPWMHandler(pi, GPIO_MOTOR_L_FIN, freq=MOTOR_PWM_FREQ)
    handler_motor_L_rin = PigpioPWMHandler(pi, GPIO_MOTOR_L_RIN, freq=MOTOR_PWM_FREQ)
    handler_motor_R_fin = PigpioPWMHandler(pi, GPIO_MOTOR_R_FIN, freq=MOTOR_PWM_FREQ)
    handler_motor_R_rin = PigpioPWMHandler(pi, GPIO_MOTOR_R_RIN, freq=MOTOR_PWM_FREQ)
    handler_mosfet_para = PigpioDigitalOutputHandler(pi, GPIO_MOSFET_PARA, name=NAME_MOSFET_PARA)
    handler_mosfet_child = PigpioDigitalOutputHandler(pi, GPIO_MOSFET_CHILD, name=NAME_MOSFET_CHILD)
    handler_sonic_trig = PigpioDigitalOutputHandler(pi, GPIO_SONIC_TRIG)
    handler_sonic_echo = PigpioDigitalInputHandler(pi, GPIO_SONIC_ECHO)
    handler_led = PigpioDigitalOutputHandler(pi, GPIO_LED, name=NAME_LED)

    # actuator
    motor_L = BD62xx(handler_motor_L_fin, handler_motor_L_rin, name=NAME_MOTOR_L)
    motor_R = BD62xx(handler_motor_R_fin, handler_motor_R_rin, name=NAME_MOTOR_R)
    wheels = TwoWheels(motor_L, motor_R, name=NAME_WHEELS)

    # transceiver
    im920 = Im920(handler_im920, name=NAME_IM920)
    im920.clear_buf()
    socket_transceiver = SocketTransceiver(im920, certain=True, name=NAME_SOCKET_TRANSCEIVER)

    # sensor
    bno055 = Bno055(handler_bno055, name=NAME_BNO055)
    bno055.change_operation_mode(Bno055.OperationMode.NDOF)
    bno055.remap_axis(Bno055.Axis.Y, Bno055.Axis.X, Bno055.Axis.Z)
    bno055.remap_sign(y=Bno055.AxisSign.NEGATIVE)
    bme280 = Bme280(handler_bme280, name=NAME_BME280)
    gps = SamM8Q(handler_gps, name=NAME_GPS)
    sonic = HcSr04(handler_sonic_echo, handler_sonic_trig, name=NAME_SUPERSONIC)
    
    que = LogQueue(LoggingModel, maxlen=10000, name=NAME_LOGQUEUE)
    dlogger = DataLogger(que, bno055, bme280, gps, sonic, name=NAME_DATA_LOGGER)

    slogger = SystemLogger(name=NAME_SYSTEM_LOGGER)
    slogger.setFileHandler()

    # register callable components in Nodes
    manager = ComponentManager(motor_L, motor_R, wheels, im920, socket_transceiver, 
                               handler_mosfet_para, handler_mosfet_child, handler_led, dlogger, slogger, 
                               recursive=True, name=NAME_MANAGER)

    # context setting
    context = Context({
                        MissionStandbyNode: {True: FallingNode,         False: MissionStandbyNode},
                        FallingNode:        {True: ParaSeparateNode,    False: FallingNode},
                        ParaSeparateNode:   {True: FirstRunningNode,    False: ParaSeparateNode},
                        FirstRunningNode:   {True: ChildSeparateNode,   False: FirstRunningNode},
                        ChildSeparateNode:  {True: SencondRunningNode,  False: ChildSeparateNode},
                        SencondRunningNode: {True: GoalSearchNode,      False: SencondRunningNode},
                        GoalSearchNode:     {True: GoalDetectNode,      False: GoalSearchNode},
                        GoalDetectNode:     {True: None,                False: GoalDetectNode}
                    },
                    start=MissionStandbyNode)

    # build a cansat
    cansat = CanSat(context, manager, dlogger=dlogger, slogger=slogger)
    cansat.run()


if __name__ == "__main__":
    run_parent()
