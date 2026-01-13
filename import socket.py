import socket
import pygame
import os
import numpy as np
os.environ['SDL_VIDEO_WINDOW_POS'] = "1920,0"

pygame.init()
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

ESP_IP = "192.168.4.1"
PORTA = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ESP_IP, PORTA))
sock.send(b"ok")

print("Conectado ao ESP32")

pygame.mixer.init(frequency=44100, size=-16, channels=1)

def gerar_tom(frequencia, duracao=1.0, volume=0.5):
    sample_rate = 44100
    t = np.linspace(0, duracao, int(sample_rate * duracao), False)

    onda = np.sin(2 * np.pi * frequencia * t)

    audio = onda * (2**15 - 1) * volume
    audio = audio.astype(np.int16)

    som = pygame.mixer.Sound(buffer=audio)
    som.play()

try:
    while True:
        dado = sock.recv(1024).decode().strip()
        if dado:
            tela.fill((0, 0, 0))
            linha = ""
            for c in dado:
                if c == '\n':
                    exec(linha)
                    linha = ""
                else:
                    linha += c
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

except KeyboardInterrupt:
    print("Encerrando...")
finally:
    sock.close()
pygame.quit()