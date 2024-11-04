#create connect4 game between two players
import numpy as np
import pygame
import sys
import math , time
import os

# Inicializar Pygame e o mixer para tocar música
pygame.init()
pygame.mixer.init()

# Caminho para o arquivo de música
music_path = os.path.join("soundtrack", "background.mp3")
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1) 
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (board[r][c] == piece and
                board[r][c + 1] == piece and
                board[r][c + 2] == piece and
                board[r][c + 3] == piece):
                return [(r, c), (r, c + 1), (r, c + 2), (r, c + 3)]
    
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and
                board[r + 1][c] == piece and
                board[r + 2][c] == piece and
                board[r + 3][c] == piece):
                return [(r, c), (r + 1, c), (r + 2, c), (r + 3, c)]
    
    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and
                board[r + 1][c + 1] == piece and
                board[r + 2][c + 2] == piece and
                board[r + 3][c + 3] == piece):
                return [(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)]
    
    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == piece and
                board[r - 1][c + 1] == piece and
                board[r - 2][c + 2] == piece and
                board[r - 3][c + 3] == piece):
                return [(r, c), (r - 1, c + 1), (r - 2, c + 2), (r - 3, c + 3)]

    return None  # No win

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
    
board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(posx // SQUARESIZE)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                if turn == 0:
                    drop_piece(board, row, col, 1)

                    # Check for Player 1 win
                    if winning_move(board, 1):
                        small_font = pygame.font.SysFont("monospace", 50)
                        label = small_font.render("Jogador 1 ganhou!", 1, RED)
                        
                        winning_coords = winning_move(board, 1)  # Get the winning coordinates
                        # Draw a line connecting the winning pieces
                        draw_board(board)

                        pygame.draw.line(
                            screen, BLACK,
                            (winning_coords[0][1] * SQUARESIZE + SQUARESIZE // 2, height - (winning_coords[0][0] * SQUARESIZE + SQUARESIZE // 2)),
                            (winning_coords[-1][1] * SQUARESIZE + SQUARESIZE // 2, height - (winning_coords[-1][0] * SQUARESIZE + SQUARESIZE // 2)),
                            10  # Line thickness
                        )
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True
                        colors = [
                                    (255, 0, 0),   # Vermelho
                                    (0, 255, 0),   # Verde
                                    (255, 255, 0), # Amarelo
                                    (255, 0, 255), # Magenta
                                    (0, 255, 255), # Ciano
                                    (255, 165, 0), # Laranja
                                    (75, 0, 130),  # Índigo
                                    (238, 130, 238), # Violeta
                                    (128, 0, 128), # Roxo
                                    (0, 128, 128), # Verde-azulado
                                    (255, 105, 180) # Rosa choque
                                ]  
                        color_index = 0
                        game_over = True
                        start_time = time.time()  # Marque o tempo de início
                        
                        # Loop de piscagem com duração de 5 segundos
                        while game_over and time.time() - start_time < 5:
                            # Alterne a cor das peças vencedoras
                            for coord in winning_coords:
                                row, col = coord
                                pygame.draw.circle(
                                    screen, colors[color_index],
                                    (col * SQUARESIZE + SQUARESIZE // 2, height - (row * SQUARESIZE + SQUARESIZE // 2)),
                                    RADIUS
                                )
                            
                            pygame.display.update()
                            pygame.time.delay(500)  # Controle a velocidade da piscagem

                            # Alterne para a próxima cor
                            color_index = (color_index + 1) % len(colors)
                            
                            # Verifique eventos para permitir sair do loop, como o fechamento da janela
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    game_over = False
    

                else:
                    drop_piece(board, row, col, 2)

                    # Check for Player 2 win
                    if winning_move(board, 2):
                        small_font = pygame.font.SysFont("monospace", 50)
                        label = small_font.render("Jogador 2 ganhou!", 1, YELLOW)
                        winning_coords = winning_move(board, 2)  # Get the winning coordinates
                        draw_board(board)

                        pygame.draw.line(
                            screen, BLACK,
                            (winning_coords[0][1] * SQUARESIZE + SQUARESIZE // 2, height - (winning_coords[0][0] * SQUARESIZE + SQUARESIZE // 2)),
                            (winning_coords[-1][1] * SQUARESIZE + SQUARESIZE // 2, height - (winning_coords[-1][0] * SQUARESIZE + SQUARESIZE // 2)),
                            10  # Line thickness
                        )
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        
                        game_over = True
                        colors = [
                                    (255, 0, 0),   # Vermelho
                                    (0, 255, 0),   # Verde
                                    (255, 255, 0), # Amarelo
                                    (255, 0, 255), # Magenta
                                    (0, 255, 255), # Ciano
                                    (255, 165, 0), # Laranja
                                    (75, 0, 130),  # Índigo
                                    (238, 130, 238), # Violeta
                                    (128, 0, 128), # Roxo
                                    (0, 128, 128), # Verde-azulado
                                    (255, 105, 180) # Rosa choque
                                ]  
                        color_index = 0
                        
                        start_time = time.time()  # Marque o tempo de início
                        
                        # Loop de piscagem com duração de 5 segundos
                        while game_over and time.time() - start_time < 5:
                            # Alterne a cor das peças vencedoras
                            for coord in winning_coords:
                                row, col = coord
                                pygame.draw.circle(
                                    screen, colors[color_index],
                                    (col * SQUARESIZE + SQUARESIZE // 2, height - (row * SQUARESIZE + SQUARESIZE // 2)),
                                    RADIUS
                                )
                            
                            pygame.display.update()
                            pygame.time.delay(500)  # Controle a velocidade da piscagem

                            # Alterne para a próxima cor
                            color_index = (color_index + 1) % len(colors)
                            
                            # Verifique eventos para permitir sair do loop, como o fechamento da janela
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    game_over = False
    
    
    
    
                print_board(board)
                draw_board(board)

                # Switch turns
                turn += 1
                turn = turn % 2

    if game_over:
        # ask for replay
        pygame.time.wait(3000)
        screen.fill(BLACK)
        pygame.display.update()
        #display replay message in the middle of the screen
        
      # Smaller font for replay message
        small_font = pygame.font.SysFont("monospace", 40)  # Adjust size here
        replay_message = small_font.render("Jogar denovo? (s/n)", True, BLUE)

        # Calculate position to center the message
        replay_x = (width - replay_message.get_width()) // 2
        replay_y = height // 2  # Adjust the vertical position if needed
        screen.blit(replay_message, (replay_x, replay_y))
        pygame.display.update()
        
        
        replay = None
        while replay is None:  # Change condition to None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        replay = True
                    elif event.key == pygame.K_n:
                        replay = False
                    else:
                        replay = False
        if replay:  # Restart the game
            board = create_board()
            print_board(board)
            draw_board(board)
            game_over = False
            turn = 0
        else:  # Exit the game
            pygame.quit()
            sys.exit()
            
    
      
        