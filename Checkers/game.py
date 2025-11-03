import copy
from board import Board

class Game:
    def __init__(self):
        self._init()
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = 'white'
        self.valid_moves = {}
    
    def reset(self):
        self._init()
    
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False
    
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        
        return True
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == 'white':
            self.turn = 'red'
        else:
            self.turn = 'white'
    
    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board
        self.change_turn()
        
    def get_all_moves(self, color):
        moves = []
        for piece in self.board.get_all_pieces(color):
            valid_moves = self.board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                temp_board = copy.deepcopy(self.board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                moves.append(new_board)
        
        return moves
    
    def simulate_move(self, piece, move, board, skip):
        board.move(piece, move[0], move[1])
        if skip:
            board.remove(skip)
        
        return board
    
    def draw_board(self):
        self.board.draw()
    
    def winner(self):
        return self.board.winner()