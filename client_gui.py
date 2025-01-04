import tkinter as tk


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

#starts the gui board
def create_gui(rows, cols,set_move_function,player_number):
    global window, canvas,circles,nrows,ncols,set_move_callback,playercolor
    window = tk.Tk()
    window.title("Connect 4")
    nrows=rows
    ncols=cols
    player_num=player_number
    if player_num == 1:
        playercolor = 'red'
    else:
        playercolor = 'yellow'
    set_move_callback = set_move_function
    # Set up the canvas to display the game board
    canvas = tk.Canvas(window, width=cols * 80, height=(rows * 80 + 100), bg="blue")
    canvas.pack()
    canvas.create_rectangle(0, 0, cols * 80, 100, fill="white", outline="white")


    for row in range(rows):
        rowcircles = []
        for col in range(cols):
            # Adjust y-position so circles start below the white space
            x1, y1 = col * 80 + 10, row * 80 + 110  # y-position adjusted for the white space
            x2, y2 = x1 + 60, y1 + 60
            circle = canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black")
            rowcircles.append(circle)
        circles.append(rowcircles)

    canvas.bind("<Motion>", lambda event, canvas=canvas, cols=ncols: on_hover(event, canvas, cols))
    canvas.bind("<Button-1>", lambda event, canvas=canvas, cols=ncols: on_click(event, canvas, cols))

#updates the gui board
def update_circle(row, col, cell_value):
            if cell_value == 1:
                fill_color = "red"
            elif cell_value == 2:
                fill_color = "yellow"
            elif cell_value == 0:
                fill_color = 'white'

            circle = circles[row][col]
            canvas.itemconfig(circle,fill = fill_color)

def update_gui(board):
    for row in range(nrows):
        for col in range(ncols):
            update_circle(row,col,board[row][col])

    window.update()

#handle click
def canmakeamove(val):
    global canmake
    canmake = val
    if val == True :
        show_message("its your turn")
    if val == False:
        canvas.delete(temp_circle)


def on_click(event,canvas,cols):
    if canmake == True :
        col = event.x // 80  # Adjust 100 to the width of your cells
        if set_move_callback:
            set_move_callback(col)


def on_hover(event, canvas, cols):
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
    message_label = canvas.create_text(400, 50, text=message, font=('Helvetica', 24), fill='black')
    canvas.after(2000, canvas.delete, message_label)


# Start the Tkinter event loop
# Example usage: Display a 6x7 board (rows x columns)
def run_gui():
    if window is not None:
        window.mainloop()