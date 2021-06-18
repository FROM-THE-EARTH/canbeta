
from pisat.comm.transceiver import CommSocket

from can09.server import (
    CommandBase, CommandParams, ResponseBase, 
    Request, RequestForm, RequestParams
)


class StartCommand(CommandBase):
    
    COMMAND = b"ST"
    LEN_ARGS = CommandParams.ARGS_NOTHING
    LEN_RESPONSE = 1

    @classmethod
    def exec(cls, socket: CommSocket, params: RequestParams) -> None:
        pass
