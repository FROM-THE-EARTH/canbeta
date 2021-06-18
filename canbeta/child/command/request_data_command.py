
from pisat.comm.transceiver import CommSocket

from can09.server import (
    CommandBase, CommandParams, ResponseBase, 
    Request, RequestForm, RequestParams
)


class RequestDataCommand(CommandBase):
    COMMAND = b"RD"
    # TODO
    LEN_ARGS = CommandParams

    # TODO
    @classmethod
    def exec(cls, socket: CommSocket, params: RequestParams) -> None:
        pass
