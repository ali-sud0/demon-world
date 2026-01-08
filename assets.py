def images_init(cell_size,pygame):
    images = {}

    wall_img = pygame.image.load("./images/wall.png").convert_alpha()
    wall_img = pygame.transform.smoothscale(wall_img, (cell_size, cell_size))
    images['wall'] = wall_img

    floor_img = pygame.image.load("./images/floor.png").convert_alpha()
    floor_img = pygame.transform.smoothscale(floor_img, (cell_size, cell_size))
    images['floor'] = floor_img


    demon_img = pygame.image.load("./images/demon.png").convert_alpha()
    demon_img = pygame.transform.smoothscale(demon_img, (cell_size, cell_size))
    images['demon'] = demon_img


    hero_img = pygame.image.load("./images/hero.png").convert_alpha()
    hero_img = pygame.transform.smoothscale(hero_img, (cell_size, cell_size))
    images['hero'] = hero_img


    sword_img = pygame.image.load("./images/sword.png").convert_alpha()
    sword_img = pygame.transform.smoothscale(sword_img, (cell_size, cell_size))
    images['sword'] = sword_img


    ear_img = pygame.image.load("./images/ear.png").convert_alpha()
    ear_img = pygame.transform.smoothscale(ear_img, (cell_size, cell_size))
    images['ear'] = ear_img


    lose_img = pygame.image.load("./images/lose.png").convert_alpha()
    images['lose'] = lose_img


    win_img = pygame.image.load("./images/win.png").convert_alpha()
    images['win'] = win_img

    return images