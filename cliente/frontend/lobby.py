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

nombre_ventana, base_class = uic.loadUiType("lobby.ui")

class Lobby(QMainWindow, nombre_ventana, base_class):

    senal_enviar_usuario = pyqtSignal(dict)
    senal_cambio = pyqtSignal(int)

    def __init__(self):
        
        super().__init__()
        self.setupUi(self)

        self.show()

    def enviar_nombre_usuario(self):
        nombre = self.nombre_usuario.text()
        dic = {"accion": "login", "nombre": nombre}
        self.senal_enviar_usuario.emit(dic)

    def validacion_login(self, event):
        if event["estado"] == "invalido":
            self.error.setStyleSheet("background-color: lightblue;")
            if event["razon"] == "nombre":
                self.error.setText("  Error, nombre ya utilizado")  
            else:
                self.error.setText("  Error, usuario invalido")  
        
        elif event["estado"] == "valido":

            self.senal_cambio.emit(event["timer"])
            self.hide()

        elif event["estado"] == "sala_llena":
            self.error.setText("     La sala esta llena, prueba mas tarde")




    

        
