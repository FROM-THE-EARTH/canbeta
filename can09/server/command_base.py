
from enum import Enum, auto
from typing import Any

from pisat.comm.transceiver import CommSocket

from can09.server.request import RequestParams


class CommandParams(Enum):
    ARGS_NOTHING = auto()
    ARGS_ARBITARY = auto()


class CommandBase:
    
    COMMAND = b""
    LEN_ARGS = CommandParams.ARGS_NOTHING
    
    @classmethod
    def exec(cls, socket: CommSocket, params: RequestParams) -> Any:
        pass
    
class ResponseBase(CommandBase):
    
    COMMAND = b"FF"
