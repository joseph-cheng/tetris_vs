from board import Board
from piece import Piece
from player import Player
from colour import Colour
import random

class State:

    MOVE_DELAY = 10
    MOVE_INTERVAL = 5
    
    def __init__(self, game_w, game_h, board_w, board_h):
        self.board = Board(board_w, board_h)
        self.w = game_w
        self.h = game_h

        self.T = 0.2
        
        self.block_pool = list("iotszjl"*4)
        random.shuffle(self.block_pool)
        
        self.current_piece = Piece(self.block_pool.pop(0), board_w//2-1, 0)
        self.held_piece_shape = ""
        self.held_this_turn = False

        self.player = Player(100,100, 10)
        
        self.tick_num = 0
        self.step_max = 30
        self.fast_step = 3
        self.current_step = self.step_max


        self.movement = 0
        self.counter = State.MOVE_DELAY

        #self.generate_junk_lines(self.board.h//2)




    def generate_new_piece(self):
        for block in self.current_piece.blocks:
            self.board.board[block[1]][block[0]] = self.current_piece.colour.value
        piece_shape = self.block_pool.pop(0)
        self.current_piece = Piece(piece_shape, self.board.w//2-1, 0)
        
        if len(self.block_pool) == 7:
            self.block_pool += random.sample("iotszjl"*3, 21)

    def hold_piece(self):
        if not(self.held_this_turn):
            if self.held_piece_shape == "":
                self.held_piece_shape = self.current_piece.shape
                piece_shape = self.block_pool.pop(0)
                self.current_piece = Piece(piece_shape, self.board.w//2-1, 0)
                
                if len(self.block_pool) == 7:
                    self.block_pool += random.sample("iotszjl"*3, 21)
            else:
                current_piece_shape = self.current_piece.shape
                self.current_piece = Piece(self.held_piece_shape, self.board.w//2-1, 0)
                self.held_piece_shape = current_piece_shape
            self.held_this_turn = True
        
    def step(self):
        generated_new_piece = False
        
        
        can_move = True
        for block in self.current_piece.blocks:

            if block[1] == self.board.h-1 or self.board.board[block[1]+1][block[0]] != 0 :
                can_move = False

        if can_move:
            self.current_piece.move([0, 1])
        else:
            self.generate_new_piece()
            generated_new_piece = True

        self.check_for_completed_rows()
        return generated_new_piece
        
    def check_for_completed_rows(self):
        for row_num, row in enumerate(self.board.board):
            if all(row):
                self.board.board[row_num] = [0 for _ in range(self.board.w)]
                for other_row_num in range(row_num-1, -1, -1):

                    self.board.board[other_row_num+1] = self.board.board[other_row_num][:]

    def generate_junk_lines(self, num_of_junk_lines):
        for row_num in range(num_of_junk_lines, self.board.h):
            self.board.board[row_num-num_of_junk_lines] = self.board.board[row_num][:]
            
        for row_num in range(self.board.h-num_of_junk_lines, self.board.h):
            empty_pos = random.randint(0,self.board.w-1)
            self.board.board[row_num] = [0 if _ == empty_pos else random.randint(1, len(Colour)-1) for _ in range(self.board.w)]
            

    def update(self):

        
        if self.tick_num % self.current_step == 0:
            generated_new_piece = self.step()
            if generated_new_piece:
                self.held_this_turn = False

        if self.movement:
            self.counter -= 1
        if self.counter == 0:
            can_move = True
            for block in self.current_piece.blocks:
                if block[0] == (0 if self.movement==-1 else self.board.w-1) or self.board.board[block[1]][block[0]+self.movement] != 0:
                    can_move = False

            if can_move:
                self.current_piece.move([self.movement,0])
            self.counter = State.MOVE_INTERVAL

        self.player.update(self)
        
        self.tick_num += 1
