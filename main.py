import pygame
import sys
from ChessGame import ChessGame

# pygame.init()
#
# # Set up the display
# WIDTH = HEIGHT = 800
# DIMENSION = 8  # dimensions of a chess board are 8x8
# SQUARE_SIZE = HEIGHT // DIMENSION
# MAX_FPS = 15
# IMAGES = {}
#
# def load_images():
#     pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
#     for piece in pieces:
#         IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))
#
# def draw_board(screen, board):
#     colors = [pygame.Color("white"), pygame.Color("gray")]
#     for row in range(DIMENSION):
#         for col in range(DIMENSION):
#             color = colors[((row + col) % 2)]
#             pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
#
#             piece = board[row][col]
#             if piece != '  ':
#                 screen.blit(IMAGES[piece], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def main():
    # screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption("Chess")
    # clock = pygame.time.Clock()
    #
    # load_images()

    game = ChessGame()
    game.run()
    # board = game.get_board()
    #
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #
    #     draw_board(screen, board)
    #
    #     clock.tick(MAX_FPS)
    #     pygame.display.flip()

if __name__ == "__main__":
    main()
