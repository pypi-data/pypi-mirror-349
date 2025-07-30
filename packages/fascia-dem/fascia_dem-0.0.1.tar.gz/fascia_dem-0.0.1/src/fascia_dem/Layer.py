import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
import time
import ast
from math import *
import random as rnd
from Functions import *

class Layer:

    def __init__(self,Id: str, angle: float, dimensions: list[float]):
        self.Shape=self.__Define_shape (dimensions)
        self.dimX, self.dimY = self.__Center()
        self.Id = Id 
        self.Nodes = np.ndarray((0,4), dtype='float')
        self.Bond  = np.ndarray((0,2),dtype='int64')
        self.Angle = angle
        self.Elasticity_modulus = 2.13e9
        self.Radius = 2e-4
        self.Collagen_ratio = 0.7
        self.Interpenetration = 0.8
        self.altitude = 0
        self.Stiffness = self.Elasticity_modulus*pi*(self.Radius)**2/(self.Interpenetration*2*self.Radius) 
        self.N_DE      = 0
        self.Set_of_DE   = dict()
        self.Set_of_Fiber = dict()
        self.N_Bond    = 0
        self.Set_of_Bond = dict()
        self.N_fiber = 0

    def __str__(self):
        output = f'The layer Id is {self.Id}\n'
        output += f'The layers contains {len(self.Nodes)} nodes and {len(self.Bond)} bonds\n'
        output += f'The elasticity moudlus of the fibers is {self.Elasticity_modulus} Pa\n'
        output += f'The radius of the fibers is {self.Radius} m and the collagen ratio is {self.Collagen_ratio}%\n'
        output += f'The angle of the fibers is {self.Angle}°' 
        return(output)
    
    def __Define_shape (self,dimensions: list[float]):
        if len(dimensions) == 2:
            a = dimensions[0]
            b = dimensions[1]
            Bound = np.ndarray((0,2))
            Bound = np.vstack((Bound,np.array([np.linspace(-a/2,a/2,250),np.linspace(b/2,b/2,250)]).T))
            Bound = np.vstack((Bound,np.array([np.linspace(a/2,a/2,250),np.linspace(b/2,-b/2,250)]).T))
            Bound = np.vstack((Bound,np.array([np.linspace(a/2,-a/2,250),np.linspace(-b/2,-b/2,250)]).T)) 
            Bound = np.vstack((Bound,np.array([np.linspace(-a/2,-a/2,250),np.linspace(-b/2,b/2,250)]).T))
        elif len(dimensions) == 1:
            R = dimensions[0]
            Bound = np.ndarray((1000,2))
            Theta = np.linspace(0,2*pi,1000)
            Bound[:,0]=R*np.cos(Theta)
            Bound[:,1]=R*np.sin(Theta)
        else:
            print("The dimensions of the domain are not correctly specified\nThe programm will stop.")
            quit()
        return(Bound)


    def __Center (self):
        dimsX = np.array([min(self.Shape[:,0]),max(self.Shape[:,0])])
        dimsY = np.array([min(self.Shape[:,1]),max(self.Shape[:,1])])
        dimX = (dimsX[1]-dimsX[0])/2
        dimY = (dimsY[1]-dimsY[0])/2
        lx=dimX - dimsX[1]
        ly=dimY - dimsY[1]
        self.Shape=self.Shape+[lx,ly]
        return(2*dimX,2*dimY)
    
    def Set_elasticity_modulus(self,E: float):
        self.Elasticity_modulus = 2.13e9
        self.Stiffness = self.Elasticity_modulus*pi*(self.Radius)**2/(self.Interpenetration*2*self.Radius) 

    def Set_radius(self,R: float):
        self.Radius = R
        self.Stiffness = self.Elasticity_modulus*pi*(self.Radius)**2/(self.Interpenetration*2*self.Radius)
        self.Nodes[:,3] = R

    def Set_interpenetration(self,Interpenetration: float):
        self.Interpenetration = 0.8
        self.Stiffness = self.Elasticity_modulus*pi*(self.Radius)**2/(self.Interpenetration*2*self.Radius)
        if self.Bond.shape[0] != 0:
            print('Nodes will be rebuilt')
            self.Build_Nodes()

    def Set_collagen_ratio(self,ratio: float):
        self.Collagen_ratio = ratio
        if self.Bond.shape[0] != 0:
            print('Nodes will be rebuilt')
            self.Build_Nodes()

    def Set_angle(self,angle:float):
        self.Angle = angle
        if self.Bond.shape[0] != 0:
            print('Nodes will be rebuilt')
            self.Build_Nodes()

    def Clean_geometry(self):
        self.Nodes = np.ndarray((0,4), dtype='float')
        self.Bond  = np.ndarray((0,2),dtype='int64')                
        self.N_DE      = 0
        self.Set_of_DE   = dict()
        self.Set_of_Fiber = dict()
        self.N_Bond    = 0
        self.Set_of_Bond = dict()
        self.N_fiber = 0

    def Set_altitude(self, Z: float):
        self.altitude = Z    

    def Build_nodes(self):
        self.Clean_geometry()
        fiber_spacing = 2*self.Radius*pi/(4*self.Collagen_ratio)
        if self.Angle == 0:
            self.__Build_horizontal(fiber_spacing)
        elif self.Angle == 90:
            self.__Build_vertical(fiber_spacing)
        else:
            self.__Build_Angled(fiber_spacing)
        self.Nodes[:,2] = self.altitude   


    def __Build_horizontal(self,fiber_spacing: float):
        dx = 2*self.Radius*self.Interpenetration
        n_bond = round(self.dimX/dx)
        x_vector = np.linspace(-self.dimX/2,self.dimX/2,n_bond+1)
        n_fiber = round(self.dimY/fiber_spacing)
        y_vector = -np.linspace(-self.dimY/2,self.dimY/2,n_fiber)
        new_fiber = 0
        fibers_group = np.ndarray((0,2)) 
        for i,e in enumerate(y_vector[:]):
            P=Get_intersection_points([0,e],self.Shape)
            fiber , new = self.__Create_fiber(P,dx,[0,e],new_fiber)
            if new:
                new_fiber += 1
                fibers_group = np.vstack((fibers_group,fiber))
        self.__Add_to_domain(fibers_group)        
                    
    def __Build_vertical(self,fiber_spacing: float):
        dy = 2*self.Radius*self.Interpenetration
        n_bond = round(self.dimY/dy)
        x_vector = np.linspace(-self.dimY/2,self.dimY/2,n_bond+1)
        n_fiber = round(self.dimX/fiber_spacing)
        y_vector = -np.linspace(-self.dimX/2,self.dimX/2,n_fiber)
        new_fiber = 0
        fibers_group = np.ndarray((0,2)) 
        for i,e in enumerate(y_vector[:]):
            P=Get_intersection_points([0,e],np.flip(self.Shape,1))
            fiber , new = self.__Create_fiber(np.flip(P,1),dy,[0,e],new_fiber)
            if new:
                new_fiber += 1
                fibers_group = np.vstack((fibers_group,fiber))
        self.__Add_to_domain(fibers_group)                                
    
    def __Build_Angled(self,fiber_spacing: float):
        angle = np.radians(self.Angle)
        d_f = fiber_spacing/abs(np.sin(angle))
        n_f = round(self.dimX/d_f)
        dx = 2*self.Radius*self.Interpenetration
        while angle < -pi/2 or angle > pi/2:
            angle = pi - angle
        if angle > 0 and angle < pi/2: 
            x_vector = np.linspace(-self.dimX/2,self.dimY/np.tan(angle)+self.dimX/2,round((self.dimY/np.tan(angle)+self.dimX)/d_f))
        elif angle < 0 and angle > -pi/2:
            x_vector = np.linspace(-(self.dimY/np.tan(-angle)+self.dimX/2),self.dimX/2,round((self.dimY/np.tan(-angle)+self.dimX)/d_f))
        else:
            pass        
        d_f = x_vector[1] - x_vector[0]
        new_fiber = 0
        fibers_group = np.ndarray((0,2))
        for i,e in enumerate(x_vector[:]):
            a = np.tan(angle)
            b = self.dimY/2 - a*e 
            P = Get_intersection_points([a,b],self.Shape)
            fiber, new = self.__Create_fiber(P,dx,[a,b],new_fiber)
            if new:
                new_fiber += 1
                fibers_group = np.vstack((fibers_group,fiber))       
        self.__Add_to_domain(fibers_group)              


    
    def __Create_fiber(self, P: list[list[float]],dx: float,param: list[float], new_fiber: int):
        if len(P) == 2:
                P1, P2 = P
                fiber_length = np.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)
                n_de_fiber = round(fiber_length/dx)
                if n_de_fiber >1:
                    a, b = param
                    fiber = np.ndarray((n_de_fiber+1,2))
                    if P2[0] != P1[0]:
                        fiber[:,0] = np.linspace(P2[0],P1[0],n_de_fiber+1)
                        fiber[:,1] = a*fiber[:,0]+b
                    else: 
                        fiber[:,1] = np.linspace(P2[1],P1[1],n_de_fiber+1)
                        fiber[:,0] = a*fiber[:,1]+b                            
                    self.__Add_bond(n_de_fiber,new_fiber)
                    return(fiber, True)
                else: 
                    return([], False) 
        else:
            return([], False)               

    def __Add_bond(self,n_bond: int, i: int):
        bond = np.ndarray((n_bond,2),dtype='int64')
        bond[:,0] = np.arange(n_bond,dtype='int64')
        bond[:,1] = 1+np.arange(n_bond,dtype='int64')
        self.Set_of_Bond[f'{self.Id}_{i}'] = np.arange(n_bond,dtype='int64') + self.N_Bond
        self.Set_of_Fiber[f'{self.Id}_{i}'] = np.arange(n_bond+1,dtype='int64') + self.N_DE
        self.N_DE += n_bond+1
        self.Bond = np.vstack((self.Bond,bond+self.N_Bond+self.N_fiber))           
        self.N_fiber += 1
        self.N_Bond += bond.shape[0]

    def __Add_to_domain(self,fibers_group: np.ndarray):
        nodes_group = np.ndarray((len(fibers_group[:,1]),4))
        nodes_group[:,0:2] = fibers_group
        nodes_group[:,2] = 0
        nodes_group[:,3] = self.Radius
        self.Nodes = np.vstack((self.Nodes,nodes_group))
        self.Set_of_DE[self.Id] = self.Set_of_Fiber[f'{self.Id}_0'][0] + np.arange(nodes_group.shape[0])
        self.Set_of_Bond[self.Id] = self.Set_of_Fiber[f'{self.Id}_0'][0] + np.arange(self.N_Bond-self.Set_of_Fiber[f'{self.Id}_0'][0])     


    def Plot_layer(self):
        plt.scatter(self.Nodes[:,0],self.Nodes[:,1])
        # plt.scatter(self.Shape[:,0],self.Shape[:,1], color='green')
        width = max(self.dimX,self.dimY)
        plt.xlim([-width,width])
        plt.ylim([-width,width])
        plt.show() 
     

if __name__ == "__main__":
    D=Layer('C1',78,[1e-3,1e-3])
    D.Set_radius(0.5*0.000112)
    D.Build_nodes()
    print(D)
    D.Plot_layer()

    