
from pisat.comm.transceiver import CommSocket

from can09.child.command.logging import logging_history, logging_state
from can09.server import (
    CommandBase, ResponseBase, 
    Request, RequestForm, RequestParams
)
import can09.setting as whole_setting
from can09.util import encode_im920


class RegisterStateCommand(CommandBase):

    COMMAND = b"GS"
    LEN_ARGS = 1
    LEN_RESPONSE = 1
    
    RESPONSE_OK = b"OK"
    RESPONSE_NG = b"NG"

    @classmethod
    def exec(cls, socket: CommSocket, params: RequestParams) -> None:
        
        form = RequestForm()
        form.reception_num = params.reception_num
        form.command = ResponseBase
        logging_history(socket.addr_yours, cls, "")    
        
        if socket.addr_yours != whole_setting.ADDR_IM920_PARENT:
            form.args = (cls.RESPONSE_NG,)
        else:
            state = params.args[0].decode()
            logging_state(socket.addr_yours, state)
            form.args = (cls.RESPONSE_OK,)
            
        data_sending = Request.make_request(socket, form)
        data_sending = encode_im920(data_sending)
        socket.send(data_sending)
        