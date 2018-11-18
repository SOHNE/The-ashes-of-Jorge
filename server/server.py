#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
# Compatibilizando com o python2

import socket
import os
import sys
import logging
import rank


HOST = '127.0.0.1' # Endereco IP do Servidor. No caso, um loopback ip.
PORT = 5000 # Porta de comunicação do servidor
RUNNING = True 

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Iniciando o socket pela subclasse e definindo o makefile
self = (HOST, PORT) # Agrupando as informações
 
# Aplicando o endereço IP e a porta no Socket
tcp.bind(self)
 
# Garante ao server aceitar conexões
tcp.listen(1)
 
print('\nServidor TCP iniciado no IP', HOST, 'na porta', PORT)
 
while RUNNING:
    # Aceitando uma nova conexão, caso haja
    conexao, cliente = tcp.accept()
    print('\nNova conexão:', cliente)

    while True:
        # Recebendo as mensagens através da conexão
        mensagem = conexao.recv(1024)
        
        # Se a conexão for encerrada
        if not mensagem:
            break

        # Caso a mensagem seja n, executar m
        if mensagem == b'E':
            print('\nEsperando envio.')
        elif mensagem == b'I':
            # Exibindo a mensagem recebida e de qual cliente
            print('\nCliente..:', cliente)
            print('Mensagem.:', mensagem.decode())
        
 
    # Exibindo a mensagem de finalização da conexão
    print('Finalizando conexão do cliente', cliente)
 
    # Fechando a conexão com o Socket
    conexao.close()