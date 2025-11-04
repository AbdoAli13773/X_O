#!/usr/bin/env python3
"""
Console Tic-Tac-Toe (X O)
- Modes: Human vs Human, Human vs Computer
- Difficulty: easy / medium / hard (Minimax)
- Run: python main.py
"""
import random
from typing import List, Optional, Tuple

WIN_COMBINATIONS = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]

def print_board(board: List[str]):
    def cell(i):
        return board[i] if board[i] != ' ' else str(i+1)
    print()
    print(f" {cell(0)} | {cell(1)} | {cell(2)} ")
    print("---+---+---")
    print(f" {cell(3)} | {cell(4)} | {cell(5)} ")
    print("---+---+---")
    print(f" {cell(6)} | {cell(7)} | {cell(8)} ")
    print()

def check_winner(board: List[str]) -> Optional[str]:
    for (a,b,c) in WIN_COMBINATIONS:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None

def is_full(board: List[str]) -> bool:
    return all(c != ' ' for c in board)

def available_moves(board: List[str]) -> List[int]:
    return [i for i, c in enumerate(board) if c == ' ']

def evaluate_board(board: List[str]) -> Optional[str]:
    return check_winner(board)

def minimax(board: List[str], depth: int, maximizing: bool, ai_player: str, human_player: str) -> Tuple[int, Optional[int]]:
    winner = evaluate_board(board)
    if winner == ai_player:
        return (10 - depth, None)
    elif winner == human_player:
        return (depth - 10, None)
    elif all(c != ' ' for c in board):
        return (0, None)

    if maximizing:
        best_score = -999
        best_move = None
        for move in available_moves(board):
            board[move] = ai_player
            score, _ = minimax(board, depth+1, False, ai_player, human_player)
            board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)
    else:
        best_score = 999
        best_move = None
        for move in available_moves(board):
            board[move] = human_player
            score, _ = minimax(board, depth+1, True, ai_player, human_player)
            board[move] = ' '
            if score < best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)

def human_turn(board: List[str], marker: str):
    moves = available_moves(board)
    while True:
        try:
            choice = input(f"Player {marker}, enter move (1-9): ").strip()
            if choice.lower() in ('q','quit','exit'):
                print("Exiting game.")
                exit(0)
            idx = int(choice) - 1
            if idx in moves:
                board[idx] = marker
                return
            else:
                print("Invalid move — choose an empty cell number (1-9).")
        except ValueError:
            print("Please enter a number between 1 and 9, or 'q' to quit.")

def computer_turn(board: List[str], ai: str, human: str, difficulty: str):
    moves = available_moves(board)
    if difficulty == 'easy':
        move = random.choice(moves)
    elif difficulty == 'medium':
        if random.random() < 0.6:
            _, move = minimax(board[:], 0, True, ai, human)
            if move is None:
                move = random.choice(moves)
        else:
            move = random.choice(moves)
    else:  # hard
        _, move = minimax(board[:], 0, True, ai, human)
        if move is None:
            move = random.choice(moves)
    board[move] = ai
    print(f"Computer ({ai}) plays position {move+1}.")

def choose_mode() -> str:
    while True:
        print("Choose mode: 1) Human vs Computer   2) Human vs Human")
        c = input("Enter 1 or 2: ").strip()
        if c == '1':
            return 'HvC'
        if c == '2':
            return 'HvH'
        print("Invalid choice.")

def choose_marker() -> str:
    while True:
        c = input("Choose your marker (X or O) [default X]: ").strip().upper()
        if c == '':
            return 'X'
        if c in ('X','O'):
            return c
        print("Invalid choice.")

def choose_difficulty() -> str:
    while True:
        print("Difficulty: 1) easy  2) medium  3) hard")
        c = input("Enter 1,2 or 3 [default 3]: ").strip()
        if c == '' or c == '3':
            return 'hard'
        if c == '1':
            return 'easy'
        if c == '2':
            return 'medium'
        print("Invalid choice.")

def play_game():
    print("=== Tic-Tac-Toe (Console) ===")
    while True:
        mode = choose_mode()
        human_marker = 'X'
        difficulty = 'hard'
        if mode == 'HvC':
            human_marker = choose_marker()
            difficulty = choose_difficulty()
            ai_marker = 'O' if human_marker == 'X' else 'X'
        else:
            ai_marker = None

        board = [' '] * 9
        current = 'X'

        print_board(board)
        while True:
            if mode == 'HvH':
                print(f"Current: {current}")
                human_turn(board, current)
            else:  # HvC
                if current == human_marker:
                    human_turn(board, current)
                else:
                    computer_turn(board, ai_marker, human_marker, difficulty)

            print_board(board)
            winner = check_winner(board)
            if winner:
                print(f"Player {winner} wins!")
                break
            if is_full(board):
                print("It's a tie!")
                break
            current = 'O' if current == 'X' else 'X'

        again = input("Play again? (y/n) [y]: ").strip().lower()
        if again == '' or again.startswith('y'):
            continue
        else:
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_game()
