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
    Classe para guardar dados de cada círculo
    """
    def __init__(self, new_carga):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.carga = new_carga


def get_new_carga(nome, position_x, position_y, valor_carga):
    """
    Função que cria e organiza os dados de cada carga
    Recebe a posição em x e y, além do nome e do valor da carga
    """
    new_carga = collections.OrderedDict()
    new_carga['nome'] = nome
    new_carga['position_x'] = int(position_x)
    new_carga['position_y'] = int(position_y)
    new_carga['valor_carga'] = float(valor_carga)
    new_carga['forcas'] = []
    return new_carga


def get_new_forca(carga1, carga2, forca):
    """
    Função para gerar nova força entre duas cargas
    Recebe o nome das duas cargas e o valor da força
    """
    new_forca = collections.OrderedDict()
    new_forca['carga1'] = carga1
    new_forca['carga2'] = carga2
    new_forca['forca'] = forca
    return new_forca


def get_new_campo(carga, campo):
    """
    Função para gerar novo campo
    Recebe o nome da carga e o valor do campo
    """
    new_forca = collections.OrderedDict()
    new_forca['carga'] = carga
    new_forca['campo'] = campo
    return new_forca


def calcula_distancia(carga_1, carga_2):
    """
    Função para calcular a distância entre duas carga/pontos
    Recebe duas cargas, ou uma carga e um ponto
    """
    # Faz a diferença entre x2/y2 e x1/y1, converte para metros
    distancia_x = (carga_1['position_x'] - carga_2['position_x'])/1000
    distancia_y = (carga_1['position_y'] - carga_2['position_y'])/1000
    # Eleva cada componente ao quadrado
    distancia_x = math.pow(distancia_x, 2)
    distancia_y = math.pow(distancia_y, 2)
    # Tira a raiz 
    distancia = math.sqrt(distancia_x+distancia_y)
    return distancia


def calcula_forca_2cargas(carga_1, carga_2):
    """
    Função para calcular a força entre duas cargas
    Recebe duas cargas
    """
    # Multiplicação entre K*q1*q2
    dividendo = const_coulomb * carga_1['valor_carga'] * carga_2['valor_carga']
    # Calcula a distancia e eleva ao quadrado
    divisor = math.pow(calcula_distancia(carga_1, carga_2), 2)
    return (dividendo / divisor)


def forcas_atuantes(bola, lista_bolas):
    """
    Função que calcula a força exercida por cada bola/carga em relação as demais
    Recebe a carga/bolas que se deseja calcular as forças e as demais cargas/bolas
    """
    compara = lambda x, y: collections.Counter(x) == collections.Counter(y)
    lista_forcas = []
    for x in lista_bolas:
        # Verifica se a carga que se deseja calcular não é a mesma da lista,
        #  assim evita-se calcular a força atuante da mesma carga sobre ela mesma.
        if not compara(x.carga, bola.carga):
            # Para cada carga, calcula a força, gera uma nova entidade de força e adiciona à lista
            lista_forcas.append(get_new_forca(bola.carga['nome'], x.carga['nome'], calcula_forca_2cargas(bola.carga, x.carga)))
    return lista_forcas


def calcula_campo_eletrico(carga1, pontox, pontoy):
    """
    Função para calcular o campo eletrico 
    Recebe a carga e o ponto em x e y
    """
    # Cria uma entidade tipo ponto que recebe as coordenadas em x e y
    #   para ficar ser usada como distância 
    ponto = collections.OrderedDict()
    ponto['position_x'] = pontox
    ponto['position_y'] = pontoy
    # Calcula a distância entre a carga e o ponto clicado 
    divisor = calcula_distancia(carga1, ponto)
    # Eleva o resultado ao quadrado
    divisor = math.pow(divisor, 2)
    # Multiplica a constante pelo valor da carga
    dividendo = const_coulomb * carga1['valor_carga']
    return (dividendo / divisor)


def fazer_bola_carga(carga):
    """
    Cria a bola 
    """
    bola = Ball(carga)

    # Como os pixeis começam a ser contados no canto superior esquerdo
    #   Essa função converte o valor, x ou y, para a posição do pixel 
    bola.x = int(centroX) + carga['position_x']
    bola.y = int(centroY) + (carga['position_y'] * (-1))

    return bola


def adiciona_nova_bola(qtd_itens):
    """
    Função adicionar uma nova bola
    Recebe a quantidade de itens para criar uma nova carga
    """
    valor = input("Digite o valor da carga em Coulomb: ")
    print("Digite o local em valores inteiros correspondentes em mm de -400 a 400")
    posicaox = input("Digite x:")
    posicaoy = input("Digite y:")
    # Faz uma nova bola adicionando uma nova cargas
    ball = fazer_bola_carga(get_new_carga(f"q{qtd_itens}",int(posicaox), int(posicaoy), valor))
    return ball


def get_campos_eletricos(ball_list, pontox, pontoy):
    """
    Função para calcular os campos elétricos gerados por cada carga
    Recebe a lista de bolas e o ponto, em x e y
    """
    lista_campos = []
    for ball in ball_list:
        # calcula um campo elétrico para cada carga e gera um novo campo para cada carga usando o ponto clicado
        campo = get_new_campo(ball.carga['nome'], calcula_campo_eletrico(ball.carga, pontox, pontoy))
        # Adiciona cada campo para lista
        lista_campos.append(campo)
    return lista_campos


if __name__ == "__main__":
    # Parte do código que seta as configurações da tela
    pygame.init()
    size = [largura_tela, altura_tela]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Calcule forças e campo elétrico")
    clock = pygame.time.Clock()
 
    done = False

    ball_list = []

    print("\nBem-vindo, comandos:\nn para nova carga\nf para mostrar as forças")
    print("\nClique com o mouse em algum ponto da tela para mostrar os campos\n\n")
    # While que funciona enquanto não tiver sido clicado o botão de fechar
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Parte do código que lida com as teclas do teclado 
                if event.key == pygame.K_n:
                    print("\n########################")
                    print("Você clicou em 'n'")
                    # Adiciona nova bola
                    ball_list.append(adiciona_nova_bola(len(ball_list)))
                    # Toda vez que uma nova bola é adicionadas é refeito o calculo para saber as 
                    #   forças atuantes entre todas as bolas
                    for bola in ball_list:
                        bola.carga['forcas'] = [a for a in forcas_atuantes(bola, ball_list)]
                if event.key == pygame.K_f:
                    print("\n########################")
                    print("Você clicou em 'f'")
                    for ball in ball_list:
                        # Parte que mostra todas as cargas ao pressionar f
                        for forca in ball.carga['forcas']:
                            print(f"\nForça entre {forca['carga1']} e {forca['carga2']}")
                            print(f"\nCarga {forca['forca']} N")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Ao clicar com o mouse em algum local da tela essa parte do código calcula o campo elétrico no local
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                pygame.draw.circle(screen, marron, [x, y], tamanho_carga)
                # Conversao para calcular e printar o ponto
                x = x - int(centroX)
                y = int(centroY) + (y * (-1))
                print("\n########################")
                print(f"\nNo ponto x={x} e y={y}")
                # Mostra o campo elétrico gerado por cada carga
                for campo in get_campos_eletricos(ball_list, x, y):
                    print(f"\nCampo gerado pela carga {campo['carga']}")
                    print(f"Valor: {campo['campo']} N/C")

        # Fundo preto
        screen.fill(preto)
        # Linha do X
        pygame.draw.line(screen, marron, [0, centroY], [largura_tela, centroY])
        # Linha do Y
        pygame.draw.line(screen, marron, [centroX, 0], [centroX, altura_tela])
        # Desenha as bolas
        for ball in ball_list:
            pygame.draw.circle(screen, branco, [ball.x, ball.y], tamanho_carga)
 
        # Limitação de 60fps para exibir a tela
        clock.tick(60)
 
        # Atualiza a tela
        pygame.display.flip()
 
    # Sair do programa
    pygame.quit()
