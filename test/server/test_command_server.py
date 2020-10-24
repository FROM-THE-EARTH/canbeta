
import threading
import time
from typing import Tuple, Any
import unittest

from pisat.comm.transceiver import SocketTransceiver
from pisat.tester.comm import TestTransceiver

from can09.server.command_base import CommandBase, CommandParams
from can09.server.command_server import CommandServer
from can09.server.request import Request, RequestForm


class TestCommand(CommandBase):
    COMMAND = b"AA"
    LEN_ARGS = CommandParams.ARGS_NOTHING
    
    @classmethod
    def exec(cls, params: Tuple[bytes]) -> Any:
        pass
    

def test_decorator(name: str):
    def _test_decorator(func):
        def test(self):
            print(f"\nStart {name}...")
            func(self)
            print(f"... Finish {name}")
        return test
    return _test_decorator


class TestCommandServer(unittest.TestCase):
    
    def setUp(self) -> None:
        
        self.addr_server = (0,)
        self.addr_client = (1,)
        
        self.transceiver_server = TestTransceiver(self.addr_server, name="server")
        self.transceiver_client = TestTransceiver(self.addr_client, name="client")
        self.socket_transceiver_server = SocketTransceiver(self.transceiver_server, name="st_server")
        self.socket_transceiver_client = SocketTransceiver(self.transceiver_client, name="st_client")
        
        self.request = Request
        self.command_server = CommandServer(self.socket_transceiver_server, self.request)
        
        self.command_server.append(TestCommand)
    
    def make_request_form(self) -> RequestForm:
        form = RequestForm()
        form.reception_num = 1
        form.command = TestCommand
        form.args = (b"a", b"b", b"c")
        
        return form
    
    def make_request(self) -> bytes:
        sock = self.socket_transceiver_client.create_socket(self.addr_server)
        form = self.make_request_form()
        return Request.make_request(sock, form)
        
    @test_decorator("test_make_request")
    def test_make_request(self):
        request_ideal = b"$\x81AA1$1:1:1$abc"
        request = self.make_request()
        self.assertEqual(request, request_ideal)
    
    @test_decorator("test_parse_request")
    def test_parse_request(self):
        self.exec_client()
        sock = self.socket_transceiver_server.listen()
        params = self.request.parse_request(sock)
        
        print(f"SC BIT: {params.sc_bit}")
        print(f"RECEPTION NUMBER: {params.reception_num}")
        print(f"COMMAND NAME: {params.command}")
        print(f"ADDRESS: {params.address}")
        print(f"ARGUMENTS: {params.args}")
        
    def exec_client(self):
        
        def _exec_client():
            time.sleep(3)
            request = self.make_request()
            self.socket_transceiver_client.send_raw(self.addr_server, request)
        
        th = threading.Thread(target=_exec_client)
        th.start()
        
    @test_decorator("test_serve")
    def test_serve(self):
        self.exec_client()
        self.command_server.start_serve(timeout=5.)
    
    
if __name__ == "__main__":
    unittest.main()
