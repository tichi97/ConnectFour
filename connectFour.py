import tkinter as tk
import random
import pygame
import sys
from math import inf as infinity
import copy
import math

#players
HUMAN= 0
COMP = 1

#pieces
EMPTY = 0
HUMAN_PIECE = 1
COMP_PIECE = 2

#drawing the board
ROWS = 6
COLUMNS = 7
SQUARESIZE = 100

#board and piece colors
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)


board=      [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def win(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively slope
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively slope
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def calculate_score(window, piece):
    score = 0
    opp_piece = HUMAN_PIECE
    if piece == HUMAN_PIECE:
        opp_piece = COMP_PIECE

    if window.count(piece) == 4:
        score += 10000000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 10

    return score

def score_position(board, piece):
    score = 0

    #Score Horizontal
    for r in range(ROWS):
        rows=board[r]
        for c in range(COLUMNS-3):
            window=rows[c:c+4]
            score += calculate_score(window, piece)

    #Score Vertical
    for c in range(COLUMNS):
        cols=[]
        for i in range(ROWS):
            cols.append(board[i][c])
        for r in range(ROWS-3):
            window = cols[r:r+4]
            score += calculate_score(window, piece)

    #Score posiive sloped diagonal
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += calculate_score(window, piece)

    #Score neg sloped diagonal
    for r in range(3,ROWS):
        for c in range(COLUMNS-3):
            window = [board[r-i][c+i] for i in range(4)]
            score += calculate_score(window, piece)

    return score

def game_over(board):#win or no more moves left
    if win(board, HUMAN_PIECE) or win(board,COMP_PIECE) or len(get_valid_moves(board)) == 0:
        return True
    else:
        return False


def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_moves(board)
    gameover = game_over(board)
    if depth == 0:
        return (None, score_position(board,COMP_PIECE))

    if gameover:
        if win(board,COMP_PIECE):
            return (None, infinity)
        elif win(board, HUMAN_PIECE):
            return (None, -infinity)
        else: # Game is over, no more valid moves
            return (None, 0)

    #COMP is maximizing player
    if maximizingPlayer:
        max_score = -infinity
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_free_pos(board, col)
            b_copy = copy.deepcopy(board)#copy board otherwise the original board may be changed
            drop_piece(b_copy, row, col,COMP_PIECE)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > max_score:#get max value
                max_score = new_score
                column = col
        return column, max_score

    else: # Minimizing Player
        min_score = infinity
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_free_pos(board, col)
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, row, col, HUMAN_PIECE)
            new_score = minimax(b_copy, depth-1,True)[1]
            if new_score < min_score:#get smaller value
                min_score = new_score
                column = col

        return column, min_score

def get_valid_moves(board):
    valid_locations = []
    for col in range(COLUMNS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def next_free_pos(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, YELLOW, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == HUMAN_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] ==COMP_PIECE:
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def get_player_name():
    box = tk.Tk()
    tk.Label(box, text="Enter Your Name").grid(row=0)
    n=tk.StringVar()
    name = tk.Entry(box, textvariable=n)
    name.grid(row=0, column=1)
    button = tk.Button(box, text='Stop', width=25, command=box.destroy)
    # button.pack()
    button.grid(row=1, column=1)
    box.mainloop()
    player_name=n.get()
    return player_name

def human_turn(board):
    turn=HUMAN
    play_game=True
    posx = event.pos[0]
    col = int(math.floor(posx/SQUARESIZE))#getting screen location

    if is_valid_location(board, col):
        row = next_free_pos(board, col)
        drop_piece(board, row, col, HUMAN_PIECE)

        if win(board, HUMAN_PIECE):
            wins = player_name + " wins!!"
            label = myfont.render(wins, 1, RED)
            screen.blit(label, (40,10))
            play_game = False

        turn=COMP
        print(board)
        draw_board(board)

    return turn,play_game

def comp_turn(board):
    turn=COMP
    play_game=True
    col, minimax_score = minimax(board, 4, True)

    if is_valid_location(board, col):
        row = next_free_pos(board, col)
        drop_piece(board, row, col,COMP_PIECE)

        if win(board,COMP_PIECE):
            label = myfont.render("Computer wins!",1, BLACK)
            screen.blit(label, (40,10))
            play_game = False

        turn=HUMAN
        print(board)
        draw_board(board)

    return turn,play_game

player_name=get_player_name()
print(board)
play_game = True

#set up pygame window
pygame.init()
width = COLUMNS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)


#PLAY GAME
turn = random.randint(HUMAN,COMP)
while play_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == HUMAN:#draw red circle on screen if humans turn
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:#when you click
            pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))

            #HUMANS TURN
            if turn == HUMAN:
                turn,play_game=human_turn(board)

    #COMPUTER TURN
    if turn ==COMP and play_game:
        turn,play_game=comp_turn(board)


    if not play_game:
        pygame.time.wait(3000)


