import paho.mqtt.client as mqtt
import numpy as np
import pygame
from pygame.locals import *
import sys

# Defina o tópico que você quer se inscrever
topic = "FPGA/input"

# Inicialize o Pygame
pygame.init()
pygame.display.set_caption('Polinvaders XD')
largura = 500
altura = 800
tela = pygame.display.set_mode((largura, altura))

# Defina o tamanho do retângulo
largura_retangulo = 40
altura_retangulo = 40


# Função para transformar a string em uma matriz 8x16
def string_to_matrix(payload_str):
  # Preencher a string com zeros à direita, se necessário
  payload_str = payload_str.ljust(16 * 8, '0')
  # Transformar a string em uma matriz 8x16
  matrix = np.array(list(payload_str)).astype(int).reshape(16, 8)
  return matrix


# Função para converter um vetor binário em decimal
def binary_to_decimal(binary_vector):
  decimal_value = 0
  for i in range(len(binary_vector)):
    decimal_value += binary_vector[i] * (2**(len(binary_vector) - 1 - i))
  return decimal_value


# Função de callback para quando uma mensagem for recebida
def on_message(client, userdata, message):
  print("Mensagem recebida no tópico {}: {}".format(message.topic,
                                                    message.payload.decode()))
  # Transformar a string recebida em uma matriz 8x16
  global matriz
  matriz = string_to_matrix(message.payload.decode())


# Crie um cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Defina a função de callback para mensagens recebidas
client.on_message = on_message

# Conecte-se ao broker MQTT
client.connect("broker.hivemq.com", 1883)

# Inscreva-se no tópico
client.subscribe(topic)

# Inicie o loop de rede MQTT para receber mensagens
client.loop_start()

# Vetor binário inicial de 4 elementos
vetor_binario = [0, 0, 0, 0]

# Loop principal do jogo
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      client.loop_stop()  # Pare o loop MQTT
      sys.exit()

  tela.fill((0, 0, 0, 0))  # Limpe a tela

  # Desenhe os retângulos com base no vetor binário
  for i in range(len(vetor_binario)):
    x = 50 + i * (largura_retangulo + 10)
    y = 50
    cor = (255, 0, 0) if vetor_binario[i] == 1 else (0, 0, 0)
    pygame.draw.rect(tela, cor, (x, y, largura_retangulo, altura_retangulo))

  pygame.display.flip()
