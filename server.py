import socket
import json
import sys

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 4444))
difficulty = 2

player_type = sys.argv[1]
rows = int(sys.argv[2])
colums = int(sys.argv[3])
if player_type == 'ai':
    firsttoplay = string(sys.argv[4])

if player_type == 'human':
    server_socket.listen(2)
else:
    server_socket.listen(1)

gametable = [[0 for _ in range(colums)] for _ in range(rows)]

client1_socket, client1_adress = server_socket.accept()
print(f"client1 connected")
if player_type == 'human':
    client2_socket, client2_adress = server_socket.accept()
    print(f"client2 connected")

initial_info1 = [rows, colums, 1]
client1_socket.sendall(json.dumps(initial_info1).encode())
if player_type == 'human':
    initial_info2 = [rows, colums, 2]
    client2_socket.sendall(json.dumps(initial_info2).encode())


def checkwin(player_number):
    global rows, colums

    # Helper function to check if 4 in a row starting from (row, col) in a direction
    def check_direction(row, col, delta_row, delta_col):
        count = 0
        for i in range(4):  # Check 4 cells in the given direction
            r, c = row + i * delta_row, col + i * delta_col
            if 0 <= r < rows and 0 <= c < colums and gametable[r][c] == player_number:
                count += 1
            else:
                break
        return count == 4

    # Loop through the board
    for row in range(rows):
        for col in range(colums):
            if gametable[row][col] == player_number:
                # Check all 4 directions
                if (check_direction(row, col, 0, 1) or  # Horizontal
                        check_direction(row, col, 1, 0) or  # Vertical
                        check_direction(row, col, 1, 1) or  # Diagonal positive slope
                        check_direction(row, col, 1, -1)):  # Diagonal negative slope
                    return True
    return False


if player_type == 'human':
    # pvp game
    while True:

        # client 1
        try:
            # send prompt
            info = [1, 2]
            client1_socket.sendall(json.dumps(info).encode())

            # Wait for Client 1's
            data = client1_socket.recv(1024).decode()
            board = json.loads(data)
            gametable = board
            info = [gametable, 0]
            if board:
                client2_socket.sendall(json.dumps(info).encode())
        except Exception as e:
            print(f"Error with Client 1: {e}")
            break

        # check win clien  1
        win = checkwin(1)
        if win == True:
            client1_socket.sendall(json.dumps([1, 1]).encode())
            client2_socket.sendall(json.dumps([0, 1]).encode())
            break

        # client 2
        try:
            # Send prompt to Client 2
            info = [1, 2]
            client2_socket.sendall(json.dumps(info).encode())

            # Wait for Client 2's message
            data = client2_socket.recv(1024).decode()
            board = json.loads(data)
            gametable = board
            info = [gametable, 0]
            if board:
                client1_socket.sendall(json.dumps(info).encode())
        except Exception as e:
            print(f"Error with Client 2: {e}")
            break

        # check win client 2
        win = checkwin(2)
        if win == True:
            client2_socket.sendall(json.dumps([1, 1]).encode())
            client1_socket.sendall(json.dumps([0, 1]).encode())
            break

client1_socket.close()
client2_socket.close()
server_socket.close()
