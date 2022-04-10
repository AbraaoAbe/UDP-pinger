from socket import *
from random import randint
import time

# What's your IP address and witch port should we use?
recieve_host = '127.0.0.1'
recieve_port = 30000

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind((recieve_host, recieve_port))

# #servidor em modo de ouvir
# serverSocket.listen()
#
# conn, ender = serverSocket.accept()


while True:
  message, address = serverSocket.recvfrom(1024)
  #message = message.upper()

  str_tester = str(message, "utf8")

  flag_erro = False

  for x in range(10): #verifica se os 10 primeiros digitos estao no padrao de digitos
    if str_tester[x] < '0' or str_tester[x] > '9':
      flag_erro = True

  if str_tester[5] != '0': #verifica se o ping esta setado em 0
    flag_erro = True

  rand = randint(1,10) #gera um numero aleatorio

  str_message = ""

  str_erro = ""
  if flag_erro:
    str_erro = " COM ERRO"

  print("Mensagem recebida"+ str_erro +" do endereço: '" + str(address[0]) + "': " + str(message, "utf8"))

  if rand == 1: #erro de sequencia
    print("Foi inserido um erro de sequência!!")

    str_message = '9' + str(message[1:5], "utf8") + '1' + str(message[6:], "utf8")
  elif rand == 2: #erro de ping
    print("Foi inserido um erro de ping/pong")
    str_message = str(message[:5], "utf8") + '0' + str(message[6:], "utf8")
  elif rand == 3: #erro de timestrap
    print("Foi inserido um erro de timestrap")
    str_message = str(message[:5], "utf8") + '1' + 'T'+ str(message[7:], "utf8")
  else:
    str_message = str(message[:5], "utf8") + '1' + str(message[6:], "utf8")


    # str_message = str(message[:5], "utf8") + '1' + str(message[6:], "utf8")  # modificando o indicador ping para pong

  serverSocket.sendto(bytes(str_message, "utf8"), address)