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

nombre_ventana, base_class = uic.loadUiType("salaespera.ui")

class SalaDeEspera(QMainWindow, nombre_ventana, base_class):

    senal_enviar_usuario = pyqtSignal(dict)
    senal_cambio = pyqtSignal(str)

    def __init__(self):
        
        super().__init__()
        self.setupUi(self)

        self.nombre_usuario
        self.nombre_rival.setText("Jugador 2")
        self.tiempo_restante_label

    def abrir(self, event):
        self.tiempo_restante_label.setText(str(event))
        self.tiempo_restante_label.repaint()
        self.show()
    
    def actualizar_nombre(self, nombre):
        self.nombre_usuario.setText(nombre)
        self.nombre_usuario.repaint()

    def actualizar_nombre_rival(self, rival):
        self.nombre_rival.setText(rival)
        self.nombre_rival.repaint()
        

    def actualizar_datos(self, event):

        self.tiempo_restante_label.setText("    "+ str(event))
        self.tiempo_restante_label.repaint()
    
    def cerrar(self):

        self.hide()