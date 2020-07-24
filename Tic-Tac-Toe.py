import pygame as pyg
import time, random, sys
pyg.init()
run = True
gameover = False

# Game window
screenSize = 600
win = pyg.display.set_mode((screenSize, screenSize))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

transparent = pyg.Surface((screenSize, screenSize))
transparent.fill(black)
transparent.set_alpha(200)

# Grid array
grid = [['', '', ''], ['', '', ''], ['', '', '']]
total = 0
tie = False

# Players
p1 = 'X'
p1_turn = True
p2 = 'O'
p2_turn = False

# Generates text
def create_text(text, name, font_size, text_color, location):
    font = pyg.font.SysFont(name, font_size, bold = True)
    ren = font.render(text, True, text_color)
    win.blit(ren, (screenSize/2 - ren.get_rect().width/2, screenSize/2 - location))

# Uses mouse input to determine location of player moves
def take_turn(x, y):
    global grid, p1_turn, p2_turn, total
    if grid[x][y] == '':
        if p1_turn:
            grid[x][y] = 'X'
            p1_turn = False
            p2_turn = True
        else:
            grid[x][y] = 'O'
            p1_turn = True
            p2_turn = False
        total += 1

# Draws an X given an x,y position for its center
def draw_X(center_x, center_y):
    x1 = center_x - (screenSize/3)/4
    y1 = center_y - (screenSize/3)/4
    x2 = center_x + (screenSize/3)/4
    y2 = center_y + (screenSize/3)/4
    pyg.draw.line(win, blue, (x1, y1), (x2, y2), width = 5)
    
    x1 = center_x + (screenSize/3)/4
    y1 = center_y - (screenSize/3)/4
    x2 = center_x - (screenSize/3)/4
    y2 = center_y + (screenSize/3)/4
    pyg.draw.line(win, blue, (x1, y1), (x2, y2), width = 5)

# Updates display
def draw():
    pyg.display.set_caption("Tic-Tac-Toe")
    win.fill(black)
    
    # Grid
    pyg.draw.line(win, white, (screenSize/3, 0), (screenSize/3, screenSize), width = 5)
    pyg.draw.line(win, white, (screenSize/3 * 2, 0), (screenSize/3 * 2, screenSize), width = 5)
    pyg.draw.line(win, white, (0, screenSize/3), (screenSize, screenSize/3), width = 5)
    pyg.draw.line(win, white, (0, screenSize/3 * 2), (screenSize, screenSize/3 * 2), width = 5)
    
    # Player moves
    for r in range(3):
        for c in range(3):
            if grid[r][c] == None:
                pass
            elif grid[r][c] == 'X':
                center_x = c*(screenSize/3) + (screenSize/3)//2
                center_y = r*(screenSize/3) + (screenSize/3)//2
                draw_X(center_x, center_y)
            elif grid[r][c] == 'O':
                pyg.draw.circle(win, red, (c*(screenSize/3) + (screenSize/3)//2, r*(screenSize/3) + (screenSize/3)//2), screenSize//8, width = 5)

# Checks if game is over
def check_win():
    global gameover, tie
    if grid[0][0] == grid[0][1] and grid[0][1] == grid[0][2] and grid[0][0] != '':
        gameover = True
    elif grid[1][0] == grid[1][1] and grid[1][1] == grid[1][2] and grid[1][0] != '':
        gameover = True
    elif grid[2][0] == grid[2][1] and grid[2][1] == grid[2][2] and grid[2][0] != '':
        gameover = True
    elif grid[0][0] == grid[1][0] and grid[1][0] == grid[2][0] and grid[0][0] != '':
        gameover = True
    elif grid[0][1] == grid[1][1] and grid[1][1] == grid[2][1] and grid[0][1] != '':
        gameover = True
    elif grid[0][2] == grid[1][2] and grid[1][2] == grid[2][2] and grid[0][2] != '':
        gameover = True
    elif grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2] and grid[0][0] != '':
        gameover = True
    elif grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0] and grid[0][2] != '':
        gameover = True
    elif total == 9:
        gameover = True
        tie = True
    
def gameloop():
    global grid, p1_turn, p2_turn, gameover, total, tie, run
    # Resetting variables if another game is played
    grid = [['', '', ''], ['', '', ''], ['', '', '']]
    p1_turn = True
    p2_turn = False
    gameover = False
    total = 0
    tie = False
    
    while run:
        # Gameover screen
        while gameover:
            win.fill(black)
            for e in pyg.event.get():
                if e.type == pyg.QUIT:
                    run = False
                    gameover = False
                    pyg.quit()
                    sys.exit()
                if e.type == pyg.MOUSEBUTTONUP:
                    gameover = False
                    gameloop()
            victory = str()
            
            if tie:
                victory = "DRAW"
            elif not p1_turn:
                victory = "Player 1 wins!"
            elif not p2_turn:
                victory = "Player 2 wins!"
            draw()
            win.blit(transparent, (0, 0))
            create_text("GAME OVER", "Courier", 48, white, 150)
            create_text(victory, "Courier", 36, white, 60)
            create_text("Click anywhere to play again", "Courier", 18, white, -25)
            pyg.display.update()
            
        # Main game
        for e in pyg.event.get():
            # Clicking X to quit
            if e.type == pyg.QUIT:
                run = False
                pyg.quit()
                sys.exit()
            
            # Mouse position
            m_x,m_y = pyg.mouse.get_pos()
            
            # Mouse position relative to grid; determines locations of moves made
            if e.type == pyg.MOUSEBUTTONUP:
                # Row 1
                if m_x < screenSize/3 and m_y < screenSize/3:
                    take_turn(0, 0)
                elif m_x > screenSize/3 and m_x < screenSize/3 * 2 and m_y < screenSize/3:
                    take_turn(0, 1)
                elif m_x > screenSize/3 * 2 and m_y < screenSize/3:
                    take_turn(0, 2)
                # Row 2
                elif m_x < screenSize/3 and m_y > screenSize/3 and m_y < screenSize/3 * 2:
                    take_turn(1, 0)
                elif m_x > screenSize/3 and m_x < screenSize/3 * 2 and m_y > screenSize/3 and m_y < screenSize/3 * 2:
                    take_turn(1, 1)
                elif m_x > screenSize/3 * 2 and m_y > screenSize/3 and m_y < screenSize/3 * 2: 
                    take_turn(1, 2)
                # Row 3
                elif m_x < screenSize/3 and m_y > screenSize/3 * 2:
                    take_turn(2, 0)
                elif m_x > screenSize/3 and m_x < screenSize/3 * 2 and m_y > screenSize/3 * 2:
                    take_turn(2, 1)
                elif m_x > screenSize/3 * 2 and m_y > screenSize/3 * 2:
                    take_turn(2, 2)
        draw()
        pyg.display.update()
        check_win()

gameloop()
