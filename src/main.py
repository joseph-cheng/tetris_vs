import pygame
from state import State
from renderer import Renderer

screen_w = 500
screen_h = 700
board_tiles_w = 10
board_tiles_h = 20
board_screen_w = 300
board_screen_h = 600


state_obj = State(board_screen_w, board_screen_h, board_tiles_w, board_tiles_h)
renderer_obj = Renderer(screen_w,screen_h, board_screen_w, board_screen_h, board_tiles_w, board_tiles_h)
clock = pygame.time.Clock()

def key_callback(state_obj):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_a:


                state_obj.movement = -1
                can_move = True
                for block in state_obj.current_piece.blocks:
                    if block[0] == 0 or state_obj.board.board[block[1]][block[0]-1] != 0:
                        can_move = False

                if can_move:
                    state_obj.current_piece.move([-1,0])
                
            elif event.key == pygame.K_d:
                state_obj.movement = 1

                can_move = True
                for block in state_obj.current_piece.blocks:
                    if block[0] == state_obj.board.w or state_obj.board.board[block[1]][block[0]+1] != 0:
                        can_move = False

                if can_move:
                    state_obj.current_piece.move([1,0])

                    
            elif event.key == pygame.K_w or event.key == pygame.K_h:
                state_obj.current_piece.rotate(1)
                for block in state_obj.current_piece.blocks:
                    if state_obj.board.board[block[1]][block[0]] != 0 or block[0] < 0 or block[0] >= state_obj.board.w or block[1] >= state_obj.board.h:
                        state_obj.current_piece.rotate(-1)
                        break
                    
            elif event.key == pygame.K_g:

                state_obj.current_piece.rotate(-1)

                for block in state_obj.current_piece.blocks:
                    if state_obj.board.board[block[1]][block[0]] != 0 or block[0] < 0 or block[0] >= state_obj.board.w or block[1] >= state_obj.board.h:
                        state_obj.current_piece.rotate(1)
                        break

                state_obj.generate_junk_lines(2)
            
            elif event.key == pygame.K_s:
                state_obj.current_step = state_obj.fast_step

            elif event.key == pygame.K_LSHIFT:
                state_obj.hold_piece()

            elif event.key == pygame.K_SPACE:
                while not(state_obj.step()):
                    pass
                state_obj.held_this_turn = False


            elif event.key == pygame.K_LEFT:
                state_obj.player.left_down = True
            elif event.key == pygame.K_RIGHT:
                state_obj.player.right_down = True
            elif event.key == pygame.K_UP:
                state_obj.player.apply_force([0,-200])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                state_obj.current_step = state_obj.step_max
            elif event.key == pygame.K_a:
                state_obj.movement = 0
                state_obj.counter = State.MOVE_DELAY
            elif event.key == pygame.K_d:
                state_obj.movement = 0
                state_obj.counter = State.MOVE_DELAY

            elif event.key == pygame.K_LEFT:
                state_obj.player.left_down = False
            elif event.key == pygame.K_RIGHT:
                state_obj.player.right_down = False


while True:

    key_callback(state_obj)

    state_obj.update()

    renderer_obj.render(state_obj)
    clock.tick(Renderer.FPS)
