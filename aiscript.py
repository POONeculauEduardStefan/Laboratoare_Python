import random

rows=None
colums = None

def point(num):
    """Returns points based on the value of 'num'. Used for evaluating positions on the board."""
    if(num==1):
        return 0
    if(num==2):
        return 2
    if(num==3):
        return 10
    if(num==4):
        return 10000
    if(num==5):
        return 100000
    else:
        return int(0)

def checkifvalid(move,gametable,colums):
    """Checks if a move is valid by ensuring it's within bounds and the column is not full."""
    if move>=colums :
        return False
    if move <0 :
        return False
    if(gametable[0][move]==0):
        return True;
    else:
        return False;

def check_direction(row, col, delta_row, delta_col,gametable,player):
    """Checks a specific direction (horizontal, vertical, diagonal) for a sequence of 'player' pieces."""
    count = 0
    opplayer=2
    if player == 2:
        opplayer=1
    for i in range(4):  # Check 4 cells in the given direction
        r, c = row + i * delta_row, col + i * delta_col
        if 0 <= r < rows and 0 <= c < colums and gametable[r][c] == player:
            count += 1
        if  0 <= r < rows and 0 <= c < colums and gametable[r][c] == opplayer:
            count = 0
            break
    if count == 0:
        return int(0)
    return count

def evaluate_board(gametable):
    """Evaluates the board for difficulty 2.Moves are chosen by checking all directions and calculating points.The enemies poins are calculated with plus one because we consider the next move of his."""
    points=0
    for x in range(rows):
        for y in range (colums):
            #horizontal
            s = check_direction(x,y,0,1,gametable,2)
            points = points + point(s)
            #vertical
            s = check_direction(x,y,1,0,gametable,2)
            points = points + point(s)
            #diagonal
            s= check_direction(x,y,1,1,gametable,2)
            points = points + point(s)
            #inverse diagonal
            s= check_direction(x,y,1,-1,gametable,2)
            points = points + point(s)
            s = check_direction(x, y, 0, 1, gametable, 1)
            points = points - point(s+1)/2
            # vertical
            s = check_direction(x, y, 1, 0, gametable, 1)
            points = points - point(s+1)/2
            # diagonal
            s = check_direction(x, y, 1, 1, gametable, 1)
            points = points - point(s+1)/2
            # inverse diagonal
            s = check_direction(x, y, 1, -1, gametable, 1)
            points = points - point(s+1)/2+1

    return  points

def evaluate_board1(gametable):
    """
    Evaluates the board for difficulty 3.It choses moves by checking directions and calculating points.
    The difference is it doesn't need to anticipate the enemies move now.The minmax aproach does that.
    """
    points=1
    for x in range(rows):
        for y in range (colums):
            #horizontal
            s = check_direction(x,y,0,1,gametable,2)
            points = points + point(s)
            #vertical
            s = check_direction(x,y,1,0,gametable,2)
            points = points + point(s)
            #diagonal
            s= check_direction(x,y,1,1,gametable,2)
            points = points + point(s)
            #inverse diagonal
            s= check_direction(x,y,1,-1,gametable,2)
            points = points + point(s)
            s = check_direction(x, y, 0, 1, gametable, 1)
            points = points - point(s)/2
            # vertical
            s = check_direction(x, y, 1, 0, gametable, 1)
            points = points - point(s)/2
            # diagonal
            s = check_direction(x, y, 1, 1, gametable, 1)
            points = points - point(s)/2
            # inverse diagonal
            s = check_direction(x, y, 1, -1, gametable, 1)
            points = points - point(s)/2

    return  points-1

def changeboard(move,gametable, rows,player):
    """Simulates droping the player's piece into the selected column and returns the position of the piece."""
    y = 0
    while gametable[y][move] == 0 :
        y=y+1
        if y == rows :
            break

    gametable[y-1][move] = player
    return [y-1,move]

def solve(gametable,diff):
    """
    Main function for determining the AI's next move based on the difficulty level.
    The difficulty levels are as follows:
    - diff == 1: Random move
    - diff == 2: Heuristic move based on evaluation of the board
                 -it simulates droping a piece in every spot posible.
                 -it evaluates the score of all the boards.
                 -it choses the board with the maximum amount of points and does that move.

    - diff == 3: Minimax-inspired approach considering multiple moves and counter-moves
                 - The algorithm simulates multiple layers of moves and counter-moves, alternating between AI and opponent.
                 - First layer (AI's Turn): The AI simulates all possible moves (dropping a piece in each column).
                 - Second layer (Opponent's Response): After the AI's move, the algorithm simulates all possible moves the opponent could make in response.
                 - Third layer (AI's Counter to Opponent's Response): Then, it simulates all possible moves for the AI after the opponent has made their move.
                 - Fourth layer (Opponent's Counter to AI's Counter): Finally, the algorithm simulates all possible counter-moves by the opponent after the AI's counter-move.
                 - The algorithm evaluates the score of each board state after each layer of moves and counter-moves.
                 - It selects the move for the AI that results in the highest score, taking into account both its own moves and the opponent's responses.
                 - To reduce computation, it checks for immediate wins or losses after each move
    """

    global rows,colums
    colums =len(gametable[0])
    rows = len(gametable)
    gametable1 = [[0 for _ in range(colums)] for _ in range(rows)]
    gametable1 = gametable
    #for the first difficulty we chose randomly a move
    if diff == 1 :
        goodmove = False
        while goodmove == False:
            col = random.randint(0,colums-1)
            if checkifvalid(col,gametable1,colums) == True :
                x,y = changeboard(col,gametable1,rows,2)
                goodmove = True
                return gametable1


    if(diff == 2):
            max_points = -2000000
            max_col= None
            for col in range(colums) :
                if checkifvalid(col,gametable,colums) == True:
                    x,y = changeboard(col,gametable,rows,2)
                    points = evaluate_board(gametable)
                    gametable[x][y] = 0
                    if(points>max_points):
                        max_points = points
                        max_col = col

            changeboard(max_col,gametable,rows,2)
            return gametable

    if(diff == 3):

        max_point=-2000000
        min_point1 = 2000000
        max_points2 = -2000000
        min_point2 = 2000000
        max_col = None
        for col1 in range(colums):
            if checkifvalid(col1, gametable, colums) == True:
                x1, y1 = changeboard(col1, gametable, rows,2)
                points = evaluate_board1(gametable)
                if points>8000:
                    return gametable
                for col2 in range(colums):
                    if checkifvalid(col2, gametable, colums) == True:
                        x2, y2 = changeboard(col2, gametable, rows,1)
                        point = evaluate_board1(gametable)
                        if point < -3000:
                            max_points2 = point
                        else:
                            for col3 in range(colums):
                                if checkifvalid(col3, gametable, colums) == True:
                                    x3, y3 = changeboard(col3, gametable, rows,2)
                                    point = evaluate_board1(gametable) #win after op move
                                    if point > 8000:
                                        min_point2 = point
                                    else:
                                        for col4 in range (colums):
                                            if checkifvalid(col4,gametable,colums) == True:
                                                x4,y4 = changeboard(col4,gametable,rows,1)
                                                point = evaluate_board1(gametable)
                                                gametable[x4][y4]=0
                                                if(point<min_point2):
                                                    min_point2 = point
                                    gametable[x3][y3] = 0
                                    if (min_point2 > max_points2):
                                        max_points2 = min_point2
                                    min_point2= 2000000
                        gametable[x2][y2] = 0
                        if(max_points2<min_point1):
                            min_point1=max_points2
                        max_points2 = -2000000
                gametable[x1][y1] = 0
                if(min_point1>max_point):
                    max_point=min_point1
                    max_col = col1
                min_point1 = 2000000
        changeboard(max_col,gametable,rows,2)
        return gametable