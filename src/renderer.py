import pygame
from piece import Piece

class Renderer:
    FPS = 60
    def __init__(self, w, h, board_w, board_h, board_cells_w, board_cells_h):
        self.w = w
        self.h = h
        self.board_w = board_w
        self.board_h = board_h
        self.cell_width = self.board_w // board_cells_w
        self.cell_height = self.board_h // board_cells_h
        self.screen = pygame.display.set_mode((w,h))

        self.colour_dict = {0: (0  ,0  ,0  ),
                       1: (0  ,255,255),
                       2: (255,255,0  ),
                       3: (128,0  ,128),
                       4: (0  ,255,0  ),
                       5: (255,0  ,0  ),
                       6: (0  ,0  ,255),
                       7: (255,165,0  )}
                       

    def render(self, state_obj):
        self.screen.fill((0,0,0))
        for row_num, row in enumerate(state_obj.board.board):
            for col_num, cell in enumerate(row):
                pygame.draw.rect(self.screen,
                                 self.colour_dict[cell],
                                 (col_num*self.cell_width+1,
                                  row_num*self.cell_height+1,
                                  self.cell_width-1,
                                  self.cell_height-1))

        #basically find the position of the block if you were to hard drop
        minimum_distance_down = 99999
        for block in state_obj.current_piece.blocks:
            distance_down = 0
            for row in range(block[1]+1, state_obj.board.h):
                if state_obj.board.board[row][block[0]] == 0:
                    distance_down += 1
                else:
                    break
            minimum_distance_down = min(minimum_distance_down, distance_down)
            
            
            
        for block in state_obj.current_piece.blocks:
            #draw shadow
            pygame.draw.rect(self.screen,
                             tuple(col*0.5 for col in self.colour_dict[state_obj.current_piece.colour.value]),
                             (block[0]*self.cell_width+1,
                              (block[1]+minimum_distance_down)*self.cell_height+1,
                              self.cell_width-1,
                              self.cell_height-1))

            #draw block
            pygame.draw.rect(self.screen,
                             self.colour_dict[state_obj.current_piece.colour.value],
                             (block[0]*self.cell_width+1,
                              block[1]*self.cell_height+1,
                              self.cell_width-1,
                              self.cell_height-1))

        pygame.draw.circle(self.screen, (255,255,255), (int(state_obj.player.x), int(state_obj.player.y)), state_obj.player.radius, 1)
        
        #render next pieces
        self.render_piece(state_obj.block_pool[0], [self.board_w+75, 50])

        #render held piece
        if state_obj.held_piece_shape:
            self.render_piece(state_obj.held_piece_shape, [self.board_w//2-50, self.board_h+50])

        #draw border
        pygame.draw.rect(self.screen,
                         (128,128,128),
                         (0,0, self.board_w+4, self.board_h+4), 5)
        
        pygame.display.flip()

    def render_piece(self, piece_shape, pos):
        p = Piece(piece_shape, pos[0]//self.cell_width, pos[1]//self.cell_height)
        for block in p.blocks:
            pygame.draw.rect(self.screen,
                                 self.colour_dict[p.colour.value],
                                 (block[0]*self.cell_width+1,
                                  block[1]*self.cell_height+1,
                                  self.cell_width-1,
                                  self.cell_height-1))

                
