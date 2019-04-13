class Board:
    def __init__(self,w,h):
        self.w = w
        self.h = h
        self.board = [[0 for _ in range(self.w)] for _ in range(self.h)]

        
