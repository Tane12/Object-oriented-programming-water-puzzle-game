'''
Created on 28 Jan 2024

@author: tanej
'''

import random
from WaterColorPuzzleAfg.game.state import State

def test_state_class():
    # Create a state
    state = State.create(sizeOfTube=4, emptyTubes=2, numColors=5)
    print(f"Initial state: {state}")

    # Test __str__ method
    print(f"String representation of state: {str(state)}")

    # Test __eq__ method
    other_state = State.create(sizeOfTube=4, emptyTubes=2, numColors=5)
    print(f"Are the states equal? {state == other_state}")

    # Test __hash__ method
    print(f"Hash of state: {hash(state)}")

    # Test get method
    print(f"Get color at position (0, 0): {state.get(0, 0)}")

    # Test tubeCount method
    print(f"Number of tubes: {state.tubeCount()}")

    # Test tubeSize method
    print(f"Size of the largest tube: {state.tubeSize()}")

    # Test isGoal method
    print(f"Is the state a goal state? {state.isGoal()}")

    # Test move method
    new_state = state.move(0, 1)
    print(f"State after moving from tube 0 to tube 1: {new_state}")

    # Test children method
    print("Children of the state:")
    for child in state.children():
        print(child)

test_state_class()

        