import sys
import time 

case = sys.argv[1]

def move(board,current_player,move):
    if board[move] != ".":
        return board
    else:
        return board[:move] + current_player + board[move+1:]

def possible_next_boards(board, current_player):
    boards = [] 
    for s in range (0,len(board)):
        if board[s] == ".":
            boards.append(board[:s] + current_player + board[s+1:])
    return boards

def gameover(board):
    if "." not in board:
        return True
    for i in range (0,9,3):
        if board[i] == board[i+1] == board[i+2] and (board[i] == "X" or board[i] == "O"):
            return True
    for i in range (0,3):
        if board[i] == board[i+3] == board[i+6] and (board[i] == "X" or board[i] == "O"):
            return True
    if (board[0] == board[4] == board[8] or board[2] == board[4] == board[6])and (board[4] == "X" or board[4] == "O"):
        return True
    return False

def score(board):
    for i in range (0,9,3):
        if board[i] == board[i+1] == board[i+2]:
            if board[i] == "X":
                return -1
            elif board[i] == "O":
                return 1
    for i in range (0,3):
        if board[i] == board[i+3] == board[i+6]:
            if board[i] == "X":
                return -1
            elif board[i] == "O":
                return 1
    if board[0] == board[4] == board[8] or board[2] == board[4] == board[6]:
        if board[4] == "X":
                return -1
        elif board[4] == "O":
                return 1
    if "." not in board:
        return 0 
    return None 

def board_print(board):
    s = ""
    for x in range (0,3):
        s = s + board[3*x] + board[3*x+1] + board[3*x+2] + "\n"
    print(s)

def max_step(board):
    if gameover(board):
        return score(board)
    results = list()
    for next_board in possible_next_boards(board, "X"):
        results.append(min_step(next_board))
    return min(results)

def min_step(board):
    if gameover(board):
        return score(board)
    results = list()
    for next_board in possible_next_boards(board, "O"):
        results.append(max_step(next_board))
    return max(results)

def best_move(board,current_player):
    if current_player == "O":
        results = list()
        for i in range (0,9):
            if board[i] == ".":
                new_board = move(board,current_player,i) 
                score = max_step(new_board)
                board_print(new_board)
                if score == -1:
                    print("Loss")
                elif score == 0:
                    print("Tie")
                elif score == 1:
                    print("Win")
                results.append((score,i))
        maxi,index = max(results)
        return index
    elif current_player == "X":
        results = list()
        for i in range (0,9):
            if board[i] == ".":
                new_board = move(board,current_player,i) 
                score = min_step(new_board)
                print(score)
                board_print(new_board)
                if score == 1:
                    print("Loss")
                elif score == 0:
                    print("Tie")
                elif score == -1:
                    print("Win")
                results.append((score,i))
        mini,index = min(results)
        return index

def freshstart():
    theboard = "........."
    print("1 to go first(X), 2 to go second(O)")
    x = int(input())
    if x == 1: 
        human = "X"
        ai = "O"
        board_print(theboard)
        print("Where would you like to move")
        themove = int(input())
        theboard = move(theboard,human,themove)
    elif x == 2:
        ai = "O"
        human = "X"
        board_print(theboard)
    while gameover(theboard) == False:
        theboard = move(theboard,ai,best_move(theboard,ai))
        if gameover(theboard) == False:
            print("------------------------")
            board_print(theboard)
            print("Where would you like to move")
            themove = int(input())
            theboard = move(theboard,human,themove)
    if (score(theboard) == 1 and ai == "O") or (score(theboard) == -1 and ai == "X"):
        print("AI won!")
    elif score(theboard) == 0:
        print("Tie!")
    elif (score(theboard) == 1 and ai == "X") or (score(theboard) == -1 and ai == "O"):
        print("You win!")
    board_print(theboard)

def started(board):
    xcount = 0 
    ocount = 0 
    for i in board:
        if i == "X":
            xcount = xcount + 1
        elif i == "O":
            ocount = ocount + 1
    if xcount == ocount:
        ai = "X"
        human = "O"
    elif xcount > ocount:
        ai = "O"
        human = "X" 
    theboard = board
    while gameover(theboard) == False:
        theboard = move(theboard,ai,best_move(theboard,ai))
        if gameover(theboard) == False:
            print("------------------------")
            board_print(theboard)
            print("Where would you like to move")
            themove = int(input())
            theboard = move(theboard,human,themove)
    if (score(theboard) == 1 and ai == "O") or (score(theboard) == -1 and ai == "X"):
        print("AI won!")
    elif score(theboard) == 0:
        print("Tie!")
    elif (score(theboard) == 1 and ai == "X") or (score(theboard) == -1 and ai == "O"):
        print("You win!")
    board_print(theboard)

def startgame(board):
    if gameover(board):
        if score(board) == 1:
            print("O Won!")
        if score(board) == 0:
            print("Tie!")
        if score(board) == -1:
            print("X Won!")
    if "X" in board:
        started(board)
    else:
        freshstart()

startgame(case)

# board = "...XX...0"
# best_move(board,"0")
# board_print(board)
# print(max_step("...XX.0.0"))
