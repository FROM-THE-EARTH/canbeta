
from typing import Tuple

from pisat.core.logger import SystemLogger
from pisat.util.about_time import get_time_stamp

from can09.server.request import CommandBase


# for register states
current_state = ""
FNAME_STATES = get_time_stamp("states", "log")
slogger_states = SystemLogger()
slogger_states.setFileHandler(filename=FNAME_STATES)

# for register communication history
FNAME_COMM_HISTORY = get_time_stamp("comm_history", "log")
slogger_history = SystemLogger()
slogger_states.setFileHandler(filename=FNAME_COMM_HISTORY)


def logging_state(addr: Tuple[str], state: str) -> None:
    global current_state
    slogger_states.info(f"From: {addr}, Exit: {state}")
    current_state = state


def logging_history(addr: Tuple[str], command: CommandBase, msg: str) -> None:
    slogger_history.info(f"From: {addr}, Command: {command.COMMAND.decode()}, Msg: {msg}")
