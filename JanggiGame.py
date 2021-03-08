

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
        if self._board.has_opponent_piece(new_space, self.color):
            self.capture(new_space)
        self.change_space(new_space)


class General(Piece):

    def get_available_adjacent_spaces(self, starting_space:str=None):
        curr_space = starting_space or self.space
        spaces = [
            self._board.get_top_space(curr_space),
            self._board.get_bottom_space(curr_space),
            self._board.get_bottom_left_space(curr_space),
            self._board.get_bottom_right_space(curr_space),
            self._board.get_top_left_space(curr_space),
            self._board.get_top_right_space(curr_space)
        ]
        return [
            space for space in spaces
            if self._board.has_opponent_piece(space, self.color) or not self._board.has_piece(space)
        ]
    
    def get_palace_moves(self):
        adjacent_spaces = set(self.get_available_adjacent_spaces())
        palace_spaces = set(self._board.get_palace_spaces(self.color))
        return list(palace_spaces & adjacent_spaces)

    def threatened(self):
        opponent_attacking_spaces = self._board.get_opponents_attacking_spaces(self.color)
        if self.space in opponent_attacking_spaces:
            return True
        return False

    def get_legal_moves(self):
        opponent_attacking_spaces = self._board.get_opponents_attacking_spaces(self.color)
        return list(set(self.get_palace_moves()) - set(opponent_attacking_spaces))


class Guard(Piece):

    def move(new_space):
        pass

class Horse(Piece):

    def get_attacking_spaces(self):
        spaces = []
        forward_space = self.get_forward_space()
        left_space = self.get_left_space()
        right_space = self.get_right_space()
        # possible spaces the piece will pass through if the first move is forward
        if not self._board.has_piece(forward_space) and self._board.valid_space(forward_space):
            forward_diag_right_space = self.get_diagonal_right(forward_space)
            if self._board.valid_space(forward_diag_right_space):
                spaces.append(forward_diag_right_space)
            forward_diag_left_space = self.get_diagonal_left(forward_space)
            if self._board.valid_space(forward_diag_left_space):
                spaces.append(forward_diag_left_space)
        # possible spaces the piece will pass through if the first move is to the left
        if not self._board.has_piece(left_space) and self._board.valid_space(left_space):
            left_diag_left_space = self.get_diagonal_left(left_space)
            if self._board.valid_space(left_diag_left_space):
                spaces.append(left_diag_left_space)
        # possible spaces the piece will pass through if the first move is to the right
        if not self._board.has_piece(right_space) and self._board.valid_space(right_space):
            right_diag_right_space = self.get_diagonal_right(right_space)
            if self._board.valid_space(right_diag_right_space):
                spaces.append(right_diag_right_space)
        return spaces

    def get_legal_moves(self):
        moves = []
        # get all possible first moves
        forward_space = self.get_forward_space()
        left_space = self.get_left_space()
        right_space = self.get_right_space()
        # first move forward checks
        if not self._board.has_piece(forward_space) and self._board.valid_space(forward_space):
            diagonal_left_space = self.get_diagonal_left(forward_space)
            diagonal_right_space = self.get_diagonal_right(forward_space)
            if not self._board.has_player_piece(diagonal_left_space, self.color) and self._board.valid_space(diagonal_left_space):
                moves.append(diagonal_left_space)
            if not self._board.has_player_piece(diagonal_right_space, self.color) and self._board.valid_space(diagonal_right_space):
                moves.append(diagonal_right_space)
        # first move to the left checks
        if not self._board.has_piece(left_space) and self._board.valid_space(left_space):
            diagonal_left_space = self.get_diagonal_left(left_space)
            if not self._board.has_player_piece(diagonal_left_space, self.color) and self._board.valid_space(diagonal_left_space):
                moves.append(diagonal_left_space)
        # first move to the right checks
        if not self._board.has_piece(right_space) and self._board.valid_space(right_space):
            diagonal_right_space = self.get_diagonal_right(right_space)
            if not self._board.has_player_piece(diagonal_right_space, self.color) and self._board.valid_space(diagonal_right_space):
                moves.append(diagonal_right_space)
        return moves
        

class Elephant(Piece):

    def get_attacking_spaces(self):
        spaces = []
        forward_space = self.get_forward_space()
        left_space = self.get_left_space()
        right_space = self.get_right_space()
        # possible spaces the piece will pass through if the first move is forward
        if not self._board.has_piece(forward_space) and self._board.valid_space(forward_space):
            forward_diag_right_space = self.get_diagonal_right(forward_space)
            if not self._board.has_piece(forward_diag_right_space) and self._board.valid_space(forward_diag_right_space):
                forward_diag_right_space = self.get_diagonal_right(forward_diag_right_space)
                if self._board.valid_space(forward_diag_right_space):
                    spaces.append(forward_diag_right_space)
            forward_diag_left_space = self.get_diagonal_left(forward_space)
            if not self._board.has_piece(forward_diag_left_space) and self._board.valid_space(forward_diag_left_space):
                forward_diag_left_space = self.get_diagonal_left(forward_diag_left_space)
                if self._board.valid_space(forward_diag_left_space):
                    spaces.append(forward_diag_left_space)
        # possible spaces the piece will pass through if the first move is to the left
        if not self._board.has_piece(left_space) and self._board.valid_space(left_space):
            left_diag_left_space = self.get_diagonal_left(left_space)
            if not self._board.has_piece(left_diag_left_space) and self._board.valid_space(left_diag_left_space):
                left_diag_left_space = self.get_diagonal_left(left_diag_left_space)
                if self._board.valid_space(left_diag_left_space):
                    spaces.append(left_diag_left_space)
        # possible spaces the piece will pass through if the first move is to the right
        if not self._board.has_piece(right_space) and self._board.valid_space(right_space):
            right_diag_right_space = self.get_diagonal_right(right_space)
            if not self._board.has_piece(right_diag_right_space) and self._board.valid_space(right_diag_right_space):
                right_diag_right_space = self.get_diagonal_left(right_diag_right_space)
                if self._board.valid_space(right_diag_right_space):
                    spaces.append(right_diag_right_space)
        return spaces


    def get_legal_moves(self):
        spaces = []
        forward_space = self.get_forward_space()
        left_space = self.get_left_space()
        right_space = self.get_right_space()
        # possible spaces the piece will pass through if the first move is forward
        if not self._board.has_piece(forward_space) and self._board.valid_space(forward_space):
            forward_diag_right_space = self.get_diagonal_right(forward_space)
            if not self._board.has_piece(forward_diag_right_space) and self._board.valid_space(forward_diag_right_space):
                forward_diag_right_space = self.get_diagonal_right(forward_diag_right_space)
                if self._board.valid_space(forward_diag_right_space) and not self._board.has_player_piece(forward_diag_right_space, self.color):
                    spaces.append(forward_diag_right_space)
            forward_diag_left_space = self.get_diagonal_left(forward_space)
            if not self._board.has_piece(forward_diag_left_space) and self._board.valid_space(forward_diag_left_space):
                forward_diag_left_space = self.get_diagonal_left(forward_diag_left_space)
                if self._board.valid_space(forward_diag_left_space) and not self._board.has_player_piece(forward_diag_left_space, self.color):
                    spaces.append(forward_diag_left_space)
        # possible spaces the piece will pass through if the first move is to the left
        if not self._board.has_piece(left_space) and self._board.valid_space(left_space):
            left_diag_left_space = self.get_diagonal_left(left_space)
            if not self._board.has_piece(left_diag_left_space) and self._board.valid_space(left_diag_left_space):
                left_diag_left_space = self.get_diagonal_left(left_diag_left_space)
                if self._board.valid_space(left_diag_left_space) and not self._board.has_player_piece(left_diag_left_space, self.color):
                    spaces.append(left_diag_left_space)
        # possible spaces the piece will pass through if the first move is to the right
        if not self._board.has_piece(right_space) and self._board.valid_space(right_space):
            right_diag_right_space = self.get_diagonal_right(right_space)
            if not self._board.has_piece(right_diag_right_space) and self._board.valid_space(right_diag_right_space):
                right_diag_right_space = self.get_diagonal_left(right_diag_right_space)
                if self._board.valid_space(right_diag_right_space) and not self._board.has_player_piece(right_diag_right_space, self.color):
                    spaces.append(right_diag_right_space)
        return spaces


class Chariot(Piece):

    def can_move_to_space(self, space):
        if self._board.has_piece(space):
            if self._board.get_piece(space).color != self.color:
                return True
            else:
                return False
        return self._board.valid_space(space)

    def get_legal_left_spaces(self):
        spaces = []
        space = self.get_left_space()
        while self._board.valid_space(space) and not self._board.has_piece(space):
            spaces.append(space)
            space = self.get_left_space(space)
        if self._board.has_opponent_piece(space, self.color):
            spaces.append(space)
        return spaces

    def get_legal_right_spaces(self):
        spaces = []
        space = self.get_right_space()
        while self._board.valid_space(space) and not self._board.has_piece(space):
            spaces.append(space)
            space = self.get_right_space(space)
        if self._board.has_opponent_piece(space, self.color):
            spaces.append(space)
        return spaces

    def get_legal_backward_spaces(self):
        spaces = []
        space = self.get_backward_space()
        while self._board.valid_space(space) and not self._board.has_piece(space):
            spaces.append(space)
            space = self.get_backward_space(space)
        if self._board.has_opponent_piece(space, self.color):
            spaces.append(space)
        return spaces

    def get_legal_forward_spaces(self):
        spaces = []
        space = self.get_forward_space()
        while self._board.valid_space(space) and not self._board.has_piece(space):
            spaces.append(space)
            space = self.get_forward_space(space)
        if self._board.has_opponent_piece(space, self.color):
            spaces.append(space)
        return spaces

    def get_possible_attack_forward(self):
        spaces = []
        space = self.get_forward_space()
        while self._board.valid_space(space) and not self._board.has_piece(space):
            spaces.append(space)
            space = self.get_forward_space(space)
        spaces.append(space)
        return spaces

    def get_possible_attack_backward(self):
        spaces = []
        space = self.get_backward_space()
        while self._board.valid_space(space) and not self._board.has_piece(space):
            spaces.append(space)
            space = self.get_backward_space(space)
        spaces.append(space)
        return spaces

    def get_possible_attacks_left(self):
        spaces = []
        space = self.get_left_space()
        while self._board.valid_space(space) and not self._board.has_piece(space):
            spaces.append(space)
            space = self.get_left_space(space)
        spaces.append(space)
        return spaces

    def get_possible_attacks_right(self):
        spaces = []
        space = self.get_right_space()
        while self._board.valid_space(space) and not self._board.has_piece(space):
            spaces.append(space)
            space = self.get_right_space(space)
        spaces.append(space)
        return spaces

    def get_attacking_spaces(self):
        forward = self.get_possible_attack_forward()
        backward = self.get_possible_attack_backward()
        left = self.get_possible_attacks_left()
        right = self.get_possible_attacks_right()
        return forward+backward+left+right
    
    def get_legal_moves(self):
        forward = self.get_legal_forward_spaces()
        backward = self.get_legal_backward_spaces()
        left = self.get_legal_left_spaces()
        right = self.get_legal_right_spaces()
        return forward+backward+left+right

        
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
        self.blue_palace_spaces = ["d8", "d9", "d10", "e8", "e9", "e10", "f8", "f9", "f10"]
        self.red_palace_spaces = ["d1", "d2", "d3", "e1", "e2", "e3", "f1", "f2", "f3"]
        self.captured_pieces = {"blue": [], "red": []}
        

    def get_palace_spaces(self, color:str):
        if color == "red":
            return self.red_palace_spaces
        elif color == "blue":
            return self.blue_palace_spaces
        else:
            return []

    def get_general(self, color):
        pieces = [self.spaces[space] for space in self.spaces if self.spaces[space] is not None]
        for piece in pieces:
            if piece.color == color and type(piece) == General:
                return piece

    def get_opponent_general(self, color):
        if color == "blue":
            return self.get_general("red")
        return self.get_general("blue")

    def valid_space(self, space):
        if space in self.spaces:
            return True
        return False

    def return_none_or_space(self, space):
        if self.valid_space(space):
            return space
        return None

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
        if not self.valid_space(space):
            return False
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

    def get_pieces(self, color=None):
        if color is None:
            return [self.get_piece(space) for space in self.spaces if self.get_piece(space) is not None]
        else:
            pieces = [self.get_piece(space) for space in self.spaces if self.get_piece(space) is not None]
            return [piece for piece in pieces if piece.color == color]

    def get_opponents_attacking_spaces(self, color):
        if color == "blue":
            pieces = self.get_pieces("red")
        else:
            pieces = self.get_pieces("blue")
        all_spaces = set()
        for piece in pieces:
            spaces = piece.get_attacking_spaces()
            for space in spaces:
                all_spaces.add(space)
        print(all_spaces)
        return all_spaces
            
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
        right_space = col+row
        return self.return_none_or_space(right_space)
    
    def get_left_space(self, space:str):
        space = Space(space)
        col = chr(space.col-1)
        row = str(space.row)
        left_space = col+row
        return self.return_none_or_space(left_space)
    
    def get_top_space(self, space:str):
        space = Space(space)
        col = chr(space.col)
        row = str(space.row-1)
        top_space = col+row
        return self.return_none_or_space(top_space)

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
        bottom_space = col+row
        return self.return_none_or_space(bottom_space)
    
    def get_top_right_space(self, space:str):
        space = Space(space)
        col = chr(space.col+1)
        row = str(space.row-1)
        top_right_space = col+row
        return self.return_none_or_space(top_right_space)
    
    def get_top_left_space(self, space:str):
        space = Space(space)
        col = chr(space.col-1)
        row = str(space.row-1)
        top_left_space = col+row
        return self.return_none_or_space(top_left_space)
    
    def get_bottom_right_space(self, space:str):
        space = Space(space)
        col = chr(space.col+1)
        row = str(space.row+1)
        bottom_right_space = col+row
        return self.return_none_or_space(bottom_right_space)
    
    def get_bottom_left_space(self, space:str):
        space = Space(space)
        col = chr(space.col-1)
        row = str(space.row+1)
        bottom_left_space = col+row
        return self.return_none_or_space(bottom_left_space)

class JanggiGame:
    
    def __init__(self):
        self._board = Board()
        self._turn = "blue"
        self._game_state = "UNFINISHED"

    def change_turn(self):
        if self._turn == "blue":
            self._turn = "red"
        else:
            self._turn = "blue"

    def make_move(self, current_space:str, new_space:str):
        if self._game_state != "UNFINISHED":
            return False
        if self.is_in_check(self._turn) and self._board.get_general(self._turn).space != current_space:
            return False
        if current_space == new_space:
            self.change_turn()
            return True
        piece = self._board.get_piece(current_space)
        if piece is None or piece.color != self._turn:
            return False
        legal_spaces = piece.get_legal_moves()
        if new_space not in legal_spaces:
            return False
        piece.move(new_space)
        # update game state
        if self._turn == "blue" and self._board.get_opponent_general("blue").get_legal_moves() == []:
            self.game_state = "BLUE_WON"
            self.game_over = True
        elif self._turn == "red" and self._board.get_opponent_general("red").get_legal_moves() == []:
            self.game_state = "RED_WON"
            self.game_over = True
        return True
    
    def is_in_check(self, color:str):
        general = self._board.get_general(color)
        return general.threatened()

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
rh = Horse("red", "h5", b)
bc = Chariot("blue", "f7", b)
be = Elephant("blue", "g6", b)
be = Elephant("blue", "d3", b)
bh = Horse("blue", "d8", b)
bh = Horse("blue", "c5", b)
bc = Chariot("blue", "h2", b)
bc = Chariot("blue", "h1", b)
rg = General("red", "e2", b)
print(type(rg) == General)
print(b.get_opponents_attacking_spaces("red"))

print(rg.get_legal_moves())
print_board(b)
bc.move("d4")
print_board(b)
print(b.captured_pieces)
bc.move("d8")
print_board(b)
print(b.captured_pieces)



    