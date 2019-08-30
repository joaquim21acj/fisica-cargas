import collections
import math
import random
import pygame

const_coulomb = 9000000000
# Define some colors
preto = (0, 0, 0)
branco = (255, 255, 255)
 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
tamanho_carga = 25

class Ball:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self, new_carga):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.carga = new_carga

def get_new_carga(nome, position_x, position_y, valor_carga):
    new_carga = collections.OrderedDict()
    new_carga['nome'] = nome
    new_carga['position_x'] = position_x
    new_carga['position_y'] = position_y
    new_carga['valor_carga'] = valor_carga
    new_carga['forcas'] = []
    return new_carga


def get_new_forca(carga1, carga2, forca):
    new_forca = collections.OrderedDict()
    new_forca['carga1'] = carga1
    new_forca['carga2'] = carga2
    new_forca['forca'] = forca
    return new_forca


def calcula_distancia(carga_1, carga_2):
    distancia_x = carga_1['position_x'] - carga_2['position_x']
    distancia_y = carga_1['position_y'] - carga_2['position_y']
    distancia_x = math.pow(distancia_x, 2)
    distancia_y = math.pow(distancia_y, 2)
    distancia = math.sqrt(distancia_x+distancia_y)
    return distancia


def calcula_forca(carga_1, carga_2):
    dividendo = const_coulomb * carga_1['valor_carga'] * carga_2['valor_carga']
    divisor = math.pow(calcula_distancia(carga_1, carga_2), 2)
    return (dividendo / divisor)


def forcas_atuantes(bola, lista_bolas):
    compara = lambda x, y: collections.Counter(x) == collections.Counter(y)
    lista_forcas = []
    for x in lista_bolas:
        if not compara(x.carga, bola.carga):
            lista_forcas.append(get_new_forca(bola.carga['nome'], x.carga['nome'], calcula_forca(bola.carga, x.carga)))
    return lista_forcas


def fazer_bola_carga(carga):
    """
    Function to make a new, random ball.
    """
    bola = Ball(carga)
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    bola.x = random.randrange(tamanho_carga, SCREEN_WIDTH - tamanho_carga)
    bola.y = random.randrange(tamanho_carga, SCREEN_HEIGHT - tamanho_carga)
 
    # Speed and direction of rectangle
    bola.change_x = random.randrange(-2, 3)
    bola.change_y = random.randrange(-2, 3)
 
    return bola


if __name__ == "__main__":
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Clique para adicionar cargas")
    clock = pygame.time.Clock()
 
    # Loop until the user clicks the close button.
    done = False

    ball_list = []
    #lista_cargas = []
    for x in range(0, 4):
        ball = fazer_bola_carga(get_new_carga(f"q{x}",random.uniform(-1.5, 1.5), random.uniform(-1.2, 1.2), random.uniform(0.000001, 0.00001)))
        ball_list.append(ball)
        #lista_cargas.append(get_new_carga(f"q{x}",random.uniform(-1.5, 1.5), random.uniform(-1.2, 1.2), random.uniform(0.000001, 0.00001)))
    
    for bola in ball_list:
        bola.carga['forcas'] = [a for a in forcas_atuantes(bola, ball_list)]


    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Space bar! Spawn a new ball.
                if event.key == pygame.K_SPACE:
                    ball = fazer_bola_carga()
                    ball_list.append(ball)
 
        # --- Logic
        for ball in ball_list:
            # Move the ball's center
            ball.x += ball.change_x
            ball.y += ball.change_y
 
            # Bounce the ball if needed
            if ball.y > SCREEN_HEIGHT - tamanho_carga or ball.y < tamanho_carga:
                ball.change_y *= -1
            if ball.x > SCREEN_WIDTH - tamanho_carga or ball.x < tamanho_carga:
                ball.change_x *= -1
 
        # --- Drawing
        # Set the screen background
        screen.fill(preto)
 
        # Draw the balls
        for ball in ball_list:
            pygame.draw.circle(screen, branco, [ball.x, ball.y], tamanho_carga)
 
        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Close everything down
    pygame.quit()
    # carga_1 = get_new_carga(0.03, 0, 0.000002)
    # carga_2 = get_new_carga(0, 0, 0.000008)
    # calcula_forca(carga_1, carga_2)
    # print(calcula_forca(carga_1, carga_2))