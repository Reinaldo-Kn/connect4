import numpy as np
import pygame
import sys
import os
import time

class Connect4:
    def __init__(self):
        pygame.init()
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.SQUARESIZE = 100
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT + 1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.BACKGROUND_COLOR = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.board = self.create_board()
        self.game_over = False
        self.turn = 0
        
        # Initialize Pygame screen
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Connect 4")
        self.draw_board()
        self.load_music()

    def create_board(self):
        return np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def winning_move(self, piece):
        # Check horizontal, vertical, and diagonal locations for win
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if all(self.board[r][c+i] == piece for i in range(4)):
                    return [(r, c+i) for i in range(4)]
        
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if all(self.board[r+i][c] == piece for i in range(4)):
                    return [(r+i, c) for i in range(4)]
        
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if all(self.board[r+i][c+i] == piece for i in range(4)):
                    return [(r+i, c+i) for i in range(4)]
        
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                if all(self.board[r-i][c+i] == piece for i in range(4)):
                    return [(r-i, c+i) for i in range(4)]
        
        return None
    
    def animate_winner(self, winning_coords):
        # Define colors for flashing
        colors = [
            (255, 0, 0),   # Red
            (0, 255, 0),   # Green
            (255, 255, 0), # Yellow
            (255, 0, 255), # Magenta
            (0, 255, 255), # Cyan
            (255, 165, 0), # Orange
            (75, 0, 130),  # Indigo
            (238, 130, 238), # Violet
            (128, 0, 128), # Purple
            (0, 128, 128), # Teal
            (255, 105, 180) # Hot Pink
        ]
        
        color_index = 0
        start_time = time.time()  # Mark the start time

        # Draw the winning line
        pygame.draw.line(
            self.screen, (0, 0, 0),  # Line color (black)
            (winning_coords[0][1] * self.SQUARESIZE + self.SQUARESIZE // 2, 
            self.height - (winning_coords[0][0] * self.SQUARESIZE + self.SQUARESIZE // 2)),
            (winning_coords[-1][1] * self.SQUARESIZE + self.SQUARESIZE // 2, 
            self.height - (winning_coords[-1][0] * self.SQUARESIZE + self.SQUARESIZE // 2)),
            10  # Line thickness
        )
        
        # Loop to flash the winning pieces for 5 seconds
        while time.time() - start_time < 5:
            self.draw_board()  # Redraw the board

            # Draw the winning line again to keep it visible
            pygame.draw.line(
                self.screen, (0, 0, 0),  # Line color (black)
                (winning_coords[0][1] * self.SQUARESIZE + self.SQUARESIZE // 2, 
                self.height - (winning_coords[0][0] * self.SQUARESIZE + self.SQUARESIZE // 2)),
                (winning_coords[-1][1] * self.SQUARESIZE + self.SQUARESIZE // 2, 
                self.height - (winning_coords[-1][0] * self.SQUARESIZE + self.SQUARESIZE // 2)),
                10  # Line thickness
            )

            # Alternate colors for the winning pieces
            for coord in winning_coords:
                row, col = coord
                pygame.draw.circle(
                    self.screen, colors[color_index],
                    (col * self.SQUARESIZE + self.SQUARESIZE // 2, 
                    self.height - (row * self.SQUARESIZE + self.SQUARESIZE // 2)),
                    self.RADIUS
                )

            pygame.display.update()
            pygame.time.delay(500)  # Control the flashing speed

            # Move to the next color
            color_index = (color_index + 1) % len(colors)

            # Check events to allow quitting the loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()



    def draw_board(self):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(self.screen, self.BLUE, (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.BACKGROUND_COLOR, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.RED, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.YELLOW, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
        pygame.display.update()

    def load_music(self):
        music_path = os.path.join("soundtrack", "background.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (0, 0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    color = self.RED if self.turn == 0 else self.YELLOW
                    pygame.draw.circle(self.screen, color, (posx, int(self.SQUARESIZE / 2)), self.RADIUS)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (0, 0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    col = int(posx // self.SQUARESIZE)

                    if self.is_valid_location(col):
                        row = self.get_next_open_row(col)
                        piece = 1 if self.turn == 0 else 2
                        self.drop_piece(row, col, piece)

                        winning_coords = self.winning_move(piece)
                        if winning_coords:
                            self.draw_board()  # Redraw the board for the win
                            pygame.draw.line(
                                self.screen, self.BACKGROUND_COLOR,
                                (winning_coords[0][1] * self.SQUARESIZE + self.SQUARESIZE // 2, 
                                self.height - (winning_coords[0][0] * self.SQUARESIZE + self.SQUARESIZE // 2)),
                                (winning_coords[-1][1] * self.SQUARESIZE + self.SQUARESIZE // 2, 
                                self.height - (winning_coords[-1][0] * self.SQUARESIZE + self.SQUARESIZE // 2)),
                                10  # Line thickness
                            )
                            label = self.display_winner(piece)  # Display winner label
                            pygame.display.update()
                            
                            self.animate_winner(winning_coords)  # Animate the winner

                            self.game_over = True  # Set game_over flag to True
                        else:
                            self.draw_board()
                            self.turn += 1
                            self.turn = self.turn % 2

            if self.game_over:
                pygame.time.wait(3000)
                self.prompt_replay()


    def display_winner(self, piece):
        label = "Jogador 1 ganhou!" if piece == 1 else "Jogador 2 ganhou!"
        small_font = pygame.font.SysFont("monospace", 50)
        msg_surface = small_font.render(label, 1, self.RED if piece == 1 else self.YELLOW)
        self.screen.blit(msg_surface, (40, 10))
        pygame.display.update()

    def prompt_replay(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        small_font = pygame.font.SysFont("monospace", 40)
        replay_message = small_font.render("Jogar denovo? (s/n)", True, self.BLUE)
        replay_x = (self.width - replay_message.get_width()) // 2
        replay_y = self.height // 2
        self.screen.blit(replay_message, (replay_x, replay_y))
        pygame.display.update()
        
        replay = None
        while replay is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        replay = True
                    elif event.key == pygame.K_n:
                        replay = False
        if replay:
            self.__init__()  # Restart the game
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    game = Connect4()
    game.run()
