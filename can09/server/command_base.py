
from enum import Enum, auto
from typing import Any, Tuple


class CommandParams(Enum):
    ARGS_NOTHING = auto()
    ARGS_ARBITARY = auto()


class CommandBase:
    
    COMMAND = b""
    LEN_ARGS = CommandParams.ARGS_NOTHING
    
    @classmethod
    def exec(cls, params: Tuple[bytes]) -> Any:
        pass
