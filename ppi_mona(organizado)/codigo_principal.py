import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Escape de Othelo')

# Cargar la imagen de fondo (asegúrate de que el archivo esté en la misma carpeta)
ruta_fondo = "assets/fondo.jpg"  # Cambia esto si la imagen está en otra ubicación
fondo = pygame.image.load(ruta_fondo)
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Ajustar tamaño

# Colores
NEGRO = (0, 0, 0)
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
        self.rect.center = (100, ALTO - 60)
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.salto = False
        self.gravedad = 0.8

    def update(self):
        self.rect.x = max(0, min(ANCHO - self.rect.width, self.rect.x + self.velocidad_x))
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

# Objeto: Policía que persigue a Othelo
class Policia(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, objetivo):
        direccion_x = objetivo.rect.centerx - self.rect.centerx
        direccion_y = objetivo.rect.centery - self.rect.centery
        distancia = math.sqrt(direccion_x ** 2 + direccion_y ** 2)
        if distancia != 0:
            direccion_x /= distancia
            direccion_y /= distancia
        self.rect.x += direccion_x * 2
        self.rect.y += direccion_y * 2

# Crear grupos de sprites
todos_sprites = pygame.sprite.Group()
othello = Othelo()
todos_sprites.add(othello)

policias = pygame.sprite.Group()
for i in range(3):
    policia = Policia(random.randint(600, 800), random.randint(0, ALTO - 60))
    policias.add(policia)
    todos_sprites.add(policia)

# Variables del juego
puntuacion = 0
running = True

# Bucle principal del juego
while running:
    clock.tick(FPS)

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
            if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                othello.velocidad_x = 0

    # Actualizar Othelo
    othello.update()

    # Actualizar policías con la referencia de Othelo
    for policia in policias:
        policia.update(othello)

    # Verificar colisiones con los policías
    if pygame.sprite.spritecollide(othello, policias, False):
        print("¡Has sido atrapado por los policías!")
        running = False

    # Dibujar el fondo antes de los sprites
    ventana.blit(fondo, (0, 0))

    # Dibujar los sprites
    todos_sprites.draw(ventana)

    # Mostrar puntuación
    texto = fuente.render(f"Puntuación: {puntuacion}", True, NEGRO)
    ventana.blit(texto, (10, 10))

    # Actualizar la ventana
    pygame.display.flip()

pygame.quit()