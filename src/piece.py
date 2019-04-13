from colour import Colour

class Piece:
    def __init__(self, shape, start_x, start_y):
        self.blocks = []
        self.shape = shape
        self.centre = [0,0]

        if shape == "i":
            self.blocks = [[start_x  , start_y+1],
                           [start_x+1, start_y+1],
                           [start_x+2, start_y+1],
                           [start_x+3, start_y+1]
                           ]
            self.centre = [start_x+1.5, start_y+1.5]
            self.colour = Colour.CYAN
            
            
        elif shape == "o":
            self.blocks = [[start_x  , start_y  ],
                           [start_x+1, start_y  ],
                           [start_x  , start_y+1],
                           [start_x+1, start_y+1]]
            self.centre = [start_x+0.5, start_y+0.5]
            self.colour = Colour.YELLOW

        elif shape == "t":
            self.blocks = [[start_x+1, start_y  ],
                           [start_x  , start_y+1],
                           [start_x+1, start_y+1],
                           [start_x+2, start_y+1]]
            self.centre = [start_x+1, start_y+1]
            self.colour = Colour.PURPLE

        elif shape == "s":
            self.blocks = [[start_x+1, start_y  ],
                           [start_x+2, start_y  ],
                           [start_x  , start_y+1],
                           [start_x+1, start_y+1]]
            self.centre = [start_x+1, start_y+1]
            self.colour = Colour.GREEN

        elif shape == "z":
            self.blocks = [[start_x  , start_y  ],
                           [start_x+1, start_y  ],
                           [start_x+1, start_y+1],
                           [start_x+2, start_y+1]]
            self.centre = [start_x+1, start_y+1]
            self.colour = Colour.RED

        elif shape == "j":
            self.blocks = [[start_x  , start_y  ],
                           [start_x  , start_y+1],
                           [start_x+1, start_y+1],
                           [start_x+2, start_y+1]]
            self.centre = [start_x+1, start_y+1]
            self.colour = Colour.BLUE

        elif shape == "l":
            self.blocks = [[start_x+2, start_y  ],
                           [start_x  , start_y+1],
                           [start_x+1, start_y+1],
                           [start_x+2, start_y+1]]
            self.centre = [start_x+1, start_y+1]
            self.colour = Colour.ORANGE


    def rotate(self, direction):
        #direction=1 means clockwise
        #direction=-1 means anticlockwise

        #convert blocks to be about centre

        new_blocks =[[x[0]-self.centre[0], x[1]-self.centre[1]] for x in self.blocks]

        #Rotate using (x,y) -> (-y, x)
        #          or (x,y) -> (y, -x)
        if direction == 1:
            new_blocks = [[-x[1], x[0]] for x in new_blocks]
        else:
            new_blocks = [[x[1], -x[0]] for x in new_blocks]

        #Return back to regular coordinates
        self.blocks = [[int(x[0]+self.centre[0]), int(x[1]+self.centre[1])] for x in new_blocks]


    def move(self, direction):
        #direction in format [-1/0/1, -1/0/1]

        self.blocks = [[x[0]+direction[0], x[1]+direction[1]] for x in self.blocks]
        self.centre = [self.centre[0]+direction[0], self.centre[1]+direction[1]]

