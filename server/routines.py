# !/usr/bin/python3
# -*- coding: utf-8 -*-
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))

def path_join(name):
    r"""
    Relativo à informação acerca do diretório em execução

    Args:
        name (str): O nome do arquivo.

    Returns:
        str: Retorna o caminho absoluto do arquivo.
    """
    return os.path.join(APP_DIR, name)