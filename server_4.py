import socket
import threading
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def format_board(board):
    return '\n'.join([' '.join(map(str, row)) for row in np.flip(board, 0)])

def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def is_board_full(board):
    return not np.any(board == 0)

def handle_game(player1, player2):
    board = create_board()
    game_over = False
    turn = 0

    player1.send("Jocul a început! Ești Player 1 (Piesa: 1)".encode())
    player2.send("Jocul a început! Ești Player 2 (Piesa: 2)".encode())

    while not game_over:
        current_player = player1 if turn == 0 else player2
        opponent = player2 if turn == 0 else player1
        piece = 1 if turn == 0 else 2

        board_state = format_board(board)
        current_player.send(f"TABLA\n{board_state}".encode())
        opponent.send(f"TABLA\n{board_state}".encode())

        current_player.send("E rândul tău. Alege o coloană (0-6): ".encode())
        col = int(current_player.recv(1024).decode())

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)

            if winning_move(board, piece):
                board_state = format_board(board)
                current_player.send(f"TABLA\n{board_state}\nAi câștigat! Felicitări!".encode())
                opponent.send(f"TABLA\n{board_state}\nAi pierdut. Încercați din nou!".encode())
                game_over = True
            elif is_board_full(board):
                board_state = format_board(board)
                player1.send(f"TABLA\n{board_state}\nJocul s-a terminat cu remiză!".encode())
                player2.send(f"TABLA\n{board_state}\nJocul s-a terminat cu remiză!".encode())
                game_over = True
            else:
                turn += 1
                turn %= 2
        else:
            current_player.send("Coloana selectată este invalidă. Încearcă din nou: ".encode())

    player1.close()
    player2.close()

def start_server():
    host = '127.0.0.1'
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"Server pornit pe {host}:{port}")

    player1, addr1 = server_socket.accept()
    print(f"Player 1 conectat de la {addr1}")
    player1.send("Așteptăm un alt jucător...".encode())

    player2, addr2 = server_socket.accept()
    print(f"Player 2 conectat de la {addr2}")
    player1.send("Un alt jucător s-a conectat. Jocul începe!".encode())
    player2.send("Un alt jucător s-a conectat. Jocul începe!".encode())

    handle_game(player1, player2)

    server_socket.close()

if __name__ == "__main__":
    start_server()
