#!/usr/bin/env python3
"""
Tic-Tac-Toe with GUI (Tkinter)
Features:
- Human vs Human and Human vs Computer
- Difficulty levels: easy / medium / hard (Minimax)
- Clear board buttons, status label, restart, mode/difficulty controls
- Single-file, standard-library only (Tkinter)
Run: python tic_tac_toe_gui.py
"""

import tkinter as tk
from tkinter import messagebox
import random
from typing import List, Optional, Tuple

WIN_COMBINATIONS = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]

class TicTacToeGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title('Tic-Tac-Toe (X O)')
        master.resizable(False, False)

        self.board: List[str] = [' '] * 9
        self.buttons: List[tk.Button] = []
        self.current_player = 'X'  # X always starts

        # Game options
        self.mode_var = tk.StringVar(value='HvC')  # HvH or HvC
        self.marker_var = tk.StringVar(value='X')  # human marker when HvC
        self.difficulty_var = tk.StringVar(value='hard')

        # Top frame: options
        opts = tk.Frame(master)
        opts.grid(row=0, column=0, padx=8, pady=6)

        tk.Label(opts, text='Mode:').grid(row=0, column=0, sticky='w')
        tk.Radiobutton(opts, text='Human vs Computer', variable=self.mode_var, value='HvC', command=self.reset_board).grid(row=0, column=1, sticky='w')
        tk.Radiobutton(opts, text='Human vs Human', variable=self.mode_var, value='HvH', command=self.reset_board).grid(row=0, column=2, sticky='w')

        tk.Label(opts, text='Your Marker:').grid(row=1, column=0, sticky='w')
        tk.Radiobutton(opts, text='X', variable=self.marker_var, value='X', command=self.reset_board).grid(row=1, column=1, sticky='w')
        tk.Radiobutton(opts, text='O', variable=self.marker_var, value='O', command=self.reset_board).grid(row=1, column=2, sticky='w')

        tk.Label(opts, text='Difficulty:').grid(row=2, column=0, sticky='w')
        tk.OptionMenu(opts, self.difficulty_var, 'easy', 'medium', 'hard', command=lambda _: self.reset_board()).grid(row=2, column=1, columnspan=2, sticky='we')

        # Status
        self.status_label = tk.Label(master, text="Current: X", font=('Arial', 12))
        self.status_label.grid(row=1, column=0, pady=(0,6))

        # Board frame
        board_frame = tk.Frame(master)
        board_frame.grid(row=2, column=0, padx=8, pady=6)

        for i in range(9):
            b = tk.Button(board_frame, text=' ', width=6, height=3, font=('Arial', 18), command=lambda i=i: self.on_click(i))
            r = i // 3
            c = i % 3
            b.grid(row=r, column=c, padx=2, pady=2)
            self.buttons.append(b)

        # Bottom controls
        controls = tk.Frame(master)
        controls.grid(row=3, column=0, pady=(6,8))
        self.restart_btn = tk.Button(controls, text='Restart', command=self.reset_board)
        self.restart_btn.grid(row=0, column=0, padx=4)
        self.quit_btn = tk.Button(controls, text='Quit', command=master.quit)
        self.quit_btn.grid(row=0, column=1, padx=4)

        self.reset_board()

    def reset_board(self, *_):
        self.board = [' '] * 9
        for b in self.buttons:
            b.config(text=' ', state='normal')
        self.current_player = 'X'
        self.status_label.config(text=f'Current: {self.current_player}')

        # If HvC and computer is X, make first move
        if self.mode_var.get() == 'HvC' and self.human_marker() != 'X':
            self.master.after(300, self.computer_move)

    def human_marker(self) -> str:
        return self.marker_var.get()

    def ai_marker(self) -> str:
        return 'O' if self.human_marker() == 'X' else 'X'

    def on_click(self, index: int):
        if self.board[index] != ' ':
            return
        if self.mode_var.get() == 'HvC' and self.current_player != self.human_marker():
            return

        self.make_move(index, self.current_player)
        self.update_ui()

        winner = self.check_winner()
        if winner or self.is_full():
            self.end_game(winner)
            return

        self.toggle_player()
        self.update_ui()

        if self.mode_var.get() == 'HvC' and self.current_player != self.human_marker():
            self.master.after(200, self.computer_move)

    def make_move(self, index: int, player: str):
        self.board[index] = player
        self.buttons[index].config(text=player)

    def update_ui(self):
        self.status_label.config(text=f'Current: {self.current_player}')

    def toggle_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self) -> Optional[str]:
        for (a,b,c) in WIN_COMBINATIONS:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != ' ':
                return self.board[a]
        return None

    def is_full(self) -> bool:
        return all(c != ' ' for c in self.board)

    def end_game(self, winner: Optional[str]):
        if winner:
            msg = f'Player {winner} wins!'
        else:
            msg = 'Its a tie!'

        # Disable buttons and highlight winning combo
        for i, b in enumerate(self.buttons):
            b.config(state='disabled')

        # Show messagebox and offer restart
        messagebox.showinfo('Game Over', msg)
        # After game over, allow restart

    # ---------------- AI / Minimax ----------------
    def available_moves(self) -> List[int]:
        return [i for i, c in enumerate(self.board) if c == ' ']

    def minimax(self, board: List[str], depth: int, maximizing: bool, ai_player: str, human_player: str) -> Tuple[int, Optional[int]]:
        winner = self.evaluate_board(board)
        if winner == ai_player:
            return (10 - depth, None)
        elif winner == human_player:
            return (depth - 10, None)
        elif all(c != ' ' for c in board):
            return (0, None)

        if maximizing:
            best_score = -999
            best_move = None
            for move in [i for i, c in enumerate(board) if c == ' ']:
                board[move] = ai_player
                score, _ = self.minimax(board, depth+1, False, ai_player, human_player)
                board[move] = ' '
                if score > best_score:
                    best_score = score
                    best_move = move
            return (best_score, best_move)
        else:
            best_score = 999
            best_move = None
            for move in [i for i, c in enumerate(board) if c == ' ']:
                board[move] = human_player
                score, _ = self.minimax(board, depth+1, True, ai_player, human_player)
                board[move] = ' '
                if score < best_score:
                    best_score = score
                    best_move = move
            return (best_score, best_move)

    def evaluate_board(self, board: List[str]) -> Optional[str]:
        for (a,b,c) in WIN_COMBINATIONS:
            if board[a] == board[b] == board[c] and board[a] != ' ':
                return board[a]
        return None

    def computer_move(self):
        difficulty = self.difficulty_var.get()
        moves = self.available_moves()
        ai = self.ai_marker()
        human = self.human_marker()

        if difficulty == 'easy':
            move = random.choice(moves)
            self.make_move(move, ai)
        elif difficulty == 'medium':
            if random.random() < 0.6:
                _, move = self.minimax(self.board[:], 0, True, ai, human)
                if move is None:
                    move = random.choice(moves)
            else:
                move = random.choice(moves)
            self.make_move(move, ai)
        else:  # hard
            _, move = self.minimax(self.board[:], 0, True, ai, human)
            if move is None:
                move = random.choice(moves)
            self.make_move(move, ai)

        self.update_ui()
        winner = self.check_winner()
        if winner or self.is_full():
            self.end_game(winner)
            return
        self.toggle_player()
        self.update_ui()


if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
