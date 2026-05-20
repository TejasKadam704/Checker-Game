import tkinter as tk

class CheckersGame:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Checkers Game")
        self.square_size = 60
        self.canvas = tk.Canvas(self.master, width=8*self.square_size, height=8*self.square_size)
        self.canvas.pack()

        self.game_started = False
        self.master.bind("<Return>", self.start_game)

        
        self.show_start_screen()
        

        self.master.mainloop()

    def show_start_screen(self):
        
        self.canvas.delete("all")
        self.canvas.create_text(240, 240, text="Press Enter to Start the Game", font=("Arial", 24), fill="black")

    def start_game(self,event):
        
        if not self.game_started:
            self.game_started = True
            self.board = self.initialize_board()
            self.current_player = 'w'
            self.selected_piece = None

            
            self.canvas.bind("<Button-1>", self.on_click)
            self.draw_board()

    def initialize_board(self):
        
        board = [[' ' for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:  # Alternating color for checkers
                    if row < 3:
                        board[row][col] = 'b'  # 'b' for black pieces
                    elif row > 4:
                        board[row][col] = 'w'  # 'w' for white pieces
        return board

    def draw_board(self):
        
        self.canvas.delete("all")
        colors = ["white", "grey"]
        for row in range(8):
            for col in range(8):
                x0, y0 = col*self.square_size, row*self.square_size
                x1, y1 = x0 + self.square_size, y0 + self.square_size
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")

                piece = self.board[row][col]
                if piece != ' ':
                    self.draw_piece(row, col, piece)

        if self.selected_piece:
            self.highlight_selected_piece(self.selected_piece)

    def draw_piece(self, row, col, piece):
        
        x0, y0 = col*self.square_size + 10, row*self.square_size + 10
        x1, y1 = x0 + self.square_size - 20, y0 + self.square_size - 20
        color = "white" if piece.lower() == 'w' else "black"
        self.canvas.create_oval(x0, y0, x1, y1, fill=color)
        
        if piece.isupper():
            self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text="K", font=("Arial", 24), fill="red")

    def highlight_selected_piece(self, position):
        
        row, col = position
        x0, y0 = col*self.square_size, row*self.square_size
        x1, y1 = x0 + self.square_size, y0 + self.square_size
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", width=3)

    def on_click(self, event):
        
        col = event.x // self.square_size
        row = event.y // self.square_size
        if self.selected_piece:
            start_row, start_col = self.selected_piece
            if (row, col) != (start_row, start_col):
                if self.move_piece(start_row, start_col, row, col):
                    self.current_player = 'b' if self.current_player == 'w' else 'w'
            self.selected_piece = None
        else:
            if self.board[row][col].lower() == self.current_player:
                self.selected_piece = (row, col)

        self.draw_board()
        self.check_game_over()

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        
        if (start_row < 0 or start_row >= 8 or start_col < 0 or start_col >= 8 or
            end_row < 0 or end_row >= 8 or end_col < 0 or end_col >= 8):
            return False
        if self.board[start_row][start_col] == ' ' or self.board[end_row][end_col] != ' ':
            return False
        if abs(start_row - end_row) not in (1, 2) or abs(start_col - end_col) not in (1, 2):
            return False
        
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        
        piece = self.board[start_row][start_col]
        if piece.lower() == 'w' and end_row >= start_row and not piece.isupper():
            return False
        if piece.lower() == 'b' and end_row <= start_row and not piece.isupper():
            return False
        return True

    def move_piece(self, start_row, start_col, end_row, end_col):
        if self.is_valid_move(start_row, start_col, end_row, end_col):
            
            if abs(start_row - end_row) == 2:  
                mid_row = (start_row + end_row) // 2
                mid_col = (start_col + end_col) // 2
                
                if self.board[mid_row][mid_col].lower() != self.current_player:
                    self.remove_piece(mid_row, mid_col)
                else:
                    return False  # Invalid move if trying to capture same color piece

            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = ' '
            if (end_row == 0 and self.board[end_row][end_col] == 'w') or (end_row == 7 and self.board[end_row][end_col] == 'b'):
                self.board[end_row][end_col] = self.board[end_row][end_col].upper() 
            return True
        return False

    def remove_piece(self, row, col):
        self.board[row][col] = ' '

    def check_game_over(self):
        white_pieces = sum(row.count('w') + row.count('W') for row in self.board)
        black_pieces = sum(row.count('b') + row.count('B') for row in self.board)
        if white_pieces == 0:
            self.display_winner("Black")
        elif black_pieces == 0:
            self.display_winner("White")

    def display_winner(self, winner):
        self.canvas.delete("all")
        self.canvas.create_text(240, 240, text=f"{winner} wins!", font=("Arial", 32), fill="green")
        self.canvas.create_text(240, 300, text="Press Enter to start a new game", font=("Arial", 16), fill="black")
        self.master.bind("<Return>", self.new_game)

    def new_game(self, event):
        self.board = self.initialize_board()
        self.current_player = 'w'
        self.selected_piece = None
        self.draw_board()

if __name__ == "main":
 game = CheckersGame()