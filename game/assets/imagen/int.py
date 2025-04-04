import pygame
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Escape de Othelo')

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Fuente
fuente = pygame.font.SysFont('Arial', 30)

# Personaje principal: Othelo
class Othelo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Usamos un cuadrado temporal
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.center = (100, ALTO - 60)  # Inicializa en la parte inferior
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.salto = False
        self.gravedad = 0.8

    def update(self):
        # Movimiento horizontal
        self.rect.x += self.velocidad_x
        # Salto
        if self.salto:
            self.velocidad_y = -15
            self.salto = False

        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y

        if self.rect.bottom >= ALTO - 60:
            self.rect.bottom = ALTO - 60
            self.velocidad_y = 0

    def mover_izquierda(self):
        self.velocidad_x = -5

    def mover_derecha(self):
        self.velocidad_x = 5

    def saltar(self):
        if self.rect.bottom >= ALTO - 60:
            self.salto = True

# Objeto: Policía
class Policia(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))  # Objeto temporal
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x -= 3
        if self.rect.x < 0:
            self.rect.x = ANCHO

# Crear grupos de sprites
todos_sprites = pygame.sprite.Group()
othello = Othelo()
todos_sprites.add(othello)

policias = pygame.sprite.Group()
for i in range(3):  # Crear 3 policías
    policia = Policia(random.randint(600, 800), random.randint(0, ALTO - 60))
    policias.add(policia)
    todos_sprites.add(policia)

# Variables del juego
puntuacion = 0
running = True

# Bucle principal del juego
while running:
    clock.tick(FPS)
    
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                othello.mover_izquierda()
            if evento.key == pygame.K_RIGHT:
                othello.mover_derecha()
            if evento.key == pygame.K_UP:
                othello.saltar()
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                othello.velocidad_x = 0

    # Actualizar todos los sprites
    todos_sprites.update()

    # Verificar colisiones con los policías
    if pygame.sprite.spritecollide(othello, policias, False):
        running = False
        print("¡Has sido atrapado por los policías!")

    # Pintar en la pantalla
    ventana.fill(BLANCO)
    todos_sprites.draw(ventana)

    # Mostrar puntuación
    texto = fuente.render(f"Puntuación: {puntuacion}", True, NEGRO)
    ventana.blit(texto, (10, 10))

    # Actualizar la ventana
    pygame.display.flip()

pygame.quit()
