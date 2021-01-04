# Author: Nathaniel Moore
# Date: 11/25/2020
# Description: Focus Game. Program classes and behaviors so that players can play the game focus. There will be a 6x6
# board initialized XXOOXX/OOXXOO... etc starting at the upper left (0,0) horizontally. Finishing at the bottom
# right (5,5). Represented (row,column). Pieces can be stacked on top of each other and can be moved vertically or
# horizontally but never diagonal. A piece may be moved if the player who's turn it is (player) has their piece on top.
# The pieces can be moved up to the number of spaces equivalent to the pieces in the stack. The maximum pieces in a
# stack is 5 pieces. By moving pieces to make more than 5 in a stack the player will remove pieces from the bottom of
# the stack. If they are (player)'s pieces they get kept in reserve and can be played later. If they are the
# other players (opponent) pieces they will be captured. The game is won by the first player to capture 6 pieces.

class Board:
    '''represents a board as a list of lists. Has a method for filling the board and a method for returning the
    pieces at any given location on the board. '''
    def __init__(self):
        self._board = []

    def get_board(self):
        return self._board
    def print_board(self):
        print (self._board)
    def fill_board(self):
        '''Initialize board by filling self._board with lists with x,y coords and empty strings'''
        for x in range (6):
            for y in range (6):
                newlist = [x, y]
                self._board.append(newlist)

    def show__pieces(self, x_y_tuple):
        '''called by show_pieces method of FocusGame class. Returns what pieces are in a coordinate'''
        for sub in self._board:
            if sub[0] == x_y_tuple[0] and sub[1] == x_y_tuple[1]:
                return (sub[2:])

    def update_pieces(self, x_y_tuple, pieces):
        '''update what pieces are in a given location by modifying the corresponding sublist. For testing'''
        for sub in self._board:
            if sub[0] == x_y_tuple[0] and sub[1] == x_y_tuple[1]:
                sub[2:] = pieces

class Player:
    '''create a player object that takes a name and color and keeps track of reserve and captured pieces'''
    def __init__(self, name, color):
        self._name = name
        self._color = color
        self._captured = 0
        self._reserved = 0

    def get_name(self):
        return self._name
    def get_color(self):
        return self._color
    def get_captured(self):
        return self._captured
    def get_reserved(self):
        return self._reserved
    def update_captured(self, pieces):
        '''takes number of pieces to update captured'''
        self._captured += pieces

    def update_reserved(self, pieces):
        '''takes number of pieces to update reserved'''
        self._reserved += pieces

class FocusGame:
    '''Main class for game. Initializes a board from the Board class via composition.  Has methods for moving a piece,
     showing pieces in a given coordinate, showing pieces in a players reserve, showing pieces captured by a player,
     and using a reserve piece with a move'''
    def __init__(self, playerA, playerB):
        '''Takes 2 tuples as arguments. initializes player A/B and their respective colors'''
        self._playerA = Player(playerA[0], playerA[1])
        self._playerB = Player(playerB[0], playerB[1])
        self._A_color = playerA[1]
        self._B_color = playerB[1]
        self._turn = None
        self._board = Board()
        self._board.fill_board()
        self.starting_pieces()

    def get_colorA(self):
        return self._A_color
    def get_colorB(self):
        return self._B_color
    def get_playerA(self):
        return self._playerA
    def get_playerB(self):
        return self._playerB

    def starting_pieces(self):
        '''add starting pieces to board coordinates'''
        for sub in self._board.get_board():
            if sub[0] == 0 or sub[0] == 2 or sub[0] == 4:
                if sub[1] == 0 or sub[1] == 1 or sub[1] == 4 or sub[1] == 5:
                    sub.append(self.get_colorA())
                else:
                    sub.append(self.get_colorB())
            if sub[0] == 1 or sub[0] == 3 or sub[0] == 5:
                if sub[1] == 0 or sub[1] == 1 or sub[1] == 4 or sub[1] == 5:
                    sub.append(self.get_colorB())
                else:
                    sub.append(self.get_colorA())

    def get_coord(self, coord):
        '''returns a sublist corresponding to the coordinate'''
        for sub in self._board.get_board():
            if sub[0] == coord[0] and sub[1] == coord[1]:
                return sub

    def get_player(self, name):
        '''returns player object corresponding to name string'''
        if self._playerA.get_name() == name:
            return self._playerA
        if self._playerB.get_name() == name:
            return self._playerB

    def check_5(self, player, coord):
        '''called at the end of move_piece. Handles >5 pieces in a location and returns message for win or
        successful move'''
        sub = self.get_coord(coord)             #retrieve sublist corresponding to coordinate
        while len(sub[2:]) > 5:
            piece = sub.pop(2)                  #remove piece from bottom and save it as piece variable.
            if piece == player.get_color():
                player.update_reserved(1)
            else:
                player.update_captured(1)
        if player == self._playerA:
            self._turn = self._playerB         #set player turn to next player
        if player == self._playerB:
            self._turn = self._playerA
        if player.get_captured() > 5:
            return player.get_name() + ' Wins'
        else:
            return 'successfully moved'

    def check_valid(self, coordSource, coordDest, move):
        '''takes coordinates and number of spaces moved and returns false if outside of game parameters'''
        if coordSource[0] < 0 or coordSource [0] > 5:
            return False
        if coordSource[1] < 0 or coordSource[1] > 5:
            return False
        if coordDest[0] < 0 or coordDest [0] > 5:
            return False
        if coordDest[1] < 0 or coordDest[1] > 5:
            return False
        if abs(coordSource[0]-coordDest[0]) > move:     #check if coords match move
            return False
        if abs(coordSource[1]-coordDest[1]) > move:
            return False
        if coordSource[0] != coordDest[0] and coordSource[1] != coordDest[1]: #check for diagonal movement
            return False

    def move_piece(self, name, coordSource, coordDest, move):
        '''Takes a player and a coordinate for the move. update Board class by calling update_pieces. Returns error
        message if out of turn, invalid location or invalid pieces. Returns "successfully moved" if move was legal.
        Evaluates win conditions and returns win message ("Player Wins"). Handles capture/reserve when 5 or more
        pieces are in the intended location.'''
        player = self.get_player(name)
        source = self.get_coord(coordSource)
        dest = self.get_coord(coordDest)

        if self.check_turn(player) == False:
            return False
        if self.check_valid(coordSource,coordDest, move) == False:
            return False
        if move > len(source[2:]):  # check if enough pieces are available for move
            return False
        else:
            for piece in source[-move:]:
                dest.append(piece)
            for piece in source[-move:]:
                source.remove(piece)
            return self.check_5(player, coordDest)

    def show_pieces(self, coord):
        '''takes a coordinate and returns the pieces at that coordinate from bottom to top'''
        return self._board.show__pieces(coord)

    def show_reserve(self, name):
        '''takes a player name and returns the count of pieces in reserve. Returns 0 if no pieces'''
        return self.get_player(name).get_reserved()

    def show_captured(self, name):
        ''' takes player name and shows count of pieces captured. returns 0 if none'''
        return self.get_player(name).get_captured()

    def reserved_move(self, name, coord):
        '''takes player name and location on the board. Places a piece on the coordinates. Reduces player
        reserve by one. Handle more than 5 pieces. returns "no pieces in reserve" if there are no pieces.'''
        player = self.get_player(name)
        dest = self.get_coord(coord)
        if self.check_turn(player) == False:
            return False
        if player.get_reserved() <1:
            return False
        if coord[0] < 0 or coord[0] > 5 or coord[1] < 0 or coord[1] > 5:
            return False
        else:
            dest.append(player.get_color())
            player.update_reserved(-1)
            return self.check_5(player, coord)

    def check_turn(self, player):
        '''test player turn'''
        if self._turn == None:
            return True
        if self._turn == player:
            return True
        else: return False


# test1 = FocusGame(('Nate', 'R'),('Ash', 'G'))
# print(test1.move_piece('Nate', (0,0), (0,1), 1))
# print(test1.move_piece('Ash', (0,2), (0,3), 1))
# print(test1.move_piece('Nate', (0,1),(0,3), 2))
# print(test1.move_piece('Ash', (0,3), (0, 4), 4))
# print(test1.move_piece('Nate', (5,5), (5,4), 1))
# print(test1.show_pieces((0,4)))
# test1._playerB.update_reserved(3)
# print(test1.reserved_move('Ash',(0,4)))
# print(test1.show_reserve('Ash'))
# print(test1.show_pieces((0,4)))
# print(test1.show_captured('Ash'))
# print(test1.show_pieces((0,0)))
# board = Board()
# board.fill_board()
# board.update_pieces((0,0), [5,1])
# board.print_board()
# board.show__pieces((0,0))


# Scenarios:
#
# Initialize the board:
#
#	FocusGame object will create a Board object when it is initialized.  The Board object will have
# a method that fills the list of lists representing the board. That method will be called when
# FocusGame is initialized.
#
# Determine how to represent multiple pieces at a given location on the board:
#
#	Each location will be an object represented by a key/dictionary in the Board class. Each
# location object will have a pieces data member which is a list of pieces from bottom to top.
#
# Determine how to make moves: (single, multi, reserve)
#
#	The make_move and reserve_move methods will call methods in the Board and Player objects
# to update the state of the board/player and evaluate win conditions.
#
# Remember captured and reserved pieces for each player:
#
#	Player object will have data members/methods for keeping track of pieces.
#
# Determine how to track which players turn it is:
#
#	make_move and reserve_move methods will call player_turn method to evaluate who’s turn it
# is.
#
# Determine how to handle >5 pieces:
#
#	make_move and reserve_move will call action_5 method to handle scenario.


# game = FocusGame(('PlayerA', 'R'),('PlayerB', 'G'))


