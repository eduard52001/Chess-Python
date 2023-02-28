import pygame
import sys

# Initialize Pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (0, 128, 0)

# Set the width and height of the screen (in pixels)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

# Set the size of each square on the chess board (in pixels)
# SQUARE_SIZE = 80

# Set the font for the chess piece labels
FONT = pygame.font.SysFont('arial', 40)

WIDTH = HEIGHT = 800
DIMENSION = 8  # dimensions of a chess board are 8x8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


class ChessGame:
    def __init__(self):
        # Initialize the chess board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.current_player = 'white'
        self.selected_piece = None

        # Initialize Pygame window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Chess Game')

    def get_board(self):
        return self.board

    def get_piece(self, pos: tuple) -> str:
        return self.board[pos[1]][pos[0]]

    def run(self):
        # Game loop
        running = True

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        clock = pygame.time.Clock()

        # self.load_images()

        while running:
            # Handle events
            self.load_images()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                        # pygame.quit()
                        # sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print('POS = ' + str(pos))
                    row = pos[1] // SQUARE_SIZE
                    col = pos[0] // SQUARE_SIZE
                    if self.selected_piece is None:
                        self.select_piece((col, row))
                    else:
                        if self.move_piece(self.selected_piece, (col, row)):
                            self.selected_piece = None

            # Draw the chess board and pieces
            self.draw_board(screen, self.get_board())

            clock.tick(MAX_FPS)
            pygame.display.flip()
            # self.draw_pieces()

            # Update the screen
            # pygame.display.update()

    def load_images(self):
        pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
        for piece in pieces:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"),
                                                   (SQUARE_SIZE, SQUARE_SIZE))

    def draw_board(self, screen, board):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = colors[((row + col) % 2)]
                pygame.draw.rect(screen, color,
                                 pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                piece = board[row][col]
                if piece != ' ':
                    screen.blit(IMAGES[piece],
                                pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def select_piece(self, pos):
        print('POS ' + str(pos) + 'was handled by select_piece function')
        # Check if the position is valid and contains a piece of the current player
        if self.get_piece(pos) == ' ' or \
                (self.get_piece(pos).startswith('w') and self.current_player == 'black') or \
                (self.get_piece(pos).startswith('b') and self.current_player == 'white'):
            return

        self.selected_piece = pos
        print('selected piece ' + str(self.selected_piece))

    def move_piece(self, start_pos, end_pos):
        # Check if the starting and ending positions are valid
        # if not self.is_valid_pos(start_pos) or not self.is_valid_pos(end_pos):
        #     return False
        print('END POS IS ' + str(end_pos))

        # Get the piece at the starting position
        piece = self.get_piece(start_pos)

        # Check if the piece belongs to the current player
        if piece.startswith('w') and self.current_player == 'black':
            return False

        # Check if the destination position is occupied by a piece
        dest_piece = self.get_piece(end_pos)
        if dest_piece != ' ' and (dest_piece.startswith('w') and self.current_player == 'white' or
                                  dest_piece.startswith('b') and self.current_player == 'black'):
            return False

        # Check if the piece can move to the destination position
        valid_moves = self.get_valid_moves(start_pos)
        print('VALID MOVES ARE ' + str(valid_moves))
        if end_pos not in valid_moves:
            print('END_POS {} NOT IN VALID MOVES'.format(end_pos))
            return False

        # Move the piece to the     destination position
        self.board[start_pos[1]][start_pos[0]] = ' '
        self.board[end_pos[1]][end_pos[0]] = piece

        # Switch the current player
        self.current_player = 'white' if self.current_player == 'black' else 'black'

        return True

    def get_valid_moves(self, pos):
        print('POS '+str(pos) + 'was handled by get_valid_moves function')
        piece = self.get_piece(pos)
        print('PIECE selected is ' + piece)

        if piece.endswith('P'):
            return self.get_valid_pawn_moves(pos)
        elif piece.endswith('R'):
            return self.get_valid_rook_moves(pos)
        elif piece.endswith('N'):
            return self.get_valid_knight_moves(pos)
        elif piece.endswith('B'):
            return self.get_valid_bishop_moves(pos)
        elif piece.endswith('Q'):
            return self.get_valid_queen_moves(pos)
        elif piece.endswith('K'):
            return self.get_valid_king_moves(pos)
        return []

    def get_valid_pawn_moves(self, pos):
        print('POS {} was handled by "get_valid_pawn_moves" function'.format(str(pos)))
        moves = []
        direction = -1 if self.current_player == 'white' else 1
        col, row = pos
        # Check the square in front of the pawn
        if self.get_piece((col, row + direction)) == ' ':
            print('OK 1')
            moves.append((col, row + direction))
        # Check the two squares in front of the pawn if it's its first move
        if ((direction == -1 and row == 6) or (direction == 1 and row == 1)) and \
                self.get_piece((col, row + 2 * direction)) == ' ':
            moves.append((col, row + 2 * direction))
        # Check the two diagonal squares to capture a piece
        if col > 0 and self.get_piece((col - 1, row + direction)) != ' ' and \
                ((self.get_piece((col - 1, row + direction)).startswith('w') and self.current_player == 'black') or
                 (self.get_piece((col - 1, row + direction)).startswith('b') and self.current_player == 'white')):
            moves.append((col - 1, row + direction))
        if col < 7 and self.get_piece((col + 1, row + direction)) != ' ' and \
                ((self.get_piece((col + 1, row + direction)).startswith('w') and self.current_player == 'black') or
                 (self.get_piece((col + 1, row + direction)).startswith('b') and self.current_player == 'white')):
            moves.append((col + 1, row + direction))
        return moves

    def get_valid_rook_moves(self, pos):
        moves = []
        row, col = pos
        # Check the squares to the right of the rook
        for i in range(col + 1, 8):
            if self.board[row][i] == ' ':
                moves.append((row, i))
            else:
                if (self.board[row][i].isupper() and self.current_player == 'white') or \
                        (self.board[row][i].islower() and self.current_player == 'black'):
                    moves.append((row, i))
                break

        # Check the squares to the left of the rook
        for i in range(col - 1, -1, -1):
            if self.board[row][i] == ' ':
                moves.append((row, i))
            else:
                if (self.board[row][i].isupper() and self.current_player == 'white') or \
                        (self.board[row][i].islower() and self.current_player == 'black'):
                    moves.append((row, i))
                break
        # Check the squares above the rook
        for i in range(row - 1, -1, -1):
            if self.board[i][col] == ' ':
                moves.append((i, col))
            else:
                if (self.board[i][col].isupper() and self.current_player == 'white') or \
                        (self.board[i][col].islower() and self.current_player == 'black'):
                    moves.append((i, col))
                break
        # Check the squares below the rook
        for i in range(row + 1, 8):
            if self.board[i][col] == ' ':
                moves.append((i, col))
            else:
                if (self.board[i][col].isupper() and self.current_player == 'white') or \
                        (self.board[i][col].islower() and self.current_player == 'black'):
                    moves.append((i, col))
                break
        return moves

    def get_valid_knight_moves(self, pos):
        moves = []
        row, col = pos
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and \
                    ((self.board[r][c] == ' ') or
                     (self.board[r][c].isupper() and self.current_player == 'black') or
                     (self.board[r][c].islower() and self.current_player == 'white')):
                moves.append((r, c))
        return moves

    def get_valid_bishop_moves(self, pos):
        moves = []
        row, col = pos
        # Check the squares to the top-right of the bishop
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, 8)):
            if self.board[i][j] == ' ':
                moves.append((i, j))
            else:
                if (self.board[i][j].isupper() and self.current_player == 'white') or \
                        (self.board[i][j].islower() and self.current_player == 'black'):
                    moves.append((i, j))
                break
        # Check the squares to the top-left of the bishop
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if self.board[i][j] == ' ':
                moves.append((i, j))
            else:
                if (self.board[i][j].isupper() and self.current_player == 'white') or \
                        (self.board[i][j].islower() and self.current_player == 'black'):
                    moves.append((i, j))
                break
        # Check the squares to the bottom-right of the bishop
        for i, j in zip(range(row + 1, 8), range(col + 1, 8)):
            if self.board[i][j] == ' ':
                moves.append((i, j))
            else:
                if (self.board[i][j].isupper() and self.current_player == 'white') or \
                        (self.board[i][j].islower() and self.current_player == 'black'):
                    moves.append((i, j))
                break
        # Check the squares to the bottom-left of the bishop
        for i, j in zip(range(row + 1, 8), range(col - 1, -1, -1)):
            if self.board[i][j] == ' ':
                moves.append((i, j))
            else:
                if (self.board[i][j].isupper() and self.current_player == 'white') or \
                        (self.board[i][j].islower() and self.current_player == 'black'):
                    moves.append((i, j))
                break
        return moves

    def get_valid_queen_moves(self, pos):
        moves = self.get_valid_rook_moves(pos) + self.get_valid_bishop_moves(pos)
        return moves

    def get_valid_king_moves(self, pos):
        moves = []
        row, col = pos
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue
                if 0 <= i < 8 and 0 <= j < 8 and \
                        ((self.board[i][j] == ' ') or
                         (self.board[i][j].isupper() and self.current_player == 'black') or
                         (self.board[i][j].islower() and self.current_player == 'white')):
                    moves.append((i, j))
        return moves

