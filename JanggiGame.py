# Author: Joseph Doiron (Obviously)
# Date: 3/11/2021


class SpaceError(Exception):
    """Exception used when a space error occurs"""
    pass

class CommitError(Exception):
    """exception used when a move revert is made before commit is called for a Move object"""
    pass


class SpaceSequence:
    """Helper class that is suppose to mimic Piece.get_[direction]_space() so a known list of spaces can be used
    in get_moves_in_direction().

    e.g.
    ------------------------------------
    sq = SpaceSequence(["a1", "a2", "a3"])
    sq.get_next() -> "a1"
    sq.get_next() - "a1"
    sq.get_next("a1") -> "a2"
    """

    def __init__(self, spaces: list):
        """
        Args:
            spaces: list
        """
        self.spaces = spaces

    def get_next(self, space: str = None):
        """Returns the first space unless another space is given.
        Args:
            space: str

        Returns: str
            If nothing is passed, this will return the first space in the list. If a space is passed, it will return
            the next space in the list. "00" is returned if a space is passed that isn't in the list.
        """
        if space is None:
            return self.spaces[0]
        spaces = self.spaces
        try:
            return spaces[spaces.index(space)+1]
        except ValueError:
            return "00"
        except IndexError:
            return "00"


class Move:
    """Helper class that represents a move on the board.
    """

    def __init__(self, curr_space, new_space, board):
        """
        Args:
            curr_space: str
            new_space: str
            board: JanggiBoard.Board
        """
        self._board = board
        self._curr_space = curr_space
        self._new_space = new_space
        self._piece = board.get_piece(curr_space)
        self._captured_piece = board.get_piece(new_space)
        self._commited = False

    def commit(self):
        """Commits the move to the board
        Returns: None
        """
        if self._board.has_opponent_piece(self._new_space, self._piece.color):
            self._board.remove_piece(self._new_space)
        self._piece.change_space(self._new_space)
        self._commited = True

    def revert(self):
        """Reverts the move if it was committed"""
        if self._commited:
            self._piece.change_space(self._curr_space)
            if self._captured_piece is not None:
                self._board.add_piece(self._new_space, self._captured_piece)
        else:
            raise CommitError("move must be committed first")


class Space:
    """Helper class for space manipulation"""
    
    def __new__(cls, space: str = None):
        """If space is None an instance will not be created and None is returned"""
        if space is None:
            return None
        return super().__new__(cls) 
         
    def __init__(self, space:str):
        """Args:
            space:  str
        """
        self._col, self._row = ord(space[0]), int(space[1:])
        
    def __str__(self):
        return chr(self.col)+str(self.row)
        
    @property
    def row(self):
        """Returns: int"""
        return self._row
    
    @property
    def col(self):
        """Returns: int"""
        return self._col


class Piece:
    """base class for all Janggi Pieces"""

    def __init__(self, color: str = None, space: str = None, board: 'Board' = None):
        """
        Args:
            color: str
                "blue" | "red"
            space: str
            board: JanggiGame.Board
        """
        self._color = color
        self._space = Space(space)
        self._board = board
        if space is not None and board is not None:
            board.place_piece(self, space)

    def __str__(self):
        return f"{self._color[0]}{self.__class__.__name__[0:2]}"

    def __repr__(self):
        return f"{self._color[0]}{self.__class__.__name__[0:2]}"

    @property
    def space(self):
        """Returns the space as a string (e.g. "a1")
        Returns: str"""
        return str(self._space)

    @property
    def row(self):
        """Returns the row as an int"""
        return self._space.row

    @property
    def col(self):
        """Returns the column as an int"""
        return self._space.col

    @property
    def color(self):
        """returns the color ("red" | "blue"
        """
        return self._color

    def get_forward_space(self, starting_space: str = None):
        """Returns the space in front (forward) of the piece. This method can also be used in a loop to get more spaces.
        Args:
            starting_space: str
                the starting space to use
        Returns: str"""
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_space(space)
        return self._board.get_bottom_space(space)

    def get_right_space(self, starting_space: str = None):
        """Returns the space to the right of the piece. This method can also be used in a loop to get more spaces.
        Args:
            starting_space: str
                the starting space to use
        Returns: str"""
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_right_space(space)
        return self._board.get_left_space(space)

    def get_left_space(self, starting_space: str = None):
        """Returns the space to the left of the piece. This method can also be used in a loop to get more spaces.
        Args:
            starting_space:
                the starting space to use
        Returns: str"""
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_left_space(space)
        return self._board.get_right_space(space)

    def get_backward_space(self, starting_space: str = None):
        """Returns the space to behind the piece. This method can also be used in a loop to get more spaces.
        Args:
            starting_space: str
                the starting space to use
        Returns: str"""
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_bottom_space(space)
        return self._board.get_top_space(space)

    def get_diagonal_forward_right(self, starting_space: str = None):
        """Returns a diagonal space. This method can also be used in a loop to get more spaces.
        Args:
            starting_space:
                the starting space to use
        Returns: str"""
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_right_space(space)
        return self._board.get_bottom_left_space(space)

    def get_diagonal_forward_left(self, starting_space: str = None):
        """Returns a diagonal space. This method can also be used in a loop to get more spaces.
        Args:
            starting_space:
                the starting space to use
        Returns: str"""
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_top_left_space(space)
        return self._board.get_bottom_right_space(space)

    def get_diagonal_backward_right(self, starting_space: str = None):
        """Returns a diagonal space. This method can also be used in a loop to get more spaces.
        Args:
            starting_space:
                the starting space to use
        Returns: str"""
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_bottom_right_space(space)
        return self._board.get_top_left_space(space)

    def get_diagonal_backward_left(self, starting_space: str = None):
        """Returns a diagonal space. This method can also be used in a loop to get more spaces.
        Args:
            starting_space:
                the starting space to use
        Returns: str"""
        space = starting_space or self.space
        if self.color == "blue":
            return self._board.get_bottom_left_space(space)
        return self._board.get_top_right_space(space)

    def in_fortress(self):
        """Returns True if the piece is in a fortress
        Returns: True | False"""
        if self.space in self._board.fortress_spaces:
            return True
        return False

    def change_space(self, new_space: str):
        """Changes the pieces space on the board
        Args:
            new_space: str
        Returns: None"""
        self._board.move_piece(self, new_space)
        self._space = new_space

    def move(self, new_space: str):
        """Creates a janggiGame.Move object to later be commited/reverted
        Args:
            new_space: str
        Returns: JanggiGame.Move"""
        return Move(self.space, new_space, self._board)

class Board:
    """Represents the game board"""

    def __init__(self):
        """initializes the board"""
        self.spaces = {col + str(row): None for col in "abcdefghi" for row in range(1, 11)}
        self.blue_fortress_spaces = ["d8", "d9", "d10", "e8", "e9", "e10", "f8", "f9", "f10"]
        self.red_fortress_spaces = ["d1", "d2", "d3", "e1", "e2", "e3", "f1", "f2", "f3"]
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

    @property
    def fortress_spaces(self):
        """Returns the fortress spaces
        Returns: list"""
        return self.red_fortress_spaces+self.blue_fortress_spaces

    def valid_space(self, space: str):
        """Determines if a space is a valid space
        Args:
            space: str
        Returns: True | False"""
        if space in self.spaces:
            return True
        return False

    def place_piece(self, piece: Piece, space: str):
        """Places a piece on the board
        Args:
            piece: JanggiGame.Piece
            space: str
        Returns: None"""
        if not self.valid_space(space):
            raise SpaceError(f"{space} is not a valid space")
        if self.spaces[space] is not None:
            raise SpaceError(f"{space} already has a piece")
        self.spaces[space] = piece
    
    def assign_space(self, space: str, piece: Piece = None):
        """Assigns a new value to a space. This should be either a Piece or None. Raises SpaceError if the space isn't valid
        Args:
            space: str
            piece: piece or None
        Returns: None"""
        if self.valid_space(space):
            self.spaces[space] = piece
        else:
            raise SpaceError(f"{space} is not a valid space")

    def move_piece(self, piece: Piece, new_space: str):
        """Moves a piece to a new space
        Args:
            piece: JanggiGame.Piece
            new_space: str
        Returns: None"""
        self.assign_space(piece.space, None)
        self.assign_space(new_space, piece)

    def remove_piece(self, space: str):
        """Removes a piece from the board.
        Args:
            space: str
        Returns: None"""
        piece = self.get_piece(space)
        self.assign_space(space, None)
        self.pieces[piece.color]["other-pieces"].remove(piece)

    def add_piece(self, space: str, piece: Piece):
        """Adds a piece back to the board.
        Args:
            space: str
            piece: janggiGame.Piece
        Returns: None"""
        self.assign_space(space, piece)
        self.pieces[piece.color]["other-pieces"].append(piece)

    def get_fortress_spaces(self, color: str):
        """Gets the fortress spaces for a color
        Args:
            color: str
        Returns: list"""
        if color == "red":
            return self.red_fortress_spaces
        elif color == "blue":
            return self.blue_fortress_spaces
        else:
            return []

    def get_general(self, color: str):
        """Gets the color's general.
        Args:
            color: str
        Returns: JanggiGame.General"""
        return self.pieces[color]["general"]

    def get_opponent_general(self, color):
        """gets the opponents general.
        Args:
            color: str
        Returns: JanggiGame.General"""
        if color == "blue":
            return self.get_general("red")
        elif color == "red":
            return self.get_general("blue")

    def get_row_spaces(self, row: int):
        """gets a row's spaces"""
        return [space for space in self.spaces if Space(space).row == row]

    def get_row(self, row: int):
        """gets a row's values"""
        return [self.spaces[space] for space in self.get_row_spaces(row)]

    def get_piece(self, space: str):
        """gets a piece"""
        if not self.valid_space(space):
            raise SpaceError(f"{space} is not a valid space")
        return self.spaces[space]

    def has_piece(self, space: str):
        """Returns True if the space has a piece. It will return False otherwise (even if the space is invalid)."""
        if not self.valid_space(space):
            return False
        if self.spaces[space] is None:
            return False
        return True

    def space_open(self, space: str):
        """Returns True if the space is open"""
        if not self.valid_space(space):
            return False
        return not self.has_piece(space)
        
    def has_player_piece(self, space, color):
        """Returns true if the space has a player's piece."""
        if self.has_piece(space):
            piece = self.spaces[space]
            if piece.color == color:
                return True
        return False

    def has_opponent_piece(self, space: str, color: str):
        """Returns true if the space has an opponents piece"""
        if self.has_piece(space):
            piece = self.spaces[space]
            if piece.color != color:
                return True
        return False

    def get_pieces(self, color: str):
        """Gets all the player's current playable (not captured) pieces."""
        return self.pieces[color]["other-pieces"]

    def get_opponents_attacking_spaces(self, color: str):
        """Gets all the opponents attacking spaces. These are spaces that piece can move to (open spaces and spaces with opossing pieces)
        as well as spaces with another piece of the same color. This allows checking for checkmate. If a general tries to capture a piece that is also one of
        another pieces attacking spaces, it can't move there since it would be captured on the next move.

        Returns: list"""
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

    def get_right_space(self, space: str):
        """gets space to the right"""
        space = Space(space)
        col = chr(space.col + 1)
        row = str(space.row)
        right_space = col + row
        return right_space

    def get_left_space(self, space: str):
        """Gets space to the left"""
        space = Space(space)
        col = chr(space.col - 1)
        row = str(space.row)
        left_space = col + row
        return left_space

    def get_top_space(self, space: str):
        """gets space above"""
        space = Space(space)
        col = chr(space.col)
        row = str(space.row - 1)
        top_space = col + row
        return top_space

    def get_bottom_space(self, space: str):
        """gets space below"""
        space = Space(space)
        col = chr(space.col)
        row = str(space.row + 1)
        bottom_space = col + row
        return bottom_space

    def get_top_right_space(self, space: str):
        """Gets top right space"""
        space = Space(space)
        col = chr(space.col + 1)
        row = str(space.row - 1)
        top_right_space = col + row
        return top_right_space

    def get_top_left_space(self, space: str):
        """gets top left space (pointless docstring ik)"""
        space = Space(space)
        col = chr(space.col - 1)
        row = str(space.row - 1)
        top_left_space = col + row
        return top_left_space

    def get_bottom_right_space(self, space: str):
        """gets bottom right space"""
        space = Space(space)
        col = chr(space.col + 1)
        row = str(space.row + 1)
        bottom_right_space = col + row
        return bottom_right_space

    def get_bottom_left_space(self, space: str):
        """gets bottom left space"""
        space = Space(space)
        col = chr(space.col - 1)
        row = str(space.row + 1)
        bottom_left_space = col + row
        return bottom_left_space


class FortressPiece(Piece):
    """Base class for General and Guard"""

    def get_available_adjacent_spaces(self, starting_space:str=None):
        """gets the available adjacent spaces in the fortress.
        Args:
            starting_space: str
        Returns: list"""
        curr_space = starting_space or self.space
        board = self._board
        adjacent_spaces = [board.get_top_space(curr_space), board.get_bottom_space(curr_space), board.get_left_space(curr_space),
                           board.get_right_space(curr_space), board.get_bottom_left_space(curr_space), board.get_bottom_right_space(curr_space),
                           board.get_top_left_space(curr_space), board.get_top_right_space(curr_space)]
        return [
            space for space in adjacent_spaces
            if (board.has_opponent_piece(space, self.color) or board.space_open(space)) and board.valid_space(space)
        ]

    def get_fortress_moves(self):
        """Returns the available spaces in the fortress the piece can move to.
        Returns: list"""
        adjacent_spaces = set(self.get_available_adjacent_spaces())
        fortress_spaces = set(self._board.get_fortress_spaces(self.color))
        return list(fortress_spaces & adjacent_spaces)


class General(FortressPiece):
    """Janggi General"""

    def in_check(self):
        """Returns if the general is in check
        Returns: True | False"""
        opponent_attacking_spaces = self._board.get_opponents_attacking_spaces(self.color)
        if self.space in opponent_attacking_spaces:
            return True
        return False

    def in_checkmate(self):
        """Returns True is the general is in checkmate
        Returns: True | False"""
        legal_moves = self.get_legal_moves()
        if legal_moves:
            return False
        return True

    def get_legal_moves(self):
        """Returns a list of spaces the general can move to
        Returns: list"""
        opponent_attacking_spaces = self._board.get_opponents_attacking_spaces(self.color)
        return list(set(self.get_fortress_moves()) - set(opponent_attacking_spaces))


class Guard(FortressPiece):
    """Janggi Guard"""

    def get_legal_moves(self):
        """Returns the spaces the piece can move to
        Returns: list"""
        return self.get_fortress_moves()

    def get_attacking_spaces(self):
        """Returns the spaces the piece can attack (this includes spaces that have pieces of the sme color).
        Returns: list"""
        return self.get_fortress_moves()

class Horse(Piece):
    """Janggi Horse"""

    def get_move_sequences(self):
        """Returns a list of tuples for each possible sequence of moves
        Returns: list"""
        forward_space = self.get_forward_space()
        left_space = self.get_left_space()
        right_space = self.get_right_space()
        move_sequences = [
            (forward_space, self.get_diagonal_forward_right(forward_space)),
            (forward_space, self.get_diagonal_forward_left(forward_space)),
            (left_space, self.get_diagonal_forward_left(left_space)),
            (left_space, self.get_diagonal_backward_left(left_space)),
            (right_space, self.get_diagonal_forward_right(right_space)),
            (right_space, self.get_diagonal_backward_right(right_space))
        ]
        return move_sequences

    def get_attacking_spaces(self):
        """Returns the spaces the piece can attack (this includes spaces that have pieces of the sme color).
        Returns: list"""
        attacking_spaces = []
        move_sequences = self.get_move_sequences()
        board = self._board
        for spaces in move_sequences:
            if board.valid_space(spaces[0]) and board.valid_space(spaces[1]):
                if board.space_open(spaces[0]):
                    attacking_spaces.append(spaces[1])
        return attacking_spaces

    def get_legal_moves(self):
        """Returns list of legal moves
        Returns: list"""
        legal_moves = []
        move_sequences = self.get_move_sequences()
        board = self._board
        for spaces in move_sequences:
            if board.valid_space(spaces[0]) and board.valid_space(spaces[1]):
                if board.space_open(spaces[0]) and not board.has_player_piece(spaces[1], self.color):
                    legal_moves.append(spaces[1])
        return legal_moves
        

class Elephant(Piece):
    """Janggi Elephant"""

    def get_move_sequences(self):
        """Returns a list of tuples for each possible sequence of moves
        Returns: list"""
        forward_space = self.get_forward_space()
        forward_diag_right_space = self.get_diagonal_forward_right(forward_space)
        forward_diag_left_space = self.get_diagonal_forward_left(forward_space)
        left_space = self.get_left_space()
        left_diag_forward_space = self.get_diagonal_forward_left(left_space)
        left_diag_backward_space = self.get_diagonal_backward_left(left_space)
        right_space = self.get_right_space()
        right_diag_forward_space = self.get_diagonal_forward_right(right_space)
        right_diag_backward_space = self.get_diagonal_backward_right(right_space)
        move_sequences = [
            (forward_space, forward_diag_right_space, self.get_diagonal_forward_right(forward_diag_right_space)),
            (forward_space, forward_diag_left_space , self.get_diagonal_forward_left(forward_diag_left_space)),
            (right_space, right_diag_forward_space, self.get_diagonal_forward_right(right_diag_forward_space)),
            (right_space, right_diag_backward_space, self.get_diagonal_backward_right(right_diag_backward_space)),
            (left_space, left_diag_forward_space, self.get_diagonal_forward_left(left_diag_forward_space)),
            (left_space, left_diag_backward_space, self.get_diagonal_backward_left(left_diag_backward_space))
        ]
        return move_sequences

    def get_attacking_spaces(self):
        """Returns the spaces the piece can attack (this includes spaces that have pieces of the sme color).
        Returns: list"""
        attacking_spaces = []
        move_sequences = self.get_move_sequences()
        board = self._board
        for spaces in move_sequences:
            if board.valid_space(spaces[0]) and board.valid_space(spaces[1]) and board.valid_space(spaces[2]):
                if board.space_open(spaces[0]) and board.space_open(spaces[1]):
                    attacking_spaces.append(spaces[2])
        return attacking_spaces


    def get_legal_moves(self):
        """gets the legal move
        Returns: list"""
        legal_moves = []
        move_sequences = self.get_move_sequences()
        board = self._board
        for spaces in move_sequences:
            if board.valid_space(spaces[0]) and board.valid_space(spaces[1]) and board.valid_space(spaces[2]):
                if board.space_open(spaces[0]) and board.space_open(spaces[1]) and not board.has_player_piece(spaces[2], self.color):
                    legal_moves.append(spaces[2])
        return legal_moves


class Chariot(Piece):
    """Janggi Chariot"""

    _diagonal_moves = {"d3": ["e2", "f1"], "d1": ["e2", "f3"], "f1": ["e2", "d3"], "f3": ["e2", "d1"],
                       "e2": ["d1", "f1", "d3", "f3"],
                       "d8": ["e9", "f10"], "d10": ["e9", "f8"], "f8": ["e9", "d10"], "f10": ["e9", "d8"],
                       "e9": ["d8", "f8", "d10", "f10"]}

    def get_moves_in_direction(self, next_space_method, move_type: str = "legal"):
        """gets spaces the piece can move to in a given direction.

        Args:
            next_space_method: a method for getting the next space
            move_type: 'attacking' | 'legal'
        Returns: list"""
        
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
        """gets the legal move
        Returns: list"""
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
        """Returns the spaces the piece can attack (this includes spaces that have pieces of the sme color).
        Returns: list"""
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
    """Janggi Cannon"""

    _diagonal_moves = {"d1": ["e2", "f3"], "f1": ["e2", "d3"], "d3": ["e2", "f1"], "f3": ["e2", "d1"],
                       "d8": ["e9", "f10"], "f8": ["e9", "d10"],
                       "d10": ["e9", "f8"], "f10": ["e9", "d8"]}

    def get_moves_in_direction(self, next_space_method, move_type: str = "legal"):
        """gets spaces the piece can move to in a given direction.

        Args:
            next_space_method: a method for getting the next space
            move_type: 'attacking' | 'legal'
        Returns: list"""
        get_next_space = next_space_method
        spaces = []
        board = self._board
        space = get_next_space()
        while board.space_open(space) and board.valid_space(space):
            space = get_next_space(space)
        if board.has_piece(space) and board.valid_space(space):
            piece = board.get_piece(space)
            if type(piece) == Cannon: # Cannon can't jump over another Cannon
                return []
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
        """gets the legal move
        Returns: list"""
        legal_forward_spaces = self.get_moves_in_direction(self.get_forward_space)
        legal_left_spaces = self.get_moves_in_direction(self.get_left_space)
        legal_right_spaces = self.get_moves_in_direction(self.get_right_space)
        legal_backward_spaces = self.get_moves_in_direction(self.get_backward_space) 
        legal_spaces = legal_forward_spaces+legal_left_spaces+legal_right_spaces+legal_backward_spaces
        if self.in_fortress() and self.space in self._diagonal_moves:
            diag_spaces = self._diagonal_moves[self.space]
            if self._board.has_piece(diag_spaces[0]) and (self._board.has_opponent_piece(self.color, diag_spaces[1]) or self._board.space_open(diag_spaces[1])):
                legal_spaces.append(diag_spaces[1])
        return legal_spaces

    def get_attacking_spaces(self):
        """Returns the spaces the piece can attack (this includes spaces that have pieces of the sme color).
        Returns: list"""
        attacking_forward_spaces = self.get_moves_in_direction(self.get_forward_space, "attacking")
        attacking_left_spaces = self.get_moves_in_direction(self.get_left_space, "attacking")
        attacking_right_spaces = self.get_moves_in_direction(self.get_right_space, "attacking")
        attacking_backward_spaces = self.get_moves_in_direction(self.get_backward_space, "attacking")
        attacking_spaces = attacking_forward_spaces+attacking_left_spaces+attacking_right_spaces+attacking_backward_spaces
        if self.in_fortress() and self.space in self._diagonal_moves:
            diag_spaces = self._diagonal_moves[self.space]
            if self._board.has_piece(diag_spaces[0]):
                attacking_spaces.append(diag_spaces[1])
        return attacking_spaces

class Soldier(Piece):
    """Janggi Soldier"""

    _diagonal_moves = {"d3": "e2", "f3": "e2", "e2": ["f1", "d1"], "d8": "e9", "f8": "e9", "e9": ["d10", "f10"]}
    
    def get_legal_moves(self):
        """gets the legal move
        Returns: list"""
        legal_spaces = []
        board = self._board
        for space in [self.get_forward_space(), self.get_left_space(), self.get_right_space()]:
            if (board.has_opponent_piece(space, self.color) or board.space_open(space)) and board.valid_space(space):
                legal_spaces.append(space)
        if self.in_fortress() and self.space in self._diagonal_moves:
            if self.space in ["e2", "e9"]:
                diag_spaces = self._diagonal_moves[self.space]
                for space in diag_spaces:
                    if board.has_opponent_piece(space, self.color) or self._board.space_open(space):
                        legal_spaces.append(space)
            else:
                space = self._diagonal_moves[self.space]
                if board.has_opponent_piece(space, self.color) or self._board.space_open(space):
                    legal_spaces.append(space)
        return legal_spaces
    
    def get_attacking_spaces(self):
        """Returns the spaces the piece can attack (this includes spaces that have pieces of the sme color).
        Returns: list"""
        attacking_spaces = []
        board = self._board
        for space in [self.get_forward_space(), self.get_left_space(), self.get_right_space()]:
            if board.valid_space(space):
                attacking_spaces.append(space)
        return attacking_spaces

class JanggiGame:
    """janggiGame class used to play janggi (aka Korean Chess)."""
    
    def __init__(self):
        """initialized board and state"""
        self._board = Board()
        self._turn = "blue"
        self._game_state = "UNFINISHED"

    def view(self):
        """prints the board"""
        print_board(self._board)

    def change_turn(self):
        """changes the turn"""
        if self._turn == "blue":
            self._turn = "red"
        else:
            self._turn = "blue"

    def make_move(self, current_space:str, new_space:str):
        """each player uses this method for moving pieces. Returns True id move was successful/legal
        Args:
            current_space: str
            new_space: str
        Returns: True | False"""
        if self._game_state != "UNFINISHED":
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
        move = piece.move(new_space)
        move.commit()
        # make sure move doesn't put player's general in check
        if self.is_in_check(self._turn):
            move.revert()
            return False
        # update game state
        if self._board.get_opponent_general(self._turn).get_legal_moves() == []:
            self._game_state = self._turn.upper()+"_WON"
        self.change_turn()
        return True
    
    def is_in_check(self, color:str):
        """Returns True if player is in check"""
        general = self._board.get_general(color)
        return general.in_check()

    def get_game_state(self):
        """returns the game state"""
        return self._game_state
        


def print_board(board):

    for col in "abcdefghi":
        if col == "a":
            print("   "+col, end=" "*5)
        else:
            print(col, end=" "*5)
    print()
    for row in [1,2,3,4,5,6,7,8,9,10]:
        print("------------------------------------------------------")
        if row == 10:
            print(str(row)+" "+" | ".join(["   " if v is None else str(v) for v in board.get_row(row)]))
        else:
            print(str(row)+"  "+" | ".join(["   " if v is None else str(v) for v in board.get_row(row)]))
    print("------------------------------------------------------")


if __name__ == "__main__":

    game = JanggiGame()
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    game.make_move('a7', 'b7')
    game.make_move('i4', 'h4')
    game.make_move('h10', 'g8')
    game.make_move('c1', 'd3')
    game.make_move('h8', 'e8')
    game.make_move('i1', 'i2')
    game.make_move('e7', 'f7')
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    game.make_move('b3', 'e3')
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    game.make_move('g10', 'e7')
    game.make_move('e4', 'd4')
    game.make_move('c10', 'd8')
    game.make_move('g1', 'e4')
    game.make_move('f10', 'f9')
    game.make_move('h1', 'g3')
    game.make_move('a10', 'a6')
    game.make_move('d4', 'd5')
    game.make_move('e9', 'f10')
    game.make_move('h3', 'f3')
    game.make_move('e8', 'h8')
    game.make_move('i2', 'h2')
    game.make_move('h8', 'f8')
    game.make_move('f1', 'f2')
    game.make_move('b8', 'e8')
    game.make_move('f3', 'f1')
    game.make_move('i7', 'h7')
    game.make_move('f1', 'c1')
    game.make_move('d10', 'e9')
    game.make_move('a4', 'b4')
    game.make_move('a6', 'a1')
    game.make_move('c1', 'a1')
    game.make_move('f8', 'd10')
    game.make_move('d5', 'c5')
    game.make_move('i10', 'i6')
    game.make_move('b1', 'd4')
    game.make_move('c7', 'c6')
    game.make_move('c5', 'b5')
    game.make_move('b10', 'd7')
    game.make_move('d4', 'f7')
    game.make_move('g7', 'f7')
    game.make_move('a1', 'f1')
    game.make_move('g8', 'f6')
    game.make_move('f1', 'f5')
    game.make_move('f6', 'd5')
    game.make_move('e3', 'e5')
    game.make_move('f7', 'f6')
    game.make_move('f5', 'f7')
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    game.make_move('f10', 'e10')
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    game.make_move('e2', 'f1')
    game.make_move('i6', 'i3')
    game.make_move('h2', 'g2')
    game.make_move('i3', 'i1')
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    game.make_move('f1', 'e2')
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    game.make_move('f6', 'f5')
    game.make_move('c4', 'd4')
    game.make_move('f5', 'e5')
    game.make_move('f7', 'd7')
    game.make_move('e7', 'g4')
    game.make_move('d4', 'd5')
    game.make_move('e5', 'e4')
    game.make_move('d3', 'e5')
    game.make_move('e4', 'e3')
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    game.make_move('e2', 'd2')
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    game.make_move('e3', 'e2')
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    print(game.make_move('d2', 'd3'))
    print(game.is_in_check('red'))
    print(game.is_in_check('blue'))
    game.make_move('e8', 'e4')
    game.make_move('f2', 'e2')
    game.make_move('i1', 'd1')
    game.make_move('e2', 'd2')
    print(game.make_move('d1', 'f3'))
    print(game.get_game_state())
    game.view()

    p = game._board.get_piece("d3")
    print(p.get_legal_moves())

    