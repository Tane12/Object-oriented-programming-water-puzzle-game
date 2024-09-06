'''
Depth first search algorithm

Generic algorithm that works on any graph of nodes. The nodes must provide the following instance operations:
- node.isGoal(): returns true if node is a goal of the search
- node.children(): generator (iterator) of all child-nodes that can be reached from node
- node.__eq__(other): equal operator used within the set of visited nodes (node in visited)
- node.__hash__(): must correspond to equal for element testing in set 
- node.parent: the parent node of a node on the search path

Non recursive implementation using built-in list as stack of active nodes.

Created on 17.10.2023
@author: beh
'''

import time

def dfs(start):
    '''
    Start a depth first search on the given node start.
    @param start: the node to start the search
    @return: the goal node if found, None else 
    '''
    stack = list()
    visited = set()
    stack.append(start)
    
    while len(stack) != 0:
        node = stack.pop()
        if not node in visited:
            visited.add(node)
            if node.isGoal():
                return node
            for child in node.children():
                stack.append(child)
        
    return None

def dfsVerbose(start):
    '''
    Start a depth first search on the given node start.
    @param start: the node to start the search
    @return: the goal node if found, None else 
    '''
    start_time = time.time()
    stack = list()
    visited = set()
    stack.append(start)
    steps, sumchild, sumnew, sumvis, sumstack = 0, 0, 0, 0, 0

    goal = None
    while len(stack) != 0:
        steps = steps+1
        sumstack = sumstack+len(stack)
        node = stack.pop()
        sumvis=sumvis+1
        if not node in visited:
            visited.add(node)
            sumnew = sumnew+1
            if node.isGoal():
                goal = node
                break
            for child in node.children():
                sumchild = sumchild+1
                stack.append(child)
        
    end_time = time.time()
    print(f'bfs: start={str(start)}')         
    print(f'bfs: running time={end_time - start_time} s, total expansions={steps}') 
    print(f'bfs: avg number of child={sumchild/steps}, new={sumnew/steps}')
    print(f'bfs: avg size of visited={sumvis/steps}, stacksize={sumstack/steps}')
    print(f'bfs: total child={sumchild}, visited={len(visited)}, last stacksize={len(stack)}')        
    print(f'bfs: goal={str(goal)}, depth={node.depth}')         
    return goal







def backtrack(goal):
    '''
    Backtrack the search tree path from goal to start 
    @param goal: the goal found by dfs()
    @return a list of all nodes back from goal to start; goal first (index=0) 
    '''
    li = []
    while not goal is None:
        li.append(goal)
        goal = goal.parent
    return li



# test code
if __name__ == "__main__":
    # from statefix import State
    # from statevar import State
    from WaterColorPuzzleAfg.game.state import State
    import cProfile
    
    # start = State('BFDC','CB  ','DECE','BAB ','ACA ','DF  ','DEF ','AFE ')
    # start = State('BFDC','CB','DECE','BAB','ACA','DF','DEF','AFE')
    # start = State(0x2643, 0x32, 0x4535, 0x212, 0x131, 0x46, 0x456, 0x165)
    # start = State(0xb24 ,0x316 ,0x8243, 0x17c9, 0x359, 0xc867, 0x91, 0x58, 0x71bb, 0x2643, 0x6a4c, 0x95b, 0x8c5a, 0xa2a7)
    start = State.create(4,2,17)
    
    print(f'start = {start}')
    def f():
        goal  = dfs(start)
        print(f'goal = {goal}')
    
    # f()
    cProfile.run('f()')
