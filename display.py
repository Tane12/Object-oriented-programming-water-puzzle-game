'''
Canvas to display the water-sort-puzzle and moves.

The generic game-state object must provide the following operations:
- state.tubeSize() 
- state.tubeCount()
- state.get(i, j)        # get the color symbol of tube i at position j
- State.create(n, m, j)  # class method to create a state-object

Created on 20.10.2023
@author: beh
'''

import tkinter as tk

class WaterSortCanvas(tk.Canvas):
    '''
    Canvas to display the water-sort-puzzle
    '''
    # geometric sizes in pixel
    Width  = 40  # width of tube
    Height = 30  # height of color segment
    Gap    = 20  # gap between tubes
    Top    = 60  # padding top, keep some space for arrow 
    Left   = 20  # padding left
    Right  = 20  # padding right
    Bottom = 20  # padding bottom
    # color definitions
    backgroundColor = "black"   # is also empty color
    lineColor       = "beige"    
    waterColors     = ["DeepPink", "DarkOrange", "yellow2", "BlueViolet", "aquamarine", "DarkRed", "CadetBlue", "YellowGreen", 
                       "chocolate", "DarkGrey", "dark magenta", "DarkCyan", "DarkOliveGreen", "SpringGreen", "DeepSkyBlue", "ForestGreen"]
    
    def __init__(self, master, **kwargs):
        '''
        Initialization of an empty display, no color definition 
        '''
        super().__init__(master, **kwargs)
        self.configure(background=WaterSortCanvas.backgroundColor)
        self.colorMap = {}
        
    def initialize(self, state):
        '''
        Complete creation of all graphic elements corresponding to a given game-state
        
        The display is cleared first; then all tubes and their containment - the waterColors - are redrawn. The symbols 
        that appear in the game-state are assigned a unique color and collected in a color map. If the game changes 
        any parameter (number of tubes, tubeSize of tube, number of different waterColors) this method must be called to 
        actualize the display.
        @param state: abstract game state, where symbols represent the waterColors 
        '''
        self.delete("all")
        bg = self["background"]
        self.colorMap = {None:bg}
        m = state.tubeCount()
        w = left + m*width + (m-1)*gap + right
        n = state.tubeSize()
        h = top + n*height + bottom
        self.configure(width=w, height=h)
        for i in range(m):
            self.createTube(state, i, left + i*(width + gap), top)
    
    def createTube(self, state, i, x, yo):
        '''
        Internal operation to draw a single tube
        '''
        n = state.tubeSize()
        y = yo + n*height
        for j in range(n):
            y -= height
            c = state.get(i, j)
            if not c in self.colorMap:
                self.colorMap[c] = WaterSortCanvas.waterColors[(len(self.colorMap)-3) % len(WaterSortCanvas.waterColors)]
            col = self.colorMap[c]
            if j == 0:
                self.create_arc(x, y-height, x+width, y+height, start=180, extent=180, style="pieslice", fill=col, outline=col, width=1, tags=('all',f'tube_{i}',f'rec_{i},{j}'))            
            else:         
                self.create_rectangle(x, y, x+width, y+height, fill=col, outline=col, width=1, tags=('all',f'tube_{i}',f'rec_{i},{j}'))
        col = WaterSortCanvas.lineColor
        yu  = yo+(n-1)*height    
        self.create_line(x,       yo-5, x,       yu, width=3, fill=col, tags=('all',f'tube_{i}'))
        self.create_line(x+width, yo-5, x+width, yu, width=3, fill=col, tags=('all',f'tube_{i}'))
        self.create_arc (x, yu-height, x+width, yu+height, start=180, extent=180, style="arc", fill=None, outline=col, width=3, tags=('all',f'tube_{i}'))
           
    def update(self, state):
        '''
        Update the color distribution after a state change due to filling a color into an other tube. 
        @param state: abstract game state, where symbols represent the waterColors         
        '''
        for i in range(state.tubeCount()):
            for j in range(state.tubeSize()):
                col = self.colorMap[state.get(i,j)]
                self.itemconfig(f'rec_{i},{j}', fill=col, outline=col)
                
    def show(self, fr, to):
        '''
        Show a move - filling of color into an other tube - as arrow
        @param fr: index of tube (0, 1 ...) from which the color is taken
        @param to: index of tube into that color is filled in 
                if fr == to the arrow is deleted
        '''
        self.delete("arrow")
        if fr == to:
            return
        dx = width//2
        x1 = left + fr*(width+gap) + dx
        x2 = left + to*(width+gap) + dx
        y0 = top//4
        y1 = top*3//4
        dx = dx if fr < to else -dx
        col = WaterSortCanvas.lineColor
        self.create_line(x1,    y1, x1+dx, y0, width=3, fill=col, tags=('all','arrow'))
        self.create_line(x1+dx, y0, x2-dx, y0, width=3, fill=col, tags=('all','arrow'))
        self.create_line(x2-dx, y0, x2,    y1, width=3, fill=col, arrow='last', tags=('all','arrow'))

# abbreviated alias names 
width  = WaterSortCanvas.Width
height = WaterSortCanvas.Height
gap    = WaterSortCanvas.Gap
top    = WaterSortCanvas.Top
left   = WaterSortCanvas.Left
right  = WaterSortCanvas.Right
bottom = WaterSortCanvas.Bottom


         

if __name__ == "__main__":
    from WaterColorPuzzleAfg.game.state import State 

    t = [chr(ord("A")+i)*6 for i in range(16)]
    t = t+[' '*6]*2
    s = State(size=6, *t)
    
    # s = State.create(4,2,5)
    s = State('AABC', 'BC', 'CBBA', 'CA', size=4)   
    c = list(s.children()) 
   
    print(f"number of children n={len(c)}")
            
    root = tk.Tk()
    root.title("Water Sort Puzzle")
    canvas = WaterSortCanvas(root)
    canvas.pack()
    canvas.initialize(s)
    canvas.show(0,0)

    root.mainloop()
