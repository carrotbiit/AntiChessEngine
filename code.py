#Part 11 10 mins in to video
import pygame as pygame
from random import randint



pygame.mixer.init()

Width = 400
Height = 400
Dimension = 8
SquareSize = Height // Dimension
Max_FPS = 30
IMAGES = {}

def drawBoard(screen):
  colors = [(181, 136, 99), (240, 217, 181)]
  for i in range(Dimension):
    for j in range(Dimension):
      color = colors[((i+j) % 2)]
      pygame.draw.rect(screen, color, pygame.Rect(i*SquareSize, j*SquareSize, SquareSize, SquareSize))
# turn list of letters to list of images
def LoadImages():
  pieces = ["bB", "bK", "bN", "bP", "bQ", "bR", "wB", "wK", "wN", "wP", "wQ", "wR"]
  for i in pieces:
    IMAGES[i] = pygame.transform.scale(pygame.image.load(("pieces/" + i + ".png")), (SquareSize, SquareSize))

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)
Screen = pygame.display.set_mode((Width, Height))
Clock = pygame.time.Clock()
Screen.fill(pygame.Color("white"))
LoadImages()

homescreen = True
xvalue = 60
yvalue = 225
king = pygame.transform.scale(pygame.image.load("images/king.png"), (100, 100))
title = font.render("antichess engine", True, (255, 255, 255), (0, 0, 0))
playeasy = font.render("play easy version", True, (255, 255, 255), (0, 255, 0))
playhard = font.render("play hard version", True, (255, 255, 255), (255, 0, 0))
easyrect = playeasy.get_rect(topleft = (xvalue, yvalue))
hardrect = playhard.get_rect(topleft = (xvalue, yvalue+50))



while homescreen:
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      homescreen = False
    elif e.type == pygame.MOUSEBUTTONDOWN:
      mousex, mousey = pygame.mouse.get_pos()
      if easyrect.collidepoint(mousex, mousey):
        DEPTH = 2
        homescreen = False
      if hardrect.collidepoint(mousex, mousey):
        DEPTH = 4
        homescreen = False
  drawBoard(Screen)
  Screen.blit(king, (150, yvalue - 125))
  Screen.blit(title, (xvalue, yvalue - 200))
  Screen.blit(playeasy, (xvalue, yvalue))
  Screen.blit(playhard, (xvalue, yvalue+50))
  pygame.display.update()
  Clock.tick(15)
  pygame.display.flip()

def main():
  # pygame.mixer.Sound("sounds/startgame.mp3")
  # pygame.mixer.Sound.play()
  #run loop
  gs = GameState()
  canTake = True
  takeMoves = gs.getAllTakeMoves()
  if len(takeMoves) == 0:
    validMoves = gs.getAllPossibleMoves()
    canTake = False
  moveMade = False
  running = True
  GameOver = False
  sqSelected = ()
  playerClicks = []
  startgame = pygame.mixer.Sound("sounds/startgame.mp3")
  pygame.mixer.Sound.play(startgame)
  drawGameState(Screen, gs, validMoves, sqSelected)
  Clock.tick(2)
  while running:
    if not GameOver:
      humanTurn = not gs.WhiteToMove
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
          if humanTurn:
            location = pygame.mouse.get_pos()
            col = location[0]//SquareSize
            row = location[1]//SquareSize
            if sqSelected == (row, col):
              sqSelected = ()
              playerClicks = []
            else:
              sqSelected = (row, col)
              playerClicks.append(sqSelected)
            if len(playerClicks) == 2:
              move = Move(playerClicks[0], playerClicks[1], gs.board)
              if canTake:
                for i in range(len(takeMoves)):
                  if move == takeMoves[i]:
                    if not takeMoves[i].isPawnPromotion:
                      gs.makeMove(takeMoves[i])
                    elif takeMoves[i].isPawnPromotion:
                      promotetext = font.render("promote to:", True, (0, 255, 0))
                      ktext = font.render("king", True, (255, 255, 255), (0, 0, 0))
                      qtext = font.render("queen", True, (255, 255, 255), (0, 0, 0))
                      btext = font.render("bishop", True, (255, 255, 255), (0, 0, 0))
                      ntext = font.render("knight", True, (255, 255, 255), (0, 0, 0))
                      rtext = font.render("rook", True, (255, 255, 255), (0, 0, 0))
                      krect = ktext.get_rect(topleft = (100, 150))
                      qrect = qtext.get_rect(topleft = (250, 150))
                      brect = btext.get_rect(topleft = (100, 200))
                      nrect = ntext.get_rect(topleft = (250, 200))
                      rrect = rtext.get_rect(topleft = (100, 250))
                      selecting = True
                      while selecting:
                        for e in pygame.event.get():
                          if e.type == pygame.QUIT:
                            running = False
                          elif e.type == pygame.MOUSEBUTTONDOWN:
                            mousepos = pygame.mouse.get_pos()
                            if krect.collidepoint(mousepos[0], mousepos[1]):
                              gs.makeMove(takeMoves[i], "K")
                              selecting = False
                            if qrect.collidepoint(mousepos[0], mousepos[1]):
                              gs.makeMove(takeMoves[i], "Q")
                              selecting = False
                            if brect.collidepoint(mousepos[0], mousepos[1]):
                              gs.makeMove(takeMoves[i], "B")
                              selecting = False
                            if nrect.collidepoint(mousepos[0], mousepos[1]):
                              gs.makeMove(takeMoves[i], "N")
                              selecting = False
                            if rrect.collidepoint(mousepos[0], mousepos[1]):
                              gs.makeMove(takeMoves[i], "R")
                              selecting = False
                        Screen.blit(promotetext, (100, 100))
                        Screen.blit(ktext, (100, 150))
                        Screen.blit(qtext, (250, 150))
                        Screen.blit(btext, (100, 200))
                        Screen.blit(ntext, (250, 200))
                        Screen.blit(rtext, (100, 250))
                        pygame.display.update()
                        pygame.display.flip()
                    moveMade = True
                    playerClicks = []
                    sqSelected = ()
              else:
                for i in range(len(validMoves)):
                  if move == validMoves[i]:
                    if not validMoves[i].isPawnPromotion:
                      gs.makeMove(validMoves[i])
                    elif validMoves[i].isPawnPromotion:
                      promotetext = font.render("promote to:", True, (0, 255, 0))
                      ktext = font.render("king", True, (255, 255, 255), (0, 0, 0))
                      qtext = font.render("queen", True, (255, 255, 255), (0, 0, 0))
                      btext = font.render("bishop", True, (255, 255, 255), (0, 0, 0))
                      ntext = font.render("knight", True, (255, 255, 255), (0, 0, 0))
                      rtext = font.render("rook", True, (255, 255, 255), (0, 0, 0))
                      krect = ktext.get_rect(topleft = (100, 150))
                      qrect = qtext.get_rect(topleft = (250, 150))
                      brect = btext.get_rect(topleft = (100, 200))
                      nrect = ntext.get_rect(topleft = (250, 200))
                      rrect = rtext.get_rect(topleft = (100, 250))
                      selecting = True
                      while selecting:
                        for e in pygame.event.get():
                          if e.type == pygame.QUIT:
                            running = False
                          elif e.type == pygame.MOUSEBUTTONDOWN:
                            mousepos = pygame.mouse.get_pos()
                            if krect.collidepoint(mousepos[0], mousepos[1]):
                              gs.makeMove(validMoves[i], "K")
                              selecting = False
                            if qrect.collidepoint(mousepos[0], mousepos[1]):
                              gs.makeMove(validMoves[i], "Q")
                              selecting = False
                            if brect.collidepoint(mousepos[0], mousepos[1]):
                              gs.makeMove(validMoves[i], "B")
                              selecting = False
                            if nrect.collidepoint(mousepos[0], mousepos[1]):
                              gs.makeMove(validMoves[i], "N")
                              selecting = False
                            if rrect.collidepoint(mousepos[0], mousepos[1]):
                              gs.makeMove(validMoves[i], "R")
                              selecting = False
                        Screen.blit(promotetext, (100, 100))
                        Screen.blit(ktext, (100, 150))
                        Screen.blit(qtext, (250, 150))
                        Screen.blit(btext, (100, 200))
                        Screen.blit(ntext, (250, 200))
                        Screen.blit(rtext, (100, 250))
                        pygame.display.update()
                        pygame.display.flip()
                    moveMade = True
                    playerClicks = []
                    sqSelected = ()
              if not moveMade:
                playerClicks = [sqSelected]
          elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_u:
              gs.undoMove()
              moveMade = True


      #bot move
      if not humanTurn:
        Clock.tick(3)
        move = findBestMove(validMoves, takeMoves, gs)
        if move != None:
          gs.makeMove(move, "Q")
        else:
          if len(takeMoves) != 0:
            gs.makeMove(takeMoves[randint(0, len(takeMoves)-1)])
          elif len(validMoves) != 0:
            gs.makeMove(validMoves[randint(0, len(validMoves)-1)])
        moveMade = True
        
    
      if moveMade:
        validMoves = []
        takeMoves = []
        canTake = True
        takeMoves = gs.getAllTakeMoves()
        if len(takeMoves) == 0:
          validMoves = gs.getAllPossibleMoves()
          canTake = False
        moveMade = False
      if len(validMoves) == 0:
        drawTakeGameState(Screen, gs, takeMoves, sqSelected)
      if len(validMoves) != 0:  
        drawGameState(Screen, gs, validMoves, sqSelected)
      if len(validMoves) == 0 and len(takeMoves) == 0:
        win = "white" if gs.WhiteToMove else "black"
        text = win + " wins!"
        wintext = font.render(text, True, (0, 255, 0), (255, 255, 255))
        Screen.blit(wintext, (100, 175))
        gameend = pygame.mixer.Sound("sounds/gameend.mp3")
        pygame.mixer.Sound.play(gameend, 0)
        moveloglist = []
        files = {0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8}
        rows = {0:"h", 1:"g", 2:"f", 3:"e", 4:"d", 5:"c", 6:"b", 7:"a"}
        for i in gs.MoveLog:
          letter1 = rows[i.startCol]
          number1 = files[i.startRow]
          letter2 = rows[i.endCol]
          number2 = files[i.endRow]
          temp = letter1+str(number1)+letter2+str(number2)
          moveloglist.append(temp)
        
        print(moveloglist)
        okbutton = font.render("ok", True, (0, 0, 0), (255, 255, 255))
        okbuttonrect = okbutton.get_rect(topleft = (150, 225))
        ok = True
        Screen.blit(okbutton, (150, 225))
        while ok:
          for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
              mousex, mousey = pygame.mouse.get_pos()
              if okbuttonrect.collidepoint(mousex, mousey):
                running = False
                ok = False
          pygame.display.update()
          Clock.tick(15)
          pygame.display.flip()
        GameOver = True
      Clock.tick(Max_FPS)
      pygame.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
  if sqSelected != ():
    row, col = sqSelected
    if gs.board[row][col][0] == ("w" if gs.WhiteToMove else "b"):
      s = pygame.Surface((SquareSize, SquareSize))
      s.set_alpha(100)
      s.fill(pygame.Color("blue"))
      screen.blit(s, (col*SquareSize, row*SquareSize))
      s.fill(pygame.Color("yellow"))
      for move in validMoves:
        if move.startRow == row and move.startCol == col:
          screen.blit(s, (SquareSize*move.endCol, SquareSize*move.endRow))


def highlightMove(screen, gs):
  if len(gs.MoveLog) != 0:
    square1 = gs.MoveLog[-1].startSq
    square2 = gs.MoveLog[-1].endSq
    s = pygame.Surface((SquareSize, SquareSize))
    s.set_alpha(100)
    s.fill(pygame.Color("green"))
    screen.blit(s, (square1[1]*SquareSize, square1[0]*SquareSize))
    screen.blit(s, (square2[1]*SquareSize, square2[0]*SquareSize))

def drawTakeSquare(screen, gs, validMoves, sqSelected):
  if sqSelected != ():
    row, col = sqSelected
    if gs.board[row][col][0] == ("w" if gs.WhiteToMove else "b"):
      s = pygame.Surface((SquareSize, SquareSize))
      s.set_alpha(100)
      s.fill(pygame.Color("blue"))
      screen.blit(s, (col*SquareSize, row*SquareSize))
      s.fill(pygame.Color("red"))
      for move in validMoves:
        if move.startRow == row and move.startCol == col:
          screen.blit(s, (SquareSize*move.endCol, SquareSize*move.endRow))


def drawGameState(Screen, gs, validMoves, SquareSelected):
  drawBoard(Screen)
  highlightSquares(Screen, gs, validMoves, SquareSelected)
  highlightMove(Screen, gs)
  drawPieces(Screen, gs.board)

def drawTakeGameState(Screen, gs, validMoves, SquareSelected):
  drawBoard(Screen)
  drawTakeSquare(Screen, gs, validMoves, SquareSelected)
  highlightMove(Screen, gs)
  drawPieces(Screen, gs.board)



def drawPieces(screen, board):
  for r in range(Dimension):
    for c in range(Dimension):
      piece = board[r][c]
      if piece != "--":
        screen.blit(IMAGES[piece], pygame.Rect(c*SquareSize, r*SquareSize, SquareSize, SquareSize))


#start of ai
#__________________________________________________________________________________________


NOPIECESWHITE = 1000
STALEMATEWHITE = 1000
STALEMATEBLACK = -1000
NOPIECESBLACK = -1000



def convertBookMoves(bookmoves):
  ranksToRows = {"8": 7, "7": 6, "6": 5, "5": 4, "4": 3, "3": 2, "2": 1, "1": 0}
  filesToCols = {"a":7, "b":6, "c":5, "d":4, "e":3, "f":2, "g":1, "h":0}
  newlog = []
  for j in bookmoves:
    templist = []
    for i in j:
      if i != "--":
        a = str(filesToCols[i[0]])
        b = str(ranksToRows[i[1]])
        c = str(filesToCols[i[2]])
        d = str(ranksToRows[i[3]])
        e = b+a+d+c
        templist.append(e)
      elif i == "--":
        templist.append("--")
    newlog.append(templist)
  return newlog

def convertMoveLog(movelog):
  moves = []
  for i in movelog:
    a = str(i.startRow)
    b = str(i.startCol)
    c = str(i.endRow)
    d = str(i.endCol)
    moves.append(a+b+c+d)
  return moves

def getValue(piece):
  count = 0
  if piece[1] == "P":
    count += 1
  if piece[1] == "R":
    count += 5
  if piece[1] == "N":
    count += 3
  if piece[1] == "B":
    count += 4
  if piece[1] == "K":
    count += 2
  if piece[1] == "Q":
    count += 5
  return count





def findBestMove(validMoves, takeMoves, gs):
  bestmove = False
  book = [
  #h6
  ["e2e3", "h7h6", "f1a6", "--", "d1g4"],
  #h5
  ["e2e3", "h7h5", "d1h5", "--", "f1a6"],
  #g5
  ["e2e3", "g7g5", "f1a6"],
  #g6 with 3. bxa6
  ["e2e3", "g7g6", "d1h5", "g6h5", "f1a6", "b7a6", "g2g4", "h5g4", "g1h3", "g4h3", "e1f1", "--", "f1g2", "h3g2", "d2d4"],
  #g6 with 3. Nxa6
  ["e2e3", "g7g6", "d1h5", "g6h5", "f1a6", "b8a6", "g2g4", "h5g4", "g1h3", "g4h3", "e1f1", "--", "f1g2", "h3g2", "d2d4"],
  #f6
  ["e2e3", "f7f6", "f1a6", "b8a6", "b2b4", "a6b4", "d1f3", "--", "f3b7"],
  #f5
  ["e2e3", "f7f5", "f1a6", "--", "d1g4"],
  #e5
  ["e2e3", "e7e5", "f1a6", "--", "d1h5"],
  #e6
  ["e2e3", "e7e6", "f1a6", "b8a6", "b2b4", "a6b4", "d1f3", "b4a2", "a1a2"],
  #e6 2
  ["e2e3", "e7e6", "f1a6", "b7a6", "d1h5", "f8a3", "b1a3"],
  #d6
  ["e2e3", "d7d6", "d1g4", "c8g4", "e1d1", "g4d1", "b1c3", "d1c2", "f1d3", "c2d3", "c3b5", "d3b5", "g1e2", "b5e2", "h1f1", "e2f1", "h2h3", "f1g2", "f2f4", "g2h3", "f4f5", "h3f5", "e3e4", "f5e4", "d2d3", "e4d3", "a1b1", "d3b1", "b2b3", "b1a2", "c1h6"],
  #d5 with bishop takes
  ["e2e3", "d7d5", "f1a6", "--", "e3e4", "d5e4", "d1g4", "c8g4", "e1d1", "g4d1", "b1c3", "d1c2", "c3e4", "c2e4", "g2g4", "e4h1", "g1f3", "h1f3", "d2d3"],
  #d5 with queen takes
  ["e2e3", "d7d5", "f1a6", "--", "e3e4", "d5e4", "d1g4", "d8d2", "c1d2", "c8g4", "e1d1", "g4d1", "b1c3", "d1c2", "c3e4", "c2e4", "g2g4", "e4h1", "g1f3", "h1f3", "d2d3"],
  #na6
  ["e2e3", "b8a6", "f1a6", "b7a6", "d1e2"]


  ]
  movelog = gs.MoveLog
  book = convertBookMoves(book)
  movelog = convertMoveLog(movelog)
  for i in book:
    if len(i) > len(movelog):
      matching = True
      for j in range(len(movelog)):
        if movelog[j] != i[j]:
          if i[j] != "--":
            matching = False
      if matching == True:
        move = i[len(movelog)]
        bestmove = Move((int(move[0]), int(move[1])), (int(move[2]), int(move[3])), gs.board)
  if bestmove != False:
    return bestmove
    
  else:
    global isPawnPromotion
    global nextMove
    global maxScoreDepth
    maxScoreDepth = None
    nextMove = None
    isPawnPromotion = -1
    if len(takeMoves) != 0:
      movelist = takeMoves
      # DEPTH = 6
    if len(takeMoves) == 0:
      movelist = validMoves
      # DEPTH = 4
    negaMaxAlphaBetaSearch(gs, movelist, DEPTH, NOPIECESBLACK, NOPIECESWHITE, 1)
    return nextMove





def negaMaxAlphaBetaSearch(gs, validMoves, depth, alpha, beta, turnMul):
  global nextMove
  global isPawnPromotion
  global maxScoreDepth
  if depth == 0:
    return turnMul*advancedScore(gs)
  else:
    maxScore = NOPIECESBLACK
    for move in validMoves:
      gs.makeMove(move, "Q", False)
      nextMoves = gs.getAllTakeMoves()
      if len(nextMoves) == 0:
        nextMoves = gs.getAllPossibleMoves()
      if len(nextMoves) == 0:
        score = -1000*turnMul
        if score == 1000:
          if maxScoreDepth == None or maxScoreDepth[0] > DEPTH-depth:
            temp = DEPTH-depth+1
            checkmatemove = gs.MoveLog[-temp]
            maxScoreDepth = [DEPTH-depth, checkmatemove]
      else:
        score = -negaMaxAlphaBetaSearch(gs, nextMoves, depth-1, -beta, -alpha, -turnMul)
      if score > maxScore:
        maxScore = score
        if depth == DEPTH:
          nextMove = move
      gs.undoMove()
      if maxScore > alpha:
        alpha = maxScore
    if depth == DEPTH:
      if maxScoreDepth != None:
        nextMove = maxScoreDepth[1]
    return maxScore



def advancedScore(gs):
  NoWhitePieces = True
  NoBlackPieces = True
  whiteIsUp = 0
  for i in range(len(gs.board)):
    for j in range(len(gs.board[i])):
      if gs.board[i][j][0] == "w":
        NoWhitePieces = False
        whiteIsUp -= getValue(gs.board[i][j])
        if gs.board[i][j][1] == "B":
          whiteIsUp -= findBishopSquares(i, j, "w", gs)
      elif gs.board[i][j][0] == "b":
        NoBlackPieces = False
        whiteIsUp += getValue(gs.board[i][j])
        if gs.board[i][j][1] == "B":
          whiteIsUp += findBishopSquares(i, j, "b", gs)
  if NoWhitePieces:
    return 1000
  elif NoBlackPieces:
    return -1000
  else:
    return whiteIsUp

  
def findBishopSquares(row, col, color, gs):
  bonus = 0
  directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
  enemycolor = "b" if color == "w" else "w"
  for d in directions:
    for i in range(1, 8):
      endRow = row + d[0] * i
      endCol = col + d[1] * i
      if 0 <= endRow < 8 and 0 <= endCol < 8:
        endPiece = gs.board[endRow][endCol]
        if endPiece == "--":
          bonus += 0.1
        elif endPiece[0] == enemycolor:
          bonus += 0.1
          break
        else:
          break
      else:
        break
  return bonus



class GameState():
  def __init__(self):
    
    
    
    self.testing = False
    
    
    if not self.testing:
      self.board = [
        ["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"], 
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"], 
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"], 
        ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR"], 
      ]
    else:
      self.board = [
        ["--", "--", "--", "--", "--", "--", "--", "--"], 
        ["--", "--", "--", "wR", "--", "--", "--", "--"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"], 
        ["--", "--", "--", "--", "--", "--", "bP", "--"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"], 
      ]
    
    self.WhiteToMove = True
    self.MoveLog = []
    self.enPassantPossible = ()
    self.noPieces = "--"
    self.stalemate = "--"
    self.NoWhitePieces = False
    self.NoBlackPieces = False
    self.OnePieceLeft = False

  def makeMove(self, move, engineline = "", playsound = True):
    #takes move object
    self.board[move.startRow][move.startCol] = "--"
    if playsound == True:
      if self.board[move.endRow][move.endCol] != "--":
        takepiece = pygame.mixer.Sound("sounds/takepiece.mp3")
        pygame.mixer.Sound.play(takepiece)
      else:
        movepiece = pygame.mixer.Sound("sounds/movepiece.mp3")
        pygame.mixer.Sound.play(movepiece)
      
    self.board[move.endRow][move.endCol] = move.pieceMoved
    self.MoveLog.append(move)
    self.WhiteToMove = not self.WhiteToMove
      
    
    if move.isPawnPromotion:
      if engineline == "":
        pass
      else:
        self.board[move.endRow][move.endCol] = move.pieceMoved[0] + engineline

    if move.isEnPassantMove:
      self.board[move.startRow][move.endCol] = "--"

    if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
      self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
    else:
      self.enPassantPossible = ()
      

  def undoMove(self):
    if len(self.MoveLog) != 0:
      move = self.MoveLog.pop()
      self.board[move.startRow][move.startCol] = move.pieceMoved
      self.board[move.endRow][move.endCol] = move.pieceCaptured
      self.WhiteToMove = not self.WhiteToMove
      if move.isEnPassantMove:
        self.board[move.endRow][move.endCol] = "--"
        self.board[move.startRow][move.endCol] = move.pieceCaptured
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.enPassantPossible = (move.endRow, move.endCol)

      if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
        self.enPassantPossible = ()
      self.noPieces = ""
      self.stalemate = ""


          
  def getAllTakeMoves(self):
    tempEnPassantPossible = self.enPassantPossible
    moves = []
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        piececolor = self.board[i][j][0]
        if (piececolor == "w" and self.WhiteToMove) or (piececolor == "b" and not self.WhiteToMove):
          piecetype = self.board[i][j][1]
          if piecetype == "P":
            self.getPawnTakeMoves(i, j, moves)
          elif piecetype == "R":
            self.getRookTakeMoves(i, j, moves)
          elif piecetype == "N":
            self.getKnightTakeMoves(i, j, moves)
          elif piecetype == "B":
            self.getBishopTakeMoves(i, j, moves)
          elif piecetype == "Q":
            self.getQueenTakeMoves(i, j, moves)
          elif piecetype == "K":
            self.getKingTakeMoves(i, j, moves)

    self.enPassantPossible = tempEnPassantPossible
    return moves

  
  def getAllPossibleMoves(self):
    moves = []
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        piececolor = self.board[i][j][0]
        if (piececolor == "w" and self.WhiteToMove) or (piececolor == "b" and not self.WhiteToMove):
          piecetype = self.board[i][j][1]
          if piecetype == "P":
            self.getPawnMoves(i, j, moves)
          elif piecetype == "R":
            self.getRookMoves(i, j, moves)
          elif piecetype == "N":
            self.getKnightMoves(i, j, moves)
          elif piecetype == "B":
            self.getBishopMoves(i, j, moves)
          elif piecetype == "Q":
            self.getQueenMoves(i, j, moves)
          elif piecetype == "K":
            self.getKingMoves(i, j, moves)
    return moves

  
  
  def getPawnMoves(self, row, col, list):
    if self.WhiteToMove:
      if self.board[row+1][col] == "--":
        list.append(Move((row, col), (row+1, col), self.board))
        if row == 1 and self.board[row+2][col] == "--":
          list.append(Move((row, col), (row+2, col), self.board))
    
    elif not self.WhiteToMove:
      if self.board[row-1][col] == "--":
        list.append(Move((row, col), (row-1, col), self.board))
        if row == 6 and self.board[row-2][col] == "--":
          list.append(Move((row, col), (row-2, col), self.board))

  def getRookMoves(self, row, col, list):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    enemycolor = "b" if self.WhiteToMove else "w"
    for d in directions:
      for i in range(1, 8):
        endRow = row + d[0] * i
        endCol = col + d[1] * i
        if 0 <= endRow < 8 and 0 <= endCol < 8:
          endPiece = self.board[endRow][endCol]
          if endPiece == "--":
            list.append(Move((row, col), (endRow, endCol), self.board))
          elif endPiece[0] == enemycolor:
            list.append(Move((row, col), (endRow, endCol), self.board))
            break
          else:
            break
        else:
          break

  def getKnightMoves(self, row, col, list):
    directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)]
    friendlycolor = "w" if self.WhiteToMove else "b"
    for d in directions:
      endRow = row + d[0]
      endCol = col + d[1]
      if 0 <= endRow < 8 and 0 <= endCol < 8:
        endPiece = self.board[endRow][endCol]
        if endPiece[0] != friendlycolor:
          list.append(Move((row, col), (endRow, endCol), self.board))

  def getBishopMoves(self, row, col, list):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    enemycolor = "b" if self.WhiteToMove else "w"
    for d in directions:
      for i in range(1, 8):
        endRow = row + d[0] * i
        endCol = col + d[1] * i
        if 0 <= endRow < 8 and 0 <= endCol < 8:
          endPiece = self.board[endRow][endCol]
          if endPiece == "--":
            list.append(Move((row, col), (endRow, endCol), self.board))
          elif endPiece[0] == enemycolor:
            list.append(Move((row, col), (endRow, endCol), self.board))
            break
          else:
            break
        else:
          break

  def getQueenMoves(self, row, col, list):
    self.getBishopMoves(row, col, list)
    self.getRookMoves(row, col, list)

  def getKingMoves(self, row, col, list):
    directions = [(1, 1), (1, -1), (1, 0), (-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1)]
    friendlycolor = "w" if self.WhiteToMove else "b"
    for d in directions:
      endRow = row + d[0]
      endCol = col + d[1]
      if 0 <= endRow < 8 and 0 <= endCol < 8:
        endPiece = self.board[endRow][endCol]
        if endPiece[0] != friendlycolor:
          list.append(Move((row, col), (endRow, endCol), self.board))

  def getPawnTakeMoves(self, row, col, list):
    if self.WhiteToMove:
      if col-1 >= 0:
        if self.board[row+1][col-1][0] == "b":
          list.append(Move((row, col), (row+1, col-1), self.board))
        elif (row+1, col-1) == self.enPassantPossible:
          list.append(Move((row, col), (row+1, col-1), self.board, enPassantPossible=True))
      if col+1 <= 7:
        if self.board[row+1][col+1][0] == "b":
          list.append(Move((row, col), (row+1, col+1), self.board))
        elif (row+1, col+1) == self.enPassantPossible:
          list.append(Move((row, col), (row+1, col+1), self.board, enPassantPossible=True))
    
    elif not self.WhiteToMove:
      if col-1 >= 0:
        if self.board[row-1][col-1][0] == "w":
          list.append(Move((row, col), (row-1, col-1), self.board))
        elif (row-1, col-1) == self.enPassantPossible:
          list.append(Move((row, col), (row-1, col-1), self.board, enPassantPossible=True))
      if col+1 <= 7:
        if self.board[row-1][col+1][0] == "w":
          list.append(Move((row, col), (row-1, col+1), self.board))
        elif (row-1, col+1) == self.enPassantPossible:
          list.append(Move((row, col), (row-1, col+1), self.board, enPassantPossible=True))

  def getRookTakeMoves(self, row, col, list):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    enemycolor = "b" if self.WhiteToMove else "w"
    friendlycolor = "w" if self.WhiteToMove else "b"
    for d in directions:
      for i in range(1, 8):
        endRow = row + d[0] * i
        endCol = col + d[1] * i
        if 0 <= endRow < 8 and 0 <= endCol < 8:
          endPiece = self.board[endRow][endCol]
          if endPiece[0] == enemycolor:
            list.append(Move((row, col), (endRow, endCol), self.board))
            break
          elif endPiece[0] == friendlycolor:
            break
        else:
          break

  def getKnightTakeMoves(self, row, col, list):
    directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)]
    enemycolor = "b" if self.WhiteToMove else "w"
    for d in directions:
      endRow = row + d[0]
      endCol = col + d[1]
      if 0 <= endRow < 8 and 0 <= endCol < 8:
        endPiece = self.board[endRow][endCol]
        if endPiece[0] == enemycolor:
          list.append(Move((row, col), (endRow, endCol), self.board))

  def getBishopTakeMoves(self, row, col, list):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    enemycolor = "b" if self.WhiteToMove else "w"
    friendlycolor = "w" if self.WhiteToMove else "b"
    for d in directions:
      for i in range(1, 8):
        endRow = row + d[0] * i
        endCol = col + d[1] * i
        if 0 <= endRow < 8 and 0 <= endCol < 8:
          endPiece = self.board[endRow][endCol]
          if endPiece[0] == enemycolor:
            list.append(Move((row, col), (endRow, endCol), self.board))
            break
          elif endPiece[0] == friendlycolor:
            break
        else:
          break

  def getQueenTakeMoves(self, row, col, list):
    self.getBishopTakeMoves(row, col, list)
    self.getRookTakeMoves(row, col, list)

  def getKingTakeMoves(self, row, col, list):
    directions = [(1, 1), (1, -1), (1, 0), (-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1)]
    enemycolor = "b" if self.WhiteToMove else "w"
    for d in directions:
      endRow = row + d[0]
      endCol = col + d[1]
      if 0 <= endRow < 8 and 0 <= endCol < 8:
        endPiece = self.board[endRow][endCol]
        if endPiece[0] == enemycolor:
          list.append(Move((row, col), (endRow, endCol), self.board))

class Move():
  ranksToRows = {"8": 7, "7": 6, "6": 5, "5": 4, "4": 3, "3": 2, "2": 1, "1": 0}
  rowsToRanks = {v: k for k, v in ranksToRows.items()}
  filesToCols = {"a":7, "b":6, "c":5, "d":4, "e":3, "f":2, "g":1, "h":0}
  colsToFiles = {v:k for k, v in filesToCols.items()}
  
  def __init__(self, startSq, endSq, board, enPassantPossible = False):
    self.startSq = startSq
    self.endSq = endSq
    self.startRow = startSq[0]
    self.startCol = startSq[1]
    self.endRow = endSq[0]
    self.endCol = endSq[1]
    self.pieceMoved = board[self.startRow][self.startCol]
    self.pieceCaptured = board[self.endRow][self.endCol]
    self.isPawnPromotion = False
    #pawn promotion
    if ((self.pieceMoved == "wP" and self.endRow == 7) or (self.pieceMoved == "bP" and self.endRow == 0)):
      self.isPawnPromotion = True

    #en passant
    self.isEnPassantMove = enPassantPossible
    if self.isEnPassantMove:
      self.pieceCaptured = "bP" if self.pieceMoved == "wP" else "wP"
      
    
    self.moveID = int(str(self.startRow * 1000) + str(self.startCol * 100) + str(self.endRow * 10) + str(self.endCol))

  def __eq__(self, other):
    if isinstance(other, Move):
      return self.moveID == other.moveID
    return False

  def getChessNotation(self):
    return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

  def getRankFile(self, r, c):
    return self.colsToFiles[c] + self.rowsToRanks[r]





if __name__ == "__main__":
  main()
