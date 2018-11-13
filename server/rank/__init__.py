# !/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from routines import *
import csv, json
__author__ = 'Leandro Peres'
__license__ = 'GPLv3'
__all__ = ['Load', 'Introduce', 'Organize']

class Organize(object):
    def __init__(self, lista):
        self.rank = {}
        self.all = {}
        for _ in lista:
            if 0 <= len(self.rank) <= 5:
                pass

class Introduce(object):
    def __init__(self):
        pass

class Load(object):
    r"""
    Classe para carregar e dispor, se requisitado, o rank.
    Além de realizar os cálculos para reorganizar o 'data.csv'
    """

    def __init__(self):
        with open(path_join('rank\\data.csv'), newline='', encoding='utf-8') as element:
            self.__list__ = []
            for _ in csv.DictReader(element):
                self.__list__.append(dict(_))
        Organize(self.__list__)
    