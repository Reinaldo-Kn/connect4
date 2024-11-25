import socket
import threading
import pygame
import numpy as np
import sys

HOST = '127.0.0.1'
PORT = 65432

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

board = np.zeros((ROW_COUNT, COLUMN_COUNT))
turn = 1  # 0: Client 1, 1: Client 2
game_over = False
lock = threading.Lock()

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def handle_communication(client_socket, screen):
    global turn, game_over
    while not game_over:
        if turn == 0:  # Espera jogada do adversário
            data = client_socket.recv(1024).decode()
            if data:
                row, col = map(int, data.split(","))
                drop_piece(board, row, col, 1)  # Atualiza o tabuleiro com a jogada recebida
                lock.acquire()
                turn = 1
                lock.release()
                draw_board(board, screen)

def main():
    global turn, game_over

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect4 - Client 2")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    threading.Thread(target=handle_communication, args=(client_socket, screen), daemon=True).start()

    draw_board(board, screen)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION and turn == 1:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == 1:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    draw_board(board, screen)

                    # Envia coordenada da jogada ao adversário
                    client_socket.sendall(f"{row},{col}".encode())
                    lock.acquire()
                    turn = 0
                    lock.release()

    client_socket.close()

if __name__ == "__main__":
    main()
