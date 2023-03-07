# SCRIPT PARA GRAFICAR LA RUTA DE VUELO DE UN DRONE
# ESTE SCRIPT PERMITE OBTENER LA COMPARACION ENTRE LA RUTA
# PLANIFICADA Y LA REALIZADA POR EL DRONE

# ARCHIVO 1: ARCHIVO .TXT CON LOS PARAMETROS DE RUTA PLANEADA
# ARCHIVO 2: ARCHIVO .TXT CON LOS DATOS DE VUELO OBTENIDOS DEL DRONE

# librerias
import os
import platform


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

import re #expresiones regulares

import warnings
warnings.filterwarnings("ignore")



def archivo_ruta(ruta):

    # variables iniciales
    cor_x = [] # latitud
    cor_y = [] # longitud
    cor_z = [] # altitud

    comando = re.compile(r"\-?(\d{1,2}\.\d{1,8},?\-?){2}\d{1,2}\.\d{1,8}")

    with open(ruta, 'r') as f:

        for linea in f:
            linea = linea.replace('\n','')
            res = re.match(comando, linea)
            if(res):
                print(linea)
                extraer = linea.split(',')
                cor_x.append(float(extraer[0]))
                cor_y.append(float(extraer[1]))
                cor_z.append(float(extraer[2]))

    print("numero de datos leidos en archivo ruta: " + str(len(cor_x)))

    return cor_x, cor_y, cor_z


def archivo_mision(ruta):

    latitude = []
    longitude = []
    height = []

    with open(ruta, 'r') as f:

        for linea in f:
            linea = linea.replace('\n','')

            vector_cap = linea.split(";")

            latitude.append(float(vector_cap[2]))
            longitude.append(float(vector_cap[3]))
            height.append(float(vector_cap[4]))

    print("numero de datos leidos en archivo mision: " + str(len(latitude)))

    return latitude, longitude, height
    



if __name__=='__main__':

    # inicio del programa
    print(" programa inicializado ")

    # directorio de trabajo
    directorio = '/content'
    
    # deteccion del sistema operativo
    sistemaop = platform.system()
    if sistemaop == 'Windows':
        print("sistema operativo - Windows")
        path = directorio
    elif sistemaop == 'Linux':
        print("sistema operativo - Linux")
        path = directorio
    
    print("directorio de trabajo: " + path)

    # extraccion del listado de archivo .txt
    lstFiles = []
    lstname = []
    lstDir = os.walk(path)

    # ciclo for de lectura de archivo
    for root, dirs, files in lstDir:
        for fichero in files:
            (nombreFichero, extension) = os.path.splitext(fichero)
            if(extension == ".txt"):
                lstFiles.append(root+"/"+nombreFichero+extension)
                lstname.append(nombreFichero)
        print(root)

    print("Archivos leidos:") 
    print(sorted(lstFiles))

    # archivo ruta (ruta) - datos iniciales del drone
    # archivo datam (mision) - datos de vuelo del Drone

    # extraccion de las rutas de archivos de ruta y mision
    for datos in lstFiles:
        if datos.find("ruta_")>0:
            nombre_ruta = datos
        elif datos.find("datam_")>0:
            nombre_mision = datos


    val_x, val_y, val_z = [], [], []
    valm_x, valm_y, valm_z = [], [], []

    # archivo ruta
    val_x, val_y, val_z = archivo_ruta(nombre_ruta)

    # archivo mision
    valm_x, valm_y, valm_z = archivo_mision(nombre_mision)

    # conversion a formato array
    # datos ruta
    X1 = np.array(val_x, dtype=np.float)
    Y1 = np.array(val_y, dtype=np.float)
    Z1 = np.array(val_z, dtype=np.float)

    # datos mision
    X2 = np.array(valm_x, dtype=np.float)
    Y2 = np.array(valm_y, dtype=np.float)
    Z2 = np.array(valm_z, dtype=np.float)

    # grafica 3D con matplotlib
    fig = plt.figure(figsize=(16, 8)) 

    ax = Axes3D(fig, rect=[0.0, 0.0, 1.0, 1.0], elev=25, azim=45.0) 

    ax.scatter(Y1, X1, Z1, s=60, color="red", marker='o', label='puntos ruta') 
    ax.plot(Y1, X1, Z1, color="green", label='ruta Drone - calculada')
    ax.scatter(Y2, X2, Z2, color="blue", label='ruta Drone - realizada')

    ax.grid()
    ax.set_title('GRAFICA DRONE - RUTA CALCULADA VS RUTA REALIZADA', fontsize=14)
    ax.set_xlabel('LONGITUD', fontsize=12)
    ax.set_ylabel('LATITUD', fontsize=12)
    ax.set_zlabel('ALTITUD', fontsize=12)
    plt.legend(fontsize=12, loc='lower right', shadow=True)

    salida_drone = path + "/" + "grafica_drone.png"
    plt.savefig(salida_drone)