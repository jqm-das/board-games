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