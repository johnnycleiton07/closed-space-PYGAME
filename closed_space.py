import pygame
import time
import random

pygame.init()

#___________________CONFIGURAÇÕES DA TELA__________________#

largura = 800
altura = 600
tamanhoTela = (800, 600)
tela = pygame.display.set_mode(tamanhoTela)

telaDoJogo = pygame.image.load("/home/johnny/Github/closed-space-PYGAME/images/screen.png")
telaInicial = pygame.image.load("/home/johnny/Github/closed-space-PYGAME/images/homescreen.png")
icone = pygame.image.load("/home/johnny/Github/closed-space-PYGAME/images/icon.png")

pygame.display.set_caption("CLOSED SPACE")
pygame.display.set_icon(icone)

preto = (0, 0, 0)
branco = (255, 255, 255)
verdeClaro = (0, 200, 0)
verdeEscuro = (0, 150, 0)
vermelhoClaro = (200, 0, 0)
vermelhoEscuro = (150, 0, 0)

imagemPersonagem1 = pygame.image.load("/home/johnny/Github/closed-space-PYGAME/images/Milenium Falcon.png")
somDeBatida = pygame.mixer.Sound("/home/johnny/Github/closed-space-PYGAME/sounds/crash.ogg")
pygame.mixer.music.load("/home/johnny/Github/closed-space-PYGAME/sounds/Orange Sunshine (Rod Hamilton & Tiffany Seal).ogg")


larguraDaNave = 170 # Largura da imagem em pixels

relogio = pygame.time.Clock()

#__________________________FUNÇÕES__________________________#

def telaDeInicio():
    intro = True
    
    while intro:
        for event in pygame.event.get():
            print (event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        tela.blit(telaInicial, (0, 0))

        botao("EXIT", 550, 450, 100, 50, vermelhoClaro, vermelhoEscuro, sairDoJogo)
        botao("PLAY", 150, 450, 100, 50, verdeClaro, verdeEscuro, circuitoDoJogo)
        
        pygame.display.update()

        relogio.tick(15)

def botao(mensagem, x, y, lar, alt, aceso, apagado, movimento = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if mensagem == "PLAY":
        if (x + lar) > mouse[0] > x and (y + alt) > mouse [1] > y:
            pygame.draw.rect(tela, apagado, (x, y, lar, alt))
            if (click[0] == 1) and (movimento != None):
                circuitoDoJogo()
            
        else:
            pygame.draw.rect(tela, aceso, (x, y, lar, alt))
            

    if mensagem == "EXIT":
        if (x + lar) > mouse[0] > x and (y + alt) > mouse [1] > y:
            pygame.draw.rect(tela, apagado, (x, y, lar, alt))
            if (click[0] == 1) and (movimento != None):
                sairDoJogo()
            
        else:
            pygame.draw.rect(tela, aceso, (x, y, lar, alt))


    smallText = pygame.font.Font(None, 25)
    textSurf, textRect = configuracoesTexto(mensagem, smallText)
    textRect.center = ((x +(lar / 2)), (y + (alt / 2)))
    tela.blit(textSurf, textRect)

def personagem(x, y):
    tela.blit(imagemPersonagem1, (x, y))

def objeto(posicaoX, posicaoY, larguraObjeto, alturaObjeto, corObjeto):
    pygame.draw.rect(tela, corObjeto, [posicaoX, posicaoY, larguraObjeto, alturaObjeto])

def esquivou(count):
    fonteDoTexto = pygame.font.SysFont(None, 25)
    texto = fonteDoTexto.render("SCORE: " + str (count), True, branco)
    tela.blit(texto, (30, 0))

def bateu():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(somDeBatida)
    
    mensagemFinal("Game Over")

def configuracoesTexto(texto, fonte):
    superficie = fonte.render(texto, True, branco)
    return superficie, superficie.get_rect()

def mensagemFinal(texto):
    textoFinal = pygame.font.Font(None, 115)
    TextSurf, TextRect = configuracoesTexto (texto, textoFinal)
    TextRect.center = ((largura / 2), (altura / 2))
    tela.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)

    telaDeInicio()
    
def configuracoesTexto2(texto):
    textoFinal = pygame.font.Font(None, 115)
    TextSurf, TextRect = configuracoesTexto (texto, textoFinal)
    TextRect.center = ((largura / 2), (altura / 2))
    tela.blit(TextSurf, TextRect)

    pygame.display.update()

def sairDoJogo():
    pygame.quit()
    quit()

#_______________________FUNÇÃO PRINCIPAL_____________________#

def circuitoDoJogo():
    sair = False
    pygame.mixer.music.play(-1)
    
    x = 300
    y = 430
    
    mover = 0
    count = 0

    posicaoX = random.randrange(0, 800) # Sorteia o objeto sobre o eixo x
    posicaoY = -600 # Objeto começa a cair vindo de fora da tela
    larguraObjeto = 80
    alturaObjeto = 50
    corObjeto = (branco)

    velocidadeObjeto = 30
        
    while (sair == False):
        for event in pygame.event.get(): # Captura eventos no hardware do computador
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN: 
                if (event.key == pygame.K_LEFT): # Tecla esquerda
                    mover = -25
                elif (event.key == pygame.K_RIGHT): # Tecla direita
                    mover = 25

            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT):
                    mover = 0
                elif (event.key == pygame.K_RIGHT):
                    mover = 0

        x = x + mover
        tela.blit(telaDoJogo, (0, 0))

        objeto(posicaoX, posicaoY, larguraObjeto, alturaObjeto, corObjeto) 
        posicaoY = posicaoY + velocidadeObjeto
        
        personagem(x, y)
        esquivou(count)

        if (posicaoY > 600):
            posicaoY = 0 - alturaObjeto
            posicaoX = random.randrange(0, 800) # Faz o objeto surgir novamente
        
            count = count + 1

        if (x > (largura - larguraDaNave) or x < 0): # Caso tente ultrapassar os extremos da tela é GAME OVER
            bateu()
            
            
        elif (y < (posicaoY + alturaObjeto)): # Se o personagem e o objeto se encontram no eixo y, OK
            if posicaoX < x + larguraDaNave and posicaoX + larguraObjeto > x: # Mas se também se encontrarem no eixo x, GAME OVER
                bateu()
            
        pygame.display.update()
        
telaDeInicio()
circuitoDoJogo()
pygame.quit()
quit()