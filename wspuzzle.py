'''
Main module to create a puzzle and start the solver for the water-sort-puzzle

Created on 24.10.2023

@author: beh
'''


import tkinter as tk
from tkinter import ttk

from WaterColorPuzzleAfg.view.display import WaterSortCanvas
from WaterColorPuzzleAfg.game.state import State
from WaterColorPuzzleAfg.search.dfsearch import dfsVerbose, backtrack

start = None
solution = []

def solve():
    '''
    Command for button 'solve'
    '''
    global solution, start, canvas
    # print(f"solve called: solution length={len(solution)}")
    if len(solution) == 0:
        return
    # show solution
    canvas.update(solution.pop())
    if solution:
        nx = solution[-1]
        canvas.show(*nx.action)
    else:
        canvas.show(0, 0)
       
def create():
    
    '''Command for button 'shuffle'''
    
    global solution, start, canvas
    # TODO: replace by your own implementation of State
    start = State.create(5, 2, 8)
    canvas.initialize(start)
    canvas.show(0, 0)
    goal = dfsVerbose(start)
    solution = backtrack(goal)


root = tk.Tk()
root.title("Water Sort Puzzle")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1) 
mainframe.rowconfigure(0, weight=1)

canvas = WaterSortCanvas(mainframe)
canvas.grid(column=0, row=0, columnspan=2, sticky=('N', 'W', 'E', 'S'))
create()

ttk.Button(mainframe, text="Shuffle", command=create).grid(column=0, row=1)
ttk.Button(mainframe, text="Solve", command=solve).grid(column=1, row=1)

root.mainloop()
