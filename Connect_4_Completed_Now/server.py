import socket
import json
import sys
import aiscript
import random

"""Initialize the server using the socket library"""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost',4444))

"""
Takes arguments from the argument vector:
- player_type: Defines whether the game is "player vs player" or "player vs AI".
- rows: The number of rows on the game board.
- colums: The number of columns on the game board.
- firsttoplay: Defines who plays first in player vs AI mode (either 'player' or 'ai').
"""

player_type = sys.argv[1]
rows = int(sys.argv[2])
colums = int(sys.argv[3])
if player_type == 'ai':
    firsttoplay = sys.argv[4]

"""Connect the number of players needed for a game to start"""
if player_type == 'human':
    server_socket.listen(2)
else:
    server_socket.listen(1)

client1_socket,client1_adress = server_socket.accept()
if player_type == 'human':
    client2_socket,client2_adress = server_socket.accept()


difficulty = None
gametable = [[0 for _ in range(colums)] for _ in range(rows)]

"""Selecting the difficulty for "player vs ai" games """

if player_type == 'ai':
    info = 1
    client1_socket.sendall(json.dumps(info).encode())
    diff = client1_socket.recv(1024).decode()
    difficulty = json.loads(diff)
else:
    info = 0
    client1_socket.sendall(json.dumps(info).encode())

"""Send information to the client for him to build a matrix of the gamestate,the client will update that matrix when moves are made"""
initial_info1 = [rows,colums,1]

client1_socket.sendall(json.dumps(initial_info1).encode())

if player_type == 'human':
    info = 0
    client2_socket.sendall(json.dumps(info).encode())
    initial_info2 = [rows,colums,2]
    client2_socket.sendall(json.dumps(initial_info2).encode())

def checkifdraw(gametable):
    """checks if there are any legal moves that can be made.If every colum has something different than a 0 it means there are no legal moves left"""
    for col in range(colums):
        if gametable[0][col] == 0:
            return 0

    return 1

def checkwin(player_number):
    """function that checks if the player with "player_number" has won based on the gametable,we check for every (row,col) if we have 4 in a row in any of the direction"""
    global rows ,colums
    """Helper function to check if 4 in a row starting from (row, col) in a direction"""

    def check_direction(row, col, delta_row, delta_col):
        count = 0
        for i in range(4):
            r, c = row + i * delta_row, col + i * delta_col
            if 0 <= r < rows and 0 <= c < colums and gametable[r][c] == player_number:
                count += 1
            else:
                break
        return count == 4

    for row in range(0,rows):
        for col in range(0,colums):
            if gametable[row][col] == player_number:
                if (check_direction(row, col, 0, 1) or  # Horizontal
                        check_direction(row, col, 1, 0) or  # Vertical
                        check_direction(row, col, 1, 1) or  # Diagonal positive slope
                        check_direction(row, col, 1, -1)):  # Diagonal negative slope
                    return True
    return False

def playervsplayer():
    """
     this is the main server gameloop for the player vs player case.
     the server:
     -sends updated gameboards to clients.
     -recieves updated gameboards
     -checks for win condition and draws
     """

    global gametable

    while True:

        try:

            info = [1, 2]
            client1_socket.sendall(json.dumps(info).encode())
            data = client1_socket.recv(1024).decode()
            board = json.loads(data)
            gametable = board
            info = [gametable, 0]
            if board:
                client2_socket.sendall(json.dumps(info).encode())
        except Exception as e:
            print(f"Error with Client 1: {e}")
            break
        win = checkwin(1)
        if win == True:
            client1_socket.sendall(json.dumps([1, 1]).encode())
            client2_socket.sendall(json.dumps([0, 1]).encode())
            break

        if checkifdraw(gametable) == 1:
            client2_socket.sendall(json.dumps([2, 1]).encode())
            client1_socket.sendall(json.dumps([2, 1]).encode())

        try:

            info = [1, 2]
            client2_socket.sendall(json.dumps(info).encode())

            data = client2_socket.recv(1024).decode()
            board = json.loads(data)
            gametable = board
            info = [gametable, 0]
            if board:
                client1_socket.sendall(json.dumps(info).encode())
        except Exception as e:
            print(f"Error with Client 2: {e}")
            break

        win = checkwin(2)
        if win == True:
            client2_socket.sendall(json.dumps([1, 1]).encode())
            client1_socket.sendall(json.dumps([0, 1]).encode())
            break

        if checkifdraw(gametable) == 1:
            client2_socket.sendall(json.dumps([2, 1]).encode())
            client1_socket.sendall(json.dumps([2, 1]).encode())

def playervsai():

    """
    this is the main server gameloop in the case of player vs ai.
    the server:
    -It recieves the updated gameboard from the client,
    -runs it through the ai which makes a move and sends it back to the client
    -checks wins and draws
    """
    global gametable

    info = [1, 5]
    client1_socket.sendall(json.dumps(info).encode())
    data = client1_socket.recv(1024).decode()
    board = json.loads(data)
    gametable = board
    if firsttoplay == 'ai':
        col = random.randint(0, colums - 1)
        gametable[rows - 1][col] = 2
        info = [gametable, 0]
        client1_socket.sendall(json.dumps(info).encode())
    while True:

        try:
            info = [1, 2]
            client1_socket.sendall(json.dumps(info).encode())

            data = client1_socket.recv(1024).decode()
            board = json.loads(data)
            gametable = board

        except Exception as e:
            print(f"Error with Client 1: {e}")
            break


        win = checkwin(1)
        if win == True:
            client1_socket.sendall(json.dumps([1, 1]).encode())
            break

        elif checkifdraw(gametable) == 1:
            client1_socket.sendall(json.dumps([2, 1]).encode())
            break

        else:
            gametable = aiscript.solve(gametable, difficulty)
            info = [gametable, 0]
            client1_socket.sendall(json.dumps(info).encode())

            win = checkwin(2)
            if win == True:
                client1_socket.sendall(json.dumps([0, 1]).encode())
                break

            if checkifdraw(gametable) == 1:
                client1_socket.sendall(json.dumps([2, 1]).encode())
                break

if player_type == 'human' :
    playervsplayer()

else:
    playervsai()

"""Close client socket"""
client1_socket.close()
if player_type == 'human':
    client2_socket.close()
server_socket.close()
