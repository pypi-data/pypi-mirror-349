import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
import time
import ast
from math import *
import random as rnd
from scipy.spatial import Delaunay
from Layer import *
from Sample import *
from scipy.stats import truncnorm

class Input_creator:

    def __init__(self, Name: str, Sample: Sample):
        self.Sample = Sample
        self.Name = Name
        self.Contact = True
        self.Contact_stiffness = self.__Compute_contact_stiffness()
        self.N_iteration = int(1e5)
        self.Loading_type = 'Uniaxial'
        self.Maximum_strain = 1.8e-2
        self.Export_PVD = True
        self.N_export = 150
        self.N_sensor = self.N_iteration
        self.Slack_parameters  = [0.55e-2,0.59e-2,0.79e-2]
        self.Layer_slack = 0
        self.Damping_factor_collagen = 0
        self.Damping_factor_matrix = 0
        self.Maximum_elongation_collagen = 1
        self.Maximum_elongation_matrix = 1
        self.Density = 1e4

    def __str__(self):
        output = f'The Input name is {self.Name} and is based on the sample {self.Sample.Id}\n'
        output += f'The simulation will use {self.N_iteration} to reach a {self.Maximum_strain} maximum strain during a {self.Loading_type} test\n'
        if self.Contact:
            output += f'The contact is enable with a stiffness of {self.Contact_stiffness} N/m.\n'
        else:
            output += 'The contact is disable'
        output += f'The slack distribution currently is on the {self.Layer_slack+1}st layer and the distribution parameters are {self.Slack_parameters}.\n'        
        output += f'The model density is {self.Density}\n'
        output += f'The damping factor of the collagen and matrix are {self.Damping_factor_collagen} and {self.Damping_factor_matrix}. Their maximum relative elongation are {self.Maximum_elongation_collagen} and {self.Maximum_elongation_matrix}\n'
        output += f'Sensors will be written {self.N_sensor} times\n'
        if self.Export_PVD:
            output += f'The PVD export is enable and the results will be exported {self.N_export} time\n'
        else: 
            output += f'The PVD export is disable'    
        return(output)    

    def __Compute_contact_stiffness(self):
       radius_max = max(self.Sample.Nodes[:,-1])
       radius_min = min(self.Sample.Nodes[:,-1])
       radius = (radius_max + radius_min)/2
       elasticity_modulus = self.Sample.Layers[list(self.Sample.Layers.keys())[0]].Elasticity_modulus
       stiffness = (elasticity_modulus * pi * radius**2)/(2*radius)
       return(stiffness)

    def Set_name(self, Name : str):
        self.Name = Name

    def Set_contact(self, enable: bool):
        self.Contact = enable

    def Set_iteration_number(self, number: int):
        self.N_iteration = number

    def Set_loading_type(self, load_type: str):
        self.Loading_type = load_type

    def Set_maximum_strain(self, strain: float):
        self.Maximum_strain = strain

    def Set_export_PVD(self, enable: bool):
        self.Export_PVD = enable

    def Set_number_export(self, number: int):
        self.N_export = number 

    def Set_number_sensor(self, number: float):
        self.N_sensor = number

    def Set_slack_parameter(self, param: list[float]):
        self.Slack_parameters = param

    def Set_layer_slack(self, layer_number: int):
        self.Layer_slack = layer_number

    def Set_damping_factor_collagen(self, damping: float):
        self.Damping_factor_collagen = damping               

    def Set_damping_factor_matrix(self, damping: float):
        self.Damping_factor_matrix = damping  

    def Set_maximum_elongation_collagen(self, maximum: float):
        self.Maximum_elongation_collagen = maximum        

    def Set_maximum_elongation_matrix(self, maximum: float):
        self.Maximum_elongation_matrix = maximum  

    def Set_density(self, density: float):
        self.Density = density    

    def Write_inp_file(self):
        header = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>

<GRANOO Version="3"  OutDir="{self.Name}" Verbose="No" ThreadNumber="1">
  <STEP Label="pre-processing">
    <READ-DOMAIN FileName="{self.Sample.Agdd_Name}.agdd"/> \n"""
        fiber_definition = self.__Write_fiber_properties()
        matrix_definition = f"    <CONVERT-ELEMENT-PAIR-TO-BEAM YoungModulus=\"{self.Sample.Matrix_elasticity_modulus}\" PoissonRatio=\"0.3\" RadiusRatio=\"1\" DampingFactor=\"{self.Damping_factor_matrix}\" MaxRelativeElongation=\"{self.Maximum_elongation_matrix}\" Set=\"Matrix\"/> \n"
        body = f"""    <InitSensor/>
    <APPLY-DENSITY Value="{self.Density}"/>         
    <COMPUTE-OPTIMAL-TIME-STEP Ratio="0.14" />

  </STEP>\n"""
        iteration = f"  <STEP Label=\"processing\" IterNumber=\"{self.N_iteration}\">\n"
        integration =  f"""    <CLEAR-LOAD/>

    <APPLY-BOND-LOAD/>
    {self.__Write_contact()}
    <INTEGRATE-ACCELERATION Linear="Yes" Angular="Yes" BetaLinear="1.3" BetaAngular="1.3"/>\n"""
        displacement = self.__Write_displacement()
        sensors = self.__Write_sensors()
        end = """  </STEP>
</GRANOO>"""
        inp_str = header+fiber_definition+matrix_definition+body+iteration+integration+displacement+sensors+end
        f = open(f'{self.Name}.inp','w')
        f.write(inp_str)
        f.close()


    def __Write_sensors(self):
        Sensors = f"""    <CHECK />

    <UPDATE-SUPPORT-SHAPE EveryIter="10" />
    <WRITE-SENSOR-DATA EveryIter="{int(self.N_iteration/self.N_sensor)}" />\n"""
        if self.Export_PVD:
            Sensors += f"""    <EXPORT-TO-PVD EveryIter="{int(self.N_iteration/self.N_export)}" Field="All"/>\n"""
        return(Sensors)        

    def __Write_displacement(self):
        if self.Loading_type == "Uniaxial":
            command = f"RAC(it,{int(0.9*self.N_iteration)},{self.Maximum_strain*self.Sample.dimX})"
        else:
            print('Not implemented yet !')
            quit()     
        displacement_str = f"""    <APPLY-DISPLACEMENT Clamp="Yes" Set="Xmin"/>
    <APPLY-DISPLACEMENT X="{command}" Set="Xmax"/> 
    <APPLY-DISPLACEMENT Y="0" Set="Xmax"/>    
    <APPLY-DISPLACEMENT Z="0" Set="Xmax"/>\n """ 
        return(displacement_str)

    def __Write_contact(self):
        contact_str=''
        if self.Contact:
            contact_str += f"""    <MANAGE-COLLISION Between="Body/Body"
      BroadPhase="Lcm" NarrowPhase="SelectiveBonds"
      CallBack="Standard2" NormalStiffness="{self.Contact_stiffness}" RestitutionCoeff="0.1" StaticFriction="0.3" />"""
        return(contact_str) 

    def __Write_fiber_properties(self):
        fiber_str = ''
        for number, layer in enumerate(self.Sample.Layers.keys()):
            current_layer = self.Sample.Layers[layer]
            stiffness = current_layer.Stiffness
            if number == self.Layer_slack:
                mean, std, maximum = self.Slack_parameters
                for numero, fiber_id in enumerate(list(current_layer.Set_of_Bond.keys())[:-1]):
                    fiber_slack = truncnorm.rvs((0-mean)/std, (maximum-mean)/std, loc=mean, scale=std)
                    fiber_str += f"    <CONVERT-ELEMENT-PAIR-TO-SLACK-SPRING Stiffness=\"{stiffness}\" DampingFactor=\"{self.Damping_factor_collagen}\" Slack=\"{fiber_slack}\"  MaxRelativeElongation=\"{self.Maximum_elongation_collagen}\" Set=\"{fiber_id}\"/>\n"
            else:         
                for numero, fiber_id in enumerate(list(current_layer.Set_of_Bond.keys())[:-1]):
                    fiber_str += f"    <CONVERT-ELEMENT-PAIR-TO-SPRING Stiffness=\"{stiffness}\" RestitutionCoeff=\"{1-self.Damping_factor_collagen}\" MaxRelativeElongation=\"{self.Maximum_elongation_collagen}\" Set=\"{fiber_id}\"/>\n"
        return(fiber_str)            



            


             
if __name__ == "__main__":
    D=Sample('Samp',[2e-2,1e-2])
    D.Build_layer('C1',0)
    D.Build_layer('C2',40)
    D.Layers['C1'].Set_collagen_ratio(0.5)
    D.Layers['C1'].Set_altitude(0)
    D.Build_geometry()
    # D.Layers['C1'].Set_altitude(5e-3)
    D.Create_matrix()
    D.Export_geometry()
    A = Input_Creator('Test_INP',D)
    print(A)
    A.Write_inp_file()
    print(D)
    