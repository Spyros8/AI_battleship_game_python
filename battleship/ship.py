import random

from battleship.convert import CellConverter

class Ship:
    """ Represent a ship that is placed on the board.
    """
    def __init__(self, start, end):
        """ Creates a ship given its start and end coordinates on the board. 
        
        The order of the cells do not matter.

        Args:
            start (tuple[int, int]): tuple of 2 positive integers representing
                the starting cell coordinates of the Ship on the board
            end (tuple[int, int]): tuple of 2 positive integers representing
                the ending cell coordinates of the Ship on the board

        Raises:
            ValueError: if the ship is neither horizontal nor vertical
        """
        # Start and end (x, y) cell coordinates of the ship
        self.x_start, self.y_start = start
        self.x_end, self.y_end = end

        # make x_start on left and x_end on right
        self.x_start, self.x_end = min(self.x_start, self.x_end), max(self.x_start, self.x_end)
        
        # make y_start on top and y_end on bottom
        self.y_start, self.y_end = min(self.y_start, self.y_end), max(self.y_start, self.y_end)

        if not self.is_horizontal() and not self.is_vertical():
            raise ValueError("The given coordinates are invalid."
                "The ship needs to be either horizontal or vertical.")

        # Set of all (x,y) cell coordinates that the ship occupies
        self.cells = self.get_cells()
        
        # Set of (x,y) cell coordinates of the ship that have been damaged
        self.damaged_cells = set()
    
    def __len__(self):
        return self.length()
        
    def __repr__(self):
        return f"Ship(start=({self.x_start},{self.y_start}), end=({self.x_end},{self.y_end}))"
        
    def is_vertical(self):
        """ Check whether the ship is vertical.
        
        Returns:
            bool : True if the ship is vertical. False otherwise.
        """
        #If the starting and ending horizontal coordinates of the ship are equal then it is vertically aligned
        if self.x_start == self.x_end:
            return True
        #If not, then return False, as it is not vertically aligned
        return False
   
    def is_horizontal(self):
        """ Check whether the ship is horizontal.
        
        Returns:
            bool : True if the ship is horizontal. False otherwise.
        """
        #If the starting and ending vertical coordinates of the ship are equal then it is horizontally aligned
        if self.y_start == self.y_end:
            return True
        #If not, then return False as it is not horizontally aligned
        return False
    
    def get_cells(self):
        """ Get the set of all cell coordinates that the ship occupies.
        
        For example, if the start cell is (3, 3) and end cell is (5, 3),
        then the method should return {(3, 3), (4, 3), (5, 3)}.
        
        This method is used in __init__() to initialise self.cells
        
        Returns:
            set[tuple] : Set of (x ,y) coordinates of all cells a ship occupies
        """
        #First check if ship is horizontally aligned
        if self.is_horizontal():
            #Create an empty cells_set of type(set)
            cells_set = set()
            #For each x_coordinate occupied by the ship, create a tuple of its x and y coordinates and add it to the cells_set
            for x_coordinate in range(self.x_start, self.x_end + 1):
                cells_set.add((x_coordinate, self.y_start))
                #Return the cells_set for the horizontally aligned ship
            return cells_set

        #Check if the ship is vertically aligned
        elif self.is_vertical():
            #Create an empty cells_set of type(set)
            cells_set = set()
             #For each y_coordinate occupied by the ship, create a tuple of its x and y coordinates and add it to the cells_set
            for y_coordinate in range(self.y_start, self.y_end + 1):
                cells_set.add((self.x_start, y_coordinate))
                #Return the cells_set for the vertically aligned ship
            return cells_set

    def length(self):
        """ Get length of ship (the number of cells the ship occupies).
        
        Returns:
            int : The number of cells the ship occupies
        """
        #For a horizontally aligned ship return the integer length of the cells (type(set)) it occupies
        if self.is_horizontal():
            return int(len(self.cells))
        #For a vertically aligned ship return the integer length of the cells (type(set)) it occupies
        elif self.is_vertical():
            return(int(len(self.cells)))
        #In the case the ship is not vertical nor horizontal return zero
        return 0

    def is_occupying_cell(self, cell):
        """ Check whether the ship is occupying a given cell

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to check

        Returns:
            bool : return True if the given cell is one of the cells occupied 
                by the ship. Otherwise, return False
        """
        #check = cell in  self.cells
        #return check
        #Define the integer variables of the coordinates of the cell to check against
        check_x, check_y = cell
        #First check if the ship is horizontal and if so, if its y-coordinate is equal to that of the cell we are checking against (check_y)
        if self.is_horizontal() and self.y_start == check_y:
            #Iterate through all x-coordinates occupied by the ship and check if any of them are equal to that of the cell we are checking against (check_x)
            for x_coordinate in range(self.x_start, self.x_end + 1):
                if check_x == x_coordinate:
                    #Return True when the first x_coordinate equals that of the cell we are checking against
                    return True
            #Return False if none of the coordinates occupied by the ship is equal to that of the cell we are checking against
            return False
        #First check if the ship is vertical and if so, if its x-coordinate is equal to that of the cell we are checking against (check_x)
        elif self.is_vertical() and self.x_start == check_x:
            #Iterate through all y-coordinates occupied by the ship and check if any of them are equal to that of the cell we are checking against (check_y)
            for y_coordinate in range(self.y_start, self.y_end + 1):
                if check_y == y_coordinate:
                    #Return True when the first y_coordinate equals that of the cell we are checking against
                    return True
            #Return False if none of the coordinates occupied by the ship is equal to that of the cell we are checking against
            return False
    
    def receive_damage(self, cell):
        """ Receive attack at given cell. 
        
        If ship occupies the cell, add the cell coordinates to the set of 
        damaged cells. Then return True. 
        
        Otherwise return False.

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the cell coordinates that is damaged

        Returns:
            bool : return True if the ship is occupying cell (ship is hit). 
                Return False otherwise.
        """
        #Use the is_occupying_cell method to check if the cell we are checking agaist is occupied by the ship
        if self.is_occupying_cell(cell):
            #If this is True then, add the cell to the damaged_cells set
            self.damaged_cells.add(cell)
            return True
        #If the ship does not occupy the cell we are checking against, do not update the damaged_cells set and return False
        else:
            return False
    
    def count_damaged_cells(self):
        """ Count the number of cells that have been damaged.
        
        Returns:
            int : the number of cells that are damaged.
        """
        #Use the len function to get the integer number of cells of the ship, that have been damaged and return this value
        damaged_cells = len(self.damaged_cells)
        return damaged_cells
        
    def has_sunk(self):
        """ Check whether the ship has sunk.
        
        Returns:
            bool : return True if the ship is damaged at all its positions. 
                Otherwise, return False
        """
        #Use the .difference() method for sets to subtract the tuples present in the damaged_cells set from those present in the cells set of the ship
        #NOTE: len(self.cells) == len(self.damaged_cells) might be a better alternative 
        if len(self.cells.difference(self.damaged_cells)) == 0:
            #If the difference is zero, return True and the ship has sunk
            return True
        #If the difference between the two sets is non-zero then the ship is still floating, and return False
        else:
            return False
    
    def is_near_ship(self, other_ship):
        """ Check whether a ship is near another ship instance.
        
        Hint: Use the method is_near_cell(...) to complete this method.

        Args:
            other_ship (Ship): another Ship instance against which to compare

        Returns:
            bool : returns True if and only if the coordinate of other_ship is 
                near to this ship. Returns False otherwise.
        """  
        assert isinstance(other_ship, Ship)
        
        #Iterate through all the cells occupied by the other_ship instance
        for cell in other_ship.cells:
            #Check if any of the cells of the other_ship are close to those of the current ship
            if self.is_near_cell(cell):
                #When this is True, return True meaning the current ship is near the other_ship
                return True 
        #If none of the cells occupied by the other ship are near to those of the current ship, return False      
        return False

    def is_near_cell(self, cell):
        """ Check whether the ship is near an (x,y) cell coordinate.

        In the example below:
        - There is a ship of length 3 represented by the letter S.
        - The positions 1, 2, 3 and 4 are near the ship
        - The positions 5 and 6 are NOT near the ship

        --------------------------
        |   |   |   |   | 3 |   |
        -------------------------
        |   | S | S | S | 4 | 5 |
        -------------------------
        | 1 |   | 2 |   |   |   |
        -------------------------
        |   |   | 6 |   |   |   |
        -------------------------

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to compare

        Returns:
            bool : returns True if and only if the (x, y) coordinate is at most
                one cell from any part of the ship OR is at the corner of the ship. Returns False otherwise.
        """
        #First check if the ship is horizontal
        if self.is_horizontal():
            #Iterate through all tuples of coordinates that the ship occupies
           for coordinates in self.cells:
               #Check if the current coordinates are close to the cell being checked against or overlapping it. If so, return True
               if ((coordinates[0] - 1 <= cell[0] <= coordinates[0] + 1) and (coordinates[1] - 1  <= cell[1] <= coordinates[1] + 1)):
                   return True
               else:
                   pass
            #Return False for the case, a horizontal ship's coordinates are not close or do not overlap those of the cell being checked against
           return False
        #First check if the ship is vertical  
        if self.is_vertical():
            #Iterate through all tuples of coordinates that the ship occupies
            for coordinates in self.cells:
                #Check if the current coordinates are close to the cell being checked against or overlapping it. If so, return True
               if ((coordinates[0] - 1 <= cell[0] <= coordinates[0] + 1) and (coordinates[1] - 1  <= cell[1] <= coordinates[1] + 1)): 
                   return True
               else:
                    pass
            #Return False for the case, a horizontal ships coordinates are not close or do not overlap that of the cell being checked against
            return False
            #NOTE: This is the initial code returned: return(self.x_start-1 <= cell[0] <= self.x_end+1 and self.y_start -1 <= cell[1] <= self.y_end +1)

class ShipFactory:
    """ Class to create new ships in specific configurations."""
    def __init__(self, board_size=(10,10), ships_per_length=None):
        """ Initialises the ShipFactory class with necessary information.
        
        Args: 
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)
            ships_per_length (dict): A dict with the length of ship as keys and
                the count as values. Defaults to 1 ship each for lengths 1-5.
        """
        self.board_size = board_size
        
        if ships_per_length is None:
            # Default: lengths 1 to 5, one ship each
            self.ships_per_length = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        else:
            self.ships_per_length = ships_per_length

    @classmethod
    def create_ship_from_str(cls, start, end, board_size=(10,10)):
        """ A class method for creating a ship from string based coordinates.
        
        Example usage: ship = ShipFactory.create_ship_from_str("A3", "C3")
        
        Args:
            start (str): starting coordinate of the ship (example: 'A3')
            end (str): ending coordinate of the ship (example: 'C3')
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)

        Returns:
            Ship : a Ship instance created from start to end string coordinates
        """
        converter = CellConverter(board_size)
        return Ship(start=converter.from_str(start),
                    end=converter.from_str(end))

    def generate_ships(self):
        """ Generate a list of ships in the appropriate configuration.
        
        The number and length of ships generated must obey the specifications 
        given in self.ships_per_length.
        
        The ships must also not overlap with each other, and must also not be too close to one another (as defined earlier in Ship::is_near_ship())
        
        The coordinates should also be valid given self.board_size
        
        Returns:
            list[Ships] : A list of Ship instances, adhering to the rules above
        """
        #import random
        from random import randrange

        #Initialise parameters. The width and height of the board and the ships list
        width, height = self.board_size
        ships = []
        
        #Iterate through the length of all ships. This must be an integer
        for length in self.ships_per_length:
            #Iterates through the number of ships of given length
            for number in range(1, self.ships_per_length[length] + 1):               
                #This first dummy variable will help in initiating the start and end coordinates of each ship instance to be created
                dummy_variable = True
                #Enter a while loop until the randomly generated start and end coordinates ensure that the ship is either horizontal or vertical
                while dummy_variable:
                    #Use the random.randrange (module.function) to randomly initialise start coordinates within the boundaries of the board
                    start_coordinate = (random.randrange(1, width + 1), random.randrange(1, height + 1))
                    #create the end_coordinate for the case the ship is horizontal
                    is_horizontal = random.choice([0, 1])
                    if is_horizontal:
                        end_coordinate = (start_coordinate[0]+ length - 1, start_coordinate[1])
                    #If the ship is not horizontal then create its end coordinate for the case it's vertical
                    else:
                        end_coordinate = (start_coordinate[0], start_coordinate[1]+ length - 1)
                    #This statement ensures the created ship is within the bounds of the board
                    if not (width >= end_coordinate[0] > 0 and height >= end_coordinate[1] > 0):
                        continue
                    #Create the ship instance after having worked through the above conditional statements
                    new_ship = Ship(start_coordinate, end_coordinate)
                    #For the list of ships, in the case the list is not empty, set the dummy_variable to False
                    if len(ships) != 0:
                        dummy_variable = False
                        #Iterate through all other ships in the list
                        for ship in ships:
                            #When one ship is found to be near the newly created ship, dummy variable is set to True and the for loop is broken
                            #This then carries on while loop until a new_ship which is not close to any ships in the ships list is created above
                            dummy_variable = ship.is_near_ship(new_ship)
                            if dummy_variable:
                                break
                        #When dummy variable is false for all ships in the list, the new ship is appended, as it is not near to any of them. As a result, the while loop is exited
                        if not dummy_variable:
                            ships.append(new_ship)
                            dummy_variable = False
                    #This conditional statement is for the first ship instance that is created
                    else:
                        ships.append(new_ship)
                        dummy_variable = False
        return ships
        
if __name__ == '__main__':
    # SANDBOX for you to play and test your methods

    ship = Ship(start=(3, 3), end=(5, 3))
    print(ship.get_cells())
    print(ship.length())
    print(ship.is_horizontal())
    print(ship.is_vertical())
    print(ship.is_near_cell((5, 3)))
    
    print(ship.receive_damage((4, 3)))
    print(ship.receive_damage((10, 3)))
    print(ship.damaged_cells)
    
    ship2 = Ship(start=(4, 1), end=(4, 5))
    print(ship.is_near_ship(ship2))

    # For Task 3
    ships = ShipFactory().generate_ships()
    print(ships)
        
    