

import time
import threading

from pisat.comm.transceiver import Im920, SocketTransceiver
from pisat.core.nav import Node
from pisat.core.logger import DataLogger

from can09.child.command import *
import can09.child.setting as child_setting
from can09.server import CommandServer, Request
import can09.setting as whole_setting


class ChildServerNode(Node):
    
    INTERVAL_LOGGING = 1        # [sec]
    TIMEOUT_SERVER = 30 * 60    # [sec]
    
    def enter(self) -> None:
        self.continue_logging = True
        
        self.transceiver: SocketTransceiver = self.manager.get_component(child_setting.NAME_SOCKET_TRANSCEIVER)
        self.dlogger: DataLogger = self.manager.get_component(child_setting.NAME_DATA_LOGGER)
        
        server = CommandServer(self.transceiver, Request)
        server.append(RegisterStateCommand, RequestDataCommand, RequestStateCommand)
        
        thread = threading.Thread(target=self.logging)
        
        thread.start()
        server.start_serve(timeout=self.TIMEOUT_SERVER)
        
        self.continue_logging = False
        thread.join()
        
    def judge(self, data: None) -> bool:
        return True
    
    def logging(self):
        while self.continue_logging:
            self.dlogger.read()
            time.sleep(self.interval)
            
    def exit(self) -> None:
        sock = self.transceiver.create_socket(whole_setting.ADDR_IM920_CONTROL)
        sock.send(Im920.encode("Child: Exit ChildServerNode."))
