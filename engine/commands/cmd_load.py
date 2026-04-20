import json
from .shared import Result
from engine.state import GameState

def cmd_load(args, state):
    filename = "savegame.json"
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        new_state = GameState.from_dict(data)
        
        return Result("__LOAD_STATE__", finding=new_state)
    
    except FileNotFoundError:
        return Result("No save file found :(...")