def draw_popup(pygame, screen, height, width, world,limit , message, images):
    
    rect_w, rect_h = 350, 250
    rect_x, rect_y = width//2 - rect_w//2, height//2 - rect_h//2

    pygame.draw.rect(screen, (200, 180, 120), (rect_x, rect_y, rect_w, rect_h), border_radius=12)
    pygame.draw.rect(screen, (100, 50, 0), (rect_x, rect_y, rect_w, rect_h), 4, border_radius=12)

    if message == "You Lose!":
        img = images['lose']
    else:
        img = images['win']

    img = pygame.transform.smoothscale(img, (100, 100))
    screen.blit(img, (rect_x + rect_w//2 - 50, rect_y + 20))

    font_msg = pygame.font.SysFont("arial", 24, bold=True)
    text = font_msg.render(message, True, (50, 20, 0))
    screen.blit(text, (rect_x + rect_w//2 - text.get_width()//2, rect_y + 130))

    font_info = pygame.font.SysFont("arial", 20)
    moves_text = font_info.render(f"Moves: {world.move_count}/{limit}", True, (50, 20, 0))
    screen.blit(moves_text, (rect_x + rect_w//2 - moves_text.get_width()//2, rect_y + 170))

    grade = 0
    if world.has_sword:
        grade += 50
    if world.win:
        grade += 100
    grade += max(0, 100 - world.move_count)  
    grade_text = font_info.render(f"Grade: {grade}", True, (50, 20, 0))
    screen.blit(grade_text, (rect_x + rect_w//2 - grade_text.get_width()//2, rect_y + 200))

    pygame.display.flip()
    print(f"******** {message} | Grade: {grade} ******** \n")
    pygame.time.wait(4000)
