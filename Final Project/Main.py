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

level =  {1: (30, 32), 2: (45, 64), 3: (60, 128), 4: (75, 256), 5: (90, 512)}

dmitri1 = ""
dmitri2 = ""
dmitri3 = ""
dmitri4 = ""
dmitri5 = ""
dmitri6 = ""
dmitri7 = ""

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

sound = pygame.mixer.Sound("backgroundmusic.mp3")
sound.play()

running = True
menuopen = False
menurestart = True
menuexit = False

fadeprogress = 0
GameTools.new_tile(matrix)
GameTools.new_tile(matrix)
print_matrix()

tutorialtext = [pygame.image.load("tutorial1.png").convert_alpha(),
                pygame.image.load("tutorial2.png").convert_alpha(),
                pygame.image.load("tutorial3.png").convert_alpha(),
                pygame.image.load("tutorial4.png").convert_alpha()]
tutorialindex = 0
tutorialcounter = 0
tutorialend = 100

text = ""
seconds = 0
timer_font = pygame.font.Font("mono.ttf", 64)
dmitri_font = pygame.font.Font("mono.ttf", 20)

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
                        matrix = {
                            11: 0, 12: 0, 13: 0, 14: 0,
                            21: 0, 22: 0, 23: 0, 24: 0,
                            31: 0, 32: 0, 33: 0, 34: 0,
                            41: 0, 42: 0, 43: 0, 44: 0
                        }
                        fadeprogress = 0
                        GameTools.new_tile(matrix)
                        GameTools.new_tile(matrix)
                        print_matrix()
                        menuopen = False
                    elif menuexit == True:
                        running = False

    screen.fill((0, 0, 0))
    main_background = pygame.image.load("background.png").convert_alpha()
    screen.blit(main_background, (0, 0))
    print_matrix()

#Max characters per line is 15
    dmitriscreen = "Home"
    if dmitriscreen == "Home":
        dmitri1 = "Press Key to"
        dmitri2 = "Select Option..."
        dmitri4 = "1) Tutorial"
        dmitri5 = "2) Power Ups"
        dmitri6 = "3) Level Select"

    render1 = dmitri_font.render(dmitri1, True, (255, 255, 255))
    render2 = dmitri_font.render(dmitri2, True, (255, 255, 255))
    render3 = dmitri_font.render(dmitri3, True, (255, 255, 255))
    render4 = dmitri_font.render(dmitri4, True, (255, 255, 255))
    render5 = dmitri_font.render(dmitri5, True, (255, 255, 255))
    render6 = dmitri_font.render(dmitri6, True, (255, 255, 255))
    render7 = dmitri_font.render(dmitri7, True, (255, 255, 255))

    screen.blit(render1, (60, 425))
    screen.blit(render2, (60, 425+10+render1.get_rect().height))
    screen.blit(render3, (60, 425+(10+render1.get_rect().height)*2))
    screen.blit(render4, (60, 425+(10+render1.get_rect().height)*3))
    screen.blit(render5, (60, 425+(10+render1.get_rect().height)*4))
    screen.blit(render6, (60, 425+(10+render1.get_rect().height)*5))
    screen.blit(render7, (60, 425 + (10 + render1.get_rect().height) * 6))

    dmitri1 = ""
    dmitri2 = ""
    dmitri3 = ""
    dmitri4 = ""
    dmitri5 = ""
    dmitri6 = ""

    minute = seconds // 60
    second = seconds % 60
    text = f'{minute}.{second:02d}'
    timer_display = timer_font.render(text, True, (255, 255, 255))
    seconds += 1
    timerdisplay_rect = timer_display.get_rect()
    screen.blit(timer_display, (1120-timerdisplay_rect.width/2, 150))

    if GameTools.game_over(matrix) == True:
        redoverlay = pygame.Surface((1280, 720))
        redoverlay.fill((255, 0, 0))
        redoverlay.set_alpha(fadeprogress)
        pygame.time.wait(1)
        screen.blit(redoverlay, (0, 0))
        fadeprogress += 8
    if fadeprogress >= 256:
        menuopen = True

    if menuopen == True:
        MiscTools.menu()
        if menurestart == True:
            menu_display = pygame.image.load("menurestart.png").convert_alpha()
        elif menuexit == True:
            menu_display = pygame.image.load("menuexit.png").convert_alpha()
        screen.blit(menu_display, (0, 0))

    main_background = pygame.image.load("overlay.png").convert_alpha()
    if fadeprogress <= 256:
        screen.blit(main_background, (0, 0))
    pygame.display.flip()
