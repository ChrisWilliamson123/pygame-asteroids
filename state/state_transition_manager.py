from state.state_type import StateType

def change_state(states, from_state, to_state):
    """Handles logic that needs to be performed as transitions occur between pairs of states"""
    if from_state == StateType.PLAY and to_state == StateType.MAIN_MENU:
        states[StateType.PLAY].reset()
