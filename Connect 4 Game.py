
import numpy as np
import pygame
import sys
import math
import random
import time

ROWS = 6
COLUMNS = 7
player_piece = 1
computer_piece = 2
empty = 0
windows_length = 4

def create_new_board():
    return np.zeros((ROWS, COLUMNS), dtype=int)

def add_piece(board, row, col, token):
    board[row][col] = token

def can_place_piece(board, col):

    return board[ROWS - 1][col] == empty

def find_open_row(board, col):
    
    for r in range(ROWS):
        if board[r][col] == empty:
            return r
    return None

def show_board(board):
    print(np.flip(board, 0))
    
# zozo 
# Winning Check
def winning(board, piece):
    # horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # negative diagonal
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False
# asmaa & Amany 
def check_four_cells(cells, piece):
    score = 0
    # opponent piece الخصم
    opponent_piece = player_piece if piece == computer_piece else computer_piece
# تقييم الخلايا
    if cells.count(piece) == 4:
        score += 100
    elif cells.count(piece) == 3 and cells.count(empty) == 1:
        score += 5
    elif cells.count(piece) == 2 and cells.count(empty) == 2:
        score += 2
# منع الخصم من الفوز
    if cells.count(opponent_piece) == 3 and cells.count(empty) == 1:
        score -= 4

    return score

def score_board(board, piece): # تقييم اللوحة
    total_score = 0
    # score center column تقييم العمود الأوسط
    center_col = [int(i) for i in list(board[:, COLUMNS//2])]
    center_count = center_col.count(piece)
    total_score += center_count * 3 # تعزيز السيطرة على العمود الأوسط

    # horizontal الأفقي
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMNS-3):
            cells = row_array[c:c+4]
            total_score += check_four_cells(cells, piece)

    # vertical العمودي
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS-3):
            cells = col_array[r:r+4]
            total_score += check_four_cells(cells, piece)

    # positive sloped diagonal الأقطار المائلة للأعلى الموجبة
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            cells = [int(board[r+i][c+i]) for i in range(4)]
            total_score += check_four_cells(cells, piece)

    # negative sloped diagonal الأقطار المائلة للأسفل السالبة
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            cells = [int(board[r+3-i][c+i]) for i in range(4)]
            total_score += check_four_cells(cells, piece)

    return total_score # تقييم اللوحة

# Minimax Algorithm with Alpha-Beta Pruning  by nour & basmala 
def is_terminal_node(board): # تحقق من حالة النهاية
    return winning(board, player_piece) or winning(board, computer_piece) or len(get_valid_locations(board)) == 0 # تحقق من تعادل اللعبة
#بحث عن الأعمدة الصالحة
def get_valid_locations(board):# ابحث عن الأعمدة الصالحة
    valid_locations = [] # قائمة الأعمدة الصالحة
    for col in range(COLUMNS):# تحقق من إمكانية وضع قطعة في العمود
        if can_place_piece(board, col):# إذا كان بإمكانك وضع قطعة في العمود
            valid_locations.append(col)# أضف العمود إلى القائمة
    return valid_locations # إرجاع الأعمدة الصالحة

def minimax(board, depth, alpha, beta, maximizingPlayer): # خوارزمية مينيماكس مع تقليم ألفا-بيتا
    valid_locations = get_valid_locations(board) # الحصول على الأعمدة الصالحة

    if depth == 0 or is_terminal_node(board):# تحقق من حالة النهاية أو الوصول إلى العمق الأقصى
        if winning(board, computer_piece): # تحقق من فوز الكمبيوتر
            return (None, 999999) # إرجاع قيمة عالية لفوز الكمبيوتر
        elif winning(board, player_piece):# تحقق من فوز اللاعب
            return (None, -999999)# إرجاع قيمة منخفضة لفوز اللاعب
        else:
            return (None, score_board(board, computer_piece)) # إرجاع تقييم اللوحة

    if maximizingPlayer: # إذا كان اللاعب الحالي هو اللاعب الذي يزيد من القيمة
        best_score = -math.inf # أفضل نتيجة مبدئية
        best_col = random.choice(valid_locations) if valid_locations else None # اختيار عمود عشوائي من الأعمدة الصالحة

        for col in valid_locations: # استعراض الأعمدة الصالحة
            row = find_open_row(board, col) # العثور على الصف المفتوح في العمود
            if row is None:# إذا لم يكن هناك صف مفتوح
                continue # تخطي هذا العمود
            b_copy = board.copy() # نسخ اللوحة
            add_piece(b_copy, row, col, computer_piece) # إضافة قطعة الكمبيوتر إلى النسخة
            score = minimax(b_copy, depth - 1, alpha, beta, False)[1] # استدعاء مينيماكس بشكل تكراري
            if score > best_score: # تحديث أفضل نتيجة إذا كانت النتيجة الحالية أفضل
                best_score = score # تحديث أفضل نتيجة
                best_col = col # تحديث أفضل عمود
            alpha = max(alpha, best_score) # تحديث ألفا
            if alpha >= beta: # تقليم ألفا-بيتا
                break
        return best_col, best_score # إرجاع أفضل عمود وأفضل نتيجة

    else:
        best_score = math.inf # أفضل نتيجة مبدئية
        best_col = random.choice(valid_locations) if valid_locations else None # اختيار عمود عشوائي من الأعمدة الصالحة

        for col in valid_locations: # استعراض الأعمدة الصالحة
            row = find_open_row(board, col) # العثور على الصف المفتوح في العمود
            if row is None: # إذا لم يكن هناك صف مفتوح
                continue # تخطي هذا العمود
            b_copy = board.copy() # نسخ اللوحة
            add_piece(b_copy, row, col, player_piece) # إضافة قطعة اللاعب إلى النسخة
            score = minimax(b_copy, depth - 1, alpha, beta, True)[1] # استدعاء مينيماكس بشكل تكراري
            if score < best_score:# تحديث أفضل نتيجة إذا كانت النتيجة الحالية أفضل
                best_score = score # تحديث أفضل نتيجة
                best_col = col # تحديث أفضل عمود
            beta = min(beta, best_score) # تحديث بيتا
            if alpha >= beta: # تقليم ألفا-بيتا
                break # إنهاء الحلقة
        return best_col, best_score # إرجاع أفضل عمود وأفضل نتيجة

# GUI
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE  
size = (width, height)

def draw_board(screen, board):
    # draw rectangles and circles
    for r in range(ROWS):
        for c in range(COLUMNS):
            # compute value to draw: board row indexing -> display top to bottom
            display_r = ROWS - 1 - r
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            val = board[display_r][c]
            if val == empty:
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif val == player_piece:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif val == computer_piece:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect 4 - Classic")
    font = pygame.font.SysFont("monospace", 50)

    board = create_new_board()
    game_over = False
    turn = 0  

    draw_board(screen, board)
    pygame.display.update()
    clock = pygame.time.Clock()

    my_depth = 4 

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mous Move
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            # PLAYER CLICK
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0 and not game_over:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)

                    if col in get_valid_locations(board):
                        row = find_open_row(board, col)
                        if row is not None:
                            add_piece(board, row, col, player_piece)
                            if winning(board, player_piece):
                                label = font.render("You win!", True, WHITE)
                                screen.blit(label, (40, 10))
                                game_over = True
                            turn = 1
                            draw_board(screen, board)

        # AI turn
        if turn == 1 and not game_over:
            # small delay to feel natural
            pygame.time.wait(500)
            col, score = minimax(board, my_depth, -math.inf, math.inf, True)
            if col is None:
                # fallback random
                valid = get_valid_locations(board)
                col = random.choice(valid) if valid else None

            if col is not None and can_place_piece(board, col):
                row = find_open_row(board, col)
                if row is not None:
                    add_piece(board, row, col, computer_piece)
                    if winning(board, computer_piece):
                        label = font.render("AI wins!", True, WHITE)
                        screen.blit(label, (40, 10))
                        game_over = True
                    draw_board(screen, board)
            turn = 0

        # check draw
        if not game_over and len(get_valid_locations(board)) == 0:
            label = font.render("Draw!", True, WHITE)
            screen.blit(label, (40, 10))
            game_over = True

        if game_over:
            pygame.display.update()
            pygame.time.wait(2000)
            
            board = create_new_board()
            draw_board(screen, board)
            game_over = False
            turn = 0

        clock.tick(30)

if __name__ == "__main__":
    main()
