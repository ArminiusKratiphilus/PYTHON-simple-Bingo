#Bingo by https://github.com/ArminiusKratiphilus
def imports():
    import tkinter as tk
    from tkinter import ttk
    from random import randrange
    global tk, ttk, randrange

def random_content():
    content = list(new_data)[randrange(len(new_data))]
    new_data.discard(content)
    return content
    
def even_or_odd():
    if (pattern_size % 2) == 0:
        return "even"
    else:
        return "odd"

def even_joker_placement(joker_i,i,j):
    return (   (i == joker_i and i == j)
            or (i == joker_i-1 and i == j)
            or (i == joker_i and i-1 == j)
            or (i == joker_i-1 and i == j-1))
    
def odd_joker_placement(joker_i,i,j):
    return i == joker_i and i == j

def create_grid(frame):
    joker_placement = even_or_odd()
    if joker_placement == "even":
        joker_i = round(0.5*pattern_size)
    if joker_placement == "odd":
        joker_i = round(0.5*(pattern_size-1))
        
    for i in range(pattern_size): #row number
        gridcells.append([])
        for j in range(pattern_size): #column number
            
            if joker:
                if joker_placement == "even":
                    if even_joker_placement(joker_i,i,j):
                        c = cell(frame,i,j,"JOKER")
                    else:
                        c = cell(frame,i,j,random_content())
                
                if joker_placement == "odd":
                    if odd_joker_placement(joker_i,i,j):
                        c = cell(frame,i,j,"JOKER")
                    else:
                        c = cell(frame,i,j,random_content())
                        
            else:
                c = cell(frame,i,j,random_content())
                
            cells.append(c)
            gridcells[i].append(c)
    
def check_grid():
    counter1 = 0
    #checking rows
    for i in range(pattern_size):
        counter0 = 0
        for j in range(pattern_size):
            counter0 += gridcells[i][j].flag
        if counter0 == pattern_size:
            counter1 += 1
    #checking columns
    for i in range(pattern_size):
        counter0 = 0
        for j in range(pattern_size):
            counter0 += gridcells[j][i].flag
        if counter0 == pattern_size:
            counter1 += 1
    #checking primary diagonal
    counter0 = 0
    for i in range(pattern_size):
        counter0 += gridcells[i][i].flag
        if counter0 == pattern_size:
            counter1 += 1
    #checking secondary diagonal
    counter0 = 0
    for i in range(pattern_size):
        counter0 += gridcells[i][pattern_size-i-1].flag
        if counter0 == pattern_size:
            counter1 += 1
            
    if counter1 > 0:
        Bingo = True
        print("Bingo!")
        bingo_message.config(fg=bingo_color)
    else:
        Bingo = False
        bingo_message.config(fg=default_color)

class cell:
    def __init__(self,frame,x,y,content):
        self.x, self.y = x, y
        if content != "JOKER":
            self.flag, self.default_color = 0, "#ffffff"
        else:
            self.flag, self.default_color = 1, "#aaffaa"
        self.frame = tk.Frame(frame, bg=self.default_color)
        self.frame.grid(row=self.x, column=self.y, padx=4, pady=4)
        self.inner_frame = tk.Frame(self.frame, width=120, height=120, bg=self.default_color)
        self.inner_frame.pack()
        self.inner_frame.pack_propagate(0)
        self.label = tk.Label(self.inner_frame, text=content, bg=self.default_color, font=("Arial",10))
        self.label.place(anchor="c", relx=0.5, rely=0.5)
        if content != "JOKER":
            self.frame.bind("<Button-1>", lambda event: self.click(event))
            self.inner_frame.bind("<Button-1>", lambda event: self.click(event))
            self.label.bind("<Button-1>", lambda event: self.click(event))
    def click(self,event):
        if self.flag == 0:
            self.flag = 1
            self.frame.config(bg="#aaffaa")
            self.inner_frame.config(bg="#aaffaa")
            self.label.config(bg="#aaffaa")
            check_grid()
        elif self.flag == 1:
            self.flag = 0
            self.frame.config(bg=self.default_color)
            self.inner_frame.config(bg=self.default_color)
            self.label.config(bg=self.default_color)
            check_grid()
            
def reset():
    global grid_frame
    for c in cells:
        del c
    cells.clear(), gridcells.clear()
    Bingo = False
    grid_frame.destroy()
    
    print("New Game")
    global new_data, pattern_size, joker
    new_data |= database
    grid_frame = tk.Frame(main_frame, bg="#88aabb")
    grid_frame.grid(row=1, column=0, padx=2, pady=2)
    pattern_size = int(pattern_sizer.get())
    joker = joker_var.get()
    create_grid(grid_frame)
    gui.minsize(width=130*pattern_size, height=130*pattern_size+35)
    gui.maxsize(width=130*pattern_size, height=130*pattern_size+35)
    check_grid()
            
if __name__ == "__main__":
    print("New Game")
    imports()
    
    database = set([x+1 for x in list(range(100))])
    
    new_data = set()
    new_data |= database
    default_color, bingo_color = "#ffffff", "#00aa00"
    cells, gridcells = [], []
    Bingo = False
    
    gui = tk.Tk()
    gui.title("BINGO by https://github.com/ArminiusKratiphilus")
    gui.resizable(False, False)
    main_frame = tk.Frame(gui)
    main_frame.pack()
    control_panel = tk.Frame(main_frame)
    control_panel.grid(row=0, column=0)
    grid_frame = tk.Frame(main_frame, bg="#88aabb")
    grid_frame.grid(row=1, column=0, padx=2, pady=2)
    
    pattern_sizer = ttk.Combobox(control_panel, width=5, values=["3","4","5","6","7","8","9","10"])
    pattern_sizer.grid(row=0, column=1, padx=5)
    pattern_sizer.current(2)
    pattern_size = int(pattern_sizer.get())
    
    joker_var = tk.BooleanVar()
    joker_var.set(True)
    joker_check = ttk.Checkbutton(control_panel, text="Joker", variable=joker_var, onvalue=True, offvalue=False)
    joker_check.grid(row=0, column=2, padx=5)
    joker = joker_var.get()
    
    reset_button = ttk.Button(control_panel, text="New Game", padding=3, command=reset)
    reset_button.grid(row=0, column=0, padx=5)
    
    bingo_message = tk.Label(control_panel, text="Bingo!", font=("Arial",20), fg=default_color)
    bingo_message.grid(row=0, column=3, padx=40)
    
    create_grid(grid_frame)
    
    gui.minsize(width=130*pattern_size, height=130*pattern_size+35)
    gui.maxsize(width=130*pattern_size, height=130*pattern_size+35)
    gui.mainloop()