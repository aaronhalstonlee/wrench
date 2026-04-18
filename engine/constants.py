# engine/constants.py
from enum import Enum, auto

class ResultAction(Enum):
    SHOW_JOB_TICKET = auto()
    SHOW_STATUS = auto()
    SHOW_HELP = auto()
    SHOW_FINDINGS = auto()
