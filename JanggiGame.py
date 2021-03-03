# exceptions

class InvalidCapture(Exception):
    pass

class InvalidMove(Exception):
    pass

# pieces

class Piece:
    
    def __init__(self, color=None, space=None):
        self._color = color
        self._space = space
        if space is not None:
            space.add_piece(self)
            
    def __str__(self):
        return f"piece at {self.space}"
    
    @property
    def space(self):
        return self._space
    
    @property
    def is_blue(self):
        if self._color == "blue":
            return True
        return False
    
    @property
    def is_red(self):
        if self._color == "red":
            return True
        return False
    
    @property
    def color(self):
        return self._color
    
    def get_forward_space(self, board):
        if self.is_blue:
            return board.get_top_space(self.space.as_str)
        else:
            return board.get_bottom_space(self.space.as_str)
    
    def get_right_space(self, board):
        if self.is_blue:
            return board.get_right_space(self.space.as_str)
        else:
            return board.get_left_space(self.space.as_str)
    
    def get_left_space(self, board):
        if self.is_blue:
            return board.get_left_space(self.space.as_str)
        else:
            return board.get_right_space(self.space.as_str)
    
    def get_backward_space(self, board):
        if self.is_blue:
            return board.get_bottom_space(self.space.as_str) 
        else:
            return board.get_top_space(self.space.as_str)
    
    def change_space(self, new_space):
        self._space = new_space
        
    def capture(space):
        if space.has_piece and space.get_piece().color != self.color:
            space.remove_piece()
            space.add_piece(self)
            self._space = space
        else:
            raise InvalidCapture
            
    

class General(Piece):
    
    def move(new_space):
        pass
        # 1. figures out what the possible spaces it can move to are
        # 2. sees if the new space is one of the possible spaces it can move to
        # 3. if it is a possible move, it see's if the new space has an opponents piece
        #    and if it does, it captures it, removing it form the space, and then updating the space's piece and its space
        # Notes: Once the opponents piece is removed, it can be deleted from memory.

class Guard(Piece):

    def move(new_space):
        pass

class Horse(Piece):
    
    def is_blocked(self, new_space, board): # this can either be a red or blue piece
        row_diff = abs(self.space.row - new_space.row)
        
        if row_diff == 2: # first move is forward
            space_to_check = self.get_forward_space(board)
        elif (new_space.col - self.space.col) > 0: # first move is to the right
            space_to_check = self.get_right_space(board)
        else: # first move is to the left
            space_to_check = self.get_left_space(board)
            
        if space_to_check.has_piece:
            return True
        return False
                
    
    def is_valid_move(self, new_space, board):
        # piece has to move forward
        if (self.is_blue and new_space.row >= self.space.row) or (self.is_red and new_space.row <= self.space.row):
            return False
        if self.is_blocked(new_space, board):
            return False
        if new_space.piece is not None:
            if new_space.piece.color == self.color: # the new space already has a player's piece
                return False
        delta_row = abs(new_space.row - self.space.row)
        delta_col = abs(new_space.col - self.space.col)
        return delta_row * delta_col == 2
    
    def move(self, new_space, board):
        if self.is_valid_move(new_space, board):
            self.change_space(new_space)
            if new_space.has_opponent_piece(self.color):
                new_space.remove_piece()
            new_space.add_piece(self)
        else:
            raise InvalidMove(f"{self} can't move to {new_space}")

class Elephant(Piece):
    
    def is_valid_move(self, new_space, board):
        # piece has to move foreward
        if (self.is_blue() and new_space.row >= self.space.row) or (self.is_red() and new_space.row <= self.space.row):
            return False
        if self.is_blocked(new_space, board):
            return False
        delta_row = abs(new_space.row - self.space.row)
        delta_col = abs(new_space.col - self.space.col)
        return delta_row * delta_col == 6
         
    
    def move(new_space):
        pass

class Chariot(Piece):
    
    def move(new_space, board):
        if new_space.col != self.space.col and new_space.row != self.space.row:
            raise InvalidMove
        
            
            

class Cannon(Piece):
    
    def move(new_space):
        pass

class Soldier(Piece):
    
    def is_valid_move(self):
        pass
    
    def move(new_space):
        pass

# other objects
# -------------

# probably not needed
class Space:
    
    def __init__(self, col, row, piece=None):
        self._col = ord(col) # 'a' -> 97
        self._row = int(row)
        self._piece = piece
        if piece is not None:
            piece.change_space(self)
        
    def __str__(self):
        return self.as_str
    
    def __repr__(self):
        return self.as_str
    
    @property
    def row(self):
        return self._row
    
    @property
    def row_str(self):
        return str(self._row)
    
    @property
    def col(self):
        return self._col
    
    @property
    def col_str(self):
        return chr(self._col)
    
    @property
    def as_str(self):
        return self.col_str+self.row_str
    
    @property
    def has_piece(self):
        if self._piece is None:
            return False
        return True
    
    @property
    def piece(self):
        return self._piece
    
    def remove_piece(self):
        self._piece = None
    
    def add_piece(self, piece):
        if not self.has_piece:
            self._piece = piece
    
    def has_opponent_piece(self, color):
        if self.has_piece and self.piece.color != color:
            return True
        return False
    
class Board:
    
    def __init__(self):
        self.spaces = {col+str(row): Space(col, row) for col in "abcdefghi" for row in range(1,11)}
    
    def get_space(self, space):
        try:
            return self.spaces[space]
        except KeyError:
            return None
    
    def get_right_space(self, space):
        col = chr(ord(space[0])+1)
        row = space[1]
        return self.get_space(col+row)
    
    def get_left_space(self, space):
        col = chr(ord(space[0])-1)
        row = space[1]
        return self.get_space(col+row)
    
    def get_top_space(self, space):
        col = space[0]
        row = str(int(space[1])-1)
        return self.get_space(col+row)
    
    def get_bottom_space(self, space):
        col = space[0]
        row = str(int(space[1])+1)
        return self.get_space(col+row)

class JanggiGame:
    
    def __init__(self):
        self._board = Board()