
from pisat.comm.transceiver import Im920, SocketTransceiver
from pisat.core.nav import Node

import can09.setting as whole_setting
import can09.parent.setting as parent_setting
from can09.server import Request


class MissionStandbyNode(Node):

    model = None
    
    def enter(self) -> None:
       self.transceiver: SocketTransceiver = self.manager.get_component(parent_setting.NAME_SOCKET_TRANSCEIVER)

    def judge(self, data: None) -> bool:
        socket = self.transceiver.listen()
        if socket is None:
            return False

        params = Request.parse_request(socket)
        
        if socket.addr_yours == whole_setting.ADDR_IM920_CONTROL \
            and params.command == whole_setting.COMMAND_START:
            return True
        else:
            return False
        
    def exit(self) -> None:
        sock2control = self.transceiver.create_socket(whole_setting.ADDR_IM920_CONTROL)
        sock2control.send(Im920.encode("Parent: Exit MissionStandbyNode."))
        