'''
Representation of a game state of the color-sort-puzzle

Class-Template to implement a game-state.
An implementation can use any data-type to represent the different colors. But as usual the different colors can be 
enumerated and are limited.

Examples for State representations:
(1,2,2,0,0); "AB  "; (Color.Cy, Color.Mg, Color.Bl, None) 

Created on 12.10.2022
@author: beh
@copyright: Manfred Beham at OTH Amberg-Weiden
@version: 1.0
'''

import random

class State(object):
    '''
    Object representing a puzzle state, that is the color distribution in different tubes.
    Implementation as an immutable tuple of any data-type
    @ivar parent: parent state from which this state was created, default: None
    @ivar action: the action (a tuple of two tube-indexes:(from, to)) applied to the parent state and results in this node
    @ivar depth: numbering of moves from start state until goal state
    '''
    def __init__(self, *tubes, size):
        '''
        Constructor of a game's state given a tuple of any tubes
        '''
        self.parent = None
        self.action = None
        self.depth  = 0
        self.tubes = [list(tube) for tube in tubes]
        assert len(tubes)>=2
        self.size = size
    
    def __str__(self):
        '''
        String representation of this state.
        '''
        return '(' + ', '.join(f"{tube}" for tube in self.tubes) + ')'
    
    def __eq__(self, other):
        '''
        Checks two color-states if they are equal, not concerning the order of the tubes 
        '''
        return sorted(self.tubes) == sorted(other.tubes)

    def __hash__(self):
        '''
        Calculates a hash-value of the color-state, the order of the tubes is ignored 
        '''
        return hash(tuple(sorted(tuple(tube) for tube in self.tubes)))

    def get(self, i, j):
        '''
        Return the color symbol of tube i at position j. If position is empty, None is returned.
        @param i: tube index 0, 1, ... tubeCount()-1
        @param j: position index 0, 1, ... tubeSize()-1
        @return: corresponding color symbol; or None if empty
        @raise IndexError: if index i or j is out of range
        '''
        assert i < len(self.tubes)
        tube = self.tubes[i]
        if j<len(tube):
            return self.tubes[i][j]
        else:
            return None

    def tubeCount(self):
        '''
        Return the total number of tubes.
        '''
        return len(self.tubes)

    def tubeSize(self):
        '''
        Get the maximum number of color segments within a tube.
        '''
        return max(len(tube) for tube in self.tubes)
        
    def isGoal(self):
        '''
        Check if all tubes are completely filled with the same color or empty
        '''
        return all(isSingleChar(tube) for tube in self.tubes)

    def move(self, i, j):
        '''
        Fill one amount of water-color from tube i into tube j.
        Or fill complete color segments of the same color from i to j.
        '''
        if not (0 <= i < len(self.tubes) and 0 <= j < len(self.tubes) and i != j):
            raise ValueError("Invalid move: Tube indices out of range or equal.")
        
        frTube = list(self.tubes[i])
        toTube = list(self.tubes[j])

        if len(frTube) > 0 and (len(toTube) == 0 or frTube[-1] == toTube[-1]):
            color = frTube.pop()
            toTube.append(color)

        new_tubes = list(self.tubes)
        new_tubes[i] = tuple(frTube)
        new_tubes[j] = tuple(toTube)

        new_state = State(*new_tubes, size=self.size)
        new_state.parent = self
        new_state.action = (i, j)
        new_state.depth = self.depth + 1
        return new_state
                      
    def children(self):
        '''
        Generates all possible successor states by filling water-colors from tube i to tube j, if possible. 
        Generator method that yields a sequence of successor states given a current state (self) 
        '''
        empty_tubes = [i for i in range(len(self.tubes)) if len(self.tubes[i]) == 0]
        non_empty_tubes = [i for i in range(len(self.tubes)) if len(self.tubes[i]) > 0]
    
    # Prioritize moving to empty tubes
        for i in non_empty_tubes:
            for j in empty_tubes:
                yield self.move(i, j)
    
    # Then move to tubes with the same color on top
        for i in non_empty_tubes:
            for j in non_empty_tubes:
                if i != j and self.tubes[i][-1] == self.tubes[j][-1]:
                    yield self.move(i, j)
    
    # Finally, consider all other moves
        for i in non_empty_tubes:
            for j in non_empty_tubes:
                if i != j and self.tubes[i][-1] != self.tubes[j][-1]:
                    yield self.move(i, j)
    
    
    @classmethod
    def create(cls, sizeOfTube, emptyTubes, numColors):
        '''
    Create a new game state randomly that uses the given parameter
    @param sizeOfTube: maximum number of color segments within a single tube (height)
    @param emptyTubes: number of empty tubes
    @param numColors: total number of different colors
    @return: a random game state  
    '''
    # Create a list of all possible colors
        all_colors = [chr(ord('A') + i) for i in range(numColors)]
    
    # Create a string of all colors and empty spaces
        colors_string = ''.join(all_colors) + (" " * emptyTubes)
    
    # Repeat the string to fill all tubes
        colors_string *= sizeOfTube
    
    # Convert the string to a list and shuffle it
        all_colors = list(colors_string)
        random.shuffle(all_colors)
    
    # Divide the shuffled list into tubes
        tubes_list = [''.join(all_colors[i:i+sizeOfTube]) for i in range(0, len(all_colors), sizeOfTube)]
    
        return cls(*tubes_list, size=sizeOfTube)

    
def isSingleChar(text):
    return all(text[ch] == text[0] for ch in range(1, len(text)))

state = State.create(sizeOfTube=4, emptyTubes=2, numColors=5)
print(state)
