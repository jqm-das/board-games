import sys
import math

def checkTan(board,i,token,op):
    if isTan(board,token,i,-1,op) or isTan(board,token,i,1,op) or isTan(board,token,i,-8,op) or isTan(board,token,i,8,op) or isTan(board,token,i,-7,op) or isTan(board,token,i,7,op) or isTan(board,token,i,9,op) or isTan(board,token,i,-9,op):
        return True
    return False 

def tanDict():
    refDict = {}
    for i in range (0,64):
        ls = []
        if i % 8 > 0:
            ls.append(i-1)
        if i % 8 < 7:
            ls.append(i+1)
        if i // 8 != 0:
            ls.append(i-8)
        if i // 8 != 7:
            ls.append(i+8)
        if i % 8 < 7 and i // 8 != 0:
            ls.append(i-7)
        if i % 8 > 0 and i // 8 != 0:
            ls.append(i-9) 
        if i % 8 > 0 and i // 8 != 7:
            ls.append(i+7) 
        if i % 8 < 7 and i // 8 != 7:
            ls.append(i+9) 
        refDict[i] = ls
    return refDict

tangents = tanDict()

def isTan(board,token,index,move,op):
    hold = index + move
    if hold in tangents.get(index):
        if board[hold] == op:
            while hold in tangents.get(index):
                if board[hold] == op:
                    hold = hold + move 
                    index = index + move
                elif board[hold] == token:
                    return True
                else:
                    return False
    return False


def possible_moves(board,token):
    indices = set()
    if token == "x":
        op = "o"
    elif token == "o":
        op = "x"
    for i in range (0,len(board)):
        if board[i] == ".":
            if checkTan(board,i,token,op):
                indices.add(i)
    return list(indices)

def allDirections(board,token,i,op):
    return isValid(board,token,i,-1,op).union(isValid(board,token,i,1,op), isValid(board,token,i,-8,op) , isValid(board,token,i,8,op) , isValid(board,token,i,-7,op) , isValid(board,token,i,7,op) , isValid(board,token,i,9,op) , isValid(board,token,i,-9,op))

def isValid(board,token,index,move,op):
    indices = set()
    empty = set()
    hold = index + move
    if hold in tangents.get(index):
        if board[hold] == op:
            indices.add(hold)
            while hold in tangents.get(index):
                if board[hold] == op:
                    hold = hold + move 
                    indices.add(hold)
                    index = index + move
                elif board[hold] == token:
                    indices.add(hold)
                    return indices
                else:
                    return empty
    return empty


def make_move(board,token,move):
    indices = set()
    if token == "x":
        op = "o"
    elif token == "o":
        op = "x"
    x = allDirections(board,token,move,op)
    if len(x) > 0:
        x.add(move)
    for i in x:
        board = board[:i] + token + board[i+1:]
    return board

corners_dict = {
    0: {1, 8, 9},
    7: {6, 14, 15},
    56: {57, 48, 49},
    63: {62, 54, 55}
}


board = sys.argv[1]
player = sys.argv[2]
depth = 1 
if player == "x":
    ai = "o"
elif player =='o':
    ai = "x"

def countup(board,player):
    counter = 0 
    for i in board:
        if i == player:
            counter = counter + 1
    return counter

def score(board):
    counter = 0 

    xmoves = possible_moves(board,"x")
    omoves = possible_moves(board,"o")
    
    if len(omoves) == 0 and len(xmoves) == 0:
        counter = 100000*(countup(board,"x") - countup(board,"o"))


    if len(xmoves) > len(omoves):
        counter = counter + math.log((len(xmoves)- len(omoves)),10)*10
    elif len(xmoves) < len(omoves):
        counter = counter - math.log((len(omoves) - len(xmoves)),10)*10
    
    for i,j in corners_dict.items():
        if board[i] == "x":
            counter = counter + 1000
            for x in j:
                if board[x] == "x":
                    counter = counter + 50
        elif board[i] == "o":
            counter = counter - 1000
            for x in j:
                if board[x] == "o":
                    counter = counter - 50
        else:
            for x in j:
                if board[x] == "x":
                    counter = counter - 200
                elif board[x] == "o":
                    counter = counter + 200

    return counter 

def negascore(board,current_player):
    if current_player == "o":
        return score(board) * -1
    else:
        return score(board) 

def negamax(board,current_player,depth,maxdepth,alpha,beta):
    if depth == maxdepth:
        return negascore(board,current_player)
    if current_player == "x":
        other_player = "o"
    elif current_player == "o":
        other_player = "x"

    moves = possible_moves(board, other_player)
    best = -100000

    if len(moves) == 0:
        return negascore(board,current_player)
        
    for i in moves:
        next_board = make_move(board,other_player,i)

        score = (-1*negamax(next_board,other_player,depth+1,maxdepth,beta,alpha))

        if best < score:
            best = score
        
        if alpha < best:
            alpha = score

        if beta <= alpha:
            break; 

    return best

def find_next_move(board,current_player,depth):
    alpha = 10000000
    beta = -10000000
    best = -10000000
    results = list()
    for i in possible_moves(board,current_player):
        new_board = make_move(board,current_player,i) 
        thescore = -1*negamax(new_board,current_player,0,depth,alpha,beta)
        if thescore > best:
            best = thescore
            results.append((thescore,i))
        
        if alpha > best:
            best = alpha
        
        if beta <= alpha:
            break

    maxi,index = max(results)
    # if len(results) == 0:
    #     index = -1
    return index

for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
   print(find_next_move(board, player, depth))
   depth += 1

