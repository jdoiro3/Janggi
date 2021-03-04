# exceptions

class InvalidCapture(Exception):
    pass

class InvalidMove(Exception):
    pass

class InvalidSpace(Exception):
    pass

class Space:
    
    def __new__(cls, space:str=None):
        if space is None:
            return None
        return super().__new__(cls) 
         
    def __init__(self, space:str):
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
    
    def __init__(self, color:str=None, space:str=None, board:Board=None):
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
        return str(self._space)
    
    @property
    def row(self):
        return self._space.row
    
    @property
    def col(self):
        return self._space.col
    
    @property
    def color(self):
        return self._color

    def get_space(self):
        return self._space
    
    def get_forward_space(self, starting_space:str=None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_space(space)
        return self._board.get_bottom_space(space)
    
    def get_right_space(self, starting_space:str=None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_right_space(space)
        return self._board.get_left_space(space)
    
    def get_left_space(self, starting_space:str=None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_left_space(space)
        return self._board.get_right_space(space)
    
    def get_backward_space(self, starting_space:str=None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_bottom_space(space) 
        return self._board.get_top_space(space)
    
    def get_diagonal_right(self, starting_space:str=None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_right_space(space) 
        return self._board.get_bottom_left_space(space)      
    
    def get_diagonal_left(self, starting_space:str=None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_left_space(space) 
        return self._board.get_bottom_right_space(space)
    
    def change_space(self, new_space:str):
        new_space = self._board.move_piece(self, new_space)
        self._space = new_space
        
    def is_valid_move(self, new_space:str, test_num:int):
        is_blue = self.color == "blue"
        is_red = self.color == "red"
        new_space = Space(new_space)
        # piece has to move forward
        if (is_blue and new_space.row >= self.row) or (is_red and new_space.row <= self.row):
            return False
        if self._board.has_piece(str(new_space)):
            if self._board.get_piece(str(new_space)).color == self.color: # the new space already has a player's piece
                return False
        delta_row = abs(new_space.row - self.row)
        delta_col = abs(new_space.col - self.col)
        return delta_row * delta_col == test_num
        
    def capture(self, space:str):
        self._board.add_captured_piece(self.color, space)
        self._board.assign_space(space, None)
            

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
    
    def is_blocked(self, new_space:str): # this can either be a red or blue piece
        new_space = Space(new_space)
        row_diff = abs(self.row - new_space.row)
        
        if row_diff == 2: # first move is forward
            space_to_check = self.get_forward_space()
        elif (new_space.col - self.col) > 0: # first move is to the right
            space_to_check = self.get_right_space()
        else: # first move is to the left
            space_to_check = self.get_left_space()
            
        if self._board.has_piece(space_to_check):
            return True
        return False
    
    def move(self, new_space:str):
        if self.is_valid_move(new_space, 2):
            if self.is_blocked(new_space):
                raise InvalidMove(f"{self} can't move to {new_space} b/c it's blocked")
            if self._board.has_opponent_piece(new_space, self.color):
                self.capture(new_space)
            self.change_space(new_space)
        else:
            raise InvalidMove(f"{self} can't move to {new_space}")

class Elephant(Piece):
    
    def is_blocked(self, new_space:str):
        row_diff = abs(self.row - new_space.row)
        move_is_right = (new_space.col - self.get_space().col) > 0
        
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
            if new_space.has_opponent_piece(self.color):
                self.capture(new_space)
            self.change_space(new_space)
        else:
            raise InvalidMove(f"{self} can't move to {new_space}")

class Chariot(Piece):
    
    def move(new_space, board):
        if new_space.col != self.get_space().col and new_space.row != self.get_space().row:
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
        self.captured_pieces = {"blue": [], "red": []}
        
    def assign_space(self, space:str, obj:Piece=None):
        if space in self.spaces:
            self.spaces[str(space)] = obj
        else:
            raise InvalidSpace(f"{space} is not a valid space")

    def add_captured_piece(self, capturer_color:str, space:str):
        self.captured_pieces[capturer_color].append(self.spaces[space])
        
    def get_row(self, row:int):
        return [self.spaces[space] for space in self.spaces.keys() if int(space[1:]) == row]

    def get_piece(self, space:str):
        try:
            return self.spaces[space]
        except KeyError:
            raise InvalidSpace(f"{space} is not a valid space")
    
    def has_piece(self, space:str):
        if self.spaces[space] is None:
            return False
        return True

    def has_opponent_piece(self, space:str, color:str):
        if self.has_piece(space) :
            piece = self.spaces[space]
            if piece.color != color:
                return True
        return False

    def place_piece(self, piece:Piece, space:str):
        if space in self.spaces:
            if self.spaces[space] is not None:
                print("can't do that")
            else:
                self.assign_space(space, piece)
        else:
            raise InvalidSpace(f"{space} is not a valid space")
            
    def move_piece(self, piece:Piece, new_space:str):
        if self.spaces[new_space] is not None:
            return piece.space
        self.assign_space(piece.space, None)
        self.assign_space(new_space, piece)
        return Space(new_space)
    
    def get_right_space(self, space:str):
        space = Space(space)
        col = chr(space.col+1)
        row = str(space.row)
        return col+row
    
    def get_left_space(self, space:str):
        space = Space(space)
        col = chr(space.col-1)
        row = str(space.row)
        return col+row
    
    def get_top_space(self, space:str):
        space = Space(space)
        col = chr(space.col)
        row = str(space.row-1)
        return col+row
    
    def get_bottom_space(self, space:str):
        space = Space(space)
        col = chr(space.col)
        row = str(space.row+1)
        return col+row
    
    def get_top_right_space(self, space:str):
        space = Space(space)
        col = chr(space.col+1)
        row = str(space.row-1)
        return col+row
    
    def get_top_left_space(self, space:str):
        space = Space(space)
        col = chr(space.col-1)
        row = str(space.row-1)
        return col+row
    
    def get_bottom_right_space(self, space:str):
        space = Space(space)
        col = chr(space.col+1)
        row = str(space.row+1)
        return col+row
    
    def get_bottom_left_space(self, space:str):
        space = Space(space)
        col = chr(space.col-1)
        row = str(space.row+1)
        return col+row

class JanggiGame:
    
    def __init__(self):
        self._board = Board()

def print_board(board):

    for col in "abcdefghi":
        if col == "a":
            print("      "+col, end="     ")
        else:
            print(col, end="     ")
    print()
    for row in [1,2,3,4,5,6,7,8,9,10]:
        if row == 10:
            print(row, "", board.get_row(row))
        else:
            print(row, " ", board.get_row(row))


b = Board()
rh = Horse("red", "g5", b)
bh = Horse("blue", "e6", b)
print_board(b)

bh.move("g5")

print_board(b)

print(b.captured_pieces)


    