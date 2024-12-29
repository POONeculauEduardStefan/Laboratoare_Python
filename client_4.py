import socket
import pygame
import numpy as np
import sys
import math

# Culori pentru interfață
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)

def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[ROW_COUNT - 1 - r][c] == 1:  # Inversăm rândurile pentru afisarea corectă
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[ROW_COUNT - 1 - r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def start_client():
    host = '127.0.0.1'  # Adresa IP a serverului (localhost)
    port = 65432         # Portul serverului

    # Creare socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))  # Se conectează la server
        print(f"Conectat la serverul de pe {host}:{port}")

        pygame.init()
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("4 în linie")

        board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
        draw_board(board, screen)
        myfont = pygame.font.SysFont("monospace", 75)

        turn_color = RED  # Default pentru Player 1

        while True:
            # Primește mesaj de la server
            response = client_socket.recv(4096).decode()

            if response.startswith("TABLA"):
                parts = response.split("\n", 1)
                if len(parts) > 1:
                    board = np.array([[int(x) for x in row.split()] for row in parts[1].strip().split("\n")])
                    draw_board(board, screen)
                continue

            print(response)

            if "Ai câștigat!" in response or "Ai pierdut." in response or "Jocul s-a terminat cu remiză!" in response:
                label = myfont.render(response.split("!\n")[0], 1, RED if "Ai câștigat" in response else YELLOW)
                screen.blit(label, (40, 10))
                pygame.display.update()
                pygame.time.wait(3000)
                break

            if "E rândul tău" in response:
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()

                        if event.type == pygame.MOUSEMOTION:
                            posx = event.pos[0]
                            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                            pygame.draw.circle(screen, turn_color, (posx, int(SQUARESIZE / 2)), RADIUS)
                            pygame.display.update()

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            posx = event.pos[0]
                            col = int(math.floor(posx / SQUARESIZE))
                            client_socket.send(str(col).encode())
                            turn_color = YELLOW if turn_color == RED else RED
                            waiting = False

    except ConnectionRefusedError:
        print("Conexiunea a fost refuzată de server.")
    except OSError:
        print("Conexiunea a fost întreruptă de server.")
    finally:
        client_socket.close()
        pygame.quit()
        print("Clientul s-a închis.")

if __name__ == "__main__":
    start_client()
