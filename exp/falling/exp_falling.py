
import pigpio
from pisat.actuator import BD62xx, TwoWheels
from pisat.comm.transceiver import Im920
from pisat.core.cansat import CanSat
from pisat.core.nav import Context
from pisat.core.manager import ComponentManager
from pisat.core.logger import (
    DataLogger, SensorController, LogQueue, SystemLogger
)
from pisat.handler import (
    PigpioI2CHandler, PyserialSerialHandler,
    PigpioDigitalInputHandler, PigpioDigitalOutputHandler
)
from pisat.handler.pigpio_pwm_handler import PigpioPWMHandler
from pisat.sensor import Bno055, Bme280, SamM8Q, HcSr04

from can09.parent.model import LoggingModel
from can09.parent.nodes import *
from can09.parent.setting import *


# NOTE For test
FallingNode.THRESHOLD_RISING_DETECT = 10        # [m]
FallingNode.THRESHOLD_LANDING_DETECT = 5        # [m]


def main():

    # device setting
    pi = pigpio.pi()
    
    handler_bno055 = PigpioI2CHandler(pi, I2C_ADDRESS_BNO055)
    handler_bme280 = PigpioI2CHandler(pi, I2C_ADDRESS_BME280)
    handler_gps = PyserialSerialHandler(SERIAL_PORT_GPS)
    handler_im920 = PyserialSerialHandler(SERIAL_PORT_IM920)
    
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
    motor_L = BD62xx(handler_motor_L_fin, handler_motor_L_rin, freq=MOTOR_PWM_FREQ, name=NAME_MOTOR_L)
    motor_R = BD62xx(handler_motor_R_fin, handler_motor_R_rin, freq=MOTOR_PWM_FREQ, name=NAME_MOTOR_R)
    wheels = TwoWheels(motor_L, motor_R, name=NAME_WHEELS)

    # transceiver
    im920 = Im920(handler_im920, name=NAME_IM920)

    # sensor
    bno055 = Bno055(handler_bno055, name=NAME_BNO055)
    bme280 = Bme280(handler_bme280, name=NAME_BME280)
    gps = SamM8Q(handler_gps, name=NAME_GPS)
    sonic = HcSr04(handler_sonic_echo, handler_sonic_trig, name=NAME_SUPERSONIC)
    
    con = SensorController(LoggingModel, bno055, bme280, gps, sonic, name=NAME_SENSOR_CONTROLLER)
    que = LogQueue(LoggingModel, maxlen=1000, name=NAME_LOGQUEUE)
    dlogger = DataLogger(con, que, name=NAME_DATA_LOGGER)

    slogger = SystemLogger(name=NAME_SYSTEM_LOGGER)
    slogger.setFileHandler()

    # register callable components in Nodes
    manager = ComponentManager(motor_L, motor_R, wheels, im920, handler_mosfet_para,
                               handler_mosfet_child, handler_led, dlogger, slogger, 
                               recursive=True, name=NAME_MANAGER)

    # context setting
    context = Context({
                        FallingNode:        {True: ParaSeparateNode,    False: FallingNode},
                        ParaSeparateNode:   {True: None,    False: ParaSeparateNode},
                        },
                    start=FallingNode)

    # build a cansat
    cansat = CanSat(context, manager, dlogger=dlogger, slogger=slogger)
    cansat.run()


if __name__ == "__main__":
    main()
