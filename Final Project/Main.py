import pygame, GameTools, MiscTools
pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("[SPEEDHACK]")

matrix = {
    11: 0, 12: 0, 13: 0, 14: 0,
    21: 0, 22: 0, 23: 0, 24: 0,
    31: 0, 32: 0, 33: 0, 34: 0,
    41: 0, 42: 0, 43: 0, 44: 0
}

levelkey =  {1: (30, 32), 2: (45, 64), 3: (60, 128), 4: (75, 256), 5: (90, 512), 6: (105, 1024), 7: (120, 2048)}
clock = pygame.time.Clock()

dt = 0
blink = 0
plinks = 0
level = 1
freeplay = False
levelup = False
running = True
menuopen = False
menurestart = True
menuexit = False
soundplayed = False
lfadeprogress = 0
wfadeprogress = 0

backgroundmusic = pygame.mixer.music.load("backgroundmusic.mp3")
glassbreak = pygame.mixer.Sound("glassbreak.mp3")
winsound = pygame.mixer.Sound("winsound.mp3")
delsound = pygame.mixer.Sound("delete.mp3")
multsound = pygame.mixer.Sound("multiply.mp3")
levelupsound = pygame.mixer.Sound("levelupsound.mp3")

scanlines = pygame.image.load("overlay.png").convert_alpha()
crosshair = pygame.image.load("crosshair.png").convert_alpha()
failoverlay = pygame.image.load("failoverlay.png").convert_alpha()
winoverlay = pygame.image.load("winoverlay.png").convert_alpha()
cheatoverlay = pygame.image.load("cheatoverlay.png").convert_alpha()
main_background = pygame.image.load("background.png").convert_alpha()
menurestartimage = pygame.image.load("menurestart.png").convert_alpha()
menuexitimage = pygame.image.load("menuexit.png").convert_alpha()

tut1 = pygame.image.load("tut1.png").convert_alpha()
tut2 = pygame.image.load("tut2.png").convert_alpha()
tut3 = pygame.image.load("tut3.png").convert_alpha()
tut4 = pygame.image.load("tut4.png").convert_alpha()
tut5 = pygame.image.load("tut5.png").convert_alpha()
tut6 = pygame.image.load("tut6.png").convert_alpha()
tut7 = pygame.image.load("tut7.png").convert_alpha()
tut8 = pygame.image.load("tut8.png").convert_alpha()
tut9 = pygame.image.load("tut9.png").convert_alpha()


timer_font = pygame.font.Font("mono.ttf", 64)
objective_font = pygame.font.Font("mono.ttf", 32)
dmitri_font = pygame.font.Font("mono.ttf", 18)
font = pygame.font.Font("7segments.ttf", 72)

def print_matrix():
    offsetx=320
    offsety=20
    colors = {
        0: (15, 35, 15),
        2: (30, 100, 30),
        4: (40, 120, 40),
        8: (55, 140, 55),
        16: (70, 160, 70),
        32: (85, 180, 85),
        64: (100, 200, 100),
        128: (120, 220, 120),
        256: (140, 240, 140),
        512: (160, 255, 160),
        1024: (180, 255, 180),
        2048: (200, 255, 200)
    }

    for element in matrix.keys():
        rect = pygame.Rect(offsetx, offsety, 160, 160)
        surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        surf.fill((colors[matrix[element]]))
        font.set_bold(True)
        if matrix[element] == 0:
            text = font.render(str(matrix[element]), True, (15, 35, 15))
        else:
            text = font.render(str(matrix[element]), True, (255, 255, 255))
        text_rect = text.get_rect(center=(rect.w / 2, rect.h / 2))
        surf.blit(text, text_rect)
        screen.blit(surf, (offsetx, offsety))
        if (element-4) % 10 == 0:
            offsetx = 320
            offsety += 160
        else:
            offsetx += 160

def restart():
    matrix = {
    11: 0, 12: 0, 13: 0, 14: 0,
    21: 0, 22: 0, 23: 0, 24: 0,
    31: 0, 32: 0, 33: 0, 34: 0,
    41: 0, 42: 0, 43: 0, 44: 0}
    GameTools.new_tile(matrix)
    GameTools.new_tile(matrix)
    return matrix


defaulttext = [">Press Key to",
"Select Option...",
"1) Tutorial",
"2) DESTROY Powerup",
"3) DOUBLER Powerup",
"4) Free Play",
"5) Restart Level"]

dmitritext = defaulttext
cheats = False
gameover = False
win = False
text = ""
msleft = (levelkey[level][0])*1000

delthreshold = 32
multthreshold = 1

tutorialopen = False
powerup = ""
destroy = 0
multiply = 0
slide = 1

pygame.mixer.music.play(-1)
GameTools.new_tile(matrix)
GameTools.new_tile(matrix)
print_matrix()

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if menuopen == False and tutorialopen == False and levelup == False and win == False and gameover == False:
            if event.type == pygame.MOUSEBUTTONDOWN and powerup:
                offsetx, offsety = 320, 20
                for tile in matrix:
                    rect = pygame.Rect(offsetx, offsety, 160, 160)
                    if (tile - 4) % 10 == 0:
                        offsetx = 320
                        offsety += 160
                    else:
                        offsetx += 160
                    if rect.collidepoint(event.pos):
                        if powerup == "destroy" and 0 < matrix[tile]:
                            if cheats == False:
                                matrix[tile] = 0
                                powerup = ""
                                destroy -= 1
                                dmitritext = defaulttext
                            if cheats == True:
                                matrix[tile] = 0
                            delsound.play()
                        elif cheats == False and powerup == "multiply" and matrix[tile] < 128 and matrix[tile] > 0:
                            matrix[tile] *= 2
                            powerup = ""
                            multiply -= 1
                            dmitritext = defaulttext
                            multsound.play()
                        elif cheats == True and powerup == "multiply" and matrix[tile] > 0:
                            matrix[tile] *= 2
                            multsound.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    oldmatrix = matrix.copy()
                    GameTools.move_right(matrix)
                    if matrix != oldmatrix:
                        GameTools.new_tile(matrix)
                elif event.key == pygame.K_LEFT:
                    oldmatrix = matrix.copy()
                    GameTools.move_left(matrix)
                    if matrix != oldmatrix:
                        GameTools.new_tile(matrix)
                elif event.key == pygame.K_UP:
                    oldmatrix = matrix.copy()
                    GameTools.move_up(matrix)
                    if matrix != oldmatrix:
                        GameTools.new_tile(matrix)
                elif event.key == pygame.K_DOWN:
                    oldmatrix = matrix.copy()
                    GameTools.move_down(matrix)
                    if matrix != oldmatrix:
                        GameTools.new_tile(matrix)
                elif event.key == pygame.K_c:
                    if cheats == True:
                        cheats = False
                    else: cheats = True
                elif event.key == pygame.K_1:
                    tutorialopen = True
                elif event.key == pygame.K_2 and (freeplay == False or cheats == True):
                    if cheats == True or destroy > 0:
                        powerup = "destroy"
                elif event.key == pygame.K_3 and (freeplay == False or cheats == True):
                    if cheats == True or multiply > 0:
                        powerup = "multiply"
                elif event.key == pygame.K_4:
                    matrix = restart()
                    if freeplay == False:
                        freeplay = True
                        defaulttext = [">Press Key to",
                         "Select Option...",
                         "1) Tutorial",
                         "POWERUPS DISABLED",
                         "IN FREE PLAY",
                         "4) Timed Mode",
                         "5) Restart Level"]
                    elif freeplay == True:
                        freeplay = False
                        defaulttext = [">Press Key to",
                         "Select Option...",
                         "1) Tutorial",
                         "2) DESTROY Powerup",
                         "3) DOUBLER Powerup",
                         "4) Free Play",
                         "5) Restart Level"]
                        matrix = restart()
                        level = 1
                        msleft = (levelkey[level][0]) * 1000
                        lfadeprogress = 0
                        wfadeprogress = 0
                        menuopen = False
                        gameover = False
                        soundplayed = False
                        destroy = 0
                        multiply = 0
                        powerup = ""
                        delthreshold = 32
                        multthreshold = 1
                    dmitritext = defaulttext
                elif event.key == pygame.K_5:
                    matrix = restart()
                    lfadeprogress = 0
                    menuopen = False
                    msleft = (levelkey[level][0]) * 1000
                    gameover = False
                    soundplayed = False
                    destroy = 0
                    powerup = ""
                    delthreshold = 32
                elif (event.key == pygame.K_ESCAPE
                      and powerup):
                    powerup = ""
                    dmitritext = defaulttext
                elif event.key == pygame.K_ESCAPE and not powerup:
                    menuopen = True
        elif tutorialopen == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_1:
                    tutorialopen = False
                elif event.key == pygame.K_LEFT:
                    if slide > 1:
                        slide -= 1
                elif event.key == pygame.K_RIGHT:
                    if slide < 9:
                        slide += 1
        elif menuopen == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menuopen = False
                elif event.key == pygame.K_UP:
                    menurestart = True
                    menuexit = False
                elif event.key == pygame.K_DOWN:
                    menurestart = False
                    menuexit = True
                elif event.key == pygame.K_RETURN:
                    if menurestart == True:
                        win = False
                        matrix = restart()
                        level = 1
                        msleft = (levelkey[level][0]) * 1000
                        lfadeprogress = 0
                        wfadeprogress = 0
                        menuopen = False
                        gameover = False
                        soundplayed = False
                        destroy = 0
                        multiply = 0
                        powerup = ""
                        delthreshold = 32
                        multthreshold = 1
                        pygame.mixer.music.play(-1)
                    elif menuexit == True:
                        running = False

        for tile in matrix.values():
            if tile >= delthreshold:
                destroy += 1
                delthreshold *= 2
        if level > multthreshold:
            multiply += 1
            multthreshold += 1

    screen.fill((0, 0, 0))
    screen.blit(main_background, (0, 0))
    print_matrix()

    for tile in matrix:
        if freeplay == False:
            if matrix[tile] == levelkey[level][1]:
                if level < 7:
                    level += 1
                    levelup = True
        if matrix[tile] == 2048:
            win = True

    if levelup == True:
        plinks += dt


    for i in range(7):
        if len(dmitritext) > i:
            render = dmitri_font.render(dmitritext[i], True, (255, 255, 255))
            i += 1
            screen.blit(render, (60, 400 + (10 + (render.get_rect().height))*i))

    if tutorialopen == False and menuopen == False and levelup == False and freeplay == False and cheats == False and win == False and gameover == False:
        msleft -= dt
    if msleft <= 0:
        msleft = 0
        gameover = True
    seconds = msleft // 1000
    centiseconds = (msleft % 1000) // 10
    text = f'{seconds}.{centiseconds:02d}'
    if freeplay == False:
        timer_display = timer_font.render(text, True, (255, 255, 255))
        timerdisplay_rect = timer_display.get_rect()
        screen.blit(timer_display, (1120-timerdisplay_rect.width/2, 150))
    else:
        timer_display = timer_font.render("N/A", True, (255, 255, 255))
        timerdisplay_rect = timer_display.get_rect()
        screen.blit(timer_display, (1120 - timerdisplay_rect.width / 2, 150))
    if freeplay == False:
        leveldisplay = objective_font.render("Level: " + str(level), True, (255, 255, 255))
        objectivedisplay = objective_font.render(f"Goal: {levelkey[level][1]}", True, (255, 255, 255))
        destroytext = objective_font.render(f"Destroys: {destroy}", True, (255, 255, 255))
        multiplytext = objective_font.render(f"Doublers: {multiply}", True, (255, 255, 255))
        screen.blit(objectivedisplay,(1120 - objectivedisplay.get_rect().width / 2, 490 + destroytext.get_rect().height))
        screen.blit(destroytext, (1120 - destroytext.get_rect().width / 2, 500 + destroytext.get_rect().height * 2))
        screen.blit(multiplytext, (1120 - multiplytext.get_rect().width / 2, 510 + multiplytext.get_rect().height * 3))
    else:
        leveldisplay = objective_font.render("Free Play", True, (255, 255, 255))
    screen.blit(leveldisplay, (1120 - leveldisplay.get_rect().width / 2, 480))

    if powerup:
        dmitritext = (">Hacking into", "the Matrix...", "", "Click Block to Use", "Selected Powerup", "", "ESC to Cancel")
        crosshairrect = crosshair.get_rect()
        mousex, mousey = pygame.mouse.get_pos()
        screen.blit(crosshair, (mousex - crosshairrect.width/2, mousey - crosshairrect.height/2))

    if cheats == False and win == False and ((gameover == True and freeplay == False) or (freeplay == True and GameTools.game_over(matrix) == True) or (freeplay == False and destroy == 0 and GameTools.game_over(matrix) == True)):
        pygame.mixer.music.stop()
        powerup = ""
        dmitritext = defaulttext
        redoverlay = pygame.Surface((1280, 720))
        redoverlay.fill((255, 0, 0))
        redoverlay.set_alpha(lfadeprogress)
        screen.blit(redoverlay, (0, 0))
        destroy = 0
        delthreshold = 32
        gameover = True
        lfadeprogress += 8
        if lfadeprogress < 256:
            menuback = pygame.Surface((1280, 720))
            menuback.fill((0, 0, 0))
            menuback.set_alpha(128)
            screen.blit(menuback, (0, 0))
    if lfadeprogress >= 256:
        menuopen = True
        if soundplayed == False:
            glassbreak.play()
            soundplayed = True
        screen.blit(failoverlay, (0, 0))

    if win == True:
        pygame.mixer.music.stop()
        powerup = ""
        dmitritext = defaulttext
        greenoverlay = pygame.Surface((1280, 720))
        greenoverlay.fill((0, 255, 0))
        greenoverlay.set_alpha(wfadeprogress)
        screen.blit(greenoverlay, (0, 0))
        destroy = 0
        delthreshold = 32
        wfadeprogress += 8
        if wfadeprogress < 256:
            menuback = pygame.Surface((1280, 720))
            menuback.fill((0, 0, 0))
            menuback.set_alpha(128)
            screen.blit(menuback, (0, 0))
    if wfadeprogress >= 256:
        menuopen = True
        if soundplayed == False:
            winsound.play()
            soundplayed = True

    if menuopen == True:
        MiscTools.menu()
        if menurestart == True:
            screen.blit(menurestartimage, (0, 0))
        elif menuexit == True:
            screen.blit(menuexitimage, (0, 0))

    if gameover == False:
        screen.blit(scanlines, (0, 0))

    if cheats == True and win == False:
        msleft = (levelkey[level][0]) * 1000
        screen.blit(cheatoverlay, (0, 0))

    if blink < 10 and levelup == True:
        if blink == 0:
            pygame.mixer.Sound.play(levelupsound)
        if blink % 2 == 0 and plinks < 90:
            blinker = pygame.Surface((1280, 720))
            blinker.fill((0, 255, 0))
            screen.blit(blinker, (0, 0))
        if  plinks > 30:
            blink += 1
            plinks = 0
    elif blink >= 10:
        blink = 0
        levelup = False
        matrix = restart()
        msleft = (levelkey[level][0]) * 1000
        destroy = 0
        delthreshold = 32

    if tutorialopen == False:
        slide = 1

    if tutorialopen == True:
        if slide == 1:
            screen.blit(tut1, (0, 0))
        if slide == 2:
            screen.blit(tut2, (0, 0))
        if slide == 3:
            screen.blit(tut3, (0, 0))
        if slide == 4:
            screen.blit(tut4, (0, 0))
        if slide == 5:
            screen.blit(tut5, (0, 0))
        if slide == 6:
            screen.blit(tut6, (0, 0))
        if slide == 7:
            screen.blit(tut7, (0, 0))
        if slide == 8:
            screen.blit(tut8, (0, 0))
        if slide == 9:
            screen.blit(tut9, (0, 0))

    if win == True and wfadeprogress >= 256:
        screen.blit(winoverlay, (0, 0))

    dt = clock.tick(60)
    pygame.display.flip()
