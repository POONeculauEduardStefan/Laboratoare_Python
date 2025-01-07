import time
import tkinter as tk
import time

window = None
canvas = None
circles = []
canmake = False
nrows = None
ncols = None
set_move_callback = None
playercolor= None
temp_circle = None
temp_circle_col = None


def create_gui(rows, cols,set_move_function,player_number):

    """Takes the number of rows and columns and creates a window with a board that resembles Connect 4."""

    global window, canvas,circles,nrows,ncols,set_move_callback,playercolor
    window = tk.Tk()
    window.title("Connect 4")
    nrows=rows
    ncols=cols
    player_num=player_number

    """different player_numbers get different colors"""
    if player_num == 1:
        playercolor = 'red'
    else:
        playercolor = 'yellow'

    """function for changing the current_move in client script"""
    set_move_callback = set_move_function

    """Creates a blue table with a white background."""
    canvas = tk.Canvas(window, width=cols * 80, height=(rows * 80 + 100), bg="blue")
    canvas.pack()
    canvas.create_rectangle(0, 0, cols * 80, 100, fill="white", outline="white")

    """fills in white circles where the players pieces will fall.This step will give the table a connect 4 feel"""
    for row in range(rows):
        rowcircles = []
        for col in range(cols):

            x1, y1 = col * 80 + 10, row * 80 + 110
            x2, y2 = x1 + 60, y1 + 60
            circle = canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black")
            rowcircles.append(circle)
        circles.append(rowcircles)

    """Bind the movement and the click to know where the player has clicked"""
    canvas.bind("<Motion>", lambda event, canvas=canvas, cols=ncols: on_hover(event, canvas, cols))
    canvas.bind("<Button-1>", lambda event, canvas=canvas, cols=ncols: on_click(event, canvas, cols))


def update_circle(row, col, cell_value):
            """helper function that changes a circle's color in circles matrix.This will give the efect of a piece being there"""
            if cell_value == 1:
                fill_color = "red"
            elif cell_value == 2:
                fill_color = "yellow"
            elif cell_value == 0:
                fill_color = 'white'

            circle = circles[row][col]
            canvas.itemconfig(circle,fill = fill_color)

def update_gui(board):
    """for a given board it will change all the circles accordingly"""
    for row in range(nrows):
        for col in range(ncols):
            update_circle(row,col,board[row][col])

    window.update()


def canmakeamove(val):
    """the function that enables the player to make a move.It does this by changing the variable "canmake" """
    global canmake
    canmake = val
    if val == False:
        canvas.delete(temp_circle)


def on_click(event,canvas,cols):
    """if canmake is true than the players move is registered and the column he pressed on is remembered"""
    if canmake == True :
        col = event.x // 80
        if set_move_callback:
            set_move_callback(col)


def on_hover(event, canvas, cols):
    """This function will display a circle of the player's color above a column to help the player visualize which column they are selecting."""
    global temp_circle, temp_circle_col
    if canmake:
        col = event.x // 80

        if col != temp_circle_col:
            if temp_circle:
                canvas.delete(temp_circle)

            temp_circle_col = col

            x1, y1 = col * 80 + 10, 20
            x2, y2 = x1 + 60, y1 + 60
            temp_circle = canvas.create_oval(x1, y1, x2, y2, fill=playercolor, outline="black")  # Temporary red circle


def show_message(message):
    """this will show  "message" on the upper right corner"""
    message_label = canvas.create_text(ncols/2*80, 50, text=message, font=('Helvetica', 24), fill='black')
    canvas.after(2000, canvas.delete, message_label)
    window.update()
    time.sleep(1)

def run_gui():
    """this starts the window.mainloop"""
    if window is not None:
        window.mainloop()
def stop_gui():
    """this stops the window"""
    window.destroy()