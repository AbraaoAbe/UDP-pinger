from socket import *
from datetime import datetime
import math

#calculo do desvio de acordo com a formula de desvio padrao
def desvio(lista_rtts , media):
    if len(lista_rtts) == 0:
        return 0
    soma = 0.0

    for i in lista_rtts:
        soma += (i - media)**2

    soma = soma/len(lista_rtts)

    soma = math.sqrt(soma)

    return soma

def tratamento_erros(ID, timestap, original_message, recieve_message, ping, host):
    str_rmessage = str(recieve_message, "utf8") #trasforma em string


    if str_rmessage[0:5] != ID:
        print("Resposta do servidor '"+str(host)+"': " + str_rmessage + ", ms: " +str(format(ping, '.1f')) + " (erro: alteracao de sequencia)")
    elif str_rmessage[5:6] != '1':
        print("Resposta do servidor '"+str(host)+"': " + str_rmessage + ", ms: " +str(format(ping, '.1f')) + " (erro: tipo de aquisicao ping/pong)")
    elif str_rmessage[6:10] != timestap:
        print("Resposta do servidor '"+str(host)+"': " + str_rmessage + ", ms: " +str(format(ping, '.1f')) + " (erro: alteracao no timestap)")
    elif str_rmessage[10:] != original_message:
        print("Resposta do servidor '"+str(host)+"': " + str_rmessage + ", ms: " +str(format(ping, '.1f')) + " (erro: alteracao na mensagem do pacote)")
    else:
        print("Resposta do servidor '"+str(host)+"': " + str_rmessage + ", ms: " +str(format(ping, '.1f')))

def main():
    # send_host = '127.0.0.1'
    # send_port = 30000

    send_host = '152.67.56.170'
    send_port = 54321

    # send_host = '44.201.148.94'
    # send_port = 4789

    # send_host = '200.137.66.110'
    # send_port = 30000

    adress = (send_host, send_port)
    #print(adress)

    timeAll = datetime.now()
    timeAll.microsecond

    send_message = ""
    senders = 0
    receivers = 0

    flag = 0

    min = 0
    max = 0
    media = 0

    lista_rtts = []
    verify_list = []

    for i in range(10):
        socket_client = socket(AF_INET, SOCK_DGRAM)  # cria o socket


        try:
            socket_client.settimeout(1) #controle de tempo em segundos
            timeInic = datetime.now().microsecond
            timestap = int(timeInic/100) #tempo inicial de envio da mensagem


            ID = str(i).zfill(5) #00001, 00002, 00003...
            str_timestap = str(timestap).zfill(4) #timestap ajustado para o envio da mensagem
            #print(str_timestap)
            str_messagemax30 = "Abraao Jesus Dos Santos" #mensagem a ser enviada (nome do aluno)

            verify_list.append([ID, str_timestap, str_messagemax30]) #lista de envios

            send_message = ID + str(0) + str_timestap + str_messagemax30
            socket_client.sendto(bytes(send_message, "utf8"), adress) #envio da mensagem
            senders += 1

            message, address = socket_client.recvfrom(1024) #recebimento da mensagem ( ou nao)
            timeEnd = datetime.now().microsecond #tempo final de recebimento da mensagem
            receivers += 1


            ping = int((timeEnd- timeInic)/100) #quebro o microseconds que eh 123456 em somente 1234
            ping = ping/10 # uma nova quebra transformando o atual 1234 em 123.4
            # print(timeInic)
            # print(ping)
            # print(timeEnd)
            # print(timestap)
            if ping < 0: #caso de "overflow" do ping
                ping += 1000

            lista_rtts.append(ping)

            if flag == 0:
                min = ping
                max = ping
                media = ping
                flag = 1
            else:
                media += ping

            if ping < min:
                min = ping
            elif ping > max:
                max = ping

        except timeout:
            print("Tentativa de conexão com o servidor '"+str(send_host)+"': Tempo excedido!!") #caso o pacote não seja enviado no tempo determinado
        else:
            #trata todos os erros e imprime na tela
            tratamento_erros(ID, str_timestap, str_messagemax30, message, ping, send_host)
            #print("Resposta do servidor: " + str(message) + "ms: " + str(ping))

    endAll = datetime.now()
    if receivers != 0:
        media = media/receivers

    #print(verify_list)

    ping_all = (endAll - timeAll)
    ms_all = (endAll - timeAll).microseconds/1000

    if ping_all.seconds > 0:
        ms_all += (ping_all.seconds * 1000)

    print(f"{senders} packets transmitted, {receivers} received, {100 - receivers/senders*100}% packet loss, time {ms_all}ms rtt min/avg/max/mdev = {format(min, '.2f')}/{format(media, '.2f')}/{format(max, '.2f')}/{format(desvio(lista_rtts, media), '.2f')}ms")
main()
