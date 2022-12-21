import sys
import time 
import math

case = sys.argv[1]
minlength = int(sys.argv[2])
started = False
if len(sys.argv) == 4:
    sofar = sys.argv[3].lower()
    started = True

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def read():
    with open(case) as f:
        line_list = [line.strip() for line in f]
    return line_list

file = read()

def createWordList():
    ls = []
    for x in file:
        bool = True
        if len(x) >= minlength:
            for i in x:
                if i.lower() not in alphabet:
                    bool = False
            if bool:
                ls.append(x.lower())
    return ls

words = createWordList()

def possibleWords(worddict,word):
    ls = []
    for x in worddict:
        if x[:len(word)] == word:
            ls.append(x)
    return ls

def possibleMoves(worddict,word):
    ls = []
    for x in worddict:
        if len(x) > len(word):
            y = x[len(word)]
            if y not in ls:
                ls.append(y)
        if x == word:
            ls.append(" ")
    return ls 


def negamax(wordlist,word,move):
    results = list()
    if word in wordlist:
        return -1
    moves = possibleMoves(wordlist,word)
    if move == 1:
        for i in moves:
            newwordlist = possibleWords(wordlist,word+i)
            results.append((-1*negamax(newwordlist,word+i,2)))
    if move == 2:
        for i in moves:
            newwordlist = possibleWords(wordlist,word+i)
            if word+i not in wordlist:
                newmoves = possibleMoves(newwordlist,word+i)
                for j in newmoves:
                    newwordlist = possibleWords(wordlist,word+i+j)
                    results.append((-1*negamax(newwordlist,word+i+j,1)))
    if len(results) == 0:
        return 1
    return min(results)

def findWinners(wordlist,word):
    winners = []
    for i in possibleMoves(wordlist,word):
        newwordlist = possibleWords(wordlist,word+i)
        neg = negamax(newwordlist,word+i,2)
        if neg == 1:
            winners.append(i.upper())
    return winners

if started:
    words = possibleWords(words,sofar)
else:
    sofar = ""
y = findWinners(words,sofar)
if len(y) == 0:
    print("Next player will lose!")
else:
    print(y)
