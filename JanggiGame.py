

# exceptions

class SpaceError(Exception):
    pass

class SpaceSequence:

    def __init__(self, spaces: list):
        self.spaces = spaces

    def get_next(self, space=None):
        if space is None:
            return self.spaces[0]
        spaces = self.spaces
        try:
            return spaces[spaces.index(space)+1]
        except ValueError:
            return "00"
        except IndexError:
            return "00"

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

    def __init__(self, color: str = None, space: str = None, board: 'Board' = None):
        self._color = color
        self._space = Space(space)
        self._board = board
        if space is not None and board is not None:
            board.place_piece(self, space)

    def __str__(self):
        return f"{self._color[0]}{self.__class__.__name__[0]}"

    def __repr__(self):
        return f"{self._color[0]}{self.__class__.__name__[0]}"

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

    def get_forward_space(self, starting_space: str = None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_space(space)
        return self._board.get_bottom_space(space)

    def get_forward_spaces(self, starting_space: str = None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_spaces(space)
        return self._board.get_bottom_spaces(space)

    def get_right_space(self, starting_space: str = None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_right_space(space)
        return self._board.get_left_space(space)

    def get_left_space(self, starting_space: str = None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_left_space(space)
        return self._board.get_right_space(space)

    def get_backward_space(self, starting_space: str = None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_bottom_space(space)
        return self._board.get_top_space(space)

    def get_diagonal_right(self, starting_space: str = None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_right_space(space)
        return self._board.get_bottom_left_space(space)

    def get_diagonal_left(self, starting_space: str = None):
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_left_space(space)
        return self._board.get_bottom_right_space(space)

    def in_fortress(self):
        if self.space in self._board.fortress_spaces:
            return True
        return False

    def change_space(self, new_space: str):
        self._board.move_piece(self, new_space)
        self._space = new_space

    def capture(self, space: str):
        self._board.add_captured_piece(self.color, space)
        self._board.assign_space(space, None)

    def move(self, new_space: str):
        if self._board.has_opponent_piece(new_space, self.color):
            self.capture(new_space)
        self.change_space(new_space)


class Board:

    def __init__(self, empty=False):
        self.spaces = {col + str(row): None for col in "abcdefghi" for row in range(1, 11)}
        self.blue_fortress_spaces = ["d8", "d9", "d10", "e8", "e9", "e10", "f8", "f9", "f10"]
        self.red_fortress_spaces = ["d1", "d2", "d3", "e1", "e2", "e3", "f1", "f2", "f3"]
        if not empty:
            self.pieces = {
                "blue": {
                    "general": General("blue", "e9", self), 
                    "other-pieces": [
                        Chariot("blue", "a10", self), Chariot("blue", "i10", self), Elephant("blue", "b10", self), Elephant("blue", "g10", self),
                        Horse("blue", "c10", self), Horse("blue", "h10", self), Cannon("blue", "b8", self), Cannon("blue", "h8", self),
                        Guard("blue", "d10", self), Guard("blue", "f10", self), Soldier("blue", "a7", self), Soldier("blue", "c7", self), 
                        Soldier("blue", "e7", self), Soldier("blue", "g7", self), Soldier("blue", "i7", self)
                        ]
                },
                "red": {
                    "general": General("red", "e2", self), 
                    "other-pieces":[
                        Chariot("red", "a1", self), Chariot("red", "i1", self), Elephant("red", "b1", self), Elephant("red", "g1", self),
                        Horse("red", "c1", self), Horse("red", "h1", self), Cannon("red", "b3", self), Cannon("red", "h3", self),
                        Guard("red", "d1", self), Guard("red", "f1", self), Soldier("red", "a4", self), Soldier("red", "c4", self), 
                        Soldier("red", "e4", self), Soldier("red", "g4", self), Soldier("red", "i4", self)
                        ]
                }
            }
        self.captured_pieces = {"blue": [], "red": []}

    @property
    def fortress_spaces(self):
        return self.red_fortress_spaces+self.blue_fortress_spaces

    def valid_space(self, space):
        if space in self.spaces:
            return True
        return False

    def place_piece(self, piece: Piece, space: str):
        if not self.valid_space(space):
            raise SpaceError(f"{space} is not a valid space")
        if self.spaces[space] is not None:
            raise SpaceError(f"{space} already has a piece")
        self.spaces[space] = piece
    
    def assign_space(self, space: str, obj: Piece = None):
        if self.valid_space(space):
            self.spaces[space] = obj
        else:
            raise SpaceError(f"{space} is not a valid space")

    def get_fortress_spaces(self, color: str):
        if color == "red":
            return self.red_fortress_spaces
        elif color == "blue":
            return self.blue_fortress_spaces
        else:
            return []

    def get_general(self, color):
        return self.pieces[color]["general"]

    def get_opponent_general(self, color):
        if color == "blue":
            return self.get_general("red")
        elif color == "red":
            return self.get_general("blue")

    def get_row_spaces(self, row: int):
        return [space for space in self.spaces if Space(space).row == row]

    def get_row(self, row: int):
        return [self.spaces[space] for space in self.get_row_spaces(row)]

    def add_captured_piece(self, capturer_color: str, space: str):
        piece = self.spaces[space]
        self.captured_pieces[capturer_color].append(piece)
        self.pieces[piece.color]["other-pieces"].remove(piece)

    def get_piece(self, space: str):
        if not self.valid_space(space):
            raise SpaceError(f"{space} is not a valid space")
        return self.spaces[space]

    def has_piece(self, space: str):
        if not self.valid_space(space):
            return False
        if self.spaces[space] is None:
            return False
        return True

    def space_open(self, space: str):
        if not self.valid_space(space):
            return False
        return not self.has_piece(space)
        
    def has_player_piece(self, space, color):
        if self.has_piece(space):
            piece = self.spaces[space]
            if piece.color == color:
                return True
        return False

    def has_opponent_piece(self, space: str, color: str):
        if self.has_piece(space):
            piece = self.spaces[space]
            if piece.color != color:
                return True
        return False

    def get_pieces(self, color):
        return self.pieces[color]["other-pieces"]

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
        return all_spaces

    def move_piece(self, piece: Piece, new_space: str):
        self.assign_space(piece.space, None)
        self.assign_space(new_space, piece)

    def get_right_space(self, space: str):
        space = Space(space)
        col = chr(space.col + 1)
        row = str(space.row)
        right_space = col + row
        return right_space

    def get_left_space(self, space: str):
        space = Space(space)
        col = chr(space.col - 1)
        row = str(space.row)
        left_space = col + row
        return left_space

    def get_top_space(self, space: str):
        space = Space(space)
        col = chr(space.col)
        row = str(space.row - 1)
        top_space = col + row
        return top_space

    def get_top_spaces(self, space: str):
        space = Space(space)
        column_spaces = self.get_column_spaces(space.col)
        return [space for space in column_spaces if Space(space).row < space.row]

    def get_bottom_spaces(self, space: str):
        space = Space(space)
        column_spaces = self.get_column_spaces(space.col)
        return [s for s in column_spaces if Space(s).row > space.row]

    def get_bottom_space(self, space: str):
        space = Space(space)
        col = chr(space.col)
        row = str(space.row + 1)
        bottom_space = col + row
        return bottom_space

    def get_top_right_space(self, space: str):
        space = Space(space)
        col = chr(space.col + 1)
        row = str(space.row - 1)
        top_right_space = col + row
        return top_right_space

    def get_top_left_space(self, space: str):
        space = Space(space)
        col = chr(space.col - 1)
        row = str(space.row - 1)
        top_left_space = col + row
        return top_left_space

    def get_bottom_right_space(self, space: str):
        space = Space(space)
        col = chr(space.col + 1)
        row = str(space.row + 1)
        bottom_right_space = col + row
        return bottom_right_space

    def get_bottom_left_space(self, space: str):
        space = Space(space)
        col = chr(space.col - 1)
        row = str(space.row + 1)
        bottom_left_space = col + row
        return bottom_left_space


class FortressPiece(Piece):

    def get_available_adjacent_spaces(self, starting_space:str=None):
        curr_space = starting_space or self.space
        board = self._board
        adjacent_spaces = [
            board.get_top_space(curr_space),
            board.get_bottom_space(curr_space),
            board.get_left_space(curr_space),
            board.get_right_space(curr_space),
            board.get_bottom_left_space(curr_space),
            board.get_bottom_right_space(curr_space),
            board.get_top_left_space(curr_space),
            board.get_top_right_space(curr_space)
        ]
        return [
            space for space in adjacent_spaces
            if (board.has_opponent_piece(space, self.color) or board.space_open(space)) and board.valid_space(space)
        ]

    def get_fortress_moves(self):
        adjacent_spaces = set(self.get_available_adjacent_spaces())
        fortress_spaces = set(self._board.get_fortress_spaces(self.color))
        return list(fortress_spaces & adjacent_spaces)


class General(FortressPiece):

    def in_check(self):
        opponent_attacking_spaces = self._board.get_opponents_attacking_spaces(self.color)
        print(self.space, opponent_attacking_spaces)
        if self.space in opponent_attacking_spaces:
            return True
        return False

    def in_checkmate(self):
        legal_moves = self.get_legal_moves()
        if legal_moves:
            return False
        return True

    def get_legal_moves(self):
        opponent_attacking_spaces = self._board.get_opponents_attacking_spaces(self.color)
        return list(set(self.get_fortress_moves()) - set(opponent_attacking_spaces))


class Guard(FortressPiece):

    def get_legal_moves(self):
        return self.get_fortress_moves()

    def get_attacking_spaces(self):
        return self.get_fortress_moves()

class Horse(Piece):

    def get_move_sequences(self):
        forward_space = self.get_forward_space()
        left_space = self.get_left_space()
        right_space = self.get_right_space()
        move_sequences = [
            (forward_space, self.get_diagonal_right(forward_space)),
            (forward_space, self.get_diagonal_left(forward_space)),
            (left_space, self.get_diagonal_left(left_space)),
            (right_space, self.get_diagonal_right(right_space))
        ]
        return move_sequences

    def get_attacking_spaces(self):
        attacking_spaces = []
        move_sequences = self.get_move_sequences()
        board = self._board
        for spaces in move_sequences:
            if board.valid_space(spaces[0]) and board.valid_space(spaces[1]):
                if board.space_open(spaces[0]):
                    attacking_spaces.append(spaces[1])
        return attacking_spaces

    def get_legal_moves(self):
        legal_moves = []
        move_sequences = self.get_move_sequences()
        board = self._board
        for spaces in move_sequences:
            if board.valid_space(spaces[0]) and board.valid_space(spaces[1]):
                if board.space_open(spaces[0]) and not board.has_player_piece(spaces[1], self.color):
                    legal_moves.append(spaces[1])
        return legal_moves
        

class Elephant(Piece):

    def get_move_sequences(self):
        forward_space = self.get_forward_space()
        forward_diag_right_space = self.get_diagonal_right(forward_space)
        forward_diag_left_space = self.get_diagonal_left(forward_space)
        left_space = self.get_left_space()
        left_diag_left_space = self.get_diagonal_left(left_space)
        right_space = self.get_right_space()
        right_diag_right_space = self.get_diagonal_right(right_space)
        move_sequences = [
            (forward_space, forward_diag_right_space, self.get_diagonal_right(forward_diag_right_space)),
            (forward_space, forward_diag_left_space , self.get_diagonal_left(forward_diag_left_space)),
            (right_space, right_diag_right_space, self.get_diagonal_right(right_diag_right_space)),
            (left_space, left_diag_left_space, self.get_diagonal_left(left_diag_left_space))
        ]
        return move_sequences

    def get_attacking_spaces(self):
        attacking_spaces = []
        move_sequences = self.get_move_sequences()
        board = self._board
        for spaces in move_sequences:
            if board.valid_space(spaces[0]) and board.valid_space(spaces[1]) and board.valid_space(spaces[2]):
                if board.space_open(spaces[0]) and board.space_open(spaces[1]):
                    attacking_spaces.append(spaces[2])
        return attacking_spaces


    def get_legal_moves(self):
        legal_moves = []
        move_sequences = self.get_move_sequences()
        board = self._board
        for spaces in move_sequences:
            if board.valid_space(spaces[0]) and board.valid_space(spaces[1]) and board.valid_space(spaces[2]):
                if board.space_open(spaces[0]) and board.space_open(spaces[1]) and not board.has_player_piece(spaces[2], self.color):
                    legal_moves.append(spaces[2])
        return legal_moves


class Chariot(Piece):

    def __init__(self, color: str = None, space: str = None, board: 'Board' = None):
        super().__init__(color, space, board)
        self._diagonal_moves = {"d3": ["e2", "f1"], "d1": ["e2","f3"], "f1": ["e2","d3"], "f3": ["e2","d1"], "e2": ["d1","f1","d3","f3"],
        "d8":["e9", "f10"], "d10":["e9", "f8"], "f8":["e9","d10"], "f10":["e9","d8"], "e9":["d8","f8","d10","f10"]}

    def get_moves_in_direction(self, next_space_method, move_type: str = "legal"):
        
        get_next_space = next_space_method
        spaces = []
        board = self._board
        space = get_next_space()
        while board.valid_space(space) and board.space_open(space):
            spaces.append(space)
            space = get_next_space(space)
        if board.has_opponent_piece(space, self.color) and move_type == "legal" and board.valid_space(space):
            spaces.append(space)
        elif move_type == "attacking" and board.valid_space(space):
            spaces.append(space)
        else:
            pass
        return spaces
    
    def get_legal_moves(self):
        legal_forward_spaces = self.get_moves_in_direction(self.get_forward_space)
        legal_left_spaces = self.get_moves_in_direction(self.get_left_space)
        legal_right_spaces = self.get_moves_in_direction(self.get_right_space)
        legal_backward_spaces = self.get_moves_in_direction(self.get_backward_space)
        spaces = legal_forward_spaces+legal_left_spaces+legal_right_spaces+legal_backward_spaces
        if self.in_fortress():
            board = self._board
            diag_spaces = self._diagonal_moves[self.space]
            if self.space in ["e2", "e9"]:
                for space in diag_spaces:
                    if board.has_opponent_piece(space, self.color) or board.space_open(space):
                        spaces.append(space)
            else:
                seq = SpaceSequence(diag_spaces)
                diag_legal_moves = self.get_moves_in_direction(seq.get_next)
                spaces += diag_legal_moves
        return spaces

    def get_attacking_spaces(self):
        attacking_forward_spaces = self.get_moves_in_direction(self.get_forward_space, "attacking")
        attacking_left_spaces = self.get_moves_in_direction(self.get_left_space, "attacking")
        attacking_right_spaces = self.get_moves_in_direction(self.get_right_space, "attacking")
        attacking_backward_spaces = self.get_moves_in_direction(self.get_backward_space, "attacking")
        spaces = attacking_forward_spaces+attacking_left_spaces+attacking_right_spaces+attacking_backward_spaces
        if self.in_fortress():
            diag_spaces = self._diagonal_moves[self.space]
            if self.space in ["e2", "e9"]:
                for space in diag_spaces:
                    spaces.append(space)
            else:
                seq = SpaceSequence(diag_spaces)
                diag_legal_moves = self.get_moves_in_direction(seq.get_next, "attacking")
                spaces += diag_legal_moves
        return spaces

        
class Cannon(Piece):

    def get_moves_in_direction(self, next_space_method, move_type: str = "legal"):
        
        get_next_space = next_space_method
        spaces = []
        board = self._board
        space = get_next_space()
        while board.space_open(space) and board.valid_space(space):
            space = get_next_space(space)
        if board.has_piece(space) and board.valid_space(space):
            space = get_next_space(space)
        while board.valid_space(space) and board.space_open(space):
            spaces.append(space)
            space = get_next_space(space)
        if move_type == "legal" and board.has_opponent_piece(space, self.color) and board.valid_space(space):
            spaces.append(space)
        if move_type == "attacking" and board.valid_space(space):
            spaces.append(space)
        return spaces
    
    def get_legal_moves(self):
        legal_forward_spaces = self.get_moves_in_direction(self.get_forward_space)
        legal_left_spaces = self.get_moves_in_direction(self.get_left_space)
        legal_right_spaces = self.get_moves_in_direction(self.get_right_space)
        legal_backward_spaces = self.get_moves_in_direction(self.get_backward_space) 
        return legal_forward_spaces+legal_left_spaces+legal_right_spaces+legal_backward_spaces

    def get_attacking_spaces(self):
        legal_forward_spaces = self.get_moves_in_direction(self.get_forward_space, "attacking")
        legal_left_spaces = self.get_moves_in_direction(self.get_left_space, "attacking")
        legal_right_spaces = self.get_moves_in_direction(self.get_right_space, "attacking")
        legal_backward_spaces = self.get_moves_in_direction(self.get_backward_space, "attacking") 
        return legal_forward_spaces+legal_left_spaces+legal_right_spaces+legal_backward_spaces

class Soldier(Piece):
    
    def get_legal_moves(self):
        legal_spaces = []
        board = self._board
        for space in [self.get_forward_space(), self.get_left_space(), self.get_right_space()]:
            if (board.has_opponent_piece(space, self.color) or board.space_open(space)) and board.valid_space(space):
                legal_spaces.append(space)
        return legal_spaces
    
    def get_attacking_spaces(self):
        attacking_spaces = []
        board = self._board
        for space in [self.get_forward_space(), self.get_left_space(), self.get_right_space()]:
            if board.valid_space(space):
                attacking_spaces.append(space)
        return attacking_spaces

class JanggiGame:
    
    def __init__(self):
        board = Board()
        self._board = board
        self._turn = "blue"
        self._game_state = "UNFINISHED"

    def view(self):
        print_board(self._board)

    def change_turn(self):
        if self._turn == "blue":
            self._turn = "red"
        else:
            self._turn = "blue"

    def make_move(self, current_space:str, new_space:str):
        if self._game_state != "UNFINISHED":
            #print("game over")
            return False
        if self.is_in_check(self._turn) and self._board.get_general(self._turn).space != current_space:
            #print("need to move general. in check")
            return False
        if current_space == new_space:
            self.change_turn()
            return True
        piece = self._board.get_piece(current_space)
        if piece is None or piece.color != self._turn:
            #print("not your turn")
            return False
        legal_spaces = piece.get_legal_moves()
        if new_space not in legal_spaces:
            #print("not a legal move")
            return False
        piece.move(new_space)
        # make sure move doesn't put player's general in check
        if self.is_in_check(self._turn):
            piece.move(current_space) # move the piece back
            #print("can't move into check")
            return False
        # update game state
        if self._turn == "blue" and self._board.get_opponent_general("blue").get_legal_moves() == []:
            self.game_state = "BLUE_WON"
            self.game_over = True
        elif self._turn == "red" and self._board.get_opponent_general("red").get_legal_moves() == []:
            self.game_state = "RED_WON"
            self.game_over = True
        self.change_turn()
        return True
    
    def is_in_check(self, color:str):
        general = self._board.get_general(color)
        return general.in_check()

    def get_game_state(self):
        return self._game_state
        


def print_board(board):

    for col in "abcdefghi":
        if col == "a":
            print("   "+col, end=" "*4)
        else:
            print(col, end=" "*4)
    print()
    for row in [1,2,3,4,5,6,7,8,9,10]:
        print("------------------------------------------------")
        if row == 10:
            print(str(row)+" "+" | ".join(["  " if v is None else str(v) for v in board.get_row(row)]))
        else:
            print(str(row)+"  "+" | ".join(["  " if v is None else str(v) for v in board.get_row(row)]))
    print("------------------------------------------------")


if __name__ == "__main__":
    col_dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}
    def move_converter(move, col_dict):
        row = move[0]
        col = col_dict[int(move[1])]
        if row == "0":
            row = "10"
        return col + row
    moves = [("79", "78"), ("41", "42"), ("02", "83"), ("12", "33"), ("82", "85"), ("32", "35"),
             ("75", "74"), ("17", "36"), ("03", "75"), ("45", "46"), ("08", "76"), ("13", "45"), ("04", "94"),
             ("25", "26"), ("06", "96"), ("11", "51"), ("77", "67"), ("16", "25")]
    conv_moves = [(move_converter(move[0], col_dict), move_converter(move[1], col_dict)) for move in moves]

    game = JanggiGame()

    for move in conv_moves:
        print(move)
        print(game._turn)
        print("red:", game.is_in_check("red"), "blue:", game.is_in_check("blue"))
        print(game.make_move(move[0], move[1]))
        game.view()
        print(game.get_game_state())

    