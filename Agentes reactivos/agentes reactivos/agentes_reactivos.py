import random
import tkinter as tk
from PIL import Image, ImageTk

# ===============================
# LÓGICA DEL MAPA Y AGENTES
# ===============================

def crea_base(mapa, filas, columnas):
    """Coloca la base en una posición aleatoria del tablero."""
    i = random.randint(0, filas-1)
    j = random.randint(0, columnas-1)
    mapa[i][j] = {'Tipo': 4, 'Cantidad': 0}  # 4 -> base
    return (i, j)

def crea_obstaculos(mapa, num_obstaculos, filas, columnas):
    """Coloca obstáculos en celdas vacías (Tipo 0)."""
    for _ in range(num_obstaculos):
        i = random.randint(0, filas-1)
        j = random.randint(0, columnas-1)
        if mapa[i][j]['Tipo'] == 0:
            mapa[i][j] = {'Tipo': 3, 'Cantidad': 0}  # 3 -> obstáculo

def crea_muestras(mapa, num_muestras, filas, columnas):
    """Coloca muestras en celdas vacías, asignando cantidad aleatoria entre 2 y 4."""
    for _ in range(num_muestras):
        i = random.randint(0, filas-1)
        j = random.randint(0, columnas-1)
        if mapa[i][j]['Tipo'] == 0:
            cantidad = random.randint(2, 4)
            mapa[i][j] = {'Tipo': 1, 'Cantidad': cantidad}  # 1 -> muestra

"""Agente reactivo"""
class Agente:
    """Valores iniciales"""
    def __init__(self, mapa, filas, columnas, base):
        self.mapa = mapa
        self.filas = filas
        self.columnas = columnas
        self.base = base
        self.pos = self.posicion_aleatoria()
        self.estado = 'A'
        self.pos_pasada = self.pos
        self.con_muestra = False

    """Se escoge una posición aleatoria del tablero para colocar al agente"""
    def posicion_aleatoria(self):
        while True:
            i = random.randint(0, self.filas - 1)
            j = random.randint(0, self.columnas - 1)
            if self.mapa[i][j]['Tipo'] == 0:
                return (i, j)

    """Dependiendo su estado, tendra un comportamiento distinto"""
    def act(self,mapa):
        self.mapa = mapa
        if self.estado == 'A':
            self.movimiento_aleatorio()
        elif self.estado in ['B','C']:
            self.trasportar_muestras()
        return(self.mapa) #Se retroalimenta el mapa

    """Se evalua la posicion dentro de la matriz"""
    def en_limites(self, p):
        i, j = p
        return 0 <= i < self.filas and 0 <= j < self.columnas

    """Comportamiento en el estado A"""
    def movimiento_aleatorio(self):
        direcciones = [(-1,0), (1,0), (0,-1), (0,1)]
        for _ in direcciones:
            d = random.choice(direcciones)
            nueva_pos = (self.pos[0] + d[0], self.pos[1] + d[1])
            """Si la posicion no es un obstaculo y esta dentro de los limites de la matriz"""
            if self.en_limites(nueva_pos) and self.mapa[nueva_pos[0]][nueva_pos[1]]['Tipo'] != 3:
                """Nos movemos"""
                self.pos_pasada = self.pos
                self.pos = nueva_pos
                celda = self.mapa[nueva_pos[0]][nueva_pos[1]]
                """Cambiamos de estado si encontramos muestras o migajas"""
                self.estado = ('B' if celda['Cantidad'] > 1 else 'C') if celda['Tipo'] == 1 else 'B' if celda['Tipo'] == 2 else 'A'
                break

    """Obtenemos las celdas y distancias a la base de nuestro entorno que cumplan con los objetos que buscamos"""
    def entorno(self, objetos, pos):
        i, j = pos
        caminos = [
            {'pos': m, 'dis': abs(self.base[0] - m[0]) + abs(self.base[1] - m[1])}
            for m in [(i, j+1), (i, j-1), (i+1, j), (i-1, j)]
            if self.en_limites(m) and m != self.pos_pasada and self.mapa[m[0]][m[1]]['Tipo'] in objetos
        ]
        return caminos

    """Uso del algoritmo A* para crear el camino de migajas de la posicion del agente a la base"""
    def crear_camino(self):
        """Inicializamos la lista de rutas con nuestra posicion inicial"""
        rutas = [{'Posiciones':[self.pos],'Distancia':abs(self.base[0] - self.pos[0]) + abs(self.base[1] - self.pos[1])}]

        while len(rutas):
            """Obtenemos la ruta con el nodo más cercano a la base"""
            rutas.sort(key=lambda r: r['Distancia'])
            ruta_actual = rutas.pop(0)
            pos_actual = ruta_actual['Posiciones'][-1]

            """Obtenemos los movimientos posibles con el nodo más cercano a la base"""
            movimientos = self.entorno([0,2,4],pos_actual)

            movimientos.sort(key=lambda mov: mov['dis'])

            for movimiento in movimientos:
                """Si llegamos a la base"""
                if movimiento['pos'] == self.base:
                    """Recorremos el camino y ponemos las migajas"""
                    for p in ruta_actual['Posiciones'][1:]:
                        if self.mapa[p[0]][p[1]]['Tipo'] == 2:
                            self.mapa[p[0]][p[1]]['Cantidad'] += 2
                        else:
                            self.mapa[p[0]][p[1]] = {'Tipo': 2, 'Cantidad': 2}
                    return
                """Si el movimiento no lo hicimos anteriormente"""
                if movimiento['pos'] not in ruta_actual['Posiciones']:
                    """Lo agregamos a la ruta, con el nuevo costo total de la ruta"""
                    nueva_ruta = [r for r in ruta_actual['Posiciones']] + [movimiento['pos']]
                    rutas.append({'Posiciones':nueva_ruta, 'Distancia':movimiento['dis']})

    """Comportamiento del estado B y C"""
    def trasportar_muestras(self):

        caminos = []

        """Si llegamos a la base, dejamos la muestra y actualizamos posición"""
        if self.mapa[self.pos[0]][self.pos[1]]['Tipo'] == 4:
            self.con_muestra = False
            self.pos_pasada = self.pos

        """Si estamos sobre una muestra"""
        if self.mapa[self.pos[0]][self.pos[1]]['Tipo'] == 1:
            """Si no cargamos ya con una muestra"""
            if not self.con_muestra:
                self.pos_pasada = self.pos
                """Actualizamos posicion, cargamos la muestra y vemos si es la ultima o hay más"""
                self.con_muestra = True
                self.mapa[self.pos[0]][self.pos[1]]['Cantidad'] -= 1
                if self.mapa[self.pos[0]][self.pos[1]]['Cantidad'] == 0:
                    self.mapa[self.pos[0]][self.pos[1]] = {'Tipo': 0,'Cantidad': 0}
                    self.estado = 'C'
                else:
                    self.estado = 'B'

                """Vemos si hay un camino a seguir o lo creamos"""
                caminos = self.entorno([2,4],self.pos)
                if not caminos:
                    self.crear_camino()

        """
        Si{
        estamos en el estado 'C' (ya no hay mas muestras que recoger)
        cargamos con una muestra
        estamos sobre el camino de migajas
        } entonces recogemos las migajas, ya que no nos sirve más el camino
        """
        if self.estado == 'C' and self.con_muestra and self.mapa[self.pos[0]][self.pos[1]]['Tipo'] == 2:
            if self.mapa[self.pos[0]][self.pos[1]]['Cantidad']-2 <= 0:
                self.mapa[self.pos[0]][self.pos[1]] = {'Tipo': 0, 'Cantidad': 0}
            else:
                self.mapa[self.pos[0]][self.pos[1]]['Cantidad'] -= 2

        """Obtenemos el camino a seguir"""
        caminos = self.entorno([2,4],self.pos)
        if not caminos:
            caminos = self.entorno([1],self.pos)

        """Si hay un camino"""
        if caminos:
            """
            Lo ordenamos, es decir:
            Si cargamos una muestra, nos acercamos a la base
            Si no cargamos una muestra, nos vamos de la base
            """
            rev = not self.con_muestra
            caminos.sort(reverse=rev, key=lambda camino: camino['dis'])
            c = caminos[0]

            self.pos_pasada = self.pos
            self.pos = c['pos']
            return

        """
        En caso de que ya no tengamos a donde ir, por alguna razón,
        si seguimos cargando una muestra, debemos entregarla a todo costo
        así que creamos un camino y pasamos al estado C por si estabamos en B
        """
        if self.con_muestra:
            self.crear_camino()
            return
        if self.estado == 'B':
            self.pos_pasada = self.pos
            self.estado = 'C'
            self.con_muestra = True
            return

        """
        Si no estamos cargando ninguna muestra,
        entonces hemos cumplido nuestra mision
        y es momento de pasar al estado A
        """
        self.estado = 'A'

# ===============================
# INTERFAZ GRÁFICA CON TKINTER
# ===============================

class SimulacionGUI(tk.Tk):
    def __init__(self, filas=10, columnas=10, retardo=500):
        super().__init__()
        self.title("Simulacion de Agentes")
        self.filas = filas
        self.columnas = columnas
        self.retardo = retardo  # milisegundos entre actualización
        self.ancho = 600
        self.alto = 600
        self.canvas = tk.Canvas(self, width=self.ancho, height=self.alto)
        self.canvas.pack()

        # Crea el mapa y coloca elementos.
        self.mapa = [[{'Tipo': 0, 'Cantidad': 0} for _ in range(self.columnas)] for _ in range(self.filas)]
        self.base = crea_base(self.mapa, self.filas, self.columnas)
        crea_obstaculos(self.mapa, 30, self.filas, self.columnas)
        crea_muestras(self.mapa, 30, self.filas, self.columnas)

        # Cargar imágenes
        self.cargar_imagenes()

        # Dibuja el fondo de la imagen en el mapa
        self.fondo_imagen = self.canvas.create_image(0, 0, anchor="nw", image=self.fondo)

        # Crea dos agentes.
        self.agenteX = Agente(self.mapa, self.filas, self.columnas, self.base)
        self.agenteY = Agente(self.mapa, self.filas, self.columnas, self.base)
        self.agenteZ = Agente(self.mapa, self.filas, self.columnas, self.base)

        # Inicia el ciclo de actualización.
        self.actualizar_simulacion()

    def cargar_imagenes(self):
        """Carga todas las imágenes necesarias para la simulación."""
        anchoCelda = self.ancho // self.columnas
        altoCelda = self.alto // self.filas
        self.fondo = ImageTk.PhotoImage(Image.open(r"C:\Users\marse\OneDrive\Escritorio\escuela\UNIVERSIDAD\FIA\practica 3\proyectoB\fondo.jpg").resize((self.ancho, self.alto)))
        self.img_muestra = ImageTk.PhotoImage(Image.open(r"C:\Users\marse\OneDrive\Escritorio\escuela\UNIVERSIDAD\FIA\practica 3\proyectoB\muestra.png").resize((anchoCelda, altoCelda)))
        self.img_migaja = ImageTk.PhotoImage(Image.open(r"C:\Users\marse\OneDrive\Escritorio\escuela\UNIVERSIDAD\FIA\practica 3\proyectoB\migaja.png").resize((anchoCelda, altoCelda)))
        self.img_obstaculo = ImageTk.PhotoImage(Image.open(r"C:\Users\marse\OneDrive\Escritorio\escuela\UNIVERSIDAD\FIA\practica 3\proyectoB\obstaculo.png").resize((anchoCelda, altoCelda)))
        self.img_base = ImageTk.PhotoImage(Image.open(r"C:\Users\marse\OneDrive\Escritorio\escuela\UNIVERSIDAD\FIA\practica 3\proyectoB\base.png").resize((anchoCelda, altoCelda)))
        self.agenteX_img = ImageTk.PhotoImage(Image.open(r"C:\Users\marse\OneDrive\Escritorio\escuela\UNIVERSIDAD\FIA\practica 3\proyectoB\agenteX.png").resize((anchoCelda, altoCelda)))
        self.agenteY_img = ImageTk.PhotoImage(Image.open(r"C:\Users\marse\OneDrive\Escritorio\escuela\UNIVERSIDAD\FIA\practica 3\proyectoB\agenteY.png").resize((anchoCelda, altoCelda)))
        self.agenteZ_img = ImageTk.PhotoImage(Image.open(r"C:\Users\marse\OneDrive\Escritorio\escuela\UNIVERSIDAD\FIA\practica 3\proyectoB\agenteZ.png").resize((anchoCelda, altoCelda)))

    def actualizar_simulacion(self):
        """Actualiza la simulación y redibuja la interfaz cada 'retardo' milisegundos."""
        self.mapa = self.agenteX.act(self.mapa)
        self.mapa = self.agenteY.act(self.mapa)
        self.mapa = self.agenteZ.act(self.mapa)
        self.dibujar_mapa()
        # Vuelve a llamar a esta función después de 'retardo' milisegundos.
        self.after(self.retardo, self.actualizar_simulacion)

    def dibujar_mapa(self):
        """Dibuja el mapa en el canvas."""
        self.canvas.delete("all")
        anchoCelda = self.ancho // self.columnas
        altoCelda = self.alto // self.filas

        # Redibujar el fondo
        self.fondo_imagen = self.canvas.create_image(0, 0, anchor="nw", image=self.fondo)

        for i in range(self.filas):
            for j in range(self.columnas):
                tipo_celda = self.mapa[i][j]['Tipo']

                x0 = j * anchoCelda
                y0 = i * altoCelda

                if tipo_celda == 1:
                    self.canvas.create_image(x0, y0, anchor="nw", image=self.img_muestra)
                elif tipo_celda == 2:
                    self.canvas.create_image(x0, y0, anchor="nw", image=self.img_migaja)
                elif tipo_celda == 3:
                    self.canvas.create_image(x0, y0, anchor="nw", image=self.img_obstaculo)
                elif tipo_celda == 4:
                    self.canvas.create_image(x0, y0, anchor="nw", image=self.img_base)

                x1 = x0 + anchoCelda
                y1 = y0 + altoCelda
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

        self.dibujar_agente(self.agenteX.pos, anchoCelda, altoCelda, self.agenteX_img)
        self.dibujar_agente(self.agenteY.pos, anchoCelda, altoCelda, self.agenteY_img)
        self.dibujar_agente(self.agenteZ.pos, anchoCelda, altoCelda, self.agenteZ_img)

    def dibujar_agente(self, pos, anchoCelda, altoCelda, imagen):
        """Dibuja un agente en la posición indicada."""
        j = pos[1]
        i = pos[0]
        x0 = j * anchoCelda
        y0 = i * altoCelda

        # Dibujar la imagen del agente
        self.canvas.create_image(x0, y0, anchor="nw", image=imagen)

if __name__ == "__main__":
    app = SimulacionGUI(filas=15, columnas=15, retardo=500)
    app.mainloop()