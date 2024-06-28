import pygame
from settings import *
import random
import time

random.seed(0)

def draw_background():
    screen.fill(BACKGROUND_COLOR)

def init_cell():
    cells=[]
    for i in range (size):
        t1=[]
        for j in range(size):
            t1.append(0)
        cells.append(t1)

    return(cells)

def draw_grid():
    for i in range (20,581,cell_width):
        pygame.draw.line(screen, DARK_GRAY, (i,20),(i,580), 1)
        pygame.draw.line(screen, DARK_GRAY, (20,i),(580,i), 1)


def gen_buttons():
    x,y,w,h=640,20,100,30
    buttons=[]
    buttons.append({'name': 'Small', 'coordinates': (x,y,w,h)})
    y=y+h+10
    buttons.append({'name': 'Medium', 'coordinates': (x,y,w,h)})
    y=y+h+10
    buttons.append({'name': 'Big', 'coordinates': (x,y,w,h)})
    y=y+h+10
    buttons.append({'name': 'Start', 'coordinates': (x,y,w,h)})
    y=y+h+10
    buttons.append({'name': 'Stop', 'coordinates': (x,y,w,h)})

    return(buttons)

def draw_buttons():
    
    for b in buttons:
        pygame.draw.rect(screen, GRAY, b['coordinates'])
        pygame.draw.rect(screen, BLACK, b['coordinates'], 3)
        text=font.render(b['name'], True, BLACK)
        screen.blit(text, (b['coordinates'][0]+10,b['coordinates'][1]+3))
    
    if selected!=-1:
        pygame.draw.rect(screen, PINK, buttons[selected]['coordinates'])
        pygame.draw.rect(screen, BLACK, buttons[selected]['coordinates'], 3)
        text=font.render(buttons[selected]['name'], True, BLACK)
        screen.blit(text, (buttons[selected]['coordinates'][0]+10,buttons[selected]['coordinates'][1]+3))

    # pygame.draw.rect(screen, GRAY, buttons[-1]['coordinates'])
    # pygame.draw.rect(screen, BLACK,  buttons[-1]['coordinates'], 3)
    # text=font.render( buttons[-1]['name'], True, BLACK)
    # screen.blit(text, ( buttons[-1]['coordinates'][0]+30, buttons[-1]['coordinates'][1]+3))

def get_cell_size():
    match selected:
        case 0:
            return(56, 560//56)
        case 1:
            return(40, 560//40)
        case 2:
            return(20, 560//20)

def draw_cell(x,y, color):
    x=(x-20)//cell_width
    y=(y-20)//cell_width
    cells[y][x]=1

    x=x*cell_width+20+5
    y=y*cell_width+20+5

    pygame.draw.rect(screen, color, (x,y,cell_width-9,cell_width-9))


def draw_update(row, col, status):
    x=col*cell_width+20+5
    y=row*cell_width+20+5
    if status==1:
        color=WHITE
    else:
        color=BACKGROUND_COLOR
    pygame.draw.rect(screen, color, (x,y,cell_width-9,cell_width-9))


def update_cells():
    global cells

    updated_cells=init_cell()

    for row in range(len(cells)):
        for col in range (len(cells)):
            alive=0
            for i in range(0,3):
                for j in range (0,3):
                    if (i!=1 or j!=1) and row-1+i>=0 and row-1+i<len(cells) and col-1+j>=0 and col-1+j<len(cells):
                        if cells[row-1+i][col-1+j]==1:
                            alive+=1
            if cells[row][col]==1:
                if alive<2 or alive>3:
                    updated_cells[row][col]=0
                else:
                    updated_cells[row][col]=1
            else:
                if alive==3:
                    updated_cells[row][col]=1
            draw_update(row,col, updated_cells[row][col])
    
    cells=updated_cells
    



if __name__=='__main__':

    pygame.init()
    clock=pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
    pygame.display.set_caption('Campo minato♥')
    font = pygame.font.SysFont('arial', 20)

    #28, 40, 56, 80
    #20, 14, 10, 7
    cell_width=560
    size=0
    selected = -1
    selected_game=-1
    game_started = False

    draw_background()
    draw_grid()
    buttons=gen_buttons()
    draw_buttons()
    cells=init_cell()



    run  = True

    number=0

    while run:

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]:
                x,y=pygame.mouse.get_pos()
                if(not(game_started) and cell_width!=560 and x>=20 and x<=560 and y>=20 and y<=560):
                    draw_cell(x,y,WHITE)
                else:
                    for i in range (len(buttons)):
                        if(x>=buttons[i]['coordinates'][0] and x<=buttons[i]['coordinates'][0]+buttons[i]['coordinates'][2] and y>=buttons[i]['coordinates'][1] and y<=buttons[i]['coordinates'][1]+buttons[i]['coordinates'][3]):
                            if(i<len(buttons)-2):
                                selected=i
                                game_started=False
                                draw_background()
                                draw_buttons()
                                cell_width, size=get_cell_size()
                                cells=init_cell()
                                draw_grid()
                                
                                break
                            elif(i==3):
                                print("start")
                                print(selected)
                                draw_buttons()
                                if game_started==False:
                                    selected_game=selected
                                    game_started=True
                            elif(i==4):
                                print("stop")
                                draw_buttons()

                                game_started=False
                    else:
                        selected=-1
                        draw_buttons()


        if game_started:
            update_cells()
            time.sleep(0.3)
            # if (event.type == pygame.KEYDOWN):
            #     pass


        pygame.display.flip()
        clock.tick(30)
        

    pygame.quit()