import pygame


pygame.init()

screen_width = 1200
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("circle square")


# Главный цикл
running = True
circle_x = 400
circle_y = 300

circle_ax = 1
circle_ay = 1

circle_aax = 0
circle_aay = 0

rect_x = 50
rect_y = screen_height//2


while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    circle_ax += circle_aax
    circle_ay += circle_aay

    circle_x += circle_ax / 5
    circle_y += circle_ay / 5

    screen.fill((0, 0, 0))  # Черный фон

    # Прямоугольник
    rect = pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, 50, 50))  # (x, y, width, height)


    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        rect_y = max(rect_y - 1, 0)
    if keys[pygame.K_DOWN]:
        rect_y = min(rect_y + 1, screen_height-50)
    if keys[pygame.K_LEFT]:
        rect_x = max(rect_x - 1, 0)
    if keys[pygame.K_RIGHT]:
        rect_x = min(rect_x + 1, screen_width-50)
    

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

    # Вектор направления
    dx = circle_x - rect_x
    dy = circle_y - rect_y

    # Нормализация (единичный вектор)
    distance = max(0.1, (dx**2 + dy**2)**0.5)  # избегаем деления на 0
    circle_aax = -(dx / distance) / 50
    circle_aay = -(dy / distance) / 50


    pygame.display.flip()   # Обновление экрана

pygame.quit()

