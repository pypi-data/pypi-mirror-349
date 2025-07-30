import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
import time
import ast
from math import *
import random as rnd
from scipy.spatial import Delaunay
import Functions as FCT
import Layer as Ly

class Sample:

    def __init__(self,Id: str, dimensions: list[float]):
        self.Shape=self.__Define_shape (dimensions)
        self.dimensions = dimensions
        self.dimX, self.dimY = self.__Center()
        self.Layers = dict()
        self.Agdd_Name = f'Geometry_{Id}'
        self.Id = Id 
        self.Matrix_elasticity_modulus = 0.1e6
        self.Nodes = np.ndarray((0,4), dtype='float')
        self.Bond  = np.ndarray((0,2),dtype='int64')
        self.N_DE      = 0
        self.Set_of_DE   = dict()
        self.Set_of_Fiber = dict()
        self.N_Bond    = 0
        self.Set_of_Bond = dict()
        self.N_fiber = 0

    def __str__(self):
        output = f'The domain is {self.Id}\n'
        output += f'The domain contains {len(self.Layers)} layers named:'
        for l in self.Layers:
            output += f' {l} '
        output += '\n'
        output += f'The domain contains {len(self.Nodes)} nodes and {len(self.Bond)} bonds\n'
        output += f'The dimensions of the domain are {self.dimX} along the X axis and {self.dimY} along the Y axis\n'
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

    def Build_layer(self, Id: str, angle: float):
        self.Layers[f'{Id}'] = Ly.Layer(Id,angle,self.dimensions)

    def Build_geometry(self):
        self.Clean_geometry()
        for l in self.Layers:
            self.Layers[l].Build_nodes()
            self.Nodes = np.vstack((self.Nodes,self.Layers[l].Nodes))
            self.Bond = np.vstack((self.Bond,self.Layers[l].Bond + self.N_DE))
            for de in self.Layers[l].Set_of_DE:
                self.Set_of_DE[de] = self.Layers[l].Set_of_DE[de] + self.N_DE
            for fi in self.Layers[l].Set_of_Fiber:
                self.Set_of_Fiber[fi] = self.Layers[l].Set_of_Fiber[fi] + self.N_DE
            for bo in self.Layers[l].Set_of_Bond:
                self.Set_of_Bond[bo] = self.Layers[l].Set_of_Bond[bo] + self.N_Bond
            self.N_DE += len(self.Layers[l].Nodes)
            self.N_Bond += len(self.Layers[l].Bond)
            self.N_fiber += self.Layers[l].N_fiber    
            print(f'Layer {l} has been built')                                       

    def Set_agdd_name(self, Name: str):
        self.Agdd_Name = Name
        
    def Set_matrix_elasticity_modulus(self, E: float):
        self.Matrix_elasticity_modulus = E
                    
    def Clean_geometry(self):
        self.Nodes = np.ndarray((0,4), dtype='float')
        self.Bond  = np.ndarray((0,2),dtype='int64')                
        self.N_DE      = 0
        self.Set_of_DE   = dict()
        self.Set_of_Fiber = dict()
        self.N_Bond    = 0
        self.Set_of_Bond = dict()
        self.N_fiber = 0
  
    def Create_matrix(self):
        raw_triangulation = Delaunay(self.Nodes[:,:-1])
        print('Triangulation is over')
        triangles_nodes = raw_triangulation.simplices
        triangles_edges = np.vstack((triangles_nodes[:,:2],triangles_nodes[:,1:3],triangles_nodes[:,2:],np.vstack((triangles_nodes[:,-1],triangles_nodes[:,0])).T))
        triangles_edges = np.sort(triangles_edges,axis=1)
        triangles_edges = set(str(triangles_edges.tolist())[1:-1].replace(' ','').replace('],[','];[').split(';'))
        triangles_edges = [[int(e.split(',')[0][1:]),int(e.split(',')[1][:-1])] for e in list(triangles_edges)]
        k = 0
        edges_number = len(triangles_edges)
        while k < edges_number:
            edge = triangles_edges[k]
            for key in self.Set_of_Fiber:                
                if edge[0]<self.Set_of_Fiber[key].max(): #The collagen fiber containing the first node of the bond is found                     
                    if edge[1] in self.Set_of_Fiber[key]: #if the second nodes belongs to the same fiber, we delete the bond
                        triangles_edges = np.delete(triangles_edges,k,axis=0) 
                        k -= 1
                        edges_number -=1 #if the bond is deleted there are one less bond in the list
                    break
            k += 1
        print('Duplicates with collagen has been deleted')    
        triangles_edges = self.__Check_length(triangles_edges)    
        triangles_edges = np.array(triangles_edges, dtype='int64')            
        self.Bond = np.vstack((self.Bond,triangles_edges))          
        self.Set_of_Bond['Matrix'] = np.arange(len(triangles_edges))+self.N_Bond                
        self.N_Bond += len(triangles_edges)                        

    def __Check_length(self,bonds : np.ndarray):
        evaluated_number = 0
        bond_number = len(bonds)
        rmax = max(self.Nodes[:,-1])
        while evaluated_number < bond_number:
            evaluated_bond = bonds[evaluated_number]
            bond_length = (sqrt((self.Nodes[evaluated_bond[0],0]-self.Nodes[evaluated_bond[1],0])**2 + (self.Nodes[evaluated_bond[0],1]-self.Nodes[evaluated_bond[1],1])**2+(self.Nodes[evaluated_bond[0],2]-self.Nodes[evaluated_bond[1],2])**2))
            if bond_length > 6*rmax or bond_length <1e-8:
                bonds = np.delete(bonds,evaluated_number,axis=0)
                bond_number -= 1
                evaluated_number -= 1
            evaluated_number += 1
        return(bonds)        
    
    def Export_geometry(self):
        assert(self.N_DE == self.Nodes.shape[0])
        assert(self.N_Bond == self.Bond.shape[0])
        self.Get_Macro_Set_of_DE()
        File_Name = self.Agdd_Name + ".agdd"
        try:
            f = open(File_Name,'xb')
        except:
            os.remove(File_Name)
            f = open(File_Name,'xb')   
        np.savetxt(f,self.Nodes,header=str(self.N_DE),comments='',delimiter='\t',fmt='%1.6f') 
        np.savetxt(f,self.Bond,header=str(self.N_Bond),comments='',delimiter='\t',fmt='%d') 
        for S in [self.Set_of_DE, self.Set_of_Bond]:
            f.write(str.encode('{}\n'.format(len(S))))
            for e in S:
                f.write(str.encode('{}\n'.format(e)))
                np.savetxt(f, S[e].T, header=str(S[e].shape[0]), comments='',delimiter='\t',fmt='%d')
        f.close()
        print(f'The file {self.Agdd_Name}.agdd has been created') 
    
    def Get_Macro_Set_of_DE(self):
        self.Set_of_DE['Xmin'] = np.where(self.Nodes[:,0]==-self.dimX/2)[0]
        self.Set_of_DE['Xmax'] = np.where(self.Nodes[:,0]==self.dimX/2)[0]
        self.Set_of_DE['Ymin'] = np.where(self.Nodes[:,1]<-self.dimY/2*0.99)[0]
        self.Set_of_DE['Ymax'] = np.where(self.Nodes[:,1]==self.dimY/2)[0]
        self.Set_of_DE['Zmin'] = np.where(self.Nodes[:,2]==self.Nodes[:,2].min())[0]
        self.Set_of_DE['Zmax'] = np.where(self.Nodes[:,2]==self.Nodes[:,2].max())[0]  

    def Cut_straigth(self,Length: float, Alpha: float):
        before_slash_nodes = []
        after_slash_nodes = []
        surrounding_nodes = []
        alpha_rad = pi/180*Alpha
        slash_extremity_left = [-Length/2*cos(alpha_rad),-Length/2*sin(alpha_rad)]
        slash_extremity_right = [Length/2*cos(alpha_rad),Length/2*sin(alpha_rad)]
        for node_index, node in enumerate(self.Nodes):
            surrounding, before_slash, after_slash = FCT.Order_nodes(slash_extremity_right,slash_extremity_left,node,Alpha)    
            if surrounding:
                surrounding_nodes.append(node_index)
            if before_slash:
                before_slash_nodes.append(node_index)    
            if after_slash:
                after_slash_nodes.append(node_index)
        self.Set_of_DE['After_slash'] = np.array(after_slash_nodes)
        self.Set_of_DE['Before_slash'] = np.array(before_slash_nodes)
        self.Set_of_DE['Slash_surrounding'] = np.array(surrounding_nodes)
        deleted_bonds = np.ndarray((0,1),dtype='int64')
        for node_before_index in before_slash_nodes:
            for node_after_index in after_slash_nodes:
                delete_bond, bond_index = self.Check_deletion_need(node_before_index, node_after_index)
                if delete_bond:
                    print('Delete')
                    deleted_bonds = np.vstack((deleted_bonds,np.array([bond_index])))
        deleted_bonds = np.sort(deleted_bonds,0)
        deleted_bonds = np.flip(deleted_bonds)
        print(deleted_bonds)
        self.Set_of_Bond['deleted'] = deleted_bonds
        for bond_index in deleted_bonds:
            self.Delete_bond(bond_index)        

                        
    def Check_deletion_need(self,node_before_index: int,node_after_index: int):
        delete_bond = False
        return_index = -1
        node_before = self.Nodes[node_before_index]
        node_after = self.Nodes[node_after_index]
        nodes_distance = sqrt((node_before[0]-node_after[0])**2+(node_before[1]-node_after[1])**2+(node_before[2]-node_after[2])**2)
        if nodes_distance <= 4*max(self.Nodes[:,-1]):
            for bond_index , [node_first, node_second]  in enumerate(self.Bond):
                if node_first in [node_before_index,node_after_index] and node_second in [node_before_index,node_after_index]:
                    return(True,bond_index)
        return(delete_bond,return_index)            

    def Delete_bond(self, bond_index: int):
        for bond_set in list(self.Set_of_Bond):
            for index_intra, index_global in enumerate(self.Set_of_Bond[bond_set]):
                if index_global == bond_index:
                    self.Set_of_Bond[bond_set] = np.delete(self.Set_of_Bond[bond_set],index_intra)
            for other_bonds_intra, other_bonds_global in enumerate(self.Set_of_Bond[bond_set]):
                if other_bonds_global > bond_index:
                    self.Set_of_Bond[bond_set][other_bonds_intra] -= 1
        if bond_index < self.Bond.shape[0]:
            self.Bond = np.vstack((self.Bond[:int(bond_index),:],self.Bond[int(bond_index)+1:,:]))
        else:
            self.Bond = self.Bond[:-1,:]
        self.N_Bond = self.N_Bond - 1                            





if __name__ == "__main__":
    D=Sample('Samp',[1e-3,1e-3])
    D.Build_layer('C1',78)
    # D.Build_layer('C2',40)
    D.Layers['C1'].Set_radius(0.000112)
    # D.Layers['C1'].Set_altitude(0)
    D.Build_geometry()
    # D.Layers['C1'].Set_altitude(5e-3)
    # D.Create_matrix()
    D.Export_geometry()
    print(D)
    