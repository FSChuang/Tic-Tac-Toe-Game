import pygame
from enum import Enum
import sys

pygame.init()

class Player(Enum):
    p1 = 'X'
    p2 = 'O'

# COLOR
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# BOARD DISPLAY CONSTANTS
Width, Height = 600, 600
BG_Color = BLACK
Line_Color = WHITE
Line_Width = 30
Cell_Size = 600 // 3
Cricle_Radius = Cell_Size // 3
Circle_Color = BLUE
Circle_Width = 30
Cross_Space = Cell_Size // 4
Cross_Color = RED
Cross_Width = 30

class TicTacToe:

    def __init__(self, w=Width, h=Height):
        self.w = w
        self.h = h
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.display = pygame.display.set_mode((self.w, self.h))
        self.player = Player.p1
        pygame.display.set_caption('Tic Tac Toe')

    def _game_is_over(self, player):
        for row in range(3):
            if all([self.board[row][col] == player for col in range(3)]):
                return True, player
            
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return True, player
        
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2-i] == player for i in range(3)]):
            return True, player
        
        if all([cell != ' ' for row in self.board for cell in row]):
            return True, 'Tie'
        
        return False, None
    
    def _draw_grid(self):
        for row in range(1, 3):
            pygame.draw.line(self.display, Line_Color, (Cell_Size*row, 0), (Cell_Size*row, Width), Line_Width)
            pygame.draw.line(self.display, Line_Color, (0, Cell_Size*row), (Height, Cell_Size*row), Line_Width)

    def _draw_flags(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == Player.p1:
                    pygame.draw.line(self.display, RED, (Cell_Size*row + Cross_Space, Cell_Size*col + Cross_Space),
                                     (Cell_Size*row + Cell_Size - Cross_Space, Cell_Size*col + Cell_Size - Cross_Space), Cross_Width)
                    pygame.draw.line(self.display, RED, (Cell_Size*row + Cross_Space, Cell_Size*col + Cell_Size - Cross_Space), 
                                     (Cell_Size*row + Cell_Size - Cross_Space, Cell_Size*col + Cross_Space), Cross_Width)
                    
                elif self.board[row][col] == Player.p2:
                    pygame.draw.circle(self.display, color = Circle_Color, center = (Cell_Size*row + Cell_Size//2, Cell_Size*col + Cell_Size//2), radius = Cricle_Radius, width = Circle_Width)

    def _update_ui(self):
        self.display.fill(BLACK)
        self._draw_grid()
        self._draw_flags()
        pygame.display.flip()

    def _play_game(self):
        # 1. Collect User's inputs
        player = self.player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                boardX = int(mouseX//Cell_Size)
                boardY = int(mouseY//Cell_Size)

                if self.board[boardX][boardY] == " ":
                    self.board[boardX][boardY] = self.player
                    self.player = Player.p2 if self.player == Player.p1 else Player.p1
                      
        # 2. check if the game is over
        game_over = False
        winner = self._game_is_over(player)[1]
        if self._game_is_over(player)[0] == True:
            game_over = True
            return game_over, winner
            
        # update ui surface
        self._update_ui()

        return game_over, winner
    
if __name__ == '__main__':
    game = TicTacToe()
    
    winner = None
    while True:
        game_over, winner = game._play_game()

        if game_over == True:
            game._update_ui()
            pygame.time.delay(200)
            break
    font = pygame.font.Font('AykaPot.ttf', 60)
    game.display.fill(BLACK)
    if winner == 'Tie':
        text = font.render("Game Over, " + winner, True, WHITE)
    else:
        text = font.render("Game Over, [" + winner.value + "] won!", True, WHITE)

    text_rect = text.get_rect(center = (Width//2, Height//2))
    game.display.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)
pygame.quit()
sys.exit()
