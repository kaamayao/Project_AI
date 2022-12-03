# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:46:20 2022

@author: David Ernesto Ramirez Arboleda
"""
import numpy as np
import random
from scipy.stats import norm  # Importa  distribución normal
    
    
class Cirugia():    
    def __init__(self,duracion,vencimiento): 
        self.duracion=duracion 
        self.vencimiento=vencimiento #prioridad
    def quirofano(self,a):
        self.quirofano=a 

class AsignacionesIniciales():
    def __init__(self):
        self.CrearCirugias() 
        self.Bubblesort()
        self.AsignacionInicial()
        
    def CrearCirugias(self):
        self.quirofanos=[[],[],[],[],[],[]]
        self.ListaCirugias=[]
        #Seis quirofanos,5 dias, cirugias entre 1 y 5 horas
        TotalCirugias=int((24*5*6)/3) #24 horas, seis pabellones 5 dias 
        for x in range(TotalCirugias):
            self.ListaCirugias.append(Cirugia(random.randint(1,5),random.randint(5,54*5)))


    def Bubblesort(self): #ordenamos la prioridad de las cirugias
        contador=1
        while contador!=0:
            contador=0
            for x in range(len(self.ListaCirugias)-1):
                if self.ListaCirugias[x].vencimiento>self.ListaCirugias[x+1].vencimiento:
                    a=self.ListaCirugias[x]
                    b=self.ListaCirugias[x+1]
                    self.ListaCirugias[x]=b
                    self.ListaCirugias[x+1]=a
                    contador+=1
                    
    def printVencimientos(self):  #Ver prioridades de cirugias
        for x in self.ListaCirugias:
            print(x.vencimiento,end="  ")
            
    def printDuraciones(self): #ver tiempos cirugias
         for x in self.ListaCirugias:
            print(x.duracion,end="  ")
    def printQuirofanos(self,n):
        for x in self.quirofanos[n]:
            print(x.duracion,x.vencimiento, end=",  ")
    def AsignacionInicial(self): #Asignamos los quirofanos por prioridad
        turno=0
        while turno<len(self.ListaCirugias):
            for y in self.quirofanos:
                y.append(self.ListaCirugias[turno])
                turno+=1
    def SumaTiemposCirugias(self,n):
        suma=0
        for x in self.quirofanos[n]:
            suma+=x.duracion
        return suma

class Simulacion():
    def __init__(self,AsignacionesQuirofanos,ListaCirugias):
        self.AsignacionesQuirofanos=AsignacionesQuirofanos
        self.ListaCirugias=ListaCirugias
        self.simular()
    def simular(self):
        retrazos=[]
        for x in self.AsignacionesQuirofanos:
            RetrazoTotal=0
            for y in x: #Solo los retrazos se suman, las cirugias + rapidas d elo programado reducen tiempo de retrazo ó dejan la sala vacia.
                mu, sigma=y.duracion, y.duracion*0.2
                retrazo=np.random.normal(mu, sigma, 1)[0]
                if RetrazoTotal>0:
                    RetrazoTotal+=retrazo
                else:
                    if retrazo>0:
                        RetrazoTotal+=retrazo
            retrazos.append(RetrazoTotal)
        print(retrazos,"####")
        print("promedio=",sum(retrazos)/len(retrazos))
        self.promedio=sum(retrazos)/len(retrazos)

                
def main_heuristics_genetic(): 
    ###SIMULACION DE ASIGNACIONES INICIALES
    prom=[]
    for x in range(10**2):
        r=AsignacionesIniciales() #Creamos cirugias, asignamos a quirofanos
        t=Simulacion(r.quirofanos,r.ListaCirugias) #simulamos con asignaciones iniciales
        prom.append((t.promedio))
    print("RESULTADO: El promedio de demora con las asignaciones iniciales es")
    print(sum(prom)/len(prom))
