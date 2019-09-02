import collections
import math
import random
import pygame

const_coulomb = 9000000000
# Define some colors
preto = (0, 0, 0)
branco = (255, 255, 255)
marron = (165,42,42)

largura_tela = 800
altura_tela = 800
centroX = largura_tela/2
centroY = altura_tela/2



tamanho_carga = 12

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
    new_carga['position_x'] = int(position_x)
    new_carga['position_y'] = int(position_y)
    new_carga['valor_carga'] = float(valor_carga)
    new_carga['forcas'] = []
    return new_carga


def get_new_forca(carga1, carga2, forca):
    new_forca = collections.OrderedDict()
    new_forca['carga1'] = carga1
    new_forca['carga2'] = carga2
    new_forca['forca'] = forca
    return new_forca


def get_new_campo(carga, campo):
    new_forca = collections.OrderedDict()
    new_forca['carga'] = carga
    new_forca['campo'] = campo
    return new_forca


def calcula_distancia(carga_1, carga_2):
    distancia_x = (carga_1['position_x'] - carga_2['position_x'])/1000
    distancia_y = (carga_1['position_y'] - carga_2['position_y'])/1000
    distancia_x = math.pow(distancia_x, 2)
    distancia_y = math.pow(distancia_y, 2)
    distancia = math.sqrt(distancia_x+distancia_y)
    return distancia


def calcula_forca_2cargas(carga_1, carga_2):
    dividendo = const_coulomb * carga_1['valor_carga'] * carga_2['valor_carga']
    divisor = math.pow(calcula_distancia(carga_1, carga_2), 2)
    return (dividendo / divisor)


def forcas_atuantes(bola, lista_bolas):
    compara = lambda x, y: collections.Counter(x) == collections.Counter(y)
    lista_forcas = []
    for x in lista_bolas:
        if not compara(x.carga, bola.carga):
            lista_forcas.append(get_new_forca(bola.carga['nome'], x.carga['nome'], calcula_forca_2cargas(bola.carga, x.carga)))
    return lista_forcas


def calcula_campo_eletrico(carga1, pontox, pontoy):
    ponto = collections.OrderedDict()

    ponto['position_x'] = pontox
    ponto['position_y'] = pontoy
    
    divisor = calcula_distancia(carga1, ponto)
    divisor = math.pow(divisor, 2)

    dividendo = const_coulomb * carga1['valor_carga']
    return (dividendo / divisor)


def fazer_bola_carga(carga):
    """
    Cria a bola 
    """
    bola = Ball(carga)

    # Local onde é colocado o local de onde a bola começa
    # Como os pixeis começam a ser contados no canto superior esquerdo
    #   Essa função converte o valor, x ou y, para a posição do pixel 
    bola.x = int(centroX) +carga['position_x']
    bola.y = int(centroY) + (carga['position_y'] * (-1))
 
 
    return bola


def adiciona_nova_bola(qtd_itens):
    valor = input("Digite o valor da carga em Coulomb: ")
    print("Digite o local em valores inteiros correspondentes em mm de -400 a 400")
    posicaox = input("Digite x:")
    posicaoy = input("Digite y:")
    # Conversão de metros para centimetro, cada pixel tem 1cm
    ball = fazer_bola_carga(get_new_carga(f"q{qtd_itens}",int(posicaox), int(posicaoy), valor))
    return ball


def get_campos_eletricos(ball_list, pontox, pontoy):
    lista_campos = []
    for ball in ball_list:
        campo = get_new_campo(ball.carga['nome'], calcula_campo_eletrico(ball.carga, pontox, pontoy))
        lista_campos.append(campo)
    return lista_campos


if __name__ == "__main__":
    pygame.init()
    size = [largura_tela, altura_tela]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Calcule forças e campo elétrico")
    clock = pygame.time.Clock()
 
    done = False

    ball_list = []
    #lista_cargas = []
    # for x in range(0, 4):
    #     ball = fazer_bola_carga(get_new_carga(f"q{x}",random.uniform(-1.5, 1.5), random.uniform(-1.2, 1.2), random.uniform(0.000001, 0.00001)))
    #     ball_list.append(ball)
        #lista_cargas.append(get_new_carga(f"q{x}",random.uniform(-1.5, 1.5), random.uniform(-1.2, 1.2), random.uniform(0.000001, 0.00001)))
    print("\nBem-vindo, comandos:\nn para nova carga\nf para mostrar as forças")
    print("\nClique com o mouse em algum ponto da tela para mostrar os campos\n\n")
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    print("\n########################")
                    print("Você clicou em 'n'")
                    ball_list.append(adiciona_nova_bola(len(ball_list)))
                    for bola in ball_list:
                        bola.carga['forcas'] = [a for a in forcas_atuantes(bola, ball_list)]
                if event.key == pygame.K_f:
                    print("\n########################")
                    print("Você clicou em 'f'")
                    for ball in ball_list:
                        for forca in ball.carga['forcas']:
                            print(f"\nForça entre {forca['carga1']} e {forca['carga2']}")
                            print(f"\nCarga {forca['forca']} N")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                pygame.draw.circle(screen, marron, [x, y], tamanho_carga)
                # Conversao para calcular e printar o ponto
                x = x - int(centroX)
                y = int(centroY) + (y * (-1))
                print("\n########################")
                print(f"\nNo ponto x={x} e y={y}")
                for campo in get_campos_eletricos(ball_list, x, y):
                    print(f"\nCampo gerado pela carga {campo['carga']}")
                    print(f"Valor: {campo['campo']} N/C")

 
        # Fundo preto
        screen.fill(preto)
        # Linha do X
        pygame.draw.line(screen, marron, [0, centroY], [largura_tela, centroY])
        # Linha do Y
        pygame.draw.line(screen, marron, [centroX, 0], [centroX, altura_tela])
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
    # calcula_forca_2cargas(carga_1, carga_2)
    # print(calcula_forca_2cargas(carga_1, carga_2))