'''
Created on 20.10.2023

@author: beh
'''

from WaterColorPuzzleAfg.search.bfsearch import bfs
from WaterColorPuzzleAfg.search.dfsearch import dfs
from WaterColorPuzzleAfg.game.state import State
import cProfile

# start = State('BFDC','CB  ','DECE','BAB ','ACA ','DF  ','DEF ','AFE ')
# start = State('BFDC','CB','DECE','BAB','ACA','DF','DEF','AFE')
# start = State(0x2643, 0x32, 0x4535, 0x212, 0x131, 0x46, 0x456, 0x165)
# start = State(0xb24 ,0x316 ,0x8243, 0x17c9, 0x359, 0xc867, 0x91, 0x58, 0x71bb, 0x2643, 0x6a4c, 0x95b, 0x8c5a, 0xa2a7) # no goal
start = State.create(4,2,12)
print(f'start = {start}')
    
def runDfs():
    goal  = dfs(start)
    print(f'dfs: goal = {goal}')
    
def runBfs():
    goal  = bfs(start)
    print(f'bfs: goal = {goal}')
    
# f()    
cProfile.run('runDfs()')
cProfile.run('runBfs()')

