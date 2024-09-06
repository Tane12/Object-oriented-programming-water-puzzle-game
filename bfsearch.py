'''
Breadth first search algorithm

Generic algorithm that works on any graph of nodes. The nodes must provide the following instance operations:

- node.isGoal():       returns true if node is a goal of the search
- node.children():     generator of all child-nodes that can be reached from node
- node.__eq__(other):  equal operator used within the set of visited nodes (node in visited)
- node.__hash__():     must correspond to equal for element testing in set 
- node.parent:         the parent node of a node on the search path; only for backtracking

Implementation using SimpleQueue as FIFO for active nodes.

Created on 17.10.2023
@author: beh
'''

from queue import SimpleQueue
import time

def bfs(start):
    '''
    Start a breadth first search on the given node start.
    @param start: the node to start the search
    @return: the goal node if found, None else 
    '''
    explored = SimpleQueue() # FIFO queue for explored but not finished nodes; boarder of explored area
    visited = set()          # SET of any seen nodes; node must define __eq__ and __hash__    
    explored.put(start)       
    visited.add(start)  
    
    while not explored.empty():
        node = explored.get()    
        if node.isGoal():
            return node
        for child in node.children():
            if not child in visited:       
                # child.parent = node
                explored.put_nowait(child) 
                visited.add(child)
    return None

def backtrack(goal):
    '''
    Backtrack the search tree path from goal to start 
    @param goal: the goal found by bfs()
    @return a list of all nodes back from goal to start; goal first (index=0) 
    '''
    li = []
    while not goal is None:
        li.append(goal)
        goal = goal.parent
    return li



def bfsVerbose(start):
    '''
    Version of bfs that collects some statistical data during search; for testing only
    '''
    start_time = time.time()
    explored = SimpleQueue()  
    visited = set()           
    explored.put(start)       
    visited.add(start)  
    
    steps, sumchild, sumnew, sumvis, sumexp = 0, 0, 0, 0, 0
    while not explored.empty():
        node = explored.get()    
        if node.isGoal():
            end_time = time.time()
            print(f'bfs: start={str(start)}')         
            print(f'bfs: running time={end_time - start_time} s, total expansions={steps}') 
            print(f'bfs: avg number of child={sumchild/steps}, new={sumnew/steps}')
            print(f'bfs: avg size of visited={sumvis/steps}, qsize={sumexp/steps}')
            print(f'bfs: total child={sumchild}, visited={len(visited)}, last qsize={explored.qsize()}')        
            print(f'bfs: goal={str(node)}, depth={node.depth}')         
            return node
        n,m = 0,0
        for child in node.children():
            n += 1
            if not child in visited:       
                # child.parent = node
                m += 1
                explored.put_nowait(child) 
                visited.add(child)
        sumchild += n
        sumnew += m
        sumvis += len(visited)
        sumexp += explored.qsize()
        steps += 1
        # print(f'bfs: step={steps}, child={n}, new={m}, total={sumchild}, vis={len(visited)}, expsize={explored.qsize()}')
    print(f'bfs: start={str(start)} search failed')         
    return None

# test code
if __name__ == "__main__":
    # from statefix import State
    # from statevar import State
    from WaterColorPuzzleAfg.game.state import State
    import cProfile
    
    #start = State('BFDC','CB  ','DECE','BAB ','ACA ','DF  ','DEF ','AFE ')
    # start = State('BFDC','CB','DECE','BAB','ACA','DF','DEF','AFE')
    start = State(0x2643, 0x32, 0x4535, 0x212, 0x131, 0x46, 0x456, 0x165)
    # start = State.create(4,2,12)
    
    def f():
        print(f'start = {start}')
        goal  = bfsVerbose(start)
        print(f'goal = {goal}')
        
    cProfile.run('f()')
