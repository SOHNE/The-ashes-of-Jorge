#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import socket
import os
import sys
import rank


HOST = '127.0.0.1' # Endereco IP do Servidor. No caso, um loopback ip.
PORT = 5000 # Porta de comunicação do servidor
 
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Iniciando o socket e definindo o makefile
self = (HOST, PORT) # Agrupando as informações
 
# Aplicando o endereço IP e a porta no Socket
tcp.bind(self)
 
# Garante ao server aceitar conexões
tcp.listen(1)
 
print('\nServidor TCP iniciado no IP', HOST, 'na porta', PORT)
 
while True:
    # Aceitando uma nova conexão
    conexao, cliente = tcp.accept()
    print('\nConexão realizada por:', cliente)
 
    while True:
        # Recebendo as mensagens através da conexão
        mensagem = conexao.recv(1024)
        
        # Conexão encerrada
        if not mensagem:
            break
 
        # Exibindo a mensagem recebida
        print('\nCliente..:', cliente)
        print('Mensagem.:', mensagem.decode())
        if mensagem.decode() == b"\x18":
            conexao.close()
 
    # Exibindo a mensagem de finalização da conexão
    print('Finalizando conexão do cliente', cliente)
 
    # Fechando a conexão com o Socket
    conexao.close()