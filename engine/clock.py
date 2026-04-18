from engine.state import GameState

def advance(state: GameState, minutes: int) -> None:
    state.time_minutes += minutes