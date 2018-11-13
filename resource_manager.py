# coding: utf-8

import os
import pygame as pg

from font import *

class ResourceManager:
    """
    Gerenciador de Recursos
    """
    sounds = {}
    musics = {}
    """
    Efeitos sonoro
    """

    fonts = {}
    """
    Fontes
    """

    images = {}
    """
    Imagens
    """

    def __init__(self, config, dir_root = None):
        """
        Construtor
        @param dir_root: Diretório raiz
        @return: Instância
        """

        self.config = config

        if dir_root:
            self.load(dir_root)

    def load(self, dir_root):
        """
        Carregar
        @param dir_root: Diretório raiz
        """
        self.dir_root = dir_root
        self.dir_music = os.path.join(self.dir_root, 'audio', 'music')
        self.dir_sound = os.path.join(self.dir_root, 'audio', 'sound')
        self.dir_font  = os.path.join(self.dir_root, 'fonts')
        self.dir_image = os.path.join(self.dir_root, 'image')

        self.load_sound()
        self.load_music()
        self.load_image()
        self.load_font()

    def load_sound(self):
        """
        Carregar efeitos sonoros
        """
        files = self.list_files(self.dir_sound)
        for file_name in files:
            file_path = os.path.join(self.dir_sound, file_name)
            if os.path.isfile(file_path):
                if self.config.sound:
                    self.sounds[file_name] = pg.mixer.Sound(file_path)
                else:
                    self.sounds[file_name] = None

    def load_music(self):
        """
        Carregar efeitos sonoros
        """
        files = self.list_files(self.dir_music)
        for file_name in files:
            file_path = os.path.join(self.dir_music, file_name)
            if os.path.isfile(file_path):
                self.musics[file_name] = file_path

    def init_mixer(self):

        if self.config.sound:
            """
            Inicia mixer
            """
            FREQ = 44100   # same as audio CD
            BITSIZE = -16  # unsigned 16 bit
            CHANNELS = 2   # 1 == mono, 2 == stereo
            BUFFER = 1024  # audio buffer size in no. of samples
            pg.mixer.pre_init(FREQ, BITSIZE, CHANNELS, BUFFER) # setup mixer to avoid sound lag
            pg.mixer.init()


    def load_font(self):
        """
        Carregar fontes
        """
        files = self.list_files(self.dir_font)
        for file_name in files:
            file_path = os.path.join(self.dir_font, file_name)
            self.fonts[file_name] = file_path

    def list_files(self, dir):
        return [f for f in os.listdir(dir) if not f.startswith('.') and not f.endswith('.db')]

    def load_image(self):
        """
        Carregar imagens
        """
        files = self.list_files(self.dir_image)
        for file_name in files:
            file_path = os.path.join(self.dir_image, file_name)
            self.images[file_name] = pg.image.load(file_path)

    def get_image(self, name):
        """
        Obtém imagem
        @param name: Nome
        @return: Imagem
        """
        # name = name.replace('.png', '.bmp')
        return self.images[name]

    def get_scalled_image(self, name, scale):
        image = self.get_image(name)
        size = image.get_size()
        w, h = int(size[0] * scale), int(size[1] * scale)
        return pg.transform.scale(image, (w, h))

    def get_font_by_name(self, name, size):
        """
        Obtém Fonte pelo nome
        @param name: Nome
        @param size: Tamanho
        @return: Fonte
        """
        font_path = self.fonts[name]
        return pg.font.Font(font_path, size)

    def get_font_very_small(self, name):
        """
        Obtém Fonte muito pequena
        @param name: Nome
        @return: Fonte
        """
        return self.get_font_by_name(name, Font.VERY_SMALL)

    def get_font_small(self, name):
        """
        Obtém Fonte pequena
        @param name: Nome
        @return: Fonte
        """
        return self.get_font_by_name(name, Font.SMALL)

    def get_font_normal(self, name):
        """
        Obtém Fonte Normal
        @param name: Nome
        @return: Fonte
        """
        return self.get_font_by_name(name, Font.NORMAL)

    def get_font_large(self, name):
        """
        Obtém Fonte Grande
        @param name: Nome
        @return: Fonte
        """
        return self.get_font_by_name(name, Font.LARGE)

    def play_sound(self, name, loops=1):
        """
        Reproduzir efeito sonoro
        @param name: Nome
        @param loops: Repetição
        """
        if self.config.sound:
            sound = self.sounds[name]
            # sound.play(loops)
            ch = pg.mixer.find_channel()
            if ch:
                ch.play(sound, loops)

    def play_music(self, name, loops=1):
        """
        Reproduz música
        @param name: Nome
        @param loops: Quantas vezes repetir
        """
        if self.config.sound:
            file_path = os.path.join(self.dir_music, name)
            pg.mixer.music.load(file_path)
            pg.mixer.music.play(loops)

    def get_font(self, size=Font.NORMAL):
        """
        Obtém Fonte padrão
        @param size: Tamanho
        @return: Fonte
        """
        default_name = self.get_font_default_name()
        return self.get_font_by_name(default_name, size)

    def get_font_default_name(self):
        """
        Obtém Fonte padrão
        @return: Fonte
        """
        if len(self.fonts) > 0:
            first_font_name = list(self.fonts.keys())[0]
            return first_font_name
        else:
            return pg.font.get_default_font()

    def get_font_path(self, name):
        """
        Obtém caminho da fonte
        @param name: Nome
        @return: Fonte
        """
        return os.path.join(self.dir_font, name)

