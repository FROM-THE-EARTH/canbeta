

import codecs
import sys

from pisat.handler import PyserialSerialHandler
from pisat.comm.transceiver import Im920, SocketTransceiver

from can09.child.command import StartCommand
import can09.control.setting as control_setting
from can09.server import RequestForm, Request
import can09.setting as whole_setting


NAME_CHILD = "child"
NAME_PARENT = "parent"


def main():
    device = sys.argv[1]
    if device not in (NAME_CHILD, NAME_PARENT):
        raise ValueError(
            "The argument must be 'child' or 'parent'."
        )
    
    handler = PyserialSerialHandler(control_setting.SERIAL_PORT, control_setting.BAUDRATE_IM920)
    im920 = Im920(handler, name=control_setting.NAME_IM920)
    transceiver = SocketTransceiver(im920, certain=True)
    
    if device == NAME_CHILD:
        socket = transceiver.create_socket(whole_setting.ADDR_IM920_CHILD)
    else:
        socket = transceiver.create_socket(whole_setting.ADDR_IM920_PARENT)
        
    form = RequestForm()
    form.reception_num = 100
    form.command = StartCommand
    
    data_sending = Request.make_request(socket.addr_mine, form)
    print(data_sending)
    data_sending = codecs.encode(data_sending, whole_setting.ENCODING_IM920)
    
    socket.send(data_sending)
    
    
if __name__ == "__main__":
    main()
