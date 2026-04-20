import json
from .shared import Result

def cmd_save(args, state):
    filename = "savegame.json"
    with open(filename, "w") as f:
        json.dump(state.to_dict(), f, indent=2)
    
    return Result(f"Game saved to {filename}.")