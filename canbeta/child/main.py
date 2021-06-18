

import pigpio

from pisat.comm.transceiver import Im920, SocketTransceiver
from pisat.core.cansat import CanSat
from pisat.core.nav import Context
from pisat.core.manager import ComponentManager
from pisat.core.logger import (
    DataLogger, LogQueue, SystemLogger
)
from pisat.handler import (
    PigpioI2CHandler, PyserialSerialHandler, PigpioDigitalOutputHandler
)
from pisat.sensor import Bme280, Opt3002, SamM8Q

from can09.child.model import ChildLoggingModel
from can09.child.nodes import *
from can09.child.setting import * 


def run_child():
    pi = pigpio.pi()
    
    # handlers
    handler_bme280 = PigpioI2CHandler(pi, I2C_ADDRESS_BME280)
    handler_opt3002 = PigpioI2CHandler(pi, I2C_ADDRESS_OPT3002)
    handler_gps = PyserialSerialHandler(SERIAL_PORT_GPS, BAUDRATE_GPS)
    handler_im920 = PyserialSerialHandler(SERIAL_PORT_IM920, BAUDRATE_IM920)
    handler_led = PigpioDigitalOutputHandler(pi, GPIO_LED, name=NAME_LED)
    
    # sensors
    bme280 = Bme280(handler_bme280, name=NAME_BME280)
    opt3002 = Opt3002(handler_opt3002, name=NAME_OPT3002)
    gps = SamM8Q(handler_gps, name=NAME_GPS)
    
    # transceiver
    im920 = Im920(handler_im920, name=NAME_IM920)
    socket_transceiver = SocketTransceiver(im920, certain=True, name=NAME_SOCKET_TRANSCEIVER)
    
    # logger
    que = LogQueue(ChildLoggingModel, maxlen=5000, name=NAME_LOGQUEUE)
    dlogger = DataLogger(que, bme280, opt3002, gps, name=NAME_DATA_LOGGER)
    
    slogger = SystemLogger(name=NAME_SYSTEM_LOGGER)
    slogger.setFileHandler()
    
    manager = ComponentManager(handler_led, im920, socket_transceiver, dlogger,
                               recursive=True, name=NAME_MANAGER)
    
    context = Context({
                        MissionStandbyNode: {True: ChildServerNode, False: MissionStandbyNode},
                        ChildServerNode:    {True: None,            False: ChildServerNode}
                      },
                      start=MissionStandbyNode)
    
    cansat = CanSat(context, manager, dlogger=dlogger, slogger=slogger)
    cansat.run()


if __name__ == "__main__":
    run_child()