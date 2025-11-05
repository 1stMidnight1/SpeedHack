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
fadeprogress = 0
menuopen = False
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
                    testmatrix = matrix.copy()
                    GameTools.move_right(matrix)
                    if matrix != testmatrix:
                        GameTools.new_tile(matrix)
                elif event.key == pygame.K_LEFT:
                    testmatrix = matrix.copy()
                    GameTools.move_left(matrix)
                    if matrix != testmatrix:
                        GameTools.new_tile(matrix)
                elif event.key == pygame.K_UP:
                    testmatrix = matrix.copy()
                    GameTools.move_up(matrix)
                    if matrix != testmatrix:
                        GameTools.new_tile(matrix)
                elif event.key == pygame.K_DOWN:
                    testmatrix = matrix.copy()
                    GameTools.move_down(matrix)
                    if matrix != testmatrix:
                        GameTools.new_tile(matrix)
                elif event.key == pygame.K_ESCAPE:
                    menustate = "restart"
                    menuopen = True
        elif menuopen == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menuopen = False
                elif event.key == pygame.K_DOWN:
                    menustate = "exit"
                elif event.key == pygame.K_UP:
                    menustate = "restart"
                elif event.key == pygame.K_RETURN:
                    if menustate == "exit":
                        running = False
                    elif menustate == "restart":
                        matrix = GameTools.reset()
                        GameTools.new_tile(matrix)
                        GameTools.new_tile(matrix)
                        menuopen = False

    screen.fill((0, 0, 0))
    main_background = pygame.image.load("background.png").convert_alpha()
    screen.blit(main_background, (0, 0))
    print_matrix()
    grid = pygame.image.load("gridoverlay.png").convert_alpha()
    screen.blit(grid, (0, 0))
    main_overlay = pygame.image.load("overlay.png").convert_alpha()
    screen.blit(main_overlay, (0, 0))
    if menuopen == True:
        MiscTools.menu(menustate)
    if GameTools.game_over(matrix) == True:
        redoverlay = pygame.Surface((1280, 720))
        redoverlay.fill((255, 0, 0))
        redoverlay.set_alpha(fadeprogress)
        pygame.time.wait(1)
        screen.blit(redoverlay, (0, 0))
        fadeprogress += 1

    pygame.display.flip()

    if fadeprogress == 255:
        print("Game Over!")
        running = False

