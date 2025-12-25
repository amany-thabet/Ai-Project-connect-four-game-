# Ai-Project-connect-four-game-

This project is a full implementation of the classic Connect Four game using Python and Pygame. Play against an intelligent AI with a visually interactive interface.

📝 Project Overview

Connect Four is a turn-based board game where players drop colored pieces into a vertical grid. The goal is to connect four of your own pieces horizontally, vertically, or diagonally before your opponent does.

This implementation covers:

Board management using NumPy

Piece placement and valid move checking

Win detection (horizontal, vertical, diagonal)

Draw detection when no moves are left

Graphical interface using Pygame

🤖 AI Opponent

The AI uses the Minimax Algorithm with Alpha-Beta Pruning for strategic decision-making:

Minimax Algorithm: Recursively evaluates all possible moves and chooses the one that maximizes the AI’s chances of winning while minimizing the player’s chances.

Alpha-Beta Pruning: Skips unnecessary branches in the game tree to improve efficiency.

Heuristic Board Evaluation:

Scores sequences of four cells to detect winning opportunities or threats.

Blocks the opponent from winning.

Prefers central columns for better board control.

⚙️ Features

Human vs AI gameplay with alternating turns

Interactive GUI with colored pieces:

Yellow: Player

Red: AI

Black: Empty cells

Automatic win, loss, and draw detection

Smooth AI decision-making with adjustable difficulty (Minimax depth)

🧩 Code Structure

1. Board Management

create_new_board(): Creates an empty board

add_piece(): Adds a piece to the board

can_place_piece(), find_open_row(): Validates moves

2. Winning Check

winning(): Checks horizontal, vertical, and diagonal victories

3. AI Evaluation

check_four_cells(): Scores sequences of four cells

score_board(): Evaluates the board for AI decision-making

4. AI Decision Making

get_valid_locations(): Returns playable columns

is_terminal_node(): Checks for game over conditions

minimax(): Implements Minimax with Alpha-Beta pruning

5. GUI

draw_board(): Draws the board with colors for empty, player, and AI pieces

Handles mouse input and updates the display

6. Main Game Loop

Alternates turns between human and AI

Detects wins, losses, and draws

Automatically resets the board after each game

🎯 Learning Outcomes

Implementation of AI in games

Recursive algorithms and game tree search

Heuristic evaluation for strategic decision-making

Integrating logic with GUI for an interactive experience

📌 Optional Enhancements

Multiple AI difficulty levels by adjusting Minimax depth

Add animations and sound effects

Track cumulative scores across multiple games

Colors in GUI:

Color	Meaning
Yellow	Player pieces
Red	AI pieces
Black	Empty cells
Blue	Board background
White	Messages (win/draw)
