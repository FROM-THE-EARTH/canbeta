

from pisat.handler import PyserialSerialHandler
from pisat.comm.transceiver import Im920

import can09.control.setting as control_setting
import can09.setting as whole_setting


def main():
    handler = PyserialSerialHandler(control_setting.SERIAL_PORT, control_setting.BAUDRATE_IM920)
    im920 = Im920(handler, name=control_setting.NAME_IM920)
    
    print(f"Listen Start from ID: {im920.id}", end="\n\n")    
    
    try:
        while True:
            if len(im920.buf):
                raw = im920.recv_raw()
                print(raw)
                if len(raw) == 2:
                    addr, data = raw
                    data = data.decode()
                    
                    device = ""
                    if addr == whole_setting.ADDR_IM920_CHILD:
                        device = "CHILD"
                    if addr == whole_setting.ADDR_IM920_PARENT:
                        device = "PARENT"
                        
                    if device:
                        print(f"from {device}: {data}")
    except KeyboardInterrupt:
        handler.close()


if __name__ == "__main__":
    main()
