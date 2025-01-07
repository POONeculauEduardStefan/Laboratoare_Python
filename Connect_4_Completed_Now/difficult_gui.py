import tkinter as tk

root = None
button_press = None
def on_button_click(diff):
    """based on the button pressed this function will change button_press to the difficulty desired"""
    global button_press
    root.destroy()  # Close the window
    button_press = diff

def main():
    """creates the main window"""
    global root,button_press
    root = tk.Tk()
    root.title("Choose Difficulty")
    root.geometry("300x200")  # Set the window size

    """creates and places buttons"""
    easy_button = tk.Button(root, text="Easy", command=lambda: on_button_click(1), width=10)
    easy_button.pack(pady=10)

    medium_button = tk.Button(root, text="Medium", command=lambda: on_button_click(2), width=10)
    medium_button.pack(pady=10)

    hard_button = tk.Button(root, text="Hard", command=lambda: on_button_click(3), width=10)
    hard_button.pack(pady=10)

    # Run the application
    root.mainloop()
    """this returns the difficuly to the server"""
    if button_press != None:
        return button_press
