from typing import Self
import pygame
from pygame.math import Vector2


class Color(pygame.Color):
    # Базовые цвета
    Red = pygame.Color("red")
    Green = pygame.Color("green")  
    Blue = pygame.Color("blue")
    Yellow = pygame.Color("yellow")
    Cyan = pygame.Color("cyan")
    Magenta = pygame.Color("magenta")
    White = pygame.Color("white")
    Black = pygame.Color("black")
    Gray = pygame.Color("gray")
    
    # Практичные оттенки
    DarkRed = pygame.Color("darkred")
    DarkGreen = pygame.Color("darkgreen") 
    DarkBlue = pygame.Color("darkblue")
    LightGray = pygame.Color("lightgray")
    DarkGray = pygame.Color("darkgray")
    
    # Популярные
    Orange = pygame.Color("orange")
    Purple = pygame.Color("purple")
    Pink = pygame.Color("pink")
    Brown = pygame.Color("brown")
    Gold = pygame.Color("gold")
    Silver = pygame.Color("silver")


class GameObject:
    def __init__(self, parent, color: tuple[int] = None, position: Vector2 = None, size: Vector2 = None, 
                 velocity: Vector2 = None, acceleration: Vector2 = None):
        self.parent = parent
        self.color = color or Color.White
        self.size: Vector2 = size or Vector2(50, 50)

        # Получаем центр родителя
        self.parentSize = self.parent.get_size()
        self.parentCenter: Vector2 = Vector2(self.parentSize[0], self.parentSize[1]) // 2

        # position
        if position is None:
            self._position: Vector2 = self.parentCenter - (self.size // 2)
        else:
            self._position: Vector2 = position + self.parentCenter - (self.size // 2)

        self.velocity = velocity or Vector2(0, 0)
        self.acceleration = acceleration or Vector2(0, 0)


    def update(self):
        self.velocity += self.acceleration

        self.position += self.velocity

    def draw(self):
        return pygame.draw.rect(self.parent, self.color, (self._position.x, self.parentSize[1] - self._position.y - self.size.y / 2, self.size.x, self.size.y))

    @property
    def position(self) -> Vector2:
        return self._position - self.parentCenter
    
    @position.setter
    def position(self, value: Vector2) -> None:
        self._position = value + self.parentCenter


class Game:
    def __init__(self):
        pygame.init()

        screen_width = 1200
        screen_height = 600

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("spring simulator")

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.objects: list[GameObject] = []

    def run(self, game_loop: callable):
        running = True
        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))  # Черный фон

            game_loop()

            self.update()
            self.render()

            pygame.display.flip()   # Обновление экрана
            self.clock.tick(60)
        pygame.quit()

    def update(self):
        for obj in self.objects:
            obj.update()

    def render(self):
        for obj in self.objects:
            obj.draw()

    def createObject(self, obj: GameObject) -> GameObject:
        self.objects.append(obj)
        return obj


class Square(GameObject):
    def __init__(self, parent, color: tuple[int] = None, position: Vector2 = None, size: Vector2 = None, 
                 velocity: Vector2 = None, acceleration: Vector2 = None):
        super().__init__(parent, color=color, position=position, size=size, 
                         velocity=velocity, acceleration=acceleration)


game_instance = Game()

sq1 = game_instance.createObject(Square(game_instance.screen, color=Color.Cyan, position=Vector2(-50, 100)))
sq2 = game_instance.createObject(Square(game_instance.screen, color=Color.Green, position=Vector2(50, 0)))
sq3 = game_instance.createObject(Square(game_instance.screen, color=Color.Green, position=Vector2(150, 0)))
sq4 = game_instance.createObject(Square(game_instance.screen, color=Color.Green, position=Vector2(250, 0)))

chain = [game_instance.createObject(Square(game_instance.screen, position=Vector2(-200 + i * 100, -100 + i * 10))) for i in range(4)]

def gameLoop():
    global sq1, sq2

    distance1 = (sq2.position.y - sq1.position.y) / 2
    distance2 = ((sq1.position.y - sq2.position.y) / 2 + (sq3.position.y - sq2.position.y) / 2) / 2
    distance3 = ((sq2.position.y - sq3.position.y) / 2 + (sq4.position.y - sq3.position.y) / 2) / 2
    distance4 = (sq3.position.y - sq4.position.y) / 2

    sq1.acceleration.y = distance1 / 100
    sq2.acceleration.y = distance2 / 100
    sq3.acceleration.y = distance3 / 100
    sq4.acceleration.y = distance4 / 100


    forces = []
    for i in range(len(chain)-1):
        force = (chain[i+1].position.y - chain[i].position.y) / 2
        forces.append(force)

    distances = []
    for i in range(len(chain)):
        if i == 0:
            distances.append(forces[0])
        elif i + 2 >= len(chain):
            distances.append(-forces[-1])
        else:
            distances.append(-forces[i] + forces[i+1])

    for obj, dist in zip(chain, distances):
        obj.acceleration.y = dist / 100




game_instance.run(gameLoop)