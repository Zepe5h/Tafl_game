import os
import random
import sys
import pygame as pg
import time

#main script -- UDLR
WINDOW_HEIGHT = 800
supermode = random.randint(0, 1)
WINDOW_WIDTH = 1000
GAME_NAME = TITLE = "Тафль"
GAME_ICON = pg.image.load("images/vh.jpg")
MAIN_MENU_TOP_BUTTON_x = 400
MAIN_MENU_TOP_BUTTON_y = 400
BOARD_TOP = 200
BOARD_LEFT = 125
CELL_WIDTH = 50
CELL_HEIGHT = 50
PIECE_RADIUS = 20
VALID_MOVE_INDICATOR_RADIUS = 10
SETTINGS_TEXT_GAP_VERTICAL = 50
SETTINGS_TEXT_GAP_HORIZONTAL = 100
AI_LEVEL_HARD = 0
AI_POSS_LEVELS = {0: "Просто", 1: "Нормально", 2: "Сложно"}
bg = (204, 102, 0)
bg2 = (40, 40, 40)
red = (240, 146, 11)
black = (0, 0, 0)
yellow = (255, 255, 1)
golden = (15, 255, 80)
white = (255, 255, 255)
pink_fuchsia = (15, 255, 80)
green_neon = (255, 0, 255)
green_dark = (2, 48, 32)
green_teal = (0, 128, 128)
blue_indigo = (63, 0, 255)
blue_zaffre = (8, 24, 168)
ATTACKER_PIECE_COLOR = (120, 21, 217)
DEFENDER_PIECE_COLOR = green_teal
KING_PIECE_COLOR = golden
VALID_MOVE_INDICATOR_COLOR = green_neon
BORDER_COLOR = blue_zaffre
GAME_ICON_resized = pg.image.load("images/vh_resized.jpg")
click_snd = os.path.join("sounds", "click_1.wav")
move_snd_1 = os.path.join("sounds", "move_1.mp3")
kill_snd_1 = os.path.join("sounds", "kill_1.mp3")
win_snd_1 = os.path.join("sounds", "win_1.mp3")
lose_snd_1 = os.path.join("sounds", "lose_1.mp3")
clicked = False


def write_text(text, screen, position, color, font, new_window=True):
    if new_window:
        screen.fill(bg2)
    txtobj = font.render(text, True, color)
    txtrect = txtobj.get_rect()
    txtrect.topleft = position
    screen.blit(txtobj, txtrect)


class Custom_button:

    button_col = (15, 10, 232)
    hover_col = (0, 0, 0)
    click_col = (50, 150, 255)
    text_col = yellow

    def __init__(self, x, y, text, screen, font, width=200, height=70):
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height

    def draw_button(self):

        global clicked
        action = False
        pos = pg.mouse.get_pos()
        button_rect = pg.Rect(self.x, self.y, self.width, self.height)
        if button_rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                clicked = True
                pg.draw.rect(self.screen, self.click_col, button_rect)
            elif pg.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pg.draw.rect(self.screen, self.hover_col, button_rect)
        else:
            pg.draw.rect(self.screen, self.button_col, button_rect)

        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.screen.blit(text_img, (self.x + int(self.width / 2) -
                                    int(text_len / 2), self.y + 15))
        return action


class ChessBoard:

    def __init__(self, screen, board_size="large"):

        self.initial_pattern11 = ["x..aaaaa..x",
                                  ".....a.....",
                                  "...........",
                                  "a....d....a",
                                  "a...ddd...a",
                                  "aa.ddcdd.aa",
                                  "a...ddd...a",
                                  "a....d....a",
                                  "...........",
                                  ".....a.....",
                                  "x..aaaaa..x"]

        self.initial_pattern9 = ["x..aaa..x",
                                 "....a....",
                                 ".........",
                                 "a..ddd..a",
                                 "aa.dcd.aa",
                                 "a..ddd..a",
                                 ".........",
                                 "....a....",
                                 "x..aaa..x"]

        if board_size == "large":
            self.initial_pattern = self.initial_pattern11
        else:
            self.initial_pattern = self.initial_pattern9

        self.rows = len(self.initial_pattern)
        self.columns = len(self.initial_pattern[0])
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT
        self.screen = screen
        self.restricted_cells = [(0, 0), (0, self.columns-1), (int(self.rows/2), int(
            self.columns/2)), (self.rows-1, 0), (self.rows-1, self.columns-1)]

    def draw_empty_board(self):

        border_top = pg.Rect(BOARD_LEFT - 10, BOARD_TOP -
                             10, self.columns*CELL_WIDTH + 20, 10)
        pg.draw.rect(self.screen, BORDER_COLOR, border_top)
        border_down = pg.Rect(BOARD_LEFT - 10, BOARD_TOP +
                              self.rows*CELL_HEIGHT, self.columns*CELL_WIDTH + 20, 10)
        pg.draw.rect(self.screen, BORDER_COLOR, border_down)
        border_left = pg.Rect(BOARD_LEFT - 10, BOARD_TOP -
                              10, 10, self.rows*CELL_HEIGHT + 10)
        pg.draw.rect(self.screen, BORDER_COLOR, border_left)
        border_right = pg.Rect(BOARD_LEFT+self.columns*CELL_WIDTH,
                               BOARD_TOP - 10, 10, self.rows*CELL_HEIGHT + 10)
        pg.draw.rect(self.screen, BORDER_COLOR, border_right)

        color_flag = True
        for row in range(self.rows):
            write_text(str(row), self.screen, (BOARD_LEFT - 30, BOARD_TOP + row*CELL_HEIGHT +
                       PIECE_RADIUS), (255, 255, 255), pg.font.SysFont("Arial", 15), False)
            write_text(str(row), self.screen, (BOARD_LEFT + row*CELL_WIDTH +
                       PIECE_RADIUS, BOARD_TOP - 30), (255, 255, 255), pg.font.SysFont("Arial", 15), False)
            for column in range(self.columns):

                cell_rect = pg.Rect(BOARD_LEFT + column * self.cell_width, BOARD_TOP +
                                    row * self.cell_height, self.cell_width, self.cell_height)

                if (row == 0 or row == self.rows-1) and (column == 0 or column == self.columns-1):
                    pg.draw.rect(self.screen, red, cell_rect)
                elif row == int(self.rows / 2) and column == int(self.columns / 2):
                    pg.draw.rect(self.screen, blue_indigo, cell_rect)
                elif color_flag:
                    pg.draw.rect(self.screen, white, cell_rect)
                else:
                    pg.draw.rect(self.screen, black, cell_rect)

                color_flag = not color_flag

    def initiate_board_pieces(self):

        att_cnt, def_cnt = 1, 1
        global piece_pid_map
        piece_pid_map = {}

        for row in range(self.rows):
            for column in range(self.columns):
                if self.initial_pattern[row][column] == 'a':
                    pid = "a" + str(att_cnt)
                    AttackerPiece(pid, row, column)
                    att_cnt += 1
                elif self.initial_pattern[row][column] == 'd':
                    pid = "d" + str(def_cnt)
                    DefenderPiece(pid, row, column)
                    def_cnt += 1
                elif self.initial_pattern[row][column] == 'c':
                    pid = "k"
                    KingPiece(pid, row, column)
                else:
                    pass

        for piece in All_pieces:
            piece_pid_map[piece.pid] = piece


class ChessPiece(pg.sprite.Sprite):

    def __init__(self, pid, row, column):

        pg.sprite.Sprite.__init__(self, self.groups)
        self.pid = pid
        self.row, self.column = (row, column)
        self.center = (BOARD_LEFT + int(CELL_WIDTH / 2) + self.column*CELL_WIDTH,
                       BOARD_TOP + int(CELL_HEIGHT / 2) + self.row*CELL_HEIGHT)

    def draw_piece(self, screen):
        pg.draw.circle(screen, self.color, self.center, PIECE_RADIUS)

    def update_piece_position(self, row, column):

        self.row, self.column = (row, column)
        self.center = (BOARD_LEFT + int(CELL_WIDTH / 2) + self.column*CELL_WIDTH,
                       BOARD_TOP + int(CELL_HEIGHT / 2) + self.row*CELL_HEIGHT)


class AttackerPiece(ChessPiece):
    def __init__(self, pid, row, column):
        ChessPiece.__init__(self, pid, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = ATTACKER_PIECE_COLOR
        self.permit_to_res_sp = False
        self.ptype = "a"


class DefenderPiece(ChessPiece):
    
    def __init__(self, pid, row, column):
        ChessPiece.__init__(self, pid, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = DEFENDER_PIECE_COLOR
        self.permit_to_res_sp = False
        self.ptype = "d"


class KingPiece(DefenderPiece):

    def __init__(self, pid, row, column):
        DefenderPiece.__init__(self, pid, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = KING_PIECE_COLOR
        self.permit_to_res_sp = True
        self.ptype = "k"


def match_specific_global_data_sprites():
    global All_pieces, Attacker_pieces, Defender_pieces, King_pieces

    All_pieces = pg.sprite.Group()
    Attacker_pieces = pg.sprite.Group()
    Defender_pieces = pg.sprite.Group()
    King_pieces = pg.sprite.Group()

    ChessPiece.groups = All_pieces
    AttackerPiece.groups = All_pieces, Attacker_pieces
    DefenderPiece.groups = All_pieces, Defender_pieces
    KingPiece.groups = All_pieces, Defender_pieces, King_pieces


class Game_manager_event_handler:

    def __init__(self, screen, board, mode, board_size="large"):
        self.screen = screen
        self.board = board
        self.turn = True
        self.king_escaped = False
        self.king_captured = False
        self.all_attackers_killed = False
        self.finish = False
        self.already_selected = None
        self.is_selected = False
        self.valid_moves = []
        self.valid_moves_positions = []
        self.current_board_status = []
        self.current_board_status_with_border = []
        self.mode = mode
        self.last_move = None
        self.board_size = board_size
        border = []
        for column in range(self.board.columns + 2):
            border.append("=")
        self.current_board_status_with_border.append(border)

        for row in self.board.initial_pattern:
            bordered_row = ["="]
            one_row = []
            for column in row:
                one_row.append(column)
                bordered_row.append(column)
            self.current_board_status.append(one_row)
            bordered_row.append("=")
            self.current_board_status_with_border.append(bordered_row)

        self.current_board_status_with_border.append(border)

    def select_piece(self, selected_piece):

        self.is_selected = True
        self.already_selected = selected_piece
        self.find_valid_moves()

    def find_valid_moves(self):

        self.valid_moves = []
        tempr = self.already_selected.row
        tempc = self.already_selected.column


        tempr -= 1
        while tempr >= 0:

            thispos = self.current_board_status[tempr][tempc]
            if thispos == "a" or thispos == "d" or thispos == "k" or (thispos == "x" and self.already_selected.ptype != "k"):
                break
            else:
                if self.already_selected.ptype == "k":
                    if tempr < self.already_selected.row - 1 or tempr > self.already_selected.row + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempr -= 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        tempr += 1
        while tempr < self.board.rows:

            thispos = self.current_board_status[tempr][tempc]
            if thispos == "a" or thispos == "d" or thispos == "k" or (thispos == "x" and self.already_selected.ptype != "k"):
                break
            else:
                if self.already_selected.ptype == "k":
                    if tempr < self.already_selected.row - 1 or tempr > self.already_selected.row + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempr += 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        tempc -= 1
        while tempc >= 0:

            thispos = self.current_board_status[tempr][tempc]
            if thispos == "a" or thispos == "d" or thispos == "k" or (thispos == "x" and self.already_selected.ptype != "k"):
                break
            else:
                if self.already_selected.ptype == "k":
                    if tempc < self.already_selected.column - 1 or tempc > self.already_selected.column + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempc -= 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        tempc += 1
        while tempc < self.board.columns:

            thispos = self.current_board_status[tempr][tempc]
            if thispos == "a" or thispos == "d" or thispos == "k" or (thispos == "x" and self.already_selected.ptype != "k"):
                break
            else:
                if self.already_selected.ptype == "k":
                    if tempc < self.already_selected.column - 1 or tempc > self.already_selected.column + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempc += 1

        for position in self.valid_moves:
            self.valid_moves_positions.append((BOARD_LEFT + int(CELL_WIDTH / 2) + position[1]*CELL_WIDTH,
                                               BOARD_TOP + int(CELL_HEIGHT / 2) + position[0]*CELL_HEIGHT))

    def show_valid_moves(self):
        for index in self.valid_moves_positions:

            pg.draw.circle(self.screen, VALID_MOVE_INDICATOR_COLOR,
                           index, VALID_MOVE_INDICATOR_RADIUS)

    def deselect(self):

        self.is_selected = False
        self.already_selected = None
        self.valid_moves = []
        self.valid_moves_positions = []

    def update_board_status(self):

        self.current_board_status = []
        self.current_board_status_with_border = []
        border = []
        for column in range(self.board.columns + 2):
            border.append("=")
        self.current_board_status_with_border.append(border)

        for row in range(self.board.rows):
            bordered_row = ["="]
            one_row = []
            for column in range(self.board.columns):
                one_row.append(".")
                bordered_row.append(".")

            if row == 0 or row == self.board.rows - 1:
                one_row[0] = "x"
                one_row[self.board.columns-1] = "x"
                bordered_row[1] = "x"
                bordered_row[self.board.columns] = "x"
            self.current_board_status.append(one_row)
            bordered_row.append("=")
            self.current_board_status_with_border.append(bordered_row)

        self.current_board_status_with_border.append(border)

        for piece in All_pieces:
            self.current_board_status[piece.row][piece.column] = piece.ptype
            self.current_board_status_with_border[piece.row +
                                                  1][piece.column+1] = piece.ptype
        if self.current_board_status[int(self.board.rows/2)][int(self.board.columns/2)] != "k":
            self.current_board_status[int(
                self.board.rows/2)][int(self.board.columns/2)] = "x"
            self.current_board_status_with_border[int(
                self.board.rows/2)+1][int(self.board.columns/2)+1] = "x"


    def capture_check(self):
        ptype, prow, pcol = self.already_selected.ptype, self.already_selected.row + \
            1, self.already_selected.column+1

        sorroundings = [(prow, pcol+1), (prow, pcol-1),
                        (prow-1, pcol), (prow+1, pcol)]
        two_hop_away = [(prow, pcol+2), (prow, pcol-2),
                        (prow-2, pcol), (prow+2, pcol)]

        for pos, item in enumerate(sorroundings):
            opp = self.current_board_status_with_border[item[0]][item[1]]
            try:
                opp2 = self.current_board_status_with_border[two_hop_away[pos]
                                                             [0]][two_hop_away[pos][1]]
            except:
                opp2 = "."

            if ptype == opp or ptype == "x" or ptype == "=" or opp == "." or opp2 == ".":
                continue

            elif opp == "k":
                self.king_capture_check(item[0], item[1])

            elif ptype != opp:
                if ptype == "a" and (ptype == opp2 or opp2 == "x"):
                    for piece in All_pieces:
                        if piece.ptype == opp and piece.row == sorroundings[pos][0]-1 and piece.column == sorroundings[pos][1]-1:
                            pg.mixer.Sound.play(pg.mixer.Sound(kill_snd_1))
                            piece.kill()
                            self.update_board_status()
                            break

                elif ptype != "a" and opp2 != "a" and opp2 != "=" and opp == "a":
                    for piece in All_pieces:
                        if piece.ptype == opp and piece.row == sorroundings[pos][0]-1 and piece.column == sorroundings[pos][1]-1:
                            pg.mixer.Sound.play(pg.mixer.Sound(kill_snd_1))
                            piece.kill()
                            self.update_board_status()
                            break
        if self.king_captured:
            self.finish = True
            pg.mixer.Sound.play(pg.mixer.Sound(lose_snd_1))

    def king_capture_check(self, kingr, kingc):
        front = self.current_board_status_with_border[kingr][kingc+1]
        back = self.current_board_status_with_border[kingr][kingc-1]
        up = self.current_board_status_with_border[kingr-1][kingc]
        down = self.current_board_status_with_border[kingr+1][kingc]

        if front == "x" or back == "x" or up == "x" or down == "x":
            return

        elif front == "d" or back == "d" or up == "d" or down == "d":
            return

        elif front == "." or back == "." or up == "." or down == ".":
            return

        else:
            self.king_captured = True

    def escape_check(self):

        if self.current_board_status[0][0] == "k" or self.current_board_status[0][self.board.columns-1] == "k" or self.current_board_status[self.board.rows-1][0] == "k" or self.current_board_status[self.board.rows-1][self.board.columns-1] == "k":
            self.king_escaped = True
            self.finish = True
            pg.mixer.Sound.play(pg.mixer.Sound(win_snd_1))

        else:
            self.king_escaped = False

    def attackers_count_check(self):
        if len(Attacker_pieces) == 0:
            self.all_attackers_killed = True
            self.finish = True
            pg.mixer.Sound.play(pg.mixer.Sound(win_snd_1))


    def match_finished(self):

        consolas = pg.font.SysFont("consolas", 22)
        if self.king_captured:
            if self.mode == 0:
                write_text("Король захвачен. Атакующие победили!", self.screen, (20, BOARD_TOP - 80), white,
                           consolas, False)
            else:
                write_text("Король захвачен. ИИ победил!", self.screen, (20, BOARD_TOP - 80), white,
                           consolas, False)

        elif self.king_escaped:
            write_text("Король сбежал. Защищающиеся победили!", self.screen, (20, BOARD_TOP - 80), white,
                       consolas, False)


        elif self.all_attackers_killed:
            write_text("Все  атакующие мертвы. Защищающиеся победили!", self.screen, (20, BOARD_TOP - 80), white,
                       consolas, False)


        else:
            pass

    def mouse_click_analyzer(self, msx, msy):

        if not self.is_selected:
            for piece in All_pieces:
                if (msx >= piece.center[0] - PIECE_RADIUS) and (msx < piece.center[0] + PIECE_RADIUS):
                    if (msy >= piece.center[1] - PIECE_RADIUS) and (msy < piece.center[1] + PIECE_RADIUS):
                        if (piece.ptype == "a" and self.turn) or (piece.ptype != "a" and not self.turn):
                            self.select_piece(piece)
                        break

        elif (self.already_selected.ptype != "a" and self.turn) or (self.already_selected.ptype == "a" and not self.turn):
            self.deselect()

        else:
            done = False

            for piece in All_pieces:
                if (msx >= piece.center[0] - PIECE_RADIUS) and (msx < piece.center[0] + PIECE_RADIUS):
                    if (msy >= piece.center[1] - PIECE_RADIUS) and (msy < piece.center[1] + PIECE_RADIUS):
                        done = True
                        if piece == self.already_selected:
                            self.deselect()
                            break
                        else:
                            self.deselect()
                            if (piece.ptype == "a" and self.turn) or (piece.ptype != "a" and not self.turn):
                                self.select_piece(piece)
                        break

            if not done:
                for ind, pos in enumerate(self.valid_moves_positions):
                    if (msx >= pos[0] - PIECE_RADIUS) and (msx < pos[0] + PIECE_RADIUS):
                        if (msy >= pos[1] - PIECE_RADIUS) and (msy < pos[1] + PIECE_RADIUS):
                            prev = (self.already_selected.row,
                                    self.already_selected.column)
                            self.already_selected.update_piece_position(
                                self.valid_moves[ind][0], self.valid_moves[ind][1])
                            curr = (self.already_selected.row,
                                    self.already_selected.column)
                            self.last_move = (prev, curr)
                            self.update_board_status()
                            pg.mixer.Sound.play(pg.mixer.Sound(move_snd_1))
                            self.capture_check()
                            if self.already_selected.ptype == "k":
                                self.escape_check()
                            if self.already_selected.ptype != "a":
                                self.attackers_count_check()
                            self.turn = not self.turn
                            done = True
                            break

                self.deselect()

    def ai_move_manager(self, piece, row, column):
        self.already_selected = piece
        prev = (self.already_selected.row, self.already_selected.column)
        self.already_selected.update_piece_position(row-1, column-1)
        curr = (row-1, column-1)
        self.last_move = (prev, curr)
        self.update_board_status()
        pg.mixer.Sound.play(pg.mixer.Sound(move_snd_1))
        self.capture_check()

        if self.already_selected.ptype == "k":
            self.escape_check()
        if self.already_selected.ptype != "a":
            self.attackers_count_check()
        self.turn = not self.turn
        self.deselect()

    def turn_msg(self, game_started):

        consolas = pg.font.SysFont("consolas", 22)
        if not game_started:
            if self.mode == 0:
                write_text(">>> Чтобы начать игру, нажмите соответствующую кнопку", self.screen,
                           (20, BOARD_TOP - 80), white, consolas, False)
            else:
                write_text(">>> Чтобы начать игру, нажмите соответствующую кнопку. ИИ атакует, вы защищаетесь.", self.screen,
                           (20, BOARD_TOP - 80), white, consolas, False)

        elif self.mode == 0 and self.turn:
            write_text(">>> Очередь атакующего", self.screen, (20, BOARD_TOP - 80), white,
                       consolas, False)

        elif self.mode == 1 and self.turn:
            write_text(">>> ИИ думает...", self.screen, (20, BOARD_TOP - 80), white,
                       consolas, False)

        else:
            write_text(">>> Очередь защищающегося", self.screen, (20, BOARD_TOP - 80), white,
                       consolas, False)


class AI_manager:

    def __init__(self, manager, screen):

        self.manager = manager
        self.screen = screen

    def move(self):
        rows = self.manager.board.rows
        columns = self.manager.board.columns
        self.rows = rows
        self.columns = columns

        current_board = []

        border_row = []
        for column in range(columns+2):
            border_row.append("=")
        current_board.append(border_row)

        for row in range(rows):
            one_row = ["="]
            for column in range(columns):
                one_row.append('.')
            one_row.append("=")
            current_board.append(one_row)

        current_board.append(border_row)

        for piece in All_pieces:
            current_board[piece.row+1][piece.column+1] = piece.pid

        current_board[1][1] = current_board[1][rows] = current_board[rows][1] = current_board[rows][columns] = 'x'
        if current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] != 'k':
            current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] = 'x'

        piece, best_move = self.find_best_move(current_board)
        row, col = best_move

        self.manager.ai_move_manager(piece, row, col)

    def find_all_possible_valid_moves(self, board_status_at_this_state, fake_turn):

        valid_moves = []
        piece_pos_this_state = {}
        for row_ind, row in enumerate(board_status_at_this_state):
            for col_ind, column in enumerate(row):
                if column != "." and column != "x" and column != "=":
                    piece_pos_this_state[column] = (row_ind, col_ind)

        for each in piece_pos_this_state.keys():
            piece = each[0]

            if (fake_turn and not piece[0] == "a") or (not fake_turn and piece[0] == "a"):
                continue

            tempr = piece_pos_this_state[each][0]
            tempc = piece_pos_this_state[each][1]

            tempr -= 1
            while tempr >= 0:
                thispos = board_status_at_this_state[tempr][tempc][0]
                if thispos == "a" or thispos == "d" or thispos == "k" or thispos == "=" or (thispos == "x" and piece != "k"):
                    break
                else:
                    if piece == "k":
                        if tempr < piece_pos_this_state[each][0] - 1 or tempr > piece_pos_this_state[each][0] + 1:
                            break
                        valid_moves.append(
                            (piece_pid_map[each], (tempr, tempc)))
                    else:
                        if thispos == ".":
                            valid_moves.append(
                                (piece_pid_map[each], (tempr, tempc)))

                tempr -= 1

            tempr = piece_pos_this_state[each][0]
            tempc = piece_pos_this_state[each][1]

            tempr += 1
            while tempr < self.manager.board.rows+2:
                thispos = board_status_at_this_state[tempr][tempc][0]
                if thispos == "a" or thispos == "d" or thispos == "k" or thispos == "=" or (thispos == "x" and piece != "k"):
                    break
                else:
                    if piece == "k":
                        if tempr < piece_pos_this_state[each][0] - 1 or tempr > piece_pos_this_state[each][0] + 1:
                            break
                        valid_moves.append(
                            (piece_pid_map[each], (tempr, tempc)))
                    else:
                        if thispos == ".":
                            valid_moves.append(
                                (piece_pid_map[each], (tempr, tempc)))

                tempr += 1

            tempr = piece_pos_this_state[each][0]
            tempc = piece_pos_this_state[each][1]

            tempc -= 1
            while tempc >= 0:
                thispos = board_status_at_this_state[tempr][tempc][0]
                if thispos == "a" or thispos == "d" or thispos == "k" or thispos == "=" or (thispos == "x" and piece != "k"):
                    break
                else:
                    if piece == "k":
                        if tempc < piece_pos_this_state[each][1] - 1 or tempc > piece_pos_this_state[each][1] + 1:
                            break
                        valid_moves.append(
                            (piece_pid_map[each], (tempr, tempc)))
                    else:
                        if thispos == ".":
                            valid_moves.append(
                                (piece_pid_map[each], (tempr, tempc)))

                tempc -= 1

            tempr = piece_pos_this_state[each][0]
            tempc = piece_pos_this_state[each][1]

            tempc += 1
            while tempc < self.manager.board.columns+2:
                thispos = board_status_at_this_state[tempr][tempc][0]
                if thispos == "a" or thispos == "d" or thispos == "k" or thispos == "=" or (thispos == "x" and piece != "k"):
                    break
                else:
                    if piece == "k":
                        if tempc < piece_pos_this_state[each][1] - 1 or tempc > piece_pos_this_state[each][1] + 1:
                            break
                        valid_moves.append(
                            (piece_pid_map[each], (tempr, tempc)))
                    else:
                        if thispos == ".":
                            valid_moves.append(
                                (piece_pid_map[each], (tempr, tempc)))

                tempc += 1

        return valid_moves

    def king_mobility(self, fake_board, r, c):
        score = 0
        i = c-1
        while(i != '='):
            if fake_board[r][i] == '.' or fake_board[r][i] == 'x':
                score += 1
            else:
                break
            i -= 1

        i = c+1
        while(i != '='):
            if fake_board[r][i] == '.' or fake_board[r][i] == 'x':
                score += 1
            else:
                break

            i += 1

        i = r-1
        while(i != '='):
            if fake_board[i][c] == '.' or fake_board[i][c] == 'x':
                score += 1
            else:
                break

            i -= 1

        i = r+1
        while(i != '='):
            if fake_board[i][c] == '.' or fake_board[i][c] == 'x':
                score += 1
            else:
                break

            i += 1

        return score

    def king_sorrounded(self, fake_board, r, c):

        score = 0
        if fake_board[r][c+1][0] == 'a':
            score += 1

        if fake_board[r][c-1][0] == 'a':
            score += 1

        if fake_board[r-1][c][0] == 'a':
            score += 1

        if fake_board[r+1][c][0] == 'a':
            score += 1

        return score

    def evaluate(self, fake_board):

        weight_pos = 5
        weight_king_pos_11 = [[10000, 10000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 10000, 10000],
                              [10000, 500, 500, 500, 500, 500,
                              500, 500, 500, 500, 10000],
                              [1000, 500, 200, 200, 200, 200,
                              200, 200, 200, 500, 1000],
                              [1000, 500, 200, 50, 50, 50, 50, 50, 200, 500, 1000],
                              [1000, 500, 200, 50, 10, 10, 10, 50, 200, 500, 1000],
                              [1000, 500, 200, 50, 10, 0, 10, 50, 200, 500, 1000],
                              [1000, 500, 200, 50, 10, 10, 10, 50, 200, 500, 1000],
                              [1000, 500, 200, 50, 50, 50, 50, 50, 200, 500, 1000],
                              [1000, 500, 200, 200, 200, 200,
                              200, 200, 200, 500, 1000],
                              [10000, 500, 500, 500, 500, 500,
                              500, 500, 500, 500, 10000],
                              [10000, 10000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 10000, 10000]]

        # for 9x9 board
        weight_king_pos_9 = [[10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000],
                            [10000, 500, 500, 500, 500, 500, 500, 500, 10000],
                            [10000, 500, 150, 150, 150, 150, 150, 500, 10000],
                            [10000, 500, 150, 30, 30, 30, 150, 500, 10000],
                            [10000, 500, 150, 30, 0, 30, 150, 500, 10000],
                            [10000, 500, 150, 30, 30, 30, 150, 500, 10000],
                            [10000, 500, 150, 150, 150, 150, 150, 500, 10000],
                            [10000, 500, 500, 500, 500, 500, 500, 500, 10000],
                            [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]]

        if self.manager.board_size == "large":
            weight_king_pos = weight_king_pos_11
            weight_attacker = 12
            weight_defender = 24
            weight_king_sorrounded = 50000
        else:
            weight_king_pos = weight_king_pos_9
            weight_attacker = 8
            weight_defender = 12
            weight_king_sorrounded = 10000


        attacker = 0

        defender = 0

        score = 0

        if self.fake_gameOver(fake_board) == 1:  # if 1 then winner is attacker
            print("c")
            score += 10000000
            return score

        elif self.fake_gameOver(fake_board) == 2: #defender win
            score -= 10000000
            return score
        for row_index, row in enumerate(fake_board):
            for col_index, col in enumerate(row):
                if(col == 'k'):
                    r = row_index
                    c = col_index
                elif(col[0] == 'a'):
                    attacker += 1
                elif(col[0] == 'd'):
                    defender += 1

        if r-3 <= 1 and c-3 <= 1:
            if fake_board[1][2][0] == 'a':
                score += 1000
            if fake_board[2][1][0] == 'a':
                score += 1000
        elif r-3 <= 1 and c+3 >=(self.columns):
            if fake_board[1][self.columns-1][0] == 'a':
                score += 1000
            if fake_board[2][self.columns][0] == 'a':
                score += 1000

        elif r+3 >= (self.rows) and c-3 <= 1:
            if fake_board[self.rows-1][1][0] == 'a':
                score += 1000
            if fake_board[self.rows][2][0] == 'a':
                score += 1000

        elif r+3 >=(self.rows) and c+3 >=(self.columns):
            if fake_board[self.rows][self.columns-1][0] == 'a':
                score += 1000
            if fake_board[self.rows-1][self.columns][0] == 'a':
                score += 1000

        score += (attacker*weight_attacker)
        score -= (defender*weight_defender)
        score -= (weight_pos*weight_king_pos[r-1][c-1])
        score += (weight_king_sorrounded *
                  self.king_sorrounded(fake_board, r, c))

        return score

    def fake_move(self, fake_board, commited_move):

        current_board = []
        for row in range(len(fake_board)):
            one_row = []
            for column in range(len(fake_board[0])):
                one_row.append(".")
            current_board.append(one_row)

        for row_index, row in enumerate(fake_board):
            for col_index, column in enumerate(row):
                current_board[row_index][col_index] = column

        for row_index, row in enumerate(current_board):
            f = True
            for column_index, col in enumerate(row):
                if(commited_move[0].pid == col):
                    current_board[row_index][column_index] = "."
                    f = False
                    break

            if not f:
                break

        if current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] == ".":
            current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] = 'x'
        current_board[commited_move[1][0]][commited_move[1]
                                           [1]] = commited_move[0].pid

        current_board, king_captured = self.fake_capture_check(
            current_board, commited_move)

        attacker = 0
        defender = 0
        for row_index, row in enumerate(current_board):
            for col_index, col in enumerate(row):
                if(col[0] == 'a'):
                    attacker += 1
                elif(col[0] == 'd'):
                    defender += 1

        if current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] == ".":
            current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] = 'x'

        return current_board, attacker-defender

    def minimax(self, fake_board, alpha, beta, max_depth, turn):


        bestvalue = -10000000000
        moves = self.find_all_possible_valid_moves(
            fake_board, turn)  # True attacker ,False Defender
        if max_depth <= 0 or self.fake_gameOver(fake_board) == 1 or self.fake_gameOver(fake_board) == 2:
            return self.evaluate(fake_board)

        current_board = []
        for row in range(len(fake_board)):
            one_row = []
            for column in range(len(fake_board[0])):
                one_row.append(".")
            current_board.append(one_row)

        for row_index, row in enumerate(fake_board):
            for col_index, column in enumerate(row):
                current_board[row_index][col_index] = column

        if(turn == True):  # attacker maximizer
            bestvalue = -1000000000000000000
            for i in moves:
                tmp_fake_board, diff = self.fake_move(current_board, i)
                value = self.minimax(tmp_fake_board, alpha,
                                     beta, max_depth-1, False)
                bestvalue = max(value, bestvalue)
                alpha = max(alpha, bestvalue)
                if(beta <= alpha):
                    break

        else:  # defender minimizer
            bestvalue = 1000000000000000000
            for i in moves:
                tmp_fake_board, diff = self.fake_move(current_board, i)
                value = self.minimax(tmp_fake_board, alpha,
                                     beta, max_depth-1, True)
                bestvalue = min(value, bestvalue)
                beta = min(beta, bestvalue)
                if(beta <= alpha):
                    break

        return bestvalue

    def strategy(self, current_board):

        bestvalue = -1000000000000000000
        max_depth = -1
        if AI_LEVEL_HARD == 1:
            max_depth = 2
        elif AI_LEVEL_HARD == 2:
            max_depth = 4
        # True attacker,False Defender
        moves = self.find_all_possible_valid_moves(current_board, True)
        if AI_LEVEL_HARD == 0:
            return moves[random.randint(0, len(moves) - 1)]
        c = 0
        diffs = {}
        for i in moves:
            c += 1
            fake_board, diff = self.fake_move(current_board, i)
            value = self.minimax(fake_board, -1000000000000000000,
                                 1000000000000000000, max_depth-1, False)
            print(value, i[1], diff)
            if(value > bestvalue):
                bestmove = i
                bestvalue = value
                diffs[value] = diff

            elif(value == bestvalue and diff > diffs[value]):
                bestmove = i
                bestvalue = value
                diffs[value] = diff

            if(value == bestvalue and (i[1] == (1, 2) or i[1] == (2, 1) or i[1] == (1, self.columns-1) or i[1] == (2, self.columns) or i[1] == (self.rows-1, 1) or i[1] == (self.rows, 2) or i[1] == (self.rows-1, self.columns) or i[1] == (self.rows, self.columns-1))):
                bestmove = i

        return bestmove

    def find_best_move(self, current_board):

        best_move = self.strategy(current_board)

        return best_move

    def fake_gameOver(self, fake_board):

        # 1 attacker win,2 defender win,3 none win
        if self.fake_king_capture_check(fake_board):
            return 1
        elif self.fake_king_escape(fake_board) or self.fake_attacker_cnt(fake_board):
            return 2
        else:
            return 3

    def fake_capture_check(self, fake_board_with_border, move):

        # storing current piece's type and index
        ptype, prow, pcol = move[0].pid[0], move[1][0], move[1][1]

        # indices of sorrounding one hop cells and two hops cells.
        sorroundings = [(prow, pcol+1), (prow, pcol-1),
                        (prow-1, pcol), (prow+1, pcol)]
        two_hop_away = [(prow, pcol+2), (prow, pcol-2),
                        (prow-2, pcol), (prow+2, pcol)]

        for pos, item in enumerate(sorroundings):

            king_captured = False
            opp = fake_board_with_border[item[0]][item[1]][0]
            try:
                opp2 = fake_board_with_border[two_hop_away[pos]
                                              [0]][two_hop_away[pos][1]][0]
            except:
                opp2 = "."

            if ptype == opp or ptype == "x" or ptype == "=" or opp == "." or opp2 == ".":
                continue

            elif opp == "k":
                king_captured = self.fake_king_capture_check(
                    fake_board_with_border)

            elif ptype != opp:
                if ptype == "a" and (ptype == opp2 or opp2 == "x"):
                    fake_board_with_border[item[0]][item[1]] = '.'

                elif ptype != "a" and opp2 != "a" and opp2 != "=" and opp == "a":
                    fake_board_with_border[item[0]][item[1]] = '.'

        return fake_board_with_border, king_captured


    def fake_king_capture_check(self, fake_board_with_border):

        for row_index, row in enumerate(fake_board_with_border):
            for col_index, col in enumerate(row):
                if col == "k":
                    kingr = row_index
                    kingc = col_index
                    break

        front = fake_board_with_border[kingr][kingc+1][0]
        back = fake_board_with_border[kingr][kingc-1][0]
        up = fake_board_with_border[kingr-1][kingc][0]
        down = fake_board_with_border[kingr+1][kingc][0]

        if front == "x" or back == "x" or up == "x" or down == "x":
            return False

        elif front == "d" or back == "d" or up == "d" or down == "d":
            return False

        elif front == "." or back == "." or up == "." or down == ".":
            return False

        else:
            return True

    def fake_king_escape(self, fake_board):

        r = self.manager.board.rows
        c = self.manager.board.columns
        if fake_board[1][1] == 'k' or fake_board[1][c] == 'k' or fake_board[r][1] == 'k' or fake_board[r][c] == 'k':
            return True

    def fake_attacker_cnt(self, fake_board):


        for row_index, row in enumerate(fake_board):
            for col_ind, col in enumerate(row):
                if col[0] == "a":
                    return False
        return True


def game_window(screen, mode):

    match_specific_global_data_sprites()
    chessboard = ChessBoard(screen)
    chessboard.draw_empty_board()
    chessboard.initiate_board_pieces()
    manager = Game_manager_event_handler(screen, chessboard, mode)
    if mode == 1:
        bot = AI_manager(manager, screen)

    tafle = True
    game_started = False
    while tafle:
        write_text("Сыграть в Тафль", screen, (20, 20), (255, 255, 255),
                   pg.font.SysFont("Arial", 40))
        backbtn = Custom_button(750, 20, "Назад", screen,
                                pg.font.SysFont("Arial", 30))

        write_text("Настройки", screen, (WINDOW_WIDTH - 250, BOARD_TOP), (255, 255, 255),
                   pg.font.SysFont("Arial", 25), False)

        write_text("Размер доски:", screen, (WINDOW_WIDTH - 310, BOARD_TOP + SETTINGS_TEXT_GAP_VERTICAL + 10), (255, 255, 255),
                   pg.font.SysFont("Arial", 20), False)

        size9by9btn = Custom_button(WINDOW_WIDTH - 300 + SETTINGS_TEXT_GAP_HORIZONTAL, BOARD_TOP + SETTINGS_TEXT_GAP_VERTICAL, "9x9", screen,
                                    pg.font.SysFont("Arial", 20), width=50, height=50)

        size11by11btn = Custom_button(WINDOW_WIDTH - 300 + SETTINGS_TEXT_GAP_HORIZONTAL*1.7, BOARD_TOP + SETTINGS_TEXT_GAP_VERTICAL, "11x11", screen,
                                      pg.font.SysFont("Arial", 20), width=50, height=50)

        backbtn = Custom_button(750, 20, "Назад", screen,
                                pg.font.SysFont("Arial", 30))

        if game_started:
            txt = "Заново"
        else:
            txt = 'Новая игра'

        newgamebtn = Custom_button(
            525, 20, txt, screen, pg.font.SysFont("Arial", 30))

        if backbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            main()

        if size9by9btn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_started = False
            match_specific_global_data_sprites()
            chessboard = ChessBoard(screen, "small")
            chessboard.draw_empty_board()
            chessboard.initiate_board_pieces()
            manager = Game_manager_event_handler(screen, chessboard, mode, "small")
            if mode == 1:
                bot = AI_manager(manager, screen)

        if size11by11btn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_started = False
            match_specific_global_data_sprites()
            chessboard = ChessBoard(screen, "large")
            chessboard.draw_empty_board()
            chessboard.initiate_board_pieces()
            manager = Game_manager_event_handler(screen, chessboard, mode, "large")
            if mode == 1:
                bot = AI_manager(manager, screen)

        if newgamebtn.draw_button():
            last_board = manager.board_size
            game_started = True
            match_specific_global_data_sprites()
            chessboard = ChessBoard(screen, last_board)
            chessboard.draw_empty_board()
            chessboard.initiate_board_pieces()
            manager = Game_manager_event_handler(screen, chessboard, mode, last_board)
            if mode == 1:
                bot = AI_manager(manager, screen)

        chessboard.draw_empty_board()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    tafle = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                msx, msy = pg.mouse.get_pos()
                if not manager.finish:
                    if mode == 0:
                        manager.mouse_click_analyzer(msx, msy)
                    else:
                        if manager.turn == False:
                            manager.mouse_click_analyzer(msx, msy)
                            chessboard.draw_empty_board()
                            for piece in All_pieces:
                                piece.draw_piece(screen)
                            if manager.finish:
                                manager.match_finished()
                            else:
                                manager.turn_msg(game_started)
                            if manager.last_move is not None:
                                pg.draw.circle(screen, (232, 13, 13), (BOARD_LEFT+(manager.last_move[0][1]*CELL_WIDTH)+(
                                    CELL_WIDTH/2), BOARD_TOP+(manager.last_move[0][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
                                pg.draw.circle(screen, white, (BOARD_LEFT+(manager.last_move[1][1]*CELL_WIDTH)+(
                                    CELL_WIDTH/2), BOARD_TOP+(manager.last_move[1][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
                            pg.display.update()

        if game_started and mode == 1 and manager.turn and not manager.finish:

            chessboard.draw_empty_board()
            for piece in All_pieces:
                piece.draw_piece(screen)
            if manager.finish:
                manager.match_finished()
            else:
                manager.turn_msg(game_started)
            if manager.last_move is not None:
                pg.draw.circle(screen, (232, 13, 13), (BOARD_LEFT+(manager.last_move[0][1]*CELL_WIDTH)+(CELL_WIDTH/2), BOARD_TOP+(
                    manager.last_move[0][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
                pg.draw.circle(screen, white, (BOARD_LEFT+(manager.last_move[1][1]*CELL_WIDTH)+(CELL_WIDTH/2), BOARD_TOP+(
                    manager.last_move[1][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
            pg.display.update()
            print("c")
            bot.move()
        for piece in All_pieces:
            piece.draw_piece(screen)

        manager.show_valid_moves()
        if manager.finish:
            manager.match_finished()
        else:
            manager.turn_msg(game_started)

        if manager.last_move is not None:
            pg.draw.circle(screen, (232, 13, 13), (BOARD_LEFT+(manager.last_move[0][1]*CELL_WIDTH)+(CELL_WIDTH/2), BOARD_TOP+(
                manager.last_move[0][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
            pg.draw.circle(screen, white, (BOARD_LEFT+(manager.last_move[1][1]*CELL_WIDTH)+(CELL_WIDTH/2), BOARD_TOP+(
                manager.last_move[1][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
        pg.display.update()


def rules(screen):
    tafle = True
    while tafle:
        write_text("Правила игры", screen, (20, 20), (255, 255, 255),
                   pg.font.SysFont("Arial", 40))
        backbtn = Custom_button(750, 20, "Назад", screen,
                                pg.font.SysFont("Arial", 30))

        if backbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            main()

        msgs = []
        msgs.append("2 игровых режима для доски: \"большая\" - 11x11 и \"малая\" - 9x9.")
        msgs.append("Центральная клетка и 4 угловые клетки называются \"недоступными\"")
        msgs.append("Все фигуры, кроме короля, могут ходить на любое количество ячеек по горизонтали или вертикали.")
        msgs.append("Король может передвигаться только на одну клетку за раз.")
        msgs.append("Только король может переместиться на любую из недоступных ячеек.")
        msgs.append("Фигуры, за исключением короля, можно захватить, зажав их с обеих сторон.")
        msgs.append("Ячейки с ограниченным доступом могут быть использованы для уничтожения противника.")
        msgs.append("Только одна фигура противника может быть захвачена в одну линию одним ходом.")
        msgs.append("Несколько фигур могут быть захвачены одним ходом.")
        msgs.append("Чтобы захватить короля, нападающим нужно окружить его со всех четырех сторон его клетки.")
        msgs.append("Если король захвачен, нападающие выигрывают.")
        msgs.append("Если король убежит на любую из четырех угловых клеток, защитники выиграют.")
        msgs.append("Если все нападающие будут схвачены, защитники победят.")
        
        consolas = pg.font.SysFont("consolas", 20)
        cnt = 0
        for msg in msgs:
            write_text(msg, screen, (20, BOARD_TOP - 80 + 40*cnt), white, consolas, False)
            cnt += 1        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    tafle = False
        pg.display.update()


def history(screen):
    tafle = True
    while tafle:
        write_text("History", screen, (20, 20), (255, 255, 255),
                   pg.font.SysFont("Arial", 40))
        backbtn = Custom_button(750, 20, "Назад", screen,
                                pg.font.SysFont("Arial", 30))

        if backbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            main()
            
        msgs = []
        
        consolas = pg.font.SysFont("consolas", 20)
        cnt = 0
        for msg in msgs:
            write_text(msg, screen, (20, BOARD_TOP - 80 + 40*cnt), white, consolas, False)
            cnt += 1        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    tafle = False
        pg.display.update()


def main():
    global AI_LEVEL_HARD
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH+100, WINDOW_HEIGHT))
    pg.display.set_caption(GAME_NAME)
    pg.display.set_icon(GAME_ICON)

    icon_rect = GAME_ICON_resized.get_rect(
        center=(500, MAIN_MENU_TOP_BUTTON_y-150))

    game_on = True

    while game_on:        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_on = False
                pg.quit()

        screen.fill(bg2)

        msgs = [["Добро пожаловать в Тафль!", (250, 20)], [AI_POSS_LEVELS[AI_LEVEL_HARD], (70, MAIN_MENU_TOP_BUTTON_y-150)], ["Уровень силы ИИ:", (70, MAIN_MENU_TOP_BUTTON_y-200)]]
        #myfont1 = pg.font.SysFont("Times New Roman", 30)
        #label = myfont1.render(msgs[1][0], 1, (255, 255 - 255 // 2 * AI_LEVEL_HARD, 0))
        for msg in msgs:
            size = 30
            if msg[0] == "Добро пожаловать в Тафль!":
                size = 50
                write_text(msg[0], screen, msg[1], (255, 255, 255), pg.font.SysFont("Times New Roman", size), False)
            else:
                if msg[0] != "Уровень силы ИИ:":
                    write_text(msg[0], screen, msg[1], (255, 255 - 255 // 2 * AI_LEVEL_HARD, 0), pg.font.SysFont("Times New Roman", size), False)
                    #screen.blit(label, msgs[1][1])
                else:
                    write_text(msg[0], screen, msg[1], white, pg.font.SysFont("Times New Roman", size), False)

        btn_font = pg.font.SysFont("Times New Roman", 28)
        gamebtn_1 = Custom_button(
            MAIN_MENU_TOP_BUTTON_x - 110, MAIN_MENU_TOP_BUTTON_y, "Игра на двоих", screen, btn_font)
        gamebtn_2 = Custom_button(
            MAIN_MENU_TOP_BUTTON_x + 110, MAIN_MENU_TOP_BUTTON_y, "Против ИИ", screen, btn_font)
        rulesbtn = Custom_button(
            MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 100, "Правила", screen, btn_font)
        historybtn = Custom_button(
            MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 200, "Сила ИИ", screen, btn_font)
        exitbtn = Custom_button(
            MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 300, "Выход", screen, btn_font)

        if gamebtn_1.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_window(screen, mode=0)

        if gamebtn_2.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_window(screen, mode=1)

        if rulesbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            rules(screen)

        if historybtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            AI_LEVEL_HARD = (AI_LEVEL_HARD + 1) % 3

        if exitbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_on = False
            pg.quit()        

        screen.blit(GAME_ICON_resized, (icon_rect))
        pg.display.update()


if __name__ == "__main__":
    main()