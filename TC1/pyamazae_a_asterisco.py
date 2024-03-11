"""
Andrea María Li Hernández - 2021028783
Deyan Andrey Sanabria Fallas - 2021046131
Erick Fabián Madrigal Zavala - 2018146983
"""

# Hola profe :) 
from pyamaze import maze,COLOR,agent, textLabel
from time import perf_counter
import random
import heapq

#Parametros generales del laberinto
#tamaño del laberinto
x_inicial = random.randint(50,90)
y_inicial = random.randint(50,90)
#posicion de la meta
y_meta = random.randint(0,y_inicial)
x_meta = random.randint(0,x_inicial)

#posicion de inicio y meta
meta = (y_meta,x_meta) #pyamaze siempre lo pone en 1,1
inicio = (random.randint(0,y_inicial),random.randint(0,x_inicial)) 

# Longitud del camino
longitud = 0

#Clase que representa una celda
class Celda: 
    def __init__(self, position = (0,0), g = float('inf'), h = 0, f = float('inf')):
        self.padres = position #(y, x)
        self.g = g
        self.h = h
        self.f = g + h

#funcion que revisa si el nodo esta en el mapa
def valido(mapa, nodo):
    return nodo in mapa

#funcion que revisa si se puede mover en la direccion del objetivo
def desbloqueado(mapa, nodo, objetivo):
    caminos = mapa[(nodo[1],nodo[2])]
    dir_y = objetivo[0] - nodo[1]
    dir_x = objetivo[1] - nodo[2]

    #se revisa la direccion que se quiere tomar y despues si hay un muro en la ruta
    if dir_x == 1:
        return caminos['E'] == 1
    if dir_x == -1:
        return caminos['W'] == 1
    if dir_y == 1:
        return caminos['S'] == 1
    if dir_y == -1:
        return caminos['N'] == 1

#funcion que revisa si el nodo es el destino
def destino (nodo):
    return nodo == meta

#El movimiento es solo en X o Y por lo que se usa la distancia manhatan 
def calcular_heuristica(actual, meta):
    base = abs(actual[0] - meta[0])
    altura = abs(actual[1] - meta[1])
    return base + altura

#funcion que arma el camino a seguir basado en las celdas visitadas
def armar_camino(celdas, destino):
    camino = []
    fila = destino[0]
    columna = destino[1]

    #se revisan y agregan los nodos padres al camino
    while not (celdas[fila][columna].padres[0] == fila and 
                celdas[fila][columna].padres[1] == columna):
        camino.append((fila, columna))
        temp_fila = celdas[fila][columna].padres[0]
        temp_columna = celdas[fila][columna].padres[1]
        fila = temp_fila
        columna = temp_columna

    #se agrega el nodo objetivo
    camino.append((fila, columna))
    #se invierte el camino para que sea del origen al destino
    camino.reverse()    
    return camino

#funcion que mueve el agente por el laberinto para mostrar el camino 
def mostrar_camino(camino):
    global longitud
    longitud = len(camino)
    for nodo in camino:
        agente.position = nodo

#algoritmo principal de A*
def a_estrella(mapa):
    x = inicio[1]
    y = inicio[0]

    lista_abierta = []
    heapq.heappush(lista_abierta, (0, y, x)) # se agrega un elemento inicial con un peso 0 y la posicion inicial
    # Lista de celdas visitadas
    lista_cerrada = [[False for _ in range((x_inicial + 1))] for _ in range((y_inicial + 1))]
	# detalles de las celdas
    detalles_celda = [[Celda() for _ in range((x_inicial + 1))] for _ in range((y_inicial + 1))]

    #se inicializa la celda de inicio
    detalles_celda[y][x].f = 0 
    detalles_celda[y][x].g = 0
    detalles_celda[y][x].h = 0
    detalles_celda[y][x].padres = (y,x)

    #flag para saber si se llego al destino
    destino_alcanzado = False

    #Logica princioal del A*
    while len(lista_abierta) > 0:
        actual = heapq.heappop(lista_abierta)
        #se marca la celda como visitada
        x = actual[2]
        y = actual[1]
        lista_cerrada[y][x] = True

        #se buscan los nodos adyacentes
        direcciones = [(y-1,x), (y+1,x), (y,x-1), (y,x+1)]
        for direccion in direcciones:
            nueva_y = direccion[0]
            nueva_x = direccion[1]

            #se revisa si el nodo es valido y desbloqueado
            if valido(mapa, direccion) and desbloqueado(mapa, actual, direccion):
                #Se revisa si el nodo es el destino
                if destino(direccion):
                    detalles_celda[nueva_y][nueva_x].padres = (y,x)
                    destino_alcanzado = True
                    camino = armar_camino(detalles_celda, meta)
                    mostrar_camino(camino)
                    return
                else: 
                    #Segun los nodos a los que se pueden llegar se generan g,h y f
                    nueva_g = detalles_celda[y][x].g + 1.0
                    nueva_h = calcular_heuristica(direccion, meta)
                    nueva_f = nueva_g + nueva_h
                    #Se revisa si el nodo ya fue visitado y si es asi se revisa si el nuevo camino es mejor
                    if detalles_celda[nueva_y][nueva_x].f == float('inf')  or detalles_celda[nueva_y][nueva_x].f > nueva_f:
                        heapq.heappush(lista_abierta, (nueva_f, nueva_y, nueva_x))
                        detalles_celda[nueva_y][nueva_x].f = nueva_f
                        detalles_celda[nueva_y][nueva_x].g = nueva_g
                        detalles_celda[nueva_y][nueva_x].h = nueva_h
                        detalles_celda[nueva_y][nueva_x].padres = (y,x)
    
    if not destino_alcanzado:
        print("No se encontro un camino al destino")



start_time = perf_counter()
#se crea el laberinto
m = maze(y_inicial,x_inicial)
# goal en 1,1 inicio en y_inicial, x_inicial
m.CreateMaze(y_meta,x_meta,loopPercent= 100)

#otras formas de generar el laberinto
#m.CreateMaze(theme=COLOR.light,pattern='v') #vertical
#m.CreateMaze(theme=COLOR.light,pattern='h') #horizontal
agente=agent(m,inicio[0],inicio[1],footprints=True,filled=True)
# maze_map -> arreglo con dato de tipo 
# {(y, x): {'E': 1, 'W': 0, 'N': 0, 'S': 0}} 1 = camino, 0 = pared
mapa = m.maze_map
maze_time = perf_counter() - start_time

start_time = perf_counter()
a_estrella(mapa)
astar_time = perf_counter() - start_time

textLabel(m,"Tiempo demorado en crear el laberinto",maze_time)
textLabel(m,"Tiempo demorado por A*",astar_time)
textLabel(m,"Tamaño",str(x_inicial) + " x " + str(y_inicial))
textLabel(m,"Pos Inicial",str(inicio[0]) + " x " + str(inicio[1]))
textLabel(m,"Pos Final",str(meta[0]) + " x " + str(meta[1]))
textLabel(m,"Distancia recorrida",longitud)


#logica del A* 
m.run()




