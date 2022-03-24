from turtle import update
from View.Interface import Ui_MainWindow
import serial
import json
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt5 import QtCore, QtGui, QtWidgets
import math

class Datos(QtWidgets.QMainWindow):

    def __init__(self): #, ui, MainWindow) -> None:
        super().__init__()
        #Llamo a la clase main window del main script, ademas
        #llamo el objeto de la clase Ui_MainWindow obtenida en el 
        #main script
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Valores de las graficas
        self.valueVel = 0
        self.sampling = 0.015
        self.period = 10 
        self.gData = []
        self.gData.append([i*self.sampling for i in range(0,math.ceil(self.period/self.sampling))])
        self.gData.append([0.0])
        self.fig = plt.figure(figsize=(10,8))
        self.fig.ylim = (0,10)
        self.fig.xlim = (0,100)
        
        #crear hilos de ejecucion, para poder leer los sensores
        #self.hiloClose = threading.Thread(target=self.askQuit)
        self.hilo1 = threading.Thread(target=self.recibir, daemon=True)
        self.reading = threading.Event()
        self.reading.set()

        #Metodo para cerrar el hilo, y que no se quede ejecutando
        #como proceso de segundo plano, infinitamente

        #objeto serial, para comenzar comunicacion serial con microcontrolador
        self.communication = serial.Serial("COM8",115200,timeout=2)
        time.sleep(1.0)

        #Signals/Slots
        self.ui.pushButtonEnviar.clicked.connect(self.enviar)

        self.isRun = True
        self.hilo1.start()
        #gafica=self.Graficar()

        #self.hiloClose.start()


    def enviar(self):
        
        print('ENVIARRR...')
        self.reading.clear()
        #print(self.reading.is_set())
        time.sleep(2)
        #self.communication.reset_input_buffer()
        #self.communication.reset_output_buffer()
        posicion = self.ui.lineEditPosicion.text()
        tiempo = self.ui.lineEditTiempo.text()
        direccion = self.ui.lineEditDireccion.text()

        #variables = {'posicion' : self.ui.lineEditPosicion.text(),'tixempo' : self.ui.lineEditTiempo.text(), 'direccion' : self.ui.lineEditDireccion.text()}
        #jsonData = json.dumps(variables)

        str = "MOVE:" + direccion + ";" + posicion + ";" + tiempo
        try:
            self.communication.write(str.encode('ascii'))
            print('envie informacion')
            time.sleep(2)
            self.reading.set()
            #print(self.reading.is_set())
        except:
            print('error buffer')
            self.reading.set()

        time.sleep(float(tiempo)+1)
        while len(self.gData[1]) < len(self.gData[0]):
            self.gData[1].append(0.0)
        plt.plot(self.gData[0],self.gData[1])
        plt.show()
        self.gData[1] = [[0.0]]
        

    def recibir(self):
        
        while self.isRun:
            
            #print(f'maricaaaa!! {self.reading.is_set()}')
            if self.reading.is_set() == True:
                try:
                    #self.communication.reset_input_buffer()
                    str = self.communication.readline().decode('utf-8').strip()
                    
                    if str:
                        try:
                            pos = str.index(':')
                            label = str[:pos]
                            value = str[pos+1:]
                            if label == 'VEL':
                                try:
                                    self.gData[1].append(float(value))
                                    print(f'gdata {self.gData[1]}')
                                    if len(self.gData[1]) > len(self.gData[0]):
                                        self.gData[1].pop(0)
                                except:
                                    print("tipo de dato")
                                self.ui.labelVelocidad.setText(value)
                            elif label == 'T':
                                self.sampling = int(value)*(10**-3)
                                self.gData[0] = [i*self.sampling for i in range(0,math.ceil(self.period/self.sampling))]
                            else:
                                continue
                        except:
                            print('Comando invalido')
                except:
                    print('hubo un leve error')
            else:
                continue


    #def Graficar(self):

        ''' def update_line(num,hl,data):
            dx = np.array(range(len(data[1])))
            dy = np.array(data[1])
            hl.set_data(dx,dy)
            return hl'''
            
        #fig = plt.figure(figsize=(10,8))
        #fig.ylim = (0,10)
        #fig.xlim = (0,100)
        #hl= plt.plot(self.gData[0],self.gData[1])

        #line_ani = animation.FuncAnimation(fig, update_line, fargs = (hl,self.gData),interval = 50, blit = False)


    def closeEvent(self,event): 

        try:
            self.isRun = False
            self.communication.close()
            plt.close(1)
            self.hilo1.join(0.1)
            print('*******Finalizado*******')
        except Exception as e:
            print(e)
