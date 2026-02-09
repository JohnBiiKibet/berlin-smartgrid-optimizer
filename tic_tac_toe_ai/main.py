from fastapi import FastAPI
from game import create_board, display_board, is_winner, is_board_full, ai_move, make_move

app = FastAPI(title="Tic-Tac-Toe AI API", version="0.1.0")
current_board = create_board()
current_player = 'X' # Player 'X' starts

@app.get("/")
def home():
    return {"status": "Tic-Tac-Toe API Online"}

@app.get("/board")
def get_board():
    return {"board": current_board}

@app.post("/move/{move}")
def make_player_move(move: int):
    global current_board, current_player
    if 0 <= move < 9 and current_board[move] == ' ':
        make_move(current_board, move, current_player)
        if is_winner(current_board, current_player):
            return {"status": f"Player {current_player} wins!", "board": current_board}
        elif is_board_full(current_board):
            return {"status": "It's a tie!", "board": current_board}
        else:
            # AI makes a move
            ai_choice = ai_move(current_board)
            make_move(current_board, ai_choice, 'O')
            if is_winner(current_board, 'O'):
                 return {"status": "AI wins!", "board": current_board}
            elif is_board_full(current_board):
                return {"status": "It's a tie!", "board": current_board}
            return {"status": "AI made a move", "board": current_board}
    return {"status": "Invalid move", "board": current_board}

@app.post("/reset")
def reset_game():
    global current_board, current_player
    current_board = create_board()
    current_player = 'X'
    return {"status": "Game reset", "board": current_board}

