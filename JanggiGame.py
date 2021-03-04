# exceptions

class InvalidCapture(Exception):
    pass

class InvalidMove(Exception):
    pass

class Space:
    
    def __new__(cls, space=None):
        if space is None:
            return None
        return super().__new__(cls) 
         
    def __init__(self, space):
        self._col, self._row = ord(space[0]), int(space[1:])
        
    def __str__(self):
        return chr(self.col)+str(self.row)
        
    @property
    def row(self):
        return self._row
    
    @property
    def col(self):
        return self._col
        

# pieces

class Piece:
    
    def __init__(self, color=None, space=None, board=None):
        self._color = color
        self._space = Space(space)
        self._board = board
        if space is not None and board is not None:
            board.place_piece(self, space)
            
            
    def __str__(self):
        return f"{self._color[0]}{self.__class__.__name__}"
    
    def __repr__(self):
        return f"{self._color[0]}{self.__class__.__name__}"
    
    @property
    def space(self):
        return self._space
    
    @property
    def row(self):
        return self._space.row
    
    @property
    def col(self):
        return self._space.col
    
    @property
    def color(self):
        return self._color
    
    def get_forward_space(self, starting_space=None):
        starting_space = Space(starting_space)
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_space(space)
        return self._board.get_bottom_space(space)
    
    def get_right_space(self, starting_space=None):
        starting_space = Space(starting_space)
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_right_space(space)
        return self._board.get_left_space(space)
    
    def get_left_space(self, starting_space=None):
        starting_space = Space(starting_space)
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_left_space(space)
        return self._board.get_right_space(space)
    
    def get_backward_space(self, starting_space=None):
        starting_space = Space(starting_space)
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_bottom_space(space) 
        return self._board.get_top_space(space)
    
    def get_diagonal_right(self, starting_space=None):
        starting_space = Space(starting_space)
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_right_space(space) 
        return self._board.get_bottom_left_space(space)      
    
    def get_diagonal_left(self, starting_space=None):
        starting_space = Space(starting_space)
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_left_space(space) 
        return self._board.get_bottom_right_space(space)
    
    def change_space(self, new_space):
        new_space = self._board.move_piece(self, new_space)
        self._space = new_space
        self._row = new_space.row or None
        self._col = new_space.col or None
        
    def is_valid_move(self, new_space, board, test_num):
        is_blue = self.color == "blue"
        is_red = self.color == "red"
        # piece has to move forward
        if (is_blue and new_space[1:] >= self.row) or (is_red and new_space[1:] <= self.row):
            return False
        if board.has_piece(new_space):
            if board.get_piece(new_space).color == self.color: # the new space already has a player's piece
                return False
        delta_row = abs(new_space[1:] - self.row)
        delta_col = abs(new_space[0] - self.col)
        return delta_row * delta_col == test_num
        
    def capture(space, board):
        if board.has_piece(space):
            if board.get_piece(space).color != self.color:
                board.remove_piece(space)
            else:
                raise InvalidCapture(f"{space} has {self.color} piece")
        else:
            raise InvalidCapture(f"{space} does not have piece")
            
    

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
    
    def is_blocked(self, new_space): # this can either be a red or blue piece
        new_space = Space(new_space)
        row_diff = abs(self.row - new_space.row)
        
        if row_diff == 2: # first move is forward
            space_to_check = self.get_forward_space()
        elif (ord(new_space[0]) - self.col) > 0: # first move is to the right
            space_to_check = self.get_right_space()
        else: # first move is to the left
            space_to_check = self.get_left_space()
            
        if self._board.has_piece(space_to_check):
            return True
        return False
    
    def move(self, new_space, board):
        if self.is_valid_move(new_space, board, 2):
            if self.is_blocked(new_space, board):
                raise InvalidMove(f"{self} can't move to {new_space} b/c it's blocked")
            self.change_space(new_space)
            if new_space.has_opponent_piece(self.color):
                self.capture(new_space)
            new_space.add_piece(self)
        else:
            raise InvalidMove(f"{self} can't move to {new_space}")

class Elephant(Piece):
    
    def is_blocked(self, new_space, board):
        row_diff = abs(self.row - new_space.row)
        move_is_right = (new_space.col - self.space.col) > 0
        
        if row_diff == 3:
            space_to_check = self.get_forward_space(board)
        elif move_is_right:
            space_to_check = self.get_right_space(board)
        else:
            space_to_check = self.get_left_space(board)
            
        if move_is_right:
            next_space = space_to_check.get_diagonal_right(board)
        else:
            next_space = space_to_check.get_diagonal_left(board)
            
        if space_to_check.has_piece or next_space.has_piece:
            return True
        return False
            
            
    def move(new_space):
        if self.is_valid_move(new_space, board, 6):
            if self.is_blocked(new_space, board):
                raise InvalidMove(f"{self} can't move to {new_space} b/c it's blocked")
            self.change_space(new_space)
            if new_space.has_opponent_piece(self.color):
                self.capture(new_space)
            new_space.add_piece(self)
        else:
            raise InvalidMove(f"{self} can't move to {new_space}")

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


    
class Board:
    
    def __init__(self):
        self.spaces = {col+str(row): None for col in "abcdefghi" for row in range(1,11)}
        
    def assign_space(self, space, obj):
        if str(space) in self.spaces:
            self.spaces[str(space)] = obj
        else:
            raise InvalidSpace(f"{space} is not a valid space")
        
    def get_row(self, row):
        return [self.spaces[space] for space in self.spaces.keys() if int(space[1:]) == row]
    
    def has_piece(self, space):
        if self.spaces[str(space)] is None:
            return False
        return True
    
    def place_piece(self, piece, space):
        if space in self.spaces:
            if self.spaces[space] is not None:
                print("can't do that")
            else:
                self.assign_space(space, piece)
        else:
            raise InvalidSpace(f"{space} is not a valid space")
            
    
    def move_piece(self, piece, new_space):
        if self.spaces[new_space] is not None:
            return piece.space
        self.assign_space(piece.space, None)
        self.assign_space(new_space, piece)
        return Space(new_space)
    
    def get_right_space(self, space):
        col = chr(space.col+1)
        row = str(space.row)
        return Space(col+row)
    
    def get_left_space(self, space):
        col = chr(space.col-1)
        row = str(space.row)
        return Space(col+row)
    
    def get_top_space(self, space):
        col = chr(space.col)
        row = str(space.row-1)
        return Space(col+row)
    
    def get_bottom_space(self, space):
        col = chr(space.col)
        row = str(space.row+1)
        return Space(col+row)
    
    def get_top_right_space(self, space):
        col = chr(space.col+1)
        row = str(space.row-1)
        return Space(col+row)
    
    def get_top_left_space(self, space):
        col = chr(space.col-1)
        row = str(space.row-1)
        return Space(col+row)
    
    def get_bottom_right_space(self, space):
        col = chr(space.col+1)
        row = str(space.row+1)
        return Space(col+row)
    
    def get_bottom_left_space(self, space):
        col = chr(space.col-1)
        row = str(space.row+1)
        return Space(col+row)

class JanggiGame:
    
    def __init__(self):
        self._board = Board()