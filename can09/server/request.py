
from typing import Sequence, Tuple, Union

from pisat.comm.transceiver import CommSocket

from can09.server.command_base import CommandBase


class InvalidRequestError(Exception):
    """Raised if a given request was invalid."""
    pass


class RequestForm:
        
    def __init__(self) -> None:
        self._reception_num: int = None
        self._command: CommandBase = None
        self._size_args: Tuple[int] = ()
        self._args: Tuple[bytes] = ()
        
    @property
    def reception_num(self):
        return self._reception_num
    
    @reception_num.setter
    def reception_num(self, val):
        if isinstance(val, int) and 0 <= val <= 127:
            self._reception_num = val
        else:
            raise ValueError(
                "'reception_num' must be int and 0 <= x <= 127."
            )
            
    @property
    def command(self):
        return self._command
    
    @command.setter
    def command(self, val):
        if issubclass(val, CommandBase):
            self._command = val
        else:
            raise TypeError(
                "'command' must be a subclass of CommandBase."
            )
            
    @property
    def args(self):
        return self._args
    
    @args.setter
    def args(self, val):
        if isinstance(val, (list, tuple)):
            sizes = []
            for arg in val:
                if not isinstance(arg, bytes):
                    raise TypeError(
                        "Each elements of args must be bytes."
                    )
                
                sizes.append(len(arg))
                
            self._size_args = tuple(sizes)
            self._args = tuple(val)
        else:
            raise TypeError(
                "'args' must be a list or tuple."
            )
    
    @property
    def size_args(self):
        return self._size_args


class Request:
    
    FROM_HEX = 16
    TO_HEX = "X"
    
    SEPARATOR = b"$"
    SEPARATOR_NUM = SEPARATOR[0]
    SEMI_SEPARATOR = b":"
    
    LEN_BYTE_HEAD = 4
    
    SC_BIT_REQUEST = 1
    SC_BIT_RESPONSE = 0
    
    
    class RequestParams:
        sc_bit: int = None
        reception_num: int = None
        command: bytes = None
        address: Tuple[bytes] = None
        args: Tuple[bytes] = None

    
    @classmethod
    def make_request(cls, 
                     socket: CommSocket,
                     form: RequestForm) -> bytes:
        data = bytearray()
        
        # head
        data.extend(cls.make_head(form))
        
        # address
        data.extend(cls.make_seq_param(socket, socket.addr_mine))
        data.extend(cls.SEPARATOR)
        
        # sizes of each args
        data.extend(cls.make_seq_param(socket, form.size_args))
        data.extend(cls.SEPARATOR)
        
        # args
        for arg in form.args:
            data.extend(arg)
            
        return bytes(data)
        
    @classmethod
    def make_head(cls, form) -> bytes:
        head = bytearray()
        head.extend(cls.SEPARATOR)
        head.append(0b1000_0000 | form.reception_num)
        head.extend(form.command.COMMAND)
        
        return head
    
    @classmethod
    def make_seq_param(cls, socket: CommSocket, seq: Sequence) -> bytes:
        data = []
        for val in seq:
            if isinstance(val, int):
                val = format(val, cls.TO_HEX)

            data.append(socket.encode(val))
        
        return cls.SEMI_SEPARATOR.join(data)

    @classmethod
    def parse_request(cls, socket: CommSocket):
        sc_bit, reception_num, command = cls.extract_head(socket)
        addr = cls.extract_param(socket).split(cls.SEMI_SEPARATOR)
        addr = tuple(map(bytes, addr))
        size_args_raw = cls.extract_param(socket).split(cls.SEMI_SEPARATOR)
        
        args = []
        for length in map(lambda x: int(x, cls.FROM_HEX), size_args_raw):
            args.append(cls.certain_recv(socket, length))
            
        cls.RequestParams.sc_bit = sc_bit
        cls.RequestParams.reception_num = reception_num
        cls.RequestParams.command = command
        cls.RequestParams.address = addr
        cls.RequestParams.args = tuple(args)
        
        return cls.RequestParams
            
    @staticmethod
    def certain_recv(socket: CommSocket, count: int) -> bytes:
        count_current = 0
        data = bytearray()
        
        while True:
            data.extend(socket.recv(count - count_current))
            count_current = len(data)
            if count_current >= count:
                break
            
        return bytes(data)
        
    @classmethod
    def extract_head(cls, socket: CommSocket) -> Tuple[Union[int, bytes]]:
        
        head = cls.certain_recv(socket, cls.LEN_BYTE_HEAD)
        if head[0] != cls.SEPARATOR_NUM:
            raise InvalidRequestError(
                f"Invalid request was detected. HEAD: {head}"
            )
            
        state = head[1]
        sc_bit = (state & 0b1000_0000) >> 7
        num_reception = state & 0b0111_1111
        command = head[2:]
        
        return (sc_bit, num_reception, command)
    
    @classmethod
    def extract_param(cls, socket: CommSocket) -> bytes:
        data = bytearray()
        while True:
            char = socket.recv(1)
            if char == cls.SEPARATOR:
                break
            
            data.extend(char)
            
        return data
    
    @classmethod
    def reset(cls) -> None:
        cls.RequestParams.sc_bit = None
        cls.RequestParams.reception_num = None
        cls.RequestParams.command = None
        cls.RequestParams.address = None
        cls.RequestParams.args = None
