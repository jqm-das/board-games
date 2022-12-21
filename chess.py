import numpy as np
import pickle 

BOARD_ROWS = 8
BOARD_COLS = 8

class State:

    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        for i in range (0,8):
            self.board[1,i] = 1
        for i in range(0,8):
            self.board[6,i] = -1
        self.board[0,4],self.board[7,4] = 10
        self.board[0,3],self.board[7,3] = 8
        self.board[0,0],self.board[0,7],self.board[8,0],self.board[8,7] = 5
        self.board[0,1],self.board[0,6],self.board[8,1],self.board[8,6] = 4
        self.board[0,2],self.board[0,5],self.board[8,2],self.board[8,5] = 3
        for i in range(0,8):
            self.board[7,i] = self.board[7,i] * -1 
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        # init p1 plays first
        self.playerSymbol = 1

    # get unique hash of current board state
    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return self.boardHash

        # only when game ends
    def giveReward(self):
        result = self.winner()
        # backpropagate reward
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)

    # board reset
    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        for i in range (0,8):
            self.board[1,i] = 1
        for i in range(0,8):
            self.board[6,i] = -1
        self.board[0,4],self.board[7,4] = 10
        self.board[0,3],self.board[7,3] = 8
        self.board[0,0],self.board[0,7],self.board[8,0],self.board[8,7] = 5
        self.board[0,1],self.board[0,6],self.board[8,1],self.board[8,6] = 4
        self.board[0,2],self.board[0,5],self.board[8,2],self.board[8,5] = 3
        for i in range(0,8):
            self.board[7,i] = self.board[7,i] * -1 
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def updateState(self, position_piece, position_move):
        self.board[position_move] = self.board[position_piece]

    def play(self,rounds):
        for i in range (0,rounds):
            while not self.isEnd:

                p1_action = self.p1.chooseAction(self.board,self.playerSymbol)

                board_hash = self.getHash()
                self.p1.addState(board_hash)

                if p1_action is None:
                    self.isEnd = True
                    break

                self.updateState(p1_action)

                p2_action = self.p2.chooseAction(self.board,self.playerSymbol)

                board_hash = self.getHash()
                self.p2.addState(board_hash)

                if p2_action is None:
                    self.isEnd = True
                    break

                self.updateState(p2_action)
            
            self.giveReward()
            self.p1.reset()
            self.p2.reset()
            self.reset()


    def showBoard(self):
        # p1: x  p2: o
        for i in range(0, BOARD_ROWS):
            print('-------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                out += self.board[i,j] + ' | '
            print(out)
        print('-------------')

class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value  

    def getHash(self, board):
        boardHash = str(board.reshape(BOARD_COLS * BOARD_ROWS))
        return boardHash

    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action

    def addState(self, state):
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

if __name__ == "__main__":
    # training
    p1 = Player("p1")
    p2 = Player("p2")

    st = State(p1, p2)
    print("training...")
    st.play(50000)