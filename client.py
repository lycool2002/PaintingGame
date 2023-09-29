import pygame,sys, random
from pygame.locals import *
import socket

blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
colour = [random.randint(100,255),random.randint(100,255),random.randint(100,255)]
serverIP = '127.0.0.1'
port = 60000

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((serverIP, port))
    #connect

    pygame.init()
    fpsClock = pygame.time.Clock()
    playSurface = pygame.display.set_mode((640,480))
    pygame.display.set_caption('paint')
    ptPosition = [100,100]
    #pygame init

    client.send(bytes(str(['join', colour]), 'utf-8'))
    serverMap = client.recv(65536)
    #join game

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:#QUIT
                buf = bytes(str(['end']), 'utf-8')
                client.send(buf)
                client.close()
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:#MOVE
                if event.key == K_RIGHT or event.key == ord('d'):
                    if ptPosition[0] < 620:
                        ptPosition[0] += 20
                    else:
                        ptPosition[0] = 0
                if event.key == K_LEFT or event.key == ord('a'):
                    if ptPosition[0] > 0:
                        ptPosition[0] -= 20
                    else:
                        ptPosition[0] = 620
                if event.key == K_UP or event.key == ord('w'):
                    if ptPosition[1] > 0:
                        ptPosition[1] -= 20
                    else:
                        ptPosition[1] = 460
                if event.key == K_DOWN or event.key == ord('s'):
                    if ptPosition[1] < 460:
                        ptPosition[1] += 20
                    else:
                        ptPosition[1] = 0
                client.send(bytes(str(['pt', ptPosition]), 'utf-8'))#send move pos
                serverMap = client.recv(65536)#recv map
                
                if event.key == event.key == ord('b'):#DRAW
                    client.send(bytes(str([colour, ptPosition]), 'utf-8'))#send draw pos
                    serverMap = client.recv(65536)#recv map
                    break
                elif event.key == event.key == ord('n'):#ERASE
                    client.send(bytes(str(['e', ptPosition]), 'utf-8'))#send erase pos
                    serverMap = client.recv(65536)#recv map
                    break
                elif event.key == K_ESCAPE:#QUIT
                    pygame.event.post(pygame.event.Event(QUIT))
        else:#ELSE
            client.send(bytes(str(['get']), 'utf-8'))#request map
            serverMap = client.recv(65536)

        try:
            serverMap = eval(serverMap)
        except:
            pass
        #DISPLAY
        ''''
        if ptPosition[0] > 620 :
            ptPosition[0] -= 20
        if ptPosition[0] < 0:
            ptPosition[0] += 20
        if ptPosition[1] > 460:
            ptPosition[1] -= 20
        if ptPosition[1] < 0:
            ptPosition[1] += 20
        '''
        playSurface.fill(blackColour)
        if serverMap:
            for i in serverMap.values():
                for pos in i['map']:
                    pygame.draw.rect(playSurface, pygame.Color(i['color']), Rect(pos[0], pos[1],20,20))
            for pos in serverMap.values():
                pygame.draw.rect(playSurface, whiteColour, Rect(pos['pt'][0], pos['pt'][1],20,20))

        pygame.display.flip()
        fpsClock.tick(100)
        
if __name__ == "__main__":
    main()