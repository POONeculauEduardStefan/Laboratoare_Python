import socket
import json
import client_gui
import threading


current_move = None
rows = None
colums = None
player_number = None
gametable = None

def rungui():
    client_gui.run_gui()

def set_current_move(col):
    global current_move
    current_move = col

def changeboard(move):
    y = 0
    while gametable[y][move] == 0 :
        y=y+1
        if y == rows :
            break

    gametable[y-1][move] = player_number

def checkifvalid(move):
    if move>=colums :
        return False
    if move <0 :
        return False
    if(gametable[0][move]==0):
        return True;
    else:
        return False;

def gameloop(client_socket):


    global rows, colums, player_number, gametable,current_move

    try:
        while True:
            #recieve message
            data = client_socket.recv(1024).decode()
            try:
                server_message = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                break

            #WIN OR LOSE
            if  server_message[1] == 1 :
                if server_message[0]==1 :
                    client_gui.show_message("you win")
                    break
                else:
                    client_gui.show_message("you lose")
                    break

            # its the players turn
            if server_message[1] == 2:
                client_gui.canmakeamove(True)

                goodmove = False
                while goodmove == False :
                    while current_move is None:
                        pass
                    if(checkifvalid(current_move) != True):
                        client_gui.show_message("move not valid")
                    else:
                        changeboard(current_move)
                        goodmove = True

                client_gui.update_gui(gametable)
                client_socket.sendall(json.dumps(gametable).encode())
                current_move = None
                client_gui.canmakeamove(0)
            #table update
            if server_message[1] == 0:
                gametable = server_message[0]
                client_gui.update_gui(gametable)



    finally:
        client_socket.close()

if __name__ == "__main__":

    server_address = 'localhost'
    server_port = 4444
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, server_port))
    except (socket.error, ConnectionError) as e:
        print(f"connection failed:{e}")

    initial_message = client_socket.recv(1024).decode()
    recieved_list = json.loads(initial_message)
    rows = recieved_list[0]
    colums = recieved_list[1]
    player_number = recieved_list[2]
    client_gui.create_gui(rows, colums, set_current_move,player_number)
    gametable = [[0 for _ in range(colums)] for _ in range(rows)]
    # Start the game loop in a separate thread
    game_thread = threading.Thread(target=gameloop, args=(client_socket,))
    game_thread.start()
    # Start the Tkinter GUI on the main thread
    rungui()
