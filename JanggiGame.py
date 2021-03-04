# exceptions

class InvalidCapture(Exception):
    pass

class InvalidMove(Exception):
    pass

# pieces

class Piece:
    """
    This class will be the base class for other pieces. It will need to communicate to the
    Space and Board classes.

    A piece knows about its space and the space will know about its piece, using references (same concept as pointers).

    It will be able to get the spaces adjacent to it based on its current space, and handle capturing an opponents piece
    """
    
    def __init__(self, color=None, space=None):
        self._color = color
        self._space = space
        if space is not None:
            space.add_piece(self)
            
    def __str__(self):
        return f"piece at {self.space}"
    
    @property
    def space(self):
        """this will return the piece's current space (an object)

        Returns:
            [type]: [description]
        """
        return self._space
    
    @property
    def is_blue(self):
        """will return true if the piece is a blue piece

        Returns:
            [type]: [description]
        """
        if self._color == "blue":
            return True
        return False
    
    @property
    def is_red(self):
        """will return true if the piece is red

        Returns:
            [type]: [description]
        """
        if self._color == "red":
            return True
        return False
    
    @property
    def color(self):
        """return the piece's color (red or blue)

        Returns:
            [type]: [description]
        """
        return self._color
    
    def get_forward_space(self, board):
        """will return the space in front of the piece, which depends on the pieces color.

        Args:
            board ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self.is_blue:
            return board.get_top_space(self.space.as_str)
        else:
            return board.get_bottom_space(self.space.as_str)
    
    def get_right_space(self, board):
        """will return the space to the right of the piece, which depends on the pieces color.

        Args:
            board ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self.is_blue:
            return board.get_right_space(self.space.as_str)
        else:
            return board.get_left_space(self.space.as_str)
    
    def get_left_space(self, board):
        """will return the space to the left of the piece, which depends on the pieces color.

        Args:
            board ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self.is_blue:
            return board.get_left_space(self.space.as_str)
        else:
            return board.get_right_space(self.space.as_str)
    
    def get_backward_space(self, board):
        """will return the space behind piece, which depends on the pieces color.

        Args:
            board ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self.is_blue:
            return board.get_bottom_space(self.space.as_str) 
        else:
            return board.get_top_space(self.space.as_str)
    
    def change_space(self, new_space):
        """will change the pieces current space

        Args:
            new_space ([type]): [description]
        """
        self._space = new_space
    
    # classes that inherite Piece must overwrite this method
    def is_blocked(self):
        """method that will be overwritten
        """
        pass
        
    def is_valid_move(self, new_space, board, test_num):
        """will return true if the move is valid (for Horses and Elephants for now)"""
        # piece has to move forward
        if (self.is_blue and new_space.row >= self.space.row) or (self.is_red and new_space.row <= self.space.row):
            return False
        if self.is_blocked(new_space, board): # piece is blocked by either a blue or red piece
            return False
        if new_space.piece is not None:
            if new_space.piece.color == self.color: # the new space already has a player's piece
                return False
        delta_row = abs(new_space.row - self.space.row)
        delta_col = abs(new_space.col - self.space.col)
        return delta_row * delta_col == test_num
        
    def capture(space):
        """this will capture a space, removing the opponents piece from the space

        Args:
            space ([type]): [description]

        Raises:
            InvalidCapture: [description]
            InvalidCapture: [description]
        """
        if space.has_piece:
            if space.piece.color != self.color:
                space.remove_piece()
            else:
                raise InvalidCapture(f"{space} has {self.color} piece")
        else:
            raise InvalidCapture(f"{space} does not have piece")
            

class General(Piece):
    """this class will implement a general piece

    Args:
        Piece ([type]): [description]
    """

    def is_blocked(self, new_space, board):
        """based on how the piece will move, it will return true if the move is valid.
        It will also need the new_space object passed to it as well as the board"""
        pass
    
    def move(new_space):
        """moves a general to a new space

        Args:
            new_space ([type]): [description]
        """
        pass
        # 1. figures out what the possible spaces it can move to are
        # 2. sees if the new space is one of the possible spaces it can move to
        # 3. if it is a possible move, it see's if the new space has an opponents piece
        #    and if it does, it captures it, removing it form the space, and then updating the space's piece and its space
        # Notes: Once the opponents piece is removed, it can be deleted from memory.


class Guard(Piece):
    """this will implement a guard piece

    Args:
        Piece ([type]): [description]
    """

    def is_blocked(self):
        """based on how the piece will move, it will return true if the move is valid.
        It will also need the new_space object passed to it as well as the board"""
        pass

    def move(new_space):
        """this will move the piece to a new space

        Args:
            new_space ([type]): [description]
        """
        pass


class Horse(Piece):
    """this will implement a horse piece

    Args:
        Piece ([type]): [description]
    """
    
    def is_blocked(self, new_space, board): # this can either be a red or blue piece
        """based on how the piece will move, it will return true if the move is valid.
        It will also need the new_space object passed to it as well as the board"""
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
    
    def move(self, new_space, board):
        """this will move the piece to a new space

        Args:
            new_space ([type]): [description]
            board ([type]): [description]

        Raises:
            InvalidMove: [description]
        """
        if self.is_valid_move(new_space, board, 2):
            self.change_space(new_space)
            if new_space.has_opponent_piece(self.color):
                self.capture(new_space)
            new_space.add_piece(self)
        else:
            raise InvalidMove(f"{self} can't move to {new_space}")


class Elephant(Piece):
    
    def is_blocked(self, new_space, board):
        """based on how the piece will move, it will return true if the move is valid.
        It will also need the new_space object passed to it as well as the board"""
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
         
    def move(new_space):
        """this will move the piece to a new space

        Args:
            new_space ([type]): [description]

        Raises:
            InvalidMove: [description]
        """
        if self.is_valid_move(new_space, board, 6):
            self.change_space(new_space)
            if new_space.has_opponent_piece(self.color):
                self.capture(new_space)
            new_space.add_piece(self)
        else:
            raise InvalidMove(f"{self} can't move to {new_space}")


class Chariot(Piece):
    """this will implement a chariot piece

    Args:
        Piece ([type]): [description]
    """

    def is_blocked(self, new_space, board):
        """based on how the piece will move, it will return true if the move is valid.
        It will also need the new_space object passed to it as well as the board"""
        pass
    
    def move(new_space, board):
        """this will move the piece to a new space

        Args:
            new_space ([type]): [description]
            board ([type]): [description]

        Raises:
            InvalidMove: [description]
        """
        if new_space.col != self.space.col and new_space.row != self.space.row:
            raise InvalidMove

                  
class Cannon(Piece):
    """this will implement the cannon piece

    Args:
        Piece ([type]): [description]
    """

    def is_blocked(self, new_space, board):
        """based on how the piece will move, it will return true if the move is valid.
        It will also need the new_space object passed to it as well as the board"""
        pass
    
    def move(new_space):
        """this will move the piece to a new space

        Args:
            new_space ([type]): [description]
        """
        pass

class Soldier(Piece):

    def is_blocked(self, new_space, board):
        """based on how the piece will move, it will return true if the move is valid.
        It will also need the new_space object passed to it as well as the board"""
        pass
    
    def is_valid_move(self):
        pass
    
    def move(new_space):
        pass

# other objects
# -------------

class Space:
    """this represents a space on the board. it knows about its piece (if any)."""
    
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
        """will remove the piece from the space
        """
        self._piece = None
    
    def add_piece(self, piece):
        """will add a piece to the space

        Args:
            piece ([type]): [description]
        """
        if not self.has_piece:
            self._piece = piece
    
    def has_opponent_piece(self, color):
        """will return True if an opponent's piece is on the space

        Args:
            color ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self.has_piece and self.piece.color != color:
            return True
        return False
    
class Board:
    """this represents the board. It will contain a dictionary of space objects and have methods to get spaces various spaces"""
    
    def __init__(self):
        self.spaces = {col+str(row): Space(col, row) for col in "abcdefghi" for row in range(1,11)}
    
    def get_space(self, space):
        """will return the space given a space (e.g. 'a1')

        Args:
            space ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            return self.spaces[space]
        except KeyError:
            return None
    
    def get_right_space(self, space):
        """will get the space to the right (e.g. get_right_space('e3') -> Space('e4'))

        Args:
            space ([type]): [description]

        Returns:
            [type]: [description]
        """
        col = chr(ord(space[0])+1)
        row = space[1]
        return self.get_space(col+row)
    
    def get_left_space(self, space):
        """will get the space to the left

        Args:
            space ([type]): [description]

        Returns:
            [type]: [description]
        """
        col = chr(ord(space[0])-1)
        row = space[1]
        return self.get_space(col+row)
    
    def get_top_space(self, space):
        """will get the space above the current space

        Args:
            space ([type]): [description]

        Returns:
            [type]: [description]
        """
        col = space[0]
        row = str(int(space[1])-1)
        return self.get_space(col+row)
    
    def get_bottom_space(self, space):
        """will get the space at the bottom of the current space

        Args:
            space ([type]): [description]

        Returns:
            [type]: [description]
        """
        col = space[0]
        row = str(int(space[1])+1)
        return self.get_space(col+row)

class JanggiGame:
    """this is the class that implements the game, utilizing other lower level interfaces.
    the class will contain the Board, allowing this class to access spaces and pieces. Still need to figure this stuff out..."""
    
    def __init__(self):
        self._board = Board()

    def get_game_state(self):
        """this will return the game's current state
        """
        pass

    def is_in_check(self, color):
        """this will return True or False based on if the player is in check or not

        Args:
            color ([type]): [description]
        """
        pass

    def make_move(self, move_from, move_two):
        """this will move a piece to a new space by utilizing lower level interfaces

        Args:
            move_from ([type]): [description]
            move_two ([type]): [description]
        """
        pass