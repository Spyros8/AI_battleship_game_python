import random

from battleship.board import Board
from battleship.convert import CellConverter

class Player:
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players
    
    def __init__(self, board=None, name=None):
        """ Initialises a new player with its board.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        
        if board is None:
            self.board = Board()
        else:
            self.board = board
        
        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name
    
    def __str__(self):
        return self.name
    
    def select_target(self):
        """ Select target coordinates to attack.
        
        Abstract method that should be implemented by any subclasses of Player.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        raise NotImplementedError
    
    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 
        
        This method does not do anything by default, but can be overridden by a subclass to do something useful, for example to record a successful or failed attack.
        
        Returns:
            None
        """
        return None
    
    def has_lost(self):
        """ Check whether player has lost the game.
        
        Returns:
            bool: True if and only if all the ships of the player have sunk.
        """
        return self.board.have_all_ships_sunk()


class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """
    def __init__(self, board, name=None):
        """ Initialise the player with a board and other attributes.
        
        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        super().__init__(board=board, name=name)
        self.converter = CellConverter((board.width, board.height))
        
    def select_target(self):
        """ Read coordinates from user prompt.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        print(f"It is now {self}'s turn.")

        while True:
            try:
                coord_str = input('coordinates target = ')
                x, y = self.converter.from_str(coord_str)
                return x, y
            except ValueError as error:
                print(error)


class RandomPlayer(Player):
    """ A Player that plays at random positions.

    However, it does not play at the positions:
    - that it has previously attacked
    """
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.tracker = set()

    def select_target(self):
        """ Generate a random cell that has previously not been attacked.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        target_cell = self.generate_random_target()
        self.tracker.add(target_cell)
        return target_cell

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None
        
        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)


class AutomaticPlayer(Player):
    """ Player playing automatically using a strategy."""
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        #Define attributes of AutomaticPlayer subclass
        #Boolean. If True it executes the strategy_function method of the AutomaticPlayer
        self.implement_strategy = False
        #A list to record all the positions of the cells which the AutomaticPlayer attacked
        self.attacked_positions = []
        #Define the previous_coordinates of the cell the AutomaticPlayer attacked
        self.previous_coordinates = None
        #Self cycle is constrained between 1-4 and is used in the strategy_function method of the AutomaticPlayer
        self.cycle = 0
        #Save the initial_coordinates, the AutomaticPlayer attacked
        self.save_ship_initial = None

        
    def select_target(self):
        """ Select target coordinates to attack.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        #When the attribute is True, the coordinates are updated via the strategy_function
        if self.implement_strategy:
            coordinates = self.strategy_function()
        #When the attribute is not True, the coordinates for the next attack are randomly generated
        else:
            coordinates = self.get_random_coordinates()
            #If the generated coordinates are in the saved list of already attacked positions, new random coordinates are generated
            while coordinates in self.attacked_positions:
                coordinates = self.get_random_coordinates()
        #Overall the new_coordinates are stored in the self.previous_coordinates attribute and appended in the self.attacked_positions list
        self.previous_coordinates = coordinates
        self.attacked_positions.append(coordinates)
        return coordinates

    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive the result of the attack.

        Args:
            is_ship_hit (bool): True if ship was attacked, False if not
            has_ship_sunk (bool): True if ship has sunk, otherwise False
        """
        #If a ship has been hit and did not sink, implement the strategy_function
        if is_ship_hit and not has_ship_sunk:
            self.implement_strategy = True
            #In the case the self.save_ship_initial attribute is None, then update it using the self.previous_coordinates attribute
            if self.save_ship_initial == None:
                self.save_ship_initial = (self.previous_coordinates[0], self.previous_coordinates[1])
        #If the ship has sunk, do not implement the strategy_function, initiate self.cycle again and set self.save_ship_initial to None
        elif has_ship_sunk:
            self.implement_strategy = False
            self.cycle = 0
            self.save_ship_initial = None
        #In the case the strategy_function was executed but the ship was not hit, update self_cycle and  the self.previous_coordinates attribute
        #This ensures that once a ship was not hit following implementation of the strategy_function, the next attack will hit the ship 
        elif not is_ship_hit and self.implement_strategy and self.cycle < 4:
            self.cycle += 1
            self.previous_coordinates = (self.save_ship_initial[0], self.save_ship_initial[1])   

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)

    def strategy_function(self):
        """ Implement a strategy once a ship is attacked.

        Return:
            coordinates (tuple(int, int)): Return updated coordinates on which to launch the next attack
        """
        x, y = self.previous_coordinates
        #If self.cycle attribute is zero, move vertically up the board by 1 cell
        if self.cycle == 0:
            coordinates = (x, y+1)
            #This ensures the move happens within the bounds of the board
            if 0 < coordinates[0] <= self.board.width and 0 < coordinates[1] <= self.board.height:
                return coordinates
            #If it does not then perform another move ie, move horizontally by 1 cell
            else:
                self.cycle += 1
        #If self.cycle attribute is one, move horizontally east of the board by 1 cell
        if self.cycle == 1:
            coordinates = (x+1, y)
            #Check if new_coordinates are within the boundaries of the board
            if 0 < coordinates[0] <= self.board.width and 0 < coordinates[1] <= self.board.height:
                return coordinates
            else:
                self.cycle += 1
        #If self.cycle attribute is two, move vertically down the board by 1 cell
        if self.cycle == 2:
            coordinates = (x, y-1)
            #Check if new_coordinates are within the boundaries of the board
            if 0 < coordinates[0] <= self.board.width and 0 < coordinates[1] <= self.board.height:
                return coordinates
            else:
                self.cycle += 1
        #If self.cycle attribute is three, move horizontally west of the board by 1 cell
        if self.cycle == 3:
            coordinates = (x-1, y)
            #Check if new_coordinates are within the boundaries of the board
            if 0 < coordinates[0] <= self.board.width and 0 < coordinates[1] <= self.board.height:
                return coordinates
            #If none of the above moves are executed the reset self_cycle attribute to zero
            else:
                self.cycle = 0
