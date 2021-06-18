
from pisat.comm.transceiver import CommSocket

from can09.child.command.logging import current_state, logging_history, logging_state

from can09.server import (
    CommandBase, CommandParams, ResponseBase, 
    Request, RequestForm, RequestParams
)
from can09.util import encode_im920


class RequestStateCommand(CommandBase):
    
    COMMAND = b"RS"
    LEN_ARGS = CommandParams.ARGS_NOTHING
    LEN_RESPONSE = 1

    @classmethod
    def exec(cls, socket: CommSocket, params: RequestParams) -> None:
        
        form = RequestForm()
        form.reception_num = params.reception_num
        form.command = ResponseBase
        logging_history(socket.addr_yours, cls, "")
        
        form.args = (current_state.encode(),)
        data_sending = Request.make_request(socket, form)
        data_sending = encode_im920(data_sending)
        socket.send(data_sending)
