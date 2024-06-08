import tkinter as tk
from tkinter import messagebox
import Engine

SIZE = 16
BOARD_DATA = Engine.make_empty_board(SIZE)

class CaroGame:
    def __init__(self, root, board_size=SIZE):
        self.root = root
        self.root.title("Caro Game")
        self.board_size = board_size
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'O'
        self.play_with_cpu = True
        self.buttons = []
        self.winning_cells = set()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        self.options_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Options", menu=self.options_menu)
        self.menu.add_command(label="Reset", command=self.reset_game)
        self.menu.add_command(label="Info", command=self.info)

        self.options_menu.add_command(label="Play with CPU", command=lambda: self.set_mode(True))
        self.options_menu.add_command(label="Play with Human", command=lambda: self.set_mode(False))
        

        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                button = self.create_button(frame, i, j)
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
    
    def info(self):
        messagebox.showinfo("Info", "Author: Tran Hao Phong")

    def create_button(self, frame, i, j):
        return tk.Button(frame, width=3, height=1, font=('Helvetica', '17'), command=lambda: self.click(i, j))

    def set_mode(self, play_with_cpu):
        self.play_with_cpu = play_with_cpu
        self.reset_game()

    def click(self, i, j):
        if self.board[i][j] == '':
            self.board[i][j] = self.current_player
            self.update_button(i, j)
            if self.check_winner(i, j):
                self.highlight_winning_cells()
                messagebox.showinfo("Caro Game", f"Player {self.current_player} wins!")
                self.reset_game()
            else:
                self.switch_player()
                if self.play_with_cpu and self.current_player == 'X':
                    self.cpu_move()

    def update_button(self, i, j):
        self.clear_highlight()
        self.buttons[i][j].config(bg='yellow', text=self.current_player, fg='blue' if self.current_player == 'O' else 'red')
        if self.current_player == 'X':
            BOARD_DATA[i][j]='b'
        else:
            BOARD_DATA[i][j]='w'

    def switch_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def cpu_move(self):
        empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] == '']
        if empty_cells:
            i, j = Engine.best_move(BOARD_DATA, 'w') 
            self.board[i][j] = self.current_player
            self.update_button(i, j)
            if self.check_winner(i, j):
                self.highlight_winning_cells()
                messagebox.showinfo("Caro Game", f"Player {self.current_player} wins!")
                self.reset_game()
            else:
                self.switch_player()


    def check_winner(self, x, y):
        return (self.check_direction(x, y, 1, 0) or
                self.check_direction(x, y, 0, 1) or
                self.check_direction(x, y, 1, 1) or
                self.check_direction(x, y, 1, -1))

    def check_direction(self, x, y, dx, dy):
        count = 1
        winning_cells = [(x, y)]
        for d in [1, -1]:
            nx, ny = x + d*dx, y + d*dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == self.current_player:
                count += 1
                winning_cells.append((nx, ny))
                nx += d*dx
                ny += d*dy
        if count >= 5:
            self.winning_cells.update(winning_cells)
            return True
        return False

    def highlight_winning_cells(self):
        for i, j in self.winning_cells:
            self.buttons[i][j].config(bg='yellow')

    def reset_game(self):
        global BOARD_DATA
        BOARD_DATA = Engine.make_empty_board(SIZE)
        self.clear_highlight()
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'O'
        self.winning_cells.clear()
        for row in self.buttons:
            for button in row:
                button.config(text='', state="normal")

    def clear_highlight(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].config(bg='SystemButtonFace')

if __name__ == "__main__":
    root = tk.Tk()
    game = CaroGame(root)
    root.mainloop()