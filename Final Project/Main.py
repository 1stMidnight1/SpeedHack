import pygame, random, GameTools, MiscTools
pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("[SPEEDHACK]")

matrix = {
    11: 0, 12: 0, 13: 0, 14: 0,
    21: 0, 22: 0, 23: 0, 24: 0,
    31: 0, 32: 0, 33: 0, 34: 0,
    41: 0, 42: 0, 43: 0, 44: 0
}

levelkey =  {1: (30, 32), 2: (45, 64), 3: (60, 128), 4: (75, 256), 5: (90, 512)}
level = 1

running = True
menuopen = False
menurestart = True
menuexit = False
fadeprogress = 0
backgroundmusic = pygame.mixer.music.load("backgroundmusic.mp3")
glassbreak = pygame.mixer.Sound("glassbreak.mp3")
soundplayed = False

def print_matrix():
    offsetx=320
    offsety=20
    colors = {
        0: (15, 35, 15),  # very dark green for empty
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
        font = pygame.font.Font("7segments.ttf", 72)
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
"4) Level Select",
"5) Restart Level"]

dmitritext = defaulttext
gameover = False
text = ""
msleft = (levelkey[level][0])*1000
clock = pygame.time.Clock()
timer_font = pygame.font.Font("mono.ttf", 64)
objective_font = pygame.font.Font("mono.ttf", 32)
dmitri_font = pygame.font.Font("mono.ttf", 18)

delthreshold = 32
multthreshold = 1

tutorialopen = False
powerup = ""
destroy = 0
multiply = 0

pygame.mixer.music.play(-1)
GameTools.new_tile(matrix)
GameTools.new_tile(matrix)
print_matrix()

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if menuopen == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    GameTools.move_right(matrix)
                    GameTools.new_tile(matrix)
                elif event.key == pygame.K_LEFT:
                    GameTools.move_left(matrix)
                    GameTools.new_tile(matrix)
                elif event.key == pygame.K_UP:
                    GameTools.move_up(matrix)
                    GameTools.new_tile(matrix)
                elif event.key == pygame.K_DOWN:
                    GameTools.move_down(matrix)
                    GameTools.new_tile(matrix)
                elif event.key == pygame.K_5:
                    matrix = restart()
                    msleft = (levelkey[level][0]) * 1000
                elif event.key == pygame.K_ESCAPE:
                    menuopen = True

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
                        matrix = restart()
                        fadeprogress = 0
                        menuopen = False
                        msleft = (levelkey[level][0]) * 1000
                        gameover = False
                        soundplayed = False
                        destroy = 0
                        pygame.mixer.music.unpause()
                    elif menuexit == True:
                        running = False

        if tutorialopen == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    tutorialopen = True
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    tutorialopen = False

        for tile in matrix.values():
            if tile >= delthreshold:
                destroy += 1
                delthreshold *= 2
        if level > multthreshold:
            multiply += 1
            multthreshold += 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_2 and destroy > 0:
                powerup = "destroy"
            elif event.key == pygame.K_3 and multiply > 0:
                powerup = "multiply"

        if event.type == pygame.MOUSEBUTTONDOWN and powerup:
            offsetx, offsety = 320, 20
            for tile in matrix:
                rect = pygame.Rect(offsetx, offsety, 160, 160)
                if rect.collidepoint(event.pos):
                    if powerup == "destroy":
                        matrix[tile] = 0
                        powerup = ""
                        destroy -= 1
                    elif powerup == "multiply" and 0 < matrix[tile] < 128:
                        matrix[tile] *= 2
                        powerup = ""
                        multiply -= 1
                        break
                elif (tile - 4) % 10 == 0:
                    offsetx = 320
                    offsety += 160
                else:
                    offsetx += 160

    if tutorialopen == True:
        tutorial_display = pygame.image.load("tutorialscreen.png").convert_alpha()
        screen.blit(tutorial_display, (0, 0))
        pygame.display.flip()
        continue

    screen.fill((0, 0, 0))
    main_background = pygame.image.load("background.png").convert_alpha()
    screen.blit(main_background, (0, 0))
    print_matrix()

    #Max characters per line is 15

    render1 = dmitri_font.render(dmitritext[0], True, (255, 255, 255))
    render2 = dmitri_font.render(dmitritext[1], True, (255, 255, 255))
    render3 = dmitri_font.render(dmitritext[2], True, (255, 255, 255))
    render4 = dmitri_font.render(dmitritext[3], True, (255, 255, 255))
    render5 = dmitri_font.render(dmitritext[4], True, (255, 255, 255))
    render6 = dmitri_font.render(dmitritext[5], True, (255, 255, 255))
    render7 = dmitri_font.render(dmitritext[6], True, (255, 255, 255))

    screen.blit(render1, (60, 430))
    screen.blit(render2, (60, 430+10+render1.get_rect().height))
    screen.blit(render3, (60, 430+(10+render1.get_rect().height)*2))
    screen.blit(render4, (60, 430+(10+render1.get_rect().height)*3))
    screen.blit(render5, (60, 430+(10+render1.get_rect().height)*4))
    screen.blit(render6, (60, 430+(10+render1.get_rect().height)*5))
    screen.blit(render7, (60, 430 + (10 + render1.get_rect().height) * 6))

    msleft -= clock.tick(60)
    if msleft <= 0:
        msleft = 0
        gameover = True
    seconds = msleft // 1000
    centiseconds = (msleft % 1000) // 10
    text = f'{seconds}.{centiseconds:02d}'
    timer_display = timer_font.render(text, True, (255, 255, 255))
    timerdisplay_rect = timer_display.get_rect()
    screen.blit(timer_display, (1120-timerdisplay_rect.width/2, 150))

    objectivedisplay = objective_font.render(f"Goal: {levelkey[level][1]}", True, (255, 255, 255))
    screen.blit(objectivedisplay, (1120 - objectivedisplay.get_rect().width / 2, 480))
    destroytext = objective_font.render(f"Destroys: {destroy}", True, (255, 255, 255))
    multiplytext = objective_font.render(f"Doublers: {multiply}", True, (255, 255, 255))
    screen.blit(destroytext, (1120 - destroytext.get_rect().width / 2, 490+destroytext.get_rect().height))
    screen.blit(multiplytext, (1120 - multiplytext.get_rect().width / 2, 500+multiplytext.get_rect().height*2))

    if GameTools.game_over(matrix) == True or gameover == True:
        pygame.mixer.music.pause()
        if soundplayed == False:
            glassbreak.play()
            soundplayed = True
        gameover = True
        redoverlay = pygame.Surface((1280, 720))
        redoverlay.fill((255, 0, 0))
        redoverlay.set_alpha(fadeprogress)
        pygame.time.wait(1)
        screen.blit(redoverlay, (0, 0))
        destroy = 0
        delthreshold = 32
        fadeprogress += 10
        if fadeprogress < 256:
            menuback = pygame.Surface((1280, 720))
            menuback.fill((0, 0, 0))
            menuback.set_alpha(128)
            screen.blit(menuback, (0, 0))
    if fadeprogress >= 256:
        menuopen = True
        failoverlay = pygame.image.load("failoverlay.png").convert_alpha()
        screen.blit(failoverlay, (0, 0))

    if menuopen == True:
        MiscTools.menu()
        if menurestart == True:
            menu_display = pygame.image.load("menurestart.png").convert_alpha()
        elif menuexit == True:
            menu_display = pygame.image.load("menuexit.png").convert_alpha()
        screen.blit(menu_display, (0, 0))

    scanlines = pygame.image.load("overlay.png").convert_alpha()
    if gameover == False:
        screen.blit(scanlines, (0, 0))

    pygame.display.flip()
