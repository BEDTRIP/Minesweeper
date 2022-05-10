import pygame, random
from webbrowser import open
#-----------------------------button_class--------------------------------------
class button():
    def set(self, posx, posy, png, info):
        self.posx = posx
        self.posy = posy
        self.width, self.height = png[0].get_rect().size
        self.png = png
        self.info = info

    def hitpoint(self):
        return pygame.Rect(self.posx, self.posy, self.width, self.height)

    def draw(self, scr, i):
        scr.blit(self.png[i], (self.posx, self.posy))
#--------------------------------draw-------------------------------------------
def button_draw(mouse_xy, button1, scr, x = 0, y = 0, a = []):
    global draw_check, flag_count_print, end_time, difficult_count, x_count, y_count
    b = [1, 0]
    if button1.info == 'flag_clock':
        if flag_count_print > 0:
            button1.draw(scr, flag_count_print%10)
            flag_count_print = flag_count_print//10
        else:
            button1.draw(scr, 10)
    elif button1.info == 'clock':
        button1.draw(scr, end_time%10)
        end_time = end_time//10
    elif button1.info == 'difficult_clock':
        button1.draw(scr, difficult_count%10)
        difficult_count = difficult_count//10
    elif button1.info == 'size_x_clock':
        button1.draw(scr, x_count%10)
        x_count = x_count//10
    elif button1.info == 'size_y_clock':
        button1.draw(scr, y_count%10)
        y_count = y_count//10
    elif x == 'check':
        button1.draw(scr, 1)
    else:
        if button1.hitpoint().collidepoint(mouse_xy):
            if draw_check:
                button1.draw(scr, 2)
                draw_check = False
            else:
                if button1.info[1:] == '_pressed':
                    b = UBER_pressed_press(x, y, a)
                button1.draw(scr, 1)
        else:
            button1.draw(scr, 0)
    return b
#-------------------------------------------------------------------------------
def scr_draw(mouse_xy):
    global win_check, lose_check

    scr.fill(GRAY)
    pygame.draw.rect(scr, WHITE, (0, 1, scr_size[0], plus_Y))
    pygame.draw.polygon(scr, GRAY, [[scr_size[0]-1, 1], [scr_size[0]-3, 3], [3, plus_Y-4], [0, plus_Y-1], [scr_size[0], plus_Y]])
    pygame.draw.rect(scr, DlightGRAY, (3, 4,  scr_size[0]-6, plus_Y -8))

    button_draw(mouse_xy, exit_button, scr)
    button_draw(mouse_xy, smile_button, scr)
    button_draw(mouse_xy, count_1_button, scr)
    button_draw(mouse_xy, count_2_button, scr)
    button_draw(mouse_xy, count_3_button, scr)

    for i in range(1, len(PlayMx)-1):
        for j in range(1, len(PlayMx[i])-1):
            button_draw((0, 0), PlayMx[i][j], scr, j, i, PlayMx)

    for i in range(1, len(PlayMx)-1):
        for j in range(1, len(PlayMx[i])-1):
            if PlayMx[i][j].hitpoint().collidepoint(mouse_xy):
                b = button_draw(mouse_xy, PlayMx[i][j], scr, j, i, PlayMx)
                if not b[0]:
                    for k in b[1]:
                        PlayMx[k[1]][k[0]].draw(scr, 1)

    if not(win_check and lose_check):
        button_draw(mouse_xy, lose_button, scr)
        button_draw(mouse_xy, win_button, scr)
        button_draw(mouse_xy, time_count_7_button, scr)
        button_draw(mouse_xy, time_count_6_button, scr)
        button_draw(mouse_xy, time_count_5_button, scr)
        button_draw(mouse_xy, time_count_4_button, scr)
    pygame.display.update()
#-------------------------------------------------------------------------------
def menu_draw(mouse_xy):

    scr.fill(GRAY)
    button_draw(mouse_xy, menu_button, scr)
    button_draw(mouse_xy, exit_menu_button, scr)
    button_draw(mouse_xy, start_menu_button, scr)
    button_draw(mouse_xy, mine_menu_button, scr)
    button_draw(mouse_xy, flag_menu_button, scr)
    button_draw(mouse_xy, author_button, scr)
    button_draw(mouse_xy, difficult_menu_button, scr)
    button_draw(mouse_xy, difficult_menu_switch, scr)
    button_draw(mouse_xy, difficult_clock2, scr)
    button_draw(mouse_xy, difficult_clock1, scr)
    button_draw(mouse_xy, size_x_menu_button, scr)
    button_draw(mouse_xy, size_x_menu_switch, scr)
    button_draw(mouse_xy, size_x_clock2, scr)
    button_draw(mouse_xy, size_x_clock1, scr)
    button_draw(mouse_xy, size_y_menu_button, scr)
    button_draw(mouse_xy, size_y_menu_switch, scr)
    button_draw(mouse_xy, size_y_clock2, scr)
    button_draw(mouse_xy, size_y_clock1, scr)

    pygame.display.flip()
#---------------------------------generation------------------------------------
def generation(count, size_x, size_y):
    PlayMx = [0] *size_y

    for i in range(size_y):
        Mx = []
        for j in range(size_x):
            Z = button()
            Z.set(j*25 -25, plus_Y + i*25 -25, button_scr, 'empty')
            Mx.append(Z)
        PlayMx[i] = Mx

    while count > 0:
        x = random.randint(1, size_x-2)
        y = random.randint(1, size_y-2)
        if PlayMx[y][x].info != 'mine':
            PlayMx[y][x].info = 'mine'
            count -= 1

    for i in range(1, size_y -1):
        for j in range(1, size_x -1):
            if PlayMx[i][j].info == 'empty':
                k = 0
                if PlayMx[i+1][j].info == 'mine':
                    k +=1
                if PlayMx[i-1][j].info == 'mine':
                    k +=1
                for g in range(-1, 2):
                    if PlayMx[i+g][j+1].info == 'mine':
                        k +=1
                    if PlayMx[i+g][j-1].info == 'mine':
                        k +=1
                PlayMx[i][j].info = str(k)
    return PlayMx
#-------------------------------------------------------------------------------
def start_help(a):
    c, x, y = 1, 0, 1
    while c:
        x += 1
        if x == len(a[0])-1:
            y += 1
            x = 0
        elif a[y][x].info == '0':
            a[y][x] = button_press(x, y, a)
            c -= 1
            c = 0
        elif y == len(a)-1:
            c = 0
    return a
#-------------------------------++function--------------------------------------
def pressed_press(info):
    if info[len(info)-5:] == '_flag':
        return True
    else:
        return False
#-------------------------------------------------------------------------------
def pressed_press1(info):
    if info.isdigit() or info[len(info)-1:] == 'e':
        return True
    else:
        return False
#-------------------------------------------------------------------------------
def UBER_pressed_press(x, y, a):
    global win_check, lose_check
    q = []
    k = int(a[y][x].info[:1])
    if pressed_press(a[y][x-1].info):
        k -=1
    if pressed_press(a[y][x+1].info):
        k -=1
    for g in range(-1, 2):
        if pressed_press(a[y+1][x+g].info):
            k -=1
        if pressed_press(a[y-1][x+g].info):
            k -=1
    if k == 0:
        if pressed_press1(a[y][x-1].info):
            q.append((x-1, y))
        if pressed_press1(a[y][x+1].info):
            q.append((x+1, y))
        for g in range(-1, 2):
            if pressed_press1(a[y+1][x+g].info):
                q.append((x+g, y+1))
            if pressed_press1(a[y-1][x+g].info):
                q.append((x+g, y-1))
    if not(win_check and lose_check):
        k = 1
    return [k, q]
#--------------------------------Gameplay---------------------------------------
def button_press(x, y, a):
    global sq_size, count, empty_count
    if a[y][x].info == '0':
        count -= 1
        empty_count -= 1
        a[y][x].png  = [sq_scr[int(a[y][x].info)], sq_scr[int(a[y][x].info)], sq_scr[int(a[y][x].info)]]
        a[y][x].info = 'pressed'

        a[y][x-1] = button_press(x-1, y, a)
        a[y][x+1] = button_press(x+1, y, a)
        for g in range(-1, 2):
            a[y+1][x+g] = button_press(x+g, y+1, a)
            a[y-1][x+g] = button_press(x+g, y-1, a)

    elif a[y][x].info[1:] == '_pressed':
        b = UBER_pressed_press(x, y, a)
        if not b[0]:
            for k in b[1]:
                a[k[1]][k[0]] = button_press(k[0], k[1], a)
                if a[k[1]][k[0]].info == 'pressed_mine':
                    lose()

    elif a[y][x].info.isdigit():
        count -= 1
        empty_count -= 1
        a[y][x].png  = [sq_scr[int(a[y][x].info)], sq_scr[int(a[y][x].info)], sq_scr[int(a[y][x].info)]]
        a[y][x].info += '_pressed'

    elif a[y][x].info == 'mine':
        a[y][x].png  = [mine_scr[1], mine_scr[1], mine_scr[1]]
        a[y][x].info = 'pressed_mine'

    return a[y][x]
#-------------------------------------------------------------------------------
def button_flag(a):
    global flag_count, mine_count, count

    if a.info[len(a.info)-5:] == '_flag' and flag_count != 1000000:
        a.info = a.info[:len(a.info)-5]
        a.png = button_scr
        flag_count += 1
        count += 1
        if a.info == 'mine':
            mine_count += 1

    elif a.info[:7] != 'pressed' and a.info[1:] != '_pressed' and flag_count > 0 and a.info != 'empty':
        count -= 1
        if a.info == 'mine':
            mine_count -= 1
        a.info = a.info + '_flag'
        a.png = [mine_scr[2], mine_scr[2], mine_scr[2]]
        flag_count -= 1

    return a
#-------------------------------------------------------------------------------
def UBER_button_press(a):
    for i in a:
        for j in i:
            if j.info == 'mine':
                j.info = 'pressed_mine'
                j.png  = [mine_scr[0], mine_scr[0], mine_scr[0]]
            elif j.info.isdigit():
                j.png  = [sq_scr[int(j.info)], sq_scr[int(j.info)], sq_scr[int(j.info)]]
            elif j.info[len(j.info)-5:] == '_flag':
                if j.info != 'mine_flag':
                    j.png = [mine_scr[3], mine_scr[3], mine_scr[3]]
    return a
#-------------------------------------------------------------------------------
def lose():
# :)
    global PlayMx, smile_button, lose_smile_scr, mine_count, flag_count, win_check, MIN1, MIN, SEC1, SEC, lose_button, scr_size, lose_scr, clock_scr, time_count_4_button, time_count_5_button, time_count_6_button, time_count_7_button
    PlayMx = UBER_button_press(PlayMx)
    smile_button.png = lose_smile_scr
    flag_count = mine_count
    win_check = 0
    MIN1 = MIN
    SEC1 = SEC
    lose_button.set(scr_size[0]//2 -67, 75, lose_scr, 'menu')
    time_count_4_button.set(scr_size[0]//2 -67 +4,   75 +73, clock_scr, 'clock')
    time_count_5_button.set(scr_size[0]//2 -67 +30,  75 +73, clock_scr, 'clock')
    time_count_6_button.set(scr_size[0]//2 -67 +80,  75 +73, clock_scr, 'clock')
    time_count_7_button.set(scr_size[0]//2 -67 +105, 75 +73, clock_scr, 'clock')
#---------------------------------SYS-PAR---------------------------------------
plus_Y = 75
menu_size = (250, 321)
sq_size = [10, 10]
difficult = 10
fps = 60

BG         = (0, 0, 0)
GRAY       = (88, 88, 88)
LightGRAY  = (195, 195, 195)
DlightGRAY = (167, 167, 167)
WHITE      = (255, 255, 255)
RED        = (180, 0, 0)
#---------------------------------PNG-------------------------------------------
sq_scr = [pygame.image.load('s_0.png'),
pygame.image.load('s_1.png'), pygame.image.load('s_2.png'),
pygame.image.load('s_3.png'), pygame.image.load('s_4.png'),
pygame.image.load('s_5.png'), pygame.image.load('s_6.png'),
pygame.image.load('s_7.png'), pygame.image.load('s_8.png')]

clock_scr = [pygame.image.load('s_c_0.png'),
pygame.image.load('s_c_1.png'), pygame.image.load('s_c_2.png'),
pygame.image.load('s_c_3.png'), pygame.image.load('s_c_4.png'),
pygame.image.load('s_c_5.png'), pygame.image.load('s_c_6.png'),
pygame.image.load('s_c_7.png'), pygame.image.load('s_c_8.png'),
pygame.image.load('s_c_9.png'), pygame.image.load('s_c.png')]

smile_scr = [pygame.image.load('s_smile.png'),
pygame.image.load('s_smile_restart.png'), pygame.image.load('s_smile_pressed.png')]

lose_smile_scr = [pygame.image.load('s_smile_lose.png'),
pygame.image.load('s_smile_restart.png'), pygame.image.load('s_smile_pressed.png')]

win_smile_scr = [pygame.image.load('s_smile_win.png'),
pygame.image.load('s_smile_restart.png'), pygame.image.load('s_smile_pressed.png')]

button_scr = [pygame.image.load('s_empty.png'), pygame.image.load('s_pressed.png'),
pygame.image.load('s_pressed.png'),]

mine_scr = [pygame.image.load('s_mine.png'), pygame.image.load('s_blowed.png'),
pygame.image.load('s_flag.png'), pygame.image.load('s_flag_bad.png')]

exit_scr = [pygame.image.load('s_exit.png'),
pygame.image.load('s_exit_choosed.png'), pygame.image.load('s_exit_choosed.png')]

start_scr = [pygame.image.load('s_start.png'),
pygame.image.load('s_start_choosed.png'), pygame.image.load('s_start_choosed.png')]

win_scr = [pygame.image.load('win.png'),
pygame.image.load('win.png'), pygame.image.load('win.png')]

lose_scr = [pygame.image.load('lose.png'),
pygame.image.load('lose.png'), pygame.image.load('lose.png')]

author_scr = [pygame.image.load('author.png'),
pygame.image.load('author_pressed.png'), pygame.image.load('author_pressed.png')]

menu_scr = [pygame.image.load('logos.png'),
pygame.image.load('logos.png'), pygame.image.load('logos.png')]

switch_1_scr = [pygame.image.load('s_switch_1.png'),
pygame.image.load('s_switch_1.png'), pygame.image.load('s_switch_1.png')]

switch_2_scr = [pygame.image.load('s_switch_2.png'),
pygame.image.load('s_switch_3.png'), pygame.image.load('s_switch_3.png')]
#---------------------------------Menu-buttons----------------------------------
#background
menu_button = button()
menu_button.set(0, 1, menu_scr, 'menu')

#difficult_setting
difficult_menu_button = button()
difficult_menu_button.set(73, 117, switch_1_scr, 'switch_1')
difficult_menu_switch = button()
difficult_menu_switch.set(116, 119, switch_2_scr, 'switch_2')
difficult = 10 + int(20*(difficult_menu_switch.posx -75)/81)

difficult_clock1 = button()
difficult_clock1.set(180, 108, clock_scr, 'difficult_clock')
difficult_clock2 = button()
difficult_clock2.set(205, 108, clock_scr, 'difficult_clock')

#field_size_setting
size_x_menu_button = button()
size_x_menu_button.set(73, 173, switch_1_scr, 'switch_1')
size_x_menu_switch = button()
size_x_menu_switch.set(89, 175, switch_2_scr, 'switch_2')
sq_size[0] = 10 + int(60*(size_x_menu_switch.posx -75)/81)

size_x_clock1 = button()
size_x_clock1.set(180, 164, clock_scr, 'size_x_clock')
size_x_clock2 = button()
size_x_clock2.set(205, 164, clock_scr, 'size_x_clock')

size_y_menu_button = button()
size_y_menu_button.set(73, 229, switch_1_scr, 'switch_1')
size_y_menu_switch = button()
size_y_menu_switch.set(115, 231, switch_2_scr, 'switch_2')
sq_size[1] = 6 + int(29*(size_y_menu_switch.posx -75)/81)

size_y_clock1 = button()
size_y_clock1.set(180, 220, clock_scr, 'size_y_clock')
size_y_clock2 = button()
size_y_clock2.set(205, 220, clock_scr, 'size_y_clock')

#other_buttons
exit_menu_button = button()
exit_menu_button.set(menu_size[0]//2 -65, menu_size[1]-40, exit_scr, 'menu')
start_menu_button = button()
start_menu_button.set(menu_size[0]//2 +5, menu_size[1]-40, start_scr, 'menu')

mine_menu_button = button()
mine_menu_button.set(41, 148, button_scr, 'menu')
flag_menu_button = button()
flag_menu_button.set(41, 204, button_scr, 'menu')

author_button = button()
author_button.set(182, 86, author_scr, 'menu')
#---------------------------------Pre-Game--------------------------------------
pygame.init()
pygame.mixer.init()
scr = pygame.display.set_mode(menu_size)
pygame.display.set_caption('Сапёр')
pygame.display.set_icon(pygame.image.load('icon.ico'))
clock = pygame.time.Clock()
end_time = 0

run1 = False
run = True
#----------------------------------MENU-----------------------------------------
while run:
#Acheve_clock_restart
    MIN = 0
    SEC = 0
    TIME = 0

    clock.tick(fps)
    mouse_xy = pygame.mouse.get_pos()
    draw_check = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = pygame.mouse.get_pressed()
#set_start_button
            if start_menu_button.hitpoint().collidepoint(mouse_xy):
                run1 = True
                draw_check = True
#Game_settings
                win_check = 1
                lose_check = 1
                count = (sq_size[0])*(sq_size[1])
                mine_count = count*difficult//100
                empty_count = count -mine_count
                flag_count = mine_count
                flag_count_print = flag_count

                scr_size = (sq_size[0]*25, sq_size[1]*25 +plus_Y)
                sq_size[0] += 2; sq_size[1] += 2
                scr = pygame.display.set_mode(scr_size)
#level_generation
                PlayMx = generation(mine_count, sq_size[0], sq_size[1])
                PlayMx = start_help(PlayMx)
#Add-game-buttons
                exit_button = button()
                exit_button.set(10, 11, exit_scr, 'menu')
                smile_button = button()
                smile_button.set(scr_size[0]//2-25, 11, smile_scr, 'menu')
                count_1_button = button()
                count_1_button.set(scr_size[0]-35, 11, clock_scr, 'flag_clock')
                count_2_button = button()
                count_2_button.set(scr_size[0]-60, 11, clock_scr, 'flag_clock')
                count_3_button = button()
                count_3_button.set(scr_size[0]-85, 11, clock_scr, 'flag_clock')

                win_button = button()
                win_button.set(-1000, -1000, win_scr, 'menu')
                lose_button = button()
                lose_button.set(-1000, -1000, lose_scr, 'menu')

                time_count_4_button = button()
                time_count_4_button.set(-100, -100, clock_scr, 'clock')
                time_count_5_button = button()
                time_count_5_button.set(-100, -100, clock_scr, 'clock')
                time_count_6_button = button()
                time_count_6_button.set(-100, -100, clock_scr, 'clock')
                time_count_7_button = button()
                time_count_7_button.set(-100, -100, clock_scr, 'clock')
#set_other_menu_buttons
            elif exit_menu_button.hitpoint().collidepoint(mouse_xy):
                run = False
            elif author_button.hitpoint().collidepoint(mouse_xy):
                if mouse_pressed[0] or mouse_pressed[2]:
                    open('https://vk.com/odnako_zdrastvyite', new=2)
            elif mine_menu_button.hitpoint().collidepoint(mouse_xy):
                if mouse_pressed[0] and mine_menu_button.png[0] != mine_scr[1]:
                    mine_menu_button.png = [mine_scr[1], mine_scr[1], mine_scr[1]]
                else:
                    mine_menu_button.png = button_scr
            elif flag_menu_button.hitpoint().collidepoint(mouse_xy):
                if mouse_pressed[2] and flag_menu_button.png[0] != mine_scr[2]:
                    flag_menu_button.png = [mine_scr[2], mine_scr[2], mine_scr[2]]
                else:
                    flag_menu_button.png = button_scr
#set_switch_options
            elif difficult_menu_button.hitpoint().collidepoint(mouse_xy) and (mouse_pressed[0] or mouse_pressed[2]):
                if mouse_xy[0] < 83:
                    difficult_menu_switch.posx = 75
                elif mouse_xy[0] > 163:
                    difficult_menu_switch.posx = 156
                else:
                    difficult_menu_switch.posx = mouse_xy[0] -8
                difficult = 10 + int(20*(difficult_menu_switch.posx -75)/81)
            elif size_x_menu_button.hitpoint().collidepoint(mouse_xy) and (mouse_pressed[0] or mouse_pressed[2]):
                if mouse_xy[0] < 83:
                    size_x_menu_switch.posx = 75
                elif mouse_xy[0] > 163:
                    size_x_menu_switch.posx = 156
                else:
                    size_x_menu_switch.posx = mouse_xy[0] -8
                sq_size[0] = 10 + int(60*(size_x_menu_switch.posx -75)/81)
            elif size_y_menu_button.hitpoint().collidepoint(mouse_xy) and (mouse_pressed[0] or mouse_pressed[2]):
                if mouse_xy[0] < 83:
                    size_y_menu_switch.posx = 75
                elif mouse_xy[0] > 163:
                    size_y_menu_switch.posx = 156
                else:
                    size_y_menu_switch.posx = mouse_xy[0] -8
                sq_size[1] = 6 + int(29*(size_y_menu_switch.posx -75)/81)
#why_switch_is_special_button
        elif event.type == pygame.MOUSEMOTION:
            mouse_pressed = pygame.mouse.get_pressed()
            if difficult_menu_button.hitpoint().collidepoint(mouse_xy) and (mouse_pressed[0] or mouse_pressed[2]):
                if mouse_xy[0] < 83:
                    difficult_menu_switch.posx = 75
                elif mouse_xy[0] > 163:
                    difficult_menu_switch.posx = 156
                else:
                    difficult_menu_switch.posx = mouse_xy[0] -8
                difficult = 10 + int(20*(difficult_menu_switch.posx -75)/81)
            elif size_x_menu_button.hitpoint().collidepoint(mouse_xy) and (mouse_pressed[0] or mouse_pressed[2]):
                if mouse_xy[0] < 83:
                    size_x_menu_switch.posx = 75
                elif mouse_xy[0] > 163:
                    size_x_menu_switch.posx = 156
                else:
                    size_x_menu_switch.posx = mouse_xy[0] -8
                sq_size[0] = 10 + int(60*(size_x_menu_switch.posx -75)/81)
            elif size_y_menu_button.hitpoint().collidepoint(mouse_xy) and (mouse_pressed[0] or mouse_pressed[2]):
                if mouse_xy[0] < 83:
                    size_y_menu_switch.posx = 75
                elif mouse_xy[0] > 163:
                    size_y_menu_switch.posx = 156
                else:
                    size_y_menu_switch.posx = mouse_xy[0] -8
                sq_size[1] = 6 + int(29*(size_y_menu_switch.posx -75)/81)
#menu_clocks_set
    difficult_count = difficult
    x_count = sq_size[0]
    y_count = sq_size[1]
    menu_draw(mouse_xy)
#----------------------------------GAME-----------------------------------------
    while run1:
#set_acheve_time
        clock.tick(fps)
        TIME += 1
        if TIME == 60:
            SEC += 1
            TIME = 0
        if SEC == 60:
            MIN += 1
            SEC = 0
#other_underground_stuff
        play_check = 0
        draw_check = False
        mouse_xy = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run1 = False
                run  = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.hitpoint().collidepoint(mouse_xy):
                    run1 = False
                    scr = pygame.display.set_mode(menu_size)
                    sq_size[0] -= 2; sq_size[1] -= 2
                elif smile_button.hitpoint().collidepoint(mouse_xy):
                    draw_check = True
                    smile_button.png = smile_scr
#Acheve_clock_restart
                    MIN = 0
                    SEC = 0
                    TIME = 0
#Game_settings_restart
                    win_check = 1
                    lose_check = 1
                    count = (sq_size[0]-2)*(sq_size[1]-2)
                    mine_count = count*difficult//100
                    empty_count = count -mine_count
                    flag_count = mine_count
                    flag_count_print = flag_count

                    win_button.set(-1000, -1000, win_scr, 'menu')
                    lose_button.set(-1000, -1000, lose_scr, 'menu')

                    time_count_4_button.set(-100, -100, clock_scr, 'clock')
                    time_count_5_button.set(-100, -100, clock_scr, 'clock')
                    time_count_6_button.set(-100, -100, clock_scr, 'clock')
                    time_count_7_button.set(-100, -100, clock_scr, 'clock')
#level_generation
                    PlayMx = generation(mine_count, sq_size[0], sq_size[1])
                    PlayMx = start_help(PlayMx)
#Left/right_mouse_button_check
                mouse_pressed = pygame.mouse.get_pressed()
                if win_check and lose_check:
                    for i in range(len(PlayMx)):
                        for j in range(len(PlayMx[i])):
                            if PlayMx[i][j].hitpoint().collidepoint(mouse_xy):
                                if mouse_pressed[2]:
                                    PlayMx[i][j] = button_flag(PlayMx[i][j])
                                elif mouse_pressed[0]:
                                    draw_check = True
                                    PlayMx[i][j] = button_press(j, i, PlayMx)
#if_u_lose
                                    if PlayMx[i][j].info == 'pressed_mine' and lose_check:
                                        lose()
#if_u_won
        if (mine_count == 0 or empty_count == 0) and win_check:
            PlayMx = UBER_button_press(PlayMx)
            smile_button.png = win_smile_scr
            flag_count = mine_count
            lose_check = 0
            win_check = 0
            MIN1 = MIN
            SEC1 = SEC
            win_button.set(scr_size[0]//2 -67, 75, win_scr, 'menu')
            time_count_4_button.set(scr_size[0]//2 -67 +4,   75 +52, clock_scr, 'clock')
            time_count_5_button.set(scr_size[0]//2 -67 +30,  75 +52, clock_scr, 'clock')
            time_count_6_button.set(scr_size[0]//2 -67 +80,  75 +52, clock_scr, 'clock')
            time_count_7_button.set(scr_size[0]//2 -67 +105, 75 +52, clock_scr, 'clock')
#game_clocks_set
        flag_count_print = flag_count
        if not(win_check and lose_check):
            end_time = 10000 + MIN1*100 + SEC1
        scr_draw(mouse_xy)
pygame.quit()
