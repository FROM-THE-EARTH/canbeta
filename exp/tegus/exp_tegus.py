

import sys
import time

import pigpio
from pisat.handler import PigpioDigitalOutputHandler

import can09.parent.setting as setting


def main():
    device = sys.argv[1]
    
    pi = pigpio.pi()
    if device == "para":
        handler_mosfet = PigpioDigitalOutputHandler(pi, setting.GPIO_MOSFET_PARA, name=setting.NAME_MOSFET_PARA)
    elif device == "child":
        handler_mosfet = PigpioDigitalOutputHandler(pi, setting.GPIO_MOSFET_CHILD, name=setting.NAME_MOSFET_CHILD)
    else:
        raise ValueError(
            "You must specify 'para' or 'child'."
        )
    
    print("TEGUS TEST")
    print("----------")
    print("NOTE: After start, press Ctrl-C as soon as tegus is melted.", end="\n\n")
    input("Press Enter to start ...")
    
    time_init = time.time()
    try:
        while True:
            handler_mosfet.set_high()
    except KeyboardInterrupt:
        time_finish = time.time()
        handler_mosfet.set_low()
        
    print(f"Result: {time_finish - time_init} [sec]")
    
    
if __name__ == "__main__":
    main()
