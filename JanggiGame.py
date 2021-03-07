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


class Piece:
    
    def __init__(self, color:str=None, space:str=None, board=None):
        self._color = color
        self._space = Space(space)
        self._board = board
        if space is not None and board is not None:
            board.place_piece(self, space)
            
    def __str__(self):
        return f"{self._color[0]}{self.__class__.__name__[0]}  "
    
    def __repr__(self):
        return f"{self._color[0]}{self.__class__.__name__[0]}  "
    
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

    def get_forward_spaces(self, starting_space:str=None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_spaces(space)
        return self._board.get_bottom_spaces(space)
    
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

    def space_has_player_piece(self, new_space:str):
        if self._board.has_piece(new_space):
            if self._board.get_piece(new_space).color == self.color:
                return True
        return False

    def capture(self, space:str):
        self._board.add_captured_piece(self.color, space)
        self._board.assign_space(space, None)

    def move(self, new_space:str):
        if self.space_has_player_piece(new_space):
            raise InvalidMove(f"{self.color} already has piece on {new_space}")
        if not self.is_movement_valid(new_space):
            raise InvalidMove(f"{self} can't move to {new_space}")
        if self.is_blocked(new_space):
            raise InvalidMove(f"{self} can't move to {new_space} b/c it's blocked.")
        if self._board.has_opponent_piece(new_space, self.color):
            self.capture(new_space)
        self.change_space(new_space)


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

    def get_all_moves(self):
        moves = []
        # get all possible first moves
        forward_space = self.get_forward_space()
        left_space = self.get_left_space()
        right_space = self.get_right_space()
        # first move forward checks
        if not self._board.has_piece(forward_space):
            diagonal_left_space = self.get_diagonal_left(forward_space)
            diagonal_right_space = self.get_diagonal_right(forward_space)
            if not self._board.has_player_piece(diagonal_left_space, self.color):
                moves.append(diagonal_left_space)
            if not self._board.has_player_piece(diagonal_right_space, self.color):
                moves.append(diagonal_right_space)
        # first move to the left checks
        if not self._board.has_piece(left_space):
            diagonal_left_space = self.get_diagonal_left(left_space)
            if not self._board.has_player_piece(diagonal_left_space, self.color):
                moves.append(diagonal_left_space)
        # first move to the right checks
        if not self._board.has_piece(right_space):
            diagonal_right_space = self.get_diagonal_right(right_space)
            if not self._board.has_player_piece(diagonal_right_space, self.color):
                moves.append(diagonal_right_space)
        return moves
        

class Elephant(Piece):

    def get_all_moves(self):
        moves = []
        # get all possible first moves
        forward_space = self.get_forward_space()
        left_space = self.get_left_space()
        right_space = self.get_right_space()
        # first move forward checks
        if not self._board.has_piece(forward_space):
            diagonal_left_space = self.get_diagonal_left(forward_space)
            next_diagonal_left_space = self.get_diagonal_left(diagonal_left_space)
            diagonal_right_space = self.get_diagonal_right(forward_space)
            next_diagonal_right_space = self.get_diagonal_right(diagonal_right_space)
            if self._board.valid_space(next_diagonal_left_space):
                if not self._board.has_piece(diagonal_left_space) and not self._board.has_player_piece(next_diagonal_left_space, self.color):
                    moves.append(next_diagonal_left_space)
            if self._board.valid_space(next_diagonal_right_space):
                if not self._board.has_piece(diagonal_right_space) and not self._board.has_player_piece(next_diagonal_right_space, self.color):
                    moves.append(next_diagonal_right_space)
        # first move to the left checks
        if not self._board.has_piece(left_space):
            diagonal_left_space = self.get_diagonal_left(left_space)
            next_diagonal_left_space = self.get_diagonal_left(diagonal_left_space)
            if self._board.valid_space(next_diagonal_left_space):
                if not self._board.has_piece(diagonal_left_space) and not self._board.has_player_piece(next_diagonal_left_space, self.color):
                    moves.append(next_diagonal_left_space)
        # first move to the right checks
        if not self._board.has_piece(right_space):
            diagonal_right_space = self.get_diagonal_right(right_space)
            next_diagonal_right_space = self.get_diagonal_right(diagonal_right_space)
            if self._board.valid_space(next_diagonal_right_space):
                if not self._board.has_piece(diagonal_right_space) and not self._board.has_player_piece(next_diagonal_right_space, self.color):
                    moves.append(next_diagonal_right_space)
        return moves


class Chariot(Piece):

    def can_move_to_space(self, space):
        if self._board.has_piece(space):
            if self._board.get_piece(space).color != self.color:
                return True
            else:
                return False
        return True
    
    def get_all_moves(self):
        forward_spaces = [space for space in self.get_forward_spaces() if self.can_move_to_space(space)]
        print(forward_spaces)

        
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

    def valid_space(self, space):
        if space in self.spaces:
            return True
        return False

    def get_column_spaces(self, column:int):
        return [space for space in self.spaces if Space(space).col == column]

    def get_column(self, column:int):
        return [self.spaces[space] for space in self.get_column_spaces(column)]

    def get_row_spaces(self, row:int):
        return [space for space in self.spaces if Space(space).row == row]

    def get_row(self, row:int):
        return [self.spaces[space] for space in self.get_row_spaces(row)]
        
    def assign_space(self, space:str, obj:Piece=None):
        if space in self.spaces:
            self.spaces[str(space)] = obj
        else:
            raise InvalidSpace(f"{space} is not a valid space")

    def add_captured_piece(self, capturer_color:str, space:str):
        self.captured_pieces[capturer_color].append(self.spaces[space])

    def get_piece(self, space:str):
        try:
            return self.spaces[space]
        except KeyError:
            raise InvalidSpace(f"{space} is not a valid space")
    
    def has_piece(self, space:str):
        if self.spaces[space] is None:
            return False
        return True

    def has_player_piece(self, space, color):
        if self.has_piece(space):
            piece = self.spaces[space]
            if piece.color == color:
                return True
        return False

    def has_opponent_piece(self, space:str, color:str):
        if self.has_piece(space):
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

    def get_top_spaces(self, space:str):
        space = Space(space)
        column_spaces = self.get_column_spaces(space.col)
        return [space for space in column_spaces if Space(space).row < space.row]

    def get_bottom_spaces(self, space:str):
        space = Space(space)
        column_spaces = self.get_column_spaces(space.col)
        return [s for s in column_spaces if Space(s).row > space.row]
    
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

    def make_move(self, current_space:str, new_space:str):
        piece = self._board.get_piece(current_space)
        if piece is None or piece.color != self._turn or self.game_over:
            return False
        moves = piece.get_all_moves()
        if new_space not in moves:
            return False
        piece.move(new_space)

        # update game state
        if self._turn == "blue" and self.is_in_check("red"):
            self.game_state = "BLUE_WON"
            self.game_over = True
        elif self.is_in_check("blue"):
            self.game_state = "RED_WON"
            self.game_over = True
    
    def is_in_check(self, color:str):
        general = self._board.get_general(color)
        moves = general.get_all_moves()
        if not moves:
            return True
        return False

    def get_game_state(self):
        return self._game_state
        


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
re = Elephant("red", "g6", b)
be = Elephant("blue", "g7", b)
bh = Horse("red", "d8", b)
rc = Chariot("red", "d4", b)
"""
bh = Horse("blue", "e6", b)
re = Elephant("red", "c2", b)
be = Elephant("blue", "d7", b)
print_board(b)
bh.move("g5")
print_board(b)
re.move("e5")
print_board(b)
re.move("c8")
print_board(b)
print(b.captured_pieces)
"""

print(rh.get_all_moves())
print(re.get_all_moves())
print("sdfsd", rc.get_all_moves())
print_board(b)


    