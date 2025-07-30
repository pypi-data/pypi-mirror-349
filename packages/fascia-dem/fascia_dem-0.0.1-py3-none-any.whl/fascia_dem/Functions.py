from math import *
import random as rnd
import os
from scipy.spatial import Delaunay
from Sample import *
from Input import *
from Layer import *
import time as tm


def Get_intersection_points(param: list[float], Shape: np.ndarray):
    P=[]
    a,b = param
    x,y = Shape[0,:]
    Y = a*x+b 
    if Y < y:
        Below = -1
    elif Y == y:
        Below = 0
        P.append([x,y])
    else:
        Below = 1
    for i, M in enumerate(Shape[1:,:]):
        Y = a*M[0]+b 
        if Below == -1:
            Crossed, point, Below = Check_cross_up(Y,M,[x,y],[a,b],P)
            if Crossed:
                P.append(point)
        elif Below == 0:
            Crossed, point, Below = Check_cross_straight(Y,M,[x,y],[a,b],P)
            if Crossed:
                P.append(point)         
        else: 
            Crossed, point, Below = Check_cross_down(Y,M,[x,y],[a,b],P)
            if Crossed:
                P.append(point)     
        x, y = M        
    return(P)           
                    

def Check_cross_up(Y: float, M: list[float], M0: list[float], param: list[float], P: list[list[float]]):
    a, b = param
    if Y > M[1]:
        if M[0] != M0[0]:
            A = (M[1]-M0[1])/(M[0]-M0[0])
            B = M0[1] - A*M0[0]
            return(True,[(B-b)/(a-A),a*(B-b)/(a-A)+b],1)
        else:
            return(True,[M0[0],Y],1)
    elif Y==M[1]:
        if [M[0],Y] not in P:
            return(True,[M[0],Y],0)
        else:
            return(False,[],0)  
    else:       
        return(False,[],-1)

def Check_cross_straight(Y: float, M: list[float], M0: list[float], param: list[float], P: list[list[float]]):
    if Y > M[1]:
        if [M[0],Y] not in P:
            return(True,[M[0],Y],1)
        else:
            return(False,[],1)
    elif Y < M[1]:
        if [M[0],Y] not in P:
            return(True,[M[0],Y],-1)
        else:
            return(False,[],-1) 
    else:
        pass
    return(False,[],0)

def Check_cross_down(Y: float, M: list[float], M0: list[float], param: list[float], P: list[list[float]]):
    a, b = param
    if Y < M[1]:            
        if M[0] != M0[0]:
            A = (M[1]-M0[1])/(M[0]-M0[0])
            B = M0[1] - A*M0[0]
            return(True,[(B-b)/(a-A),a*(B-b)/(a-A)+b],-1)
        else:
            return(True,[M0[0],Y],-1)
    elif Y==M[1]:
        if [M[0],Y] not in P:
            return(True,[M[0],Y],0)
        else:
            return(False,[],0)  
    else:       
        return(False,[],1)

def Order_nodes(slash_extremity_right: list[float], slash_extremity_left: list[float], node: list[float], Angle: float):
    if Angle == 90:
        return(Order_nodes_vertical_slash(slash_extremity_right,slash_extremity_left,node))
    if Angle == 0:
        return(Order_nodes_horizontal_slash(slash_extremity_right,slash_extremity_left,node))
    else:
        return(Order_nodes_slash(slash_extremity_right,slash_extremity_left,node,Angle))

def Order_nodes_vertical_slash(extremity_right: list[float], extremity_left: list[float], node: list[float]): 
    surrounding = False
    before_slash = False
    after_slash = False
    projection = [0,node[1]]   
    distance_projection = sqrt((projection[0]-node[0])**2+(projection[1]-node[1])**2)    
    if projection[1] < extremity_right[1] and projection[1] > extremity_left[1]:
        final_distance = distance_projection
    elif projection[1] < extremity_left[1]:
        final_distance = sqrt(distance_projection**2+(extremity_left[0]-projection[0])**2+(extremity_left[1]-projection[1])**2)
    elif projection[1] > extremity_right[1]:
        final_distance = sqrt(distance_projection**2+(extremity_right[0]-projection[0])**2+(extremity_right[1]-projection[1])**2)
    if final_distance < 8*node[3]:
        surrounding = True
        if final_distance < 4*node[3]:
            if node[0] >= projection[0]:
                before_slash = True
            else:
                after_slash = True
    return(surrounding, before_slash, after_slash)          

def Order_nodes_horizontal_slash(extremity_right: list[float], extremity_left: list[float], node: list[float]):
    surrounding = False
    before_slash = False
    after_slash = False
    projection = [node[0],0]   
    distance_projection = sqrt((projection[0]-node[0])**2+(projection[1]-node[1])**2)    
    if projection[0] < extremity_right[0] and projection[0] > extremity_left[0]:
        final_distance = distance_projection
    elif projection[0] < extremity_left[0]:
        final_distance = sqrt(distance_projection**2+(extremity_left[0]-projection[0])**2+(extremity_left[1]-projection[1])**2)
    elif projection[0] > extremity_right[0]:
        final_distance = sqrt(distance_projection**2+(extremity_right[0]-projection[0])**2+(extremity_right[1]-projection[1])**2)
    if final_distance < 8*node[3]:
        surrounding = True
        if final_distance < 4*node[3]:
            if node[1] >= projection[1]:
                before_slash = True
            else:
                after_slash = True
    return(surrounding, before_slash, after_slash)     

def Order_nodes_slash(extremity_right: list[float], extremity_left: list[float], node: list[float], Angle: float):
    surrounding = False
    before_slash = False
    after_slash = False
    alpha = pi * Angle/180
    projection_x = (node[1] + node[0] * 1/tan(alpha))/(tan(alpha) + 1/tan(alpha))
    projection = [projection_x,tan(alpha) * projection_x]   
    distance_projection = sqrt((projection[0]-node[0])**2+(projection[1]-node[1])**2)    
    if projection[0] < extremity_right[0] and projection[0] > extremity_left[0]:
        final_distance = distance_projection
    elif projection[0] < extremity_left[0]:
        final_distance = sqrt(distance_projection**2+(extremity_left[0]-projection[0])**2+(extremity_left[1]-projection[1])**2)
    elif projection[0] > extremity_right[0]:
        final_distance = sqrt(distance_projection**2+(extremity_right[0]-projection[0])**2+(extremity_right[1]-projection[1])**2)
    if final_distance < 8*node[3]:
        surrounding = True
        if final_distance < 4*node[3]:
            if node[1] >= projection[1]:
                before_slash = True
            else:
                after_slash = True
    return(surrounding, before_slash, after_slash) 


def Create_sample(sample_name: str, dimensions: list[float], fibrous_thickness: float, angles: list[float]):
    sample = Sample(sample_name,dimensions)
    sample.Build_layer('C1',angles[0])
    sample.Build_layer('C2',angles[1])
    h_inter = 0.25 * fibrous_thickness
    radius_superficiel = 0.5 * 0.4 * (fibrous_thickness-h_inter)
    radius_intermediate = 0.5 * 0.6 * (fibrous_thickness-h_inter)
    sample.Layers['C1'].Set_radius(radius_superficiel)
    sample.Layers['C2'].Set_radius(radius_intermediate)
    sample.Layers['C1'].Set_altitude(radius_superficiel+radius_intermediate+h_inter)
    print('The Sample object has been created')
    return(sample)

def Create_geometry(sample: Sample):
    sample.Build_geometry()
    sample.Create_matrix()
    print('The sample has been built')
    return(sample)

def Add_slash(sample: Sample, length: float, Angle: float):
    sample.Cut_straigth(length,Angle)
    return(sample)


def Export_geometry(sample: Sample):
    sample.Export_geometry()


def Run_simulation(Build_path: str, Inp_name: str):
    try:
        f=open(f'{Inp_name}/Sensors.txt','r') 
        f.close()
        os.system(f'rm -r ./{Inp_name}')
    except:
        pass    
    os.system(f'{Build_path}build/fasciadem.exe ./{Inp_name}.inp')    

def Check_build(build_path: str, Change_sensor: bool, New_sensors: list[float]):
    try:
        f=open(f'{build_path}/build/CMakeCache.txt','r') 
        f.close()
        if Change_sensor:
            Write_sensors(New_sensors)
            Delete_build(build_path)
            Create_build(build_path)
    except:
        if Change_sensor:
            Write_sensors(New_sensors)
        Create_build(build_path)    

def Write_sensors(New_sensors: list[float]):
    Write_sensors_hpp(New_sensors)
    Write_sensors_cpp(New_sensors)

def Delete_build(build_path: str):
    os.system(f'cd {build_path}')
    os.system(f'rm -r ./build')

def Create_build(build_path: str):
    os.chdir(build_path)
    os.system('cp -r ./source ./build')
    os.chdir('./build')
    os.system('cmake ./CMakeLists.txt')
    os.system('make')
    os.chdir('../')

def Write_sensors_hpp(New_sensors: list[float]):
    direction_dictionary = {0:'X',1:'Y',2:'Z'}
    sensors = ''
    for direction, enable in enumerate(New_sensors):
        if enable:
            vector = direction_dictionary[direction]
            sensors += f'  Extset_*     _{vector}min_;\n  Extset_*     _{vector}max_;\n'
    fsource = open('./PlugIn_InitSensor_blank.hpp','r')
    Sensor_file = fsource.read()
    fsource.close()
    fsensor = open('source/PlugIn_InitSensor.hpp','w')
    fsensor.write(Sensor_file.format(sensors))
    fsensor.close()

def Write_sensors_cpp(New_sensors: list[float]):
    direction_dictionary = {0:'X',1:'Y',2:'Z'}
    null_str = ''
    init_str = ''
    run_str = ''
    displacement_str = ''
    for direction, enable in enumerate(New_sensors):
        if enable:
            vector = direction_dictionary[direction]
            null_str += f'    _{vector}min_(nullptr),\n    _{vector}max_(nullptr)\n'
            init_str += f'  _{vector}min_ = &Core::SetOf<DEM::Element>::get("{vector}min");\n  _{vector}max_ = &Core::SetOf<DEM::Element>::get("{vector}max");\n'
            run_str += f'  Core::Sensor::new_object(*_{vector}min_, &Extset_::resultant_force, "Force_{vector}Min_");\n  Core::Sensor::new_object(*_{vector}max_, &Extset_::resultant_force, "Force_{vector}Max_");\n'
            displacement_str += f'  Core::Sensor::new_object(*_{vector}max_, &Extset_::average_displacement<Geom::{vector}>, "Disp{vector}M{vector}");\n'
    fsource = open('./PlugIn_InitSensor_blank.cpp','r')
    Sensor_file = fsource.read()
    fsource.close()
    fsensor = open('source/PlugIn_InitSensor.cpp','w')
    fsensor.write(Sensor_file.format(null_str,init_str,run_str,displacement_str))
    fsensor.close()            

   