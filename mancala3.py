import sys

#Define Global Variable 
isGreedy = False
isMiniMax = False
isAlphaBeta = False
isCompetition = False
inputCuttingOfDepth = 0
min = "-infinity"
max = "infinity"
MyPlayer = -1
bestMoves ={}

class ManacalaGame():
    players = []
    NumOfPits = 0
    totalMarbles = 0
    currentPlayer = -1
    evalValue = -1 
    depth = -1
    movedPit = -1
    value = -1
    nodeName = ""
    canMoveNext = False
    isGameOver = False
    bestScore = float("-infinity")
    children = []
    parent = None

def SetTypeOfAlgo(type):
    if(type == "1"):
            isGreedy = True
    elif(type == "2"):
        isMiniMax = True
    elif(type == "3"):
        isAlphaBeta = True
    elif(type == "4"):
        isCompetition = True

def GetGameClone(game):
    tempGame = ManacalaGame()
    tempGame.currentPlayer = game.currentPlayer
    tempGame.evalValue = game.evalValue
    tempGame.players = []
    tempGame.NumOfPits = game.NumOfPits
    tempGame.players.append([])
    tempGame.players.append([])
    
    tempGame.bestScore = game.bestScore
    tempGame.canMoveNext = game.canMoveNext
    tempGame.movedPit = game.movedPit
    tempGame.nodeName = game.nodeName
    tempGame.totalMarbles = game.totalMarbles
    tempGame.value = game.value
   
    tempGame.players[0] = list(game.players[0])
    tempGame.players[1] = list(game.players[1])

    return tempGame

def CheckIfPlayerPitsEmpty(matrix):
    isEmpty = True
    for count in range(len(matrix)-1):
        if(matrix[count + 1] != 0):
            isEmpty = False
            break
    return isEmpty

def GetValidMoves(game,currentPlayer):
    validMoves = []
    for count in range(game.NumOfPits):
        if(game.players[currentPlayer][count+1] > 0):
            validMoves.append(count + 1)
    return validMoves

def GetValue(val):
    if(val == float("-infinity")):
        return "-Infinity"
    elif(val == float("infinity")):
        return "Infinity"
    return str(val)

def GetNodeName(index,player,numOfPits):
    if(player == 1):
        return "B"+str(numOfPits - index + 2)
    else:
        return "A"+str(index + 1)

def MoveNext(game,pitNum,currentPlayer):
   tempGame = GetGameClone(game)
   tempGame.canMoveNext = False
   tempGame.isGameOver = False
   numOfMarbles = game.players[currentPlayer][pitNum]
   if(numOfMarbles <= 0):
       tempGame.evalValue = 0
       return tempGame
   currentPit = pitNum
   currentTurn = currentPlayer
   marblesToDistribute = numOfMarbles
   while(marblesToDistribute > 0):
       tempGame.players[currentPlayer][pitNum] -= 1
       marblesToDistribute -= 1
       currentPit -= 1
       #Put in player's mancala
       if(currentPit == 0):
           if(currentTurn == currentPlayer):
                tempGame.players[currentTurn][currentPit] += 1
                if(marblesToDistribute == 0):
                    #re run the algo
                    isEmpty = CheckIfPlayerPitsEmpty(tempGame.players[0])
                    isOppositeEmpty =  CheckIfPlayerPitsEmpty(tempGame.players[1])
                    #GameOver
                    if(isEmpty or isOppositeEmpty):
                           for count in range(tempGame.NumOfPits):
                                tempGame.players[0][0] += tempGame.players[0][count + 1]
                                tempGame.players[0][count + 1] = 0
                                tempGame.players[1][0] += tempGame.players[1][count + 1]
                                tempGame.players[1][count + 1] = 0    
                                tempGame.canMoveNext = False  
                                tempGame.isGameOver = True                    
                           return tempGame
                    tempGame.canMoveNext = True  
                    return tempGame     
           else:
               #marbles += 1 
               marblesToDistribute += 1
               tempGame.players[currentPlayer][pitNum] += 1
           currentPit = tempGame.NumOfPits + 1          
           currentTurn = (currentTurn + 1) % 2
       else:
           #capture
           if(currentTurn == currentPlayer and  tempGame.players[currentTurn][currentPit] == 0
              and marblesToDistribute == 0):
              tempGame.players[currentTurn][0] += tempGame.players[(currentTurn+1)%2][tempGame.NumOfPits - currentPit + 1] + 1
              tempGame.players[(currentTurn+1)%2][tempGame.NumOfPits - currentPit + 1] = 0
           #Put in a pit
           else:
            tempGame.players[currentTurn][currentPit] += 1   
   isEmpty = CheckIfPlayerPitsEmpty(tempGame.players[0])
   isOppositeEmpty =  CheckIfPlayerPitsEmpty(tempGame.players[1])
   #GameOver
   if(isEmpty or isOppositeEmpty):
       for count in range(tempGame.NumOfPits):
            tempGame.players[0][0] += tempGame.players[0][count + 1]
            tempGame.players[0][count + 1] = 0
            tempGame.players[1][0] += tempGame.players[1][count + 1]
            tempGame.players[1][count + 1] = 0
            tempGame.isGameOver = True
   return tempGame

def GoGreedyOutput(node,playerPlaying):
    if((len(GetValidMoves(node,playerPlaying)) == 0) and node.canMoveNext == False):
        return node,node.players[MyPlayer][0] - node.players[(MyPlayer+1)% 2][0]
    moves = GetValidMoves(node,playerPlaying)

    if(playerPlaying%2 == 0):
        moves.sort()
    else:
        moves.sort(reverse = True)
    optimumBoard = node

    bestMove = float("-infinity")
    for move in moves:
        child = MoveNext(node,move,playerPlaying)
        child.nodeName = GetNodeName(move,playerPlaying,child.NumOfPits)

        if(child.canMoveNext):
            child,value = GoGreedyOutput(child,playerPlaying)
        else:
            child,value = child,child.players[MyPlayer][0] - child.players[(MyPlayer+1)% 2][0]

        if(value> bestMove):
            bestMove = value 
            optimumBoard = child
    return optimumBoard,bestMove

def GoMinMaxTheOuput(node,depth,playerPlaying,f):
    moves = GetValidMoves(node,playerPlaying)
    if((depth == inputCuttingOfDepth or len(moves) <= 0) and node.canMoveNext == False):
        evalValue = node.players[MyPlayer][0] - node.players[(MyPlayer+1)% 2][0]
        f.write(node.nodeName + "," + str(depth)+ "," + str(evalValue)+"\n")  
        return node,evalValue
    
    if((playerPlaying)%2 == 0):
        moves.sort()
    else:
        moves.sort(reverse = True)
    
    optimumBoard = node
    
    if(playerPlaying == MyPlayer):
        bestMove = float("-infinity")
        f.write(node.nodeName + "," + str(depth)+ "," + str(GetValue(bestMove)) + "\n")      
        for move in moves:
            child = MoveNext(node,move,playerPlaying)
            child.nodeName = GetNodeName(move,playerPlaying,child.NumOfPits)
            tempDepth = depth
            if(node.canMoveNext == True):
                tempDepth = depth - 1 

            if(child.canMoveNext and child.isGameOver == False):
                child,value = GoMinMaxTheOuput(child,tempDepth+1,playerPlaying,f)
            elif (child.isGameOver == False):
                child,value = GoMinMaxTheOuput(child,tempDepth+1,(playerPlaying+1)%2,f)

            if(child.isGameOver == True):                            
                child.isGameOver = False
                value = child.players[MyPlayer][0] - child.players[(MyPlayer+1)% 2][0]
                f.write(child.nodeName + "," + str(tempDepth+1)+ "," + str(GetValue(value))+"\n") 
              
            if(value> bestMove):
                bestMove = value 
                optimumBoard = child
           
            f.write(node.nodeName + "," + str(depth)+ "," + str(GetValue(bestMove))+"\n")
        return optimumBoard,bestMove
    else:
        worstMove = float("infinity")
        f.write(node.nodeName + "," + str(depth) + ","+ str(GetValue(worstMove))+"\n")
        subOptimumBoard = node
    
        for move in moves:
            child = MoveNext(node,move,playerPlaying)
            child.nodeName = GetNodeName(move,playerPlaying,child.NumOfPits)
            tempDepth = depth
            if(node.canMoveNext == True):
                tempDepth = depth -1
                 
            if(child.canMoveNext and child.isGameOver == False):            
                child,value = GoMinMaxTheOuput(child,tempDepth+1,playerPlaying,f)
            elif (child.isGameOver == False):
                child,value = GoMinMaxTheOuput(child,tempDepth+1,(playerPlaying+1)%2,f)
            
            if(child.isGameOver == True):                                
                child.isGameOver = False
                value = child.players[MyPlayer][0] - child.players[(MyPlayer+1)% 2][0]
                f.write(child.nodeName + "," + str(tempDepth+1)+ "," + str(GetValue(value))+"\n")             
            
            if(worstMove> value):
                worstMove = value 
                subOptimumBoard = child
            f.write(node.nodeName + "," + str(depth)+ "," + str(GetValue(worstMove))+"\n")
        return optimumBoard,worstMove

def GoPruneTheOutput(node,depth,playerPlaying,f,alpha,beta):
    moves = GetValidMoves(node,playerPlaying)
    if((depth == inputCuttingOfDepth or len(moves) == 0) and node.canMoveNext == False):
        evalValue = node.players[MyPlayer][0] - node.players[(MyPlayer+1)% 2][0]
        f.write(node.nodeName + "," + str(depth)+ "," + str(evalValue) +"," + str(GetValue(alpha)) + "," + str(GetValue(beta))+"\n")  
        return node,evalValue

    if(playerPlaying%2 == 0):
        moves.sort()
    else:
        moves.sort(reverse = True)

    optimumBoard = node
    if(playerPlaying == MyPlayer):
        bestMove = float("-infinity")
        f.write(node.nodeName + "," + str(depth)+ "," + str(GetValue(bestMove)) +"," + str(GetValue(alpha)) + "," + str(GetValue(beta))+"\n")      
        for move in moves:
            child = MoveNext(node,move,playerPlaying)
            child.nodeName = GetNodeName(move,playerPlaying,child.NumOfPits)
            tempDepth = depth
            if(node.canMoveNext == True):
                tempDepth = depth - 1 

            if(child.canMoveNext and child.isGameOver == False):
                child,value = GoPruneTheOutput(child,tempDepth+1,playerPlaying,f,alpha,beta)
            elif(child.isGameOver == False):
                child,value = GoPruneTheOutput(child,tempDepth+1,(playerPlaying+1)%2,f,alpha,beta)
            
            if(child.isGameOver == True):
                child.isGameOver = False
                value = child.players[MyPlayer][0] - child.players[(MyPlayer+1)% 2][0]
                #alpha = value
                f.write(child.nodeName + "," + str(tempDepth+1) + ","+ str(GetValue(value))+"," + str(GetValue(alpha)) + "," + str(GetValue(beta))+"\n")
           
            if(value> bestMove):
                bestMove = value 
                optimumBoard = child
            if(value >= beta):
                #change in this
                f.write(node.nodeName + "," + str(depth) + ","+ str(GetValue(bestMove))+"," + str(GetValue(alpha)) + "," + str(GetValue(beta))+"\n")
                return optimumBoard,bestMove
            if(alpha < value):
                alpha = value

            f.write(node.nodeName + "," + str(depth)+ "," + str(GetValue(bestMove))+"," + str(GetValue(alpha)) + "," + str(GetValue(beta))+"\n")
        return optimumBoard,bestMove
    else:
        worstMove = float("infinity")
        f.write(node.nodeName + "," + str(depth) + ","+ str(GetValue(worstMove))+"," + str(GetValue(alpha)) + "," + str(GetValue(beta))+"\n")
        subOptimumBoard = node
        for move in moves:
            child = MoveNext(node,move,playerPlaying)
            child.nodeName = GetNodeName(move,playerPlaying,child.NumOfPits)
            tempDepth = depth
            if(node.canMoveNext == True):
                tempDepth = depth -1
          
            if(child.canMoveNext and child.isGameOver == False):            
                child,value = GoPruneTheOutput(child,tempDepth+1,playerPlaying,f,alpha,beta)
            elif(child.isGameOver == False):
                child,value = GoPruneTheOutput(child,tempDepth+1,(playerPlaying+1)%2,f,alpha,beta)
             
            if(child.isGameOver == True):
                child.isGameOver = False
                value = child.players[MyPlayer][0] - child.players[(MyPlayer+1)% 2][0]          
                #beta = value
                f.write(child.nodeName + "," + str(tempDepth+1) + ","+ str(GetValue(value))+"," + str(GetValue(alpha)) + "," + str(GetValue(beta))+"\n")
           
            if(worstMove> value):
                worstMove = value 
                subOptimumBoard = child
            if(value <= alpha):
                f.write(node.nodeName + "," + str(depth) + ","+ str(GetValue(worstMove))+"," + str(GetValue(alpha)) + "," + str(GetValue(beta))+"\n")
                return optimumBoard,worstMove
            if(beta > value):
                beta = value
            f.write(node.nodeName + "," + str(depth)+ "," + str(GetValue(worstMove))+"," + str(GetValue(alpha)) + "," + str(GetValue(beta))+"\n")
        return optimumBoard,worstMove

def main():                              
     try:
        #filename = sys.argv[2]
        inputFile  = open("input_1.txt","r")   
        #inputFile = open(filename,"r") 
        if inputFile.mode == 'r':
            contents =  inputFile.read().splitlines()                  
        inputFile.close()
        game = ManacalaGame()
        type = contents[0]
        SetTypeOfAlgo(type)
        global isGreedy
        global isMiniMax
        global isAlphaBeta
        global isCompetition
        global inputCuttingOfDepth
        global MyPlayer
        if(type == "1"):
            isGreedy = True
        elif(type == "2"):
            isMiniMax = True
        elif(type == "3"):
            isAlphaBeta = True
        elif(type == "4"):
            isCompetition = True
        player = contents[1]
        game.currentPlayer = int(player)%2
        MyPlayer = game.currentPlayer
        depth = contents[2]
        cuttingOfDepth = int(depth)
        inputCuttingOfDepth = cuttingOfDepth
        #2nd player at index 0
        marb2 = contents[3].split()
        marbles2 = marb2
        numOfMarbles = len(marbles2)   
        mar1 = contents[4].split()    
        marbles1  = mar1     
        mancala2 = int(contents[5])
        mancala1 = int(contents[6])

        game.players.append([])
        game.players.append([])

        game.players[0].append(mancala2);

        count = 0
        for marble in marbles2:
            game.players[0].append(int(marble))

        game.players[1].append(mancala1);

        game.NumOfPits = len(marbles2)
        #Enter in reverse order
        for count in range(game.NumOfPits):
            game.players[1].append(int(marbles1[game.NumOfPits -1 - count]))
        
        if(isGreedy):
            #bestMove = GoGreedy(game)
            #bestMove,value = GoGreedy(game,MyPlayer)
            bestMove,val = GoGreedyOutput(game,MyPlayer)
            f = open("next_state.txt","w+")
            for count in range(bestMove.NumOfPits):             
                f.write(str(bestMove.players[0][count+1]))
                if(count != game.NumOfPits - 1):
                    f.write(" ")
            
            f.write("\n")
            for count in range(bestMove.NumOfPits):             
                f.write(str(bestMove.players[1][game.NumOfPits - count]))
                if(count != game.NumOfPits - 1):
                    f.write(" ")
            f.write("\n")
            f.write(str(bestMove.players[0][0]))
            f.write("\n")
            f.write(str(bestMove.players[1][0]))
            f.close()

        if(isMiniMax):
            
            f = open("traverse_log.txt","w+")
            f.write("Node,Depth,Value")
            f.write("\n")

            initialState = game
            initialState.nodeName = "root"
            initialState.depth = 0
            initialState.value = float(min)
            state,value = GoMinMaxTheOuput(initialState,0,MyPlayer,f)
            f.close()

            outputFile = open("next_state.txt","w+")
            for count in range(state.NumOfPits):             
                outputFile.write(str(state.players[0][count+1]))
                if(count != game.NumOfPits - 1):
                    outputFile.write(" ")
            
            outputFile.write("\n")
            for count in range(state.NumOfPits):             
                outputFile.write(str(state.players[1][game.NumOfPits - count]))
                if(count != game.NumOfPits - 1):
                    outputFile.write(" ")
            outputFile.write("\n")
            outputFile.write(str(state.players[0][0]))
            outputFile.write("\n")
            outputFile.write(str(state.players[1][0]))
            outputFile.close()
        
        if(isAlphaBeta):
            
            f = open("traverse_log.txt","w+")
            f.write("Node,Depth,Value,Alpha,Beta")
            f.write("\n")

            initialState = game
            initialState.nodeName = "root"
            initialState.depth = 0
            initialState.value = float(min)
            alpha = float("-infinity")
            beta = float("infinity")
            state,value = GoPruneTheOutput(initialState,0,MyPlayer,f,alpha,beta)
            f.close()

            outputFile = open("next_state.txt","w+")
            for count in range(state.NumOfPits):             
                outputFile.write(str(state.players[0][count+1]))
                if(count != game.NumOfPits - 1):
                    outputFile.write(" ")
            
            outputFile.write("\n")
            for count in range(state.NumOfPits):             
                outputFile.write(str(state.players[1][game.NumOfPits - count]))
                if(count != game.NumOfPits -1):
                    outputFile.write(" ")
            outputFile.write("\n")
            outputFile.write(str(state.players[0][0]))
            outputFile.write("\n")
            outputFile.write(str(state.players[1][0]))
            outputFile.close()
     except Exception as e:
        print("Input File Not Found")

if __name__ == '__main__':
    main();
