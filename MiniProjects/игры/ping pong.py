import pygame


pygame.init()

screen_width = 1200
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gbyu gjyu")


# Главный цикл
running = True
circle_x = 400
circle_y = 300

circle_ax = 1
circle_ay = 1


left_rect_x = 50
left_rect_y = screen_height//2

right_rect_x = screen_width-50
right_rect_y = screen_height//2


while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    circle_x += circle_ax
    circle_y += circle_ay

    screen.fill((0, 0, 0))  # Черный фон

    # Логика игры
    # Прямоугольник
    right_rect = pygame.draw.rect(screen, (255, 255, 255), (right_rect_x, right_rect_y, 20, 200))  # (x, y, width, height)
    left_rect = pygame.draw.rect(screen, (255, 255, 255), (left_rect_x, left_rect_y, 20, 200))


    # Управление прямоугольниками
    # левый (игрок)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        left_rect_y = max(left_rect_y - 1, 0)
    if keys[pygame.K_DOWN]:
        left_rect_y = min(left_rect_y + 1, screen_height-200)

    # правый (бот)
    if circle_y < right_rect_y:
        right_rect_y = max(right_rect_y - 1, 0)
    else:
        right_rect_y = min(right_rect_y + 1, screen_height-200)


    # Круг
    radius = 10
    circle = pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), radius)  # (x, y, radius)

    if circle_x - radius < 0:  # Левая граница
        circle_ax = -circle_ax
    if circle_x + radius > screen_width:  # Правая граница
        circle_ax = -circle_ax
    if circle_y - radius < 0:  # Верхняя граница
        circle_ay = -circle_ay
    if circle_y + radius > screen_height:  # Нижняя граница
        circle_ay = -circle_ay

    if circle.colliderect(right_rect):
        circle_ax = -1
    if circle.colliderect(left_rect):
        circle_ax = 1

    pygame.display.flip()   # Обновление экрана

pygame.quit()

