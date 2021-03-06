import pygame

class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0

        self.max_y_vel = 100
        
        self.x_accel = 0
        self.y_accel = 0

        self.mass = 1

        self.damping = 0.3
        
        self.radius = radius
        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)

        self.left_down = False
        self.right_down = False
        self.on_right_wall = False
        self.on_left_wall = False
        self.on_floor = False
        

    def update(self, state_obj):
        self.apply_force([40 * self.right_down - 40*self.left_down,0])

        self.x += self.x_vel * state_obj.T + 0.5 * self.x_accel * state_obj.T**2

     
        self.x_vel = (1-self.damping) * (self.x_vel + self.x_accel * state_obj.T)
        
        self.x_accel = 0
        
        #Touching right boundary
        if self.x + self.radius > state_obj.w:
            self.x = state_obj.w-self.radius
            self.x_vel = 0
            self.on_right_wall = True

        #touching left boundary
        elif self.x - self.radius < 0:
            self.x = self.radius
            self.x_vel = 0
            self.on_left_wall = True

        self.on_right_wall = self.on_right_wall and self.right_down
        self.on_left_wall = self.on_left_wall and self.left_down


        
        self.rect.centerx = int(self.x)

        cell_width = state_obj.w//state_obj.board.w
        cell_height = state_obj.h//state_obj.board.h


        for row_num,row in enumerate(state_obj.board.board):
            for col_num, cell in enumerate(row):
                if cell == 0:
                    continue
                cell_rect = pygame.Rect(col_num*cell_width,
                                        row_num*cell_height,
                                        cell_width,
                                        cell_height)
                if self.rect.colliderect(cell_rect):
                    self.resolve_collision(cell_rect, "x")

        if self.on_right_wall or self.on_left_wall:
            self.max_y_vel = 10
        else:
            self.max_y_vel = 100
        self.apply_force([0,self.mass*9.8])
        
        if abs(self.y_vel) > self.max_y_vel:
            self.apply_force([0, -self.y_vel/abs(self.y_vel) * self.mass * 20])
            
        self.y += self.y_vel * state_obj.T + 0.5 * self.y_accel * state_obj.T**2

        self.y_vel = (self.y_vel + self.y_accel * state_obj.T)

        self.y_accel = 0

        self.rect.centery = int(self.y)

        #touching bottom
        if self.y + self.radius > state_obj.h:
            self.y = state_obj.h-self.radius
            self.y_vel = 0
            print("PLATFORMER LOSES")
            self.on_floor = True
        elif self.y - self.radius < 0:
            self.y = self.radius
            self.y_vel = 0

        for row_num,row in enumerate(state_obj.board.board):
            for col_num, cell in enumerate(row):
                if cell == 0:
                    continue
                cell_rect = pygame.Rect(col_num*cell_width,
                                        row_num*cell_height,
                                        cell_width,
                                        cell_height)
                if self.rect.colliderect(cell_rect):
                    self.resolve_collision(cell_rect, "y")



    def apply_force(self, force):
        self.x_accel += force[0]/self.mass
        self.y_accel += force[1]/self.mass

            
    def resolve_collision(self, other_rect,direction):



        if direction == "x":
            #Touching left
            collision_depth = 0
            if self.x_vel > 0:
                collision_depth = other_rect.left - self.rect.right
                self.on_right_wall = True

            #Touching right
            elif self.x_vel < 0:
                collision_depth = other_rect.right-self.rect.left
                self.on_left_wall = True
            

            self.x_vel = 0
            self.x += collision_depth
            self.rect.centerx = self.x

        elif direction == "y":
        #Touching top
            collision_depth = 0
            if self.y_vel >= 0:
                collision_depth = other_rect.top - self.rect.bottom
                self.on_floor = True
                
            #Touching bottom
            elif self.y_vel < 0:
                collision_depth = other_rect.bottom - self.rect.top

            self.y_vel = 0

            self.y += collision_depth
            self.rect.centery = self.y



        
