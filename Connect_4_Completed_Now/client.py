import socket
import json
import client_gui
import difficult_gui
import threading
import time

current_move = None
rows = None
colums = None
player_number = None
gametable = None
difficulty = None


def rungui():
    """Runs the gui for the game.Its the part that shows the gametable to the player"""
    client_gui.run_gui()

def set_current_move(col):
    """this function is passed down to the client_gui/create_gui.This enables the client_gui script to change the current_move variable in this script."""
    global current_move
    current_move = col

def changeboard(move):
    """functiont that handles the logic of droping a piece on the table"""
    y = 0
    while gametable[y][move] == 0 :
        y=y+1
        if y == rows :
            break

    gametable[y-1][move] = player_number

def checkifvalid(move):
    """function that checks if the move is valid.It checks if the row is full or the position the piece is being droped is within the colums available"""
    if move>=colums :
        return False
    if move <0 :
        return False
    if(gametable[0][move]==0):
        return True;
    else:
        return False;

def gameloop(client_socket):
    """
    this is the main game loop for the client.It works by listening to a message given by the server.
    Depending on the server message the client can:
    -for the code '0': the server has sent an updated gametable with the opponent's move. It updates his own gametable and updates the gui's gametable for it to be shown.
    -for the code '1': this is the win,lose or draw message. This will use a function the the clinet_gui to show a message with the appropriate message.
    -for the code '2': this means its the players turn to make a move:
                      -it will call the function "canmakeamove" that makes the cliks of the player record the column he clicked on.
                      -it will wait for the player to make a move and check if the move:
                                            -if the move is legal it will update the gameboard with that move using changeboard.
                                            -if the move is ilegal it will wait for another move.
                      -it will send the updated gameboard back to the server.

    -for the code '5': this will send the curent gametable of the client to the server.

    the codes mentioned above are the second element of the vector of the server message.
    """

    global rows, colums, player_number, gametable,current_move

    try:
        while True:
            """recieve message"""
            data = client_socket.recv(1024).decode()
            try:
                server_message = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                break

            """ code '0' """
            if server_message[1] == 0:
                gametable = server_message[0]
                client_gui.update_gui(gametable)

            """ code '1' """
            if  server_message[1] == 1 :
                if server_message[0]==1 :
                    client_gui.show_message("you win")
                    break
                if server_message[0]==0:
                    client_gui.show_message("you lose")
                    break
                else:
                    client_gui.show_message("draw")
                    break

            """ code '2' """
            if server_message[1] == 2:
                client_gui.canmakeamove(True)

                goodmove = False
                while goodmove == False :
                    while current_move is None:
                        pass
                    if(checkifvalid(current_move) != True):
                        client_gui.show_message("move not valid")
                        current_move=None
                    else:
                        changeboard(current_move)
                        goodmove = True

                client_gui.update_gui(gametable)
                client_socket.sendall(json.dumps(gametable).encode())
                current_move = None
                client_gui.canmakeamove(0)
            """ code '5' """
            if server_message[1] == 5:
                client_socket.sendall(json.dumps(gametable).encode())

    finally:
        """Close the connection after the game is finnished"""
        client_socket.close()
        time.sleep(2)
        client_gui.stop_gui()

if __name__ == "__main__":

    """connect to the server"""
    server_address = 'localhost'
    server_port = 4444
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, server_port))
    except (socket.error, ConnectionError) as e:
        print(f"connection failed:{e}")

    """difficulty gui"""
    is_ai = client_socket.recv(2048).decode()
    is_ai1 = json.loads(is_ai)
    if is_ai1 == 1:
        diff = difficult_gui.main()
        client_socket.sendall(json.dumps(diff).encode())

    """initial message from the server for size of gametable and player_number"""
    initial_message = client_socket.recv(2048).decode()
    recieved_list = json.loads(initial_message)
    rows = recieved_list[0]
    colums = recieved_list[1]
    player_number = recieved_list[2]

    """we create the client_gui to show the board"""
    client_gui.create_gui(rows, colums, set_current_move,player_number)
    gametable = [[0 for _ in range(colums)] for _ in range(rows)]

    """the gameloop function is handled in a different thread.Comunication with the server needs to work while the main thread show the client gui"""
    game_thread = threading.Thread(target=gameloop, args=(client_socket,), daemon=True)
    game_thread.start()

    """it runs the tkinter gui on the main thread"""
    rungui()
