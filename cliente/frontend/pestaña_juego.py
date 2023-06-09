from email.mime import image
from re import S
import sys
import os
from tkinter import Frame
from PyQt5.QtCore import pyqtSignal, QRect, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMainWindow
from PyQt5.QtGui import QPixmap
from os import path
import random as r
from PyQt5 import uic

nombre_ventana, base_class = uic.loadUiType("sala_pelea.ui")

class PestañaJuego(QMainWindow, nombre_ventana, base_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)
    
    def abrir(self):
        self.show()
