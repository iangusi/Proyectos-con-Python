import pygame
import sys
import random
import time
from collections import deque

# Definiciones globales
estado_objetivo = [x for x in range(16)]
estados_vistos = set()

# Precalcular movimientos posibles para cada posición en el tablero 4x4
movimientos = []
for i in range(16):
    movimiento = []
    if (i + 1) % 4 != 0:
        movimiento.append(i + 1)
    if (i - 1) % 4 != 3:
        movimiento.append(i - 1)
    if i + 4 <= 15:
        movimiento.append(i + 4)
    if i - 4 >= 0:
        movimiento.append(i - 4)
    movimientos.append(movimiento)

def swap(cero, pos):
    return pos, cero

# Estado incial del rompecabezas 
def crearJuego():
    estado_juego = [e for e in estado_objetivo]
    # Se hacen movimientos aleatorios hasta que se cumpla la condición aleatoria
    c = 0
    while random.randint(0, 20) != 9:
        c+=1
        cero = estado_juego.index(0)
        pos = random.choice(movimientos[cero])
        estado_juego[cero], estado_juego[pos] = swap(estado_juego[cero], estado_juego[pos])
    print("max_mov:",c)
    return estado_juego

def mostrarEstado(estado_inicial,ruta_actual):
    cero = estado_inicial.index(0)
    for r in ruta_actual:
        estado_inicial[cero], estado_inicial[r] = swap(estado_inicial[cero], estado_inicial[r])
        cero = r

# --- Algoritmos de búsqueda ---
def BFSoIDDFS(estado_inicial, iteracion=0):
    cont = 0
    nodos = 0
    rutas = [[estado_inicial.index(0)]]
    while True:
        cont += 1

        ruta_actual = []

        if(iteracion):
            iteracion += 1
            if iteracion > 5:
                ruta_actual = rutas.pop()
                iteracion = 1
            else:
                ruta_actual = rutas.pop(0)
        else:
            ruta_actual = rutas.pop(0)

        cero = ruta_actual[len(ruta_actual)-1]
                
        nuevas_rutas = []
        for movimiento in movimientos[cero]:
            
            nuevo_estado = [e for e in estado_inicial]
            mostrarEstado(nuevo_estado,ruta_actual+[movimiento])

            if nuevo_estado == estado_objetivo:
                ruta_actual.append(movimiento)
                rr = [[e for e in estado_inicial]]
                for r in range(len(ruta_actual)):
                    n_estado = [e for e in estado_inicial]
                    mostrarEstado(n_estado,ruta_actual[0:r+1])
                    rr.append(n_estado)

                return rr, cont, nodos, len(ruta_actual)

            estado_tuple = tuple(nuevo_estado)
            if estado_tuple not in estados_vistos:
                estados_vistos.add(estado_tuple)
                nodos += 1
                nuevas_rutas.append(movimiento)
                
        for estado in nuevas_rutas:
            r_actual = [r for r in ruta_actual]
            r_actual.append(estado)
            rutas.append(r_actual)

    return None, cont, nodos, 0

# Funcion wrapper para ejecutar cada algoritmo
def solve(estado_inicial, f, n=0):
    estados_vistos.clear()
    return f(estado_inicial,n)

# Interfaz gráfica con Pygame

# Configuración de la ventana y del tablero
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 550  # espacio extra para botones / métricas
BOARD_SIZE = 400
ROWS, COLS = 4, 4
TILE_SIZE = BOARD_SIZE // COLS

# Colores
BG_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (150, 250, 150)
TEXT_COLOR = (0, 0, 0)

# Cargar y dividir la imagen en 16 piezas
def load_tiles(image_path, rows=4, cols=4):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (BOARD_SIZE, BOARD_SIZE))
    tile_width = BOARD_SIZE // cols
    tile_height = BOARD_SIZE // rows
    tiles = {}
    for i in range(rows * cols):
        if i == 0:
            # La pieza 0 (espacio vacío) se deja en blanco
            tiles[i] = None
        else:
            col = i % cols
            row = i // cols
            rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
            tile_image = image.subsurface(rect).copy()
            tiles[i] = tile_image
    return tiles

def draw_board(screen, board, tiles, board_rect):
    # Dibuja cada casilla del tablero
    for i in range(ROWS):
        for j in range(COLS):
            tile_value = board[i * COLS + j]
            tile_rect = pygame.Rect(board_rect.x + j * TILE_SIZE,
                                    board_rect.y + i * TILE_SIZE,
                                    TILE_SIZE, TILE_SIZE)
            if tile_value != 0 and tiles[tile_value]:
                screen.blit(tiles[tile_value], tile_rect)
            else:
                # Casilla vacía
                pygame.draw.rect(screen, (200, 200, 200), tile_rect)
            pygame.draw.rect(screen, BORDER_COLOR, tile_rect, 2)

def draw_buttons(screen, buttons, font):
    for btn in buttons:
        color = btn['hover_color'] if btn.get('hover', False) else btn['color']
        pygame.draw.rect(screen, color, btn['rect'])
        text_surf = font.render(btn['text'], True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=btn['rect'].center)
        screen.blit(text_surf, text_rect)

def draw_metrics(screen, metrics, font, area_rect):
    # Dibuja las métricas en el área de botones
    texts = [
        f"Algoritmo: {metrics['algoritmo']}",
        f"Ciclos: {metrics['ciclos']}",
        f"Nodos creados: {metrics['nodos']}",
        f"Movimientos: {metrics['movimientos']}"
    ]
    y = area_rect.y + 10
    for t in texts:
        text_surf = font.render(t, True, TEXT_COLOR)
        screen.blit(text_surf, (area_rect.x + 10, y))
        y += text_surf.get_height() + 5

def animate_solution(screen, board_rect, solution_path, tiles, delay, metrics, font, button_area):
    # Anima la secuencia de estados de la solución
    clock = pygame.time.Clock()
    for state in solution_path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BG_COLOR)
        draw_board(screen, state, tiles, board_rect)
        screen.fill(BG_COLOR, button_area)
        draw_metrics(screen, metrics, font, button_area)
        pygame.display.update()
        time.sleep(delay)
        clock.tick(60)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Puzzle 15 - Algoritmos de busqueda")
    font = pygame.font.SysFont(None, 24)
    
    # Área del tablero (parte superior)
    board_rect = pygame.Rect(0, 0, BOARD_SIZE, BOARD_SIZE)
    # Área inferior para botones/métricas
    button_area = pygame.Rect(0, BOARD_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT - BOARD_SIZE)
    
    # Cargar la imagen y obtener las piezas
    try:
        tiles = load_tiles("vivy.jpg")
    except Exception as e:
        print("Error al cargar la imagen. Asegúrate de tener 'puzzle_image.jpg' en la carpeta.")
        pygame.quit()
        sys.exit()
    
    # Generar estado inicial revuelto
    initial_state = crearJuego()
    
    # Variables para guardar la solución y métricas
    solution_path = None
    metrics = None
    algoritmo_seleccionado = None

    # Definir botones
    button_width = 100
    button_height = 40
    gap = 20
    buttons = [
        {'text': 'BFS', 'rect': pygame.Rect(gap, BOARD_SIZE + gap, button_width, button_height),
         'color': BUTTON_COLOR, 'hover_color': BUTTON_HOVER_COLOR, 'algoritmo': 'BFS'},
        {'text': 'IDDFS', 'rect': pygame.Rect(3 * gap + 2 * button_width, BOARD_SIZE + gap, button_width, button_height),
         'color': BUTTON_COLOR, 'hover_color': BUTTON_HOVER_COLOR, 'algoritmo': 'IDDFS'},
    ]
    
    running = True
    animando = False  # banderita para indicar si se está animando la solución
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Si aún no se ha seleccionado un algoritmo y se hacen clic en algún botón
            if not animando and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn['rect'].collidepoint(mouse_pos):
                        algoritmo_seleccionado = btn['algoritmo']
                        # Ejecutar el algoritmo seleccionado
                        if algoritmo_seleccionado == 'BFS':
                            solution_path, ciclos, nodos, mov = solve(initial_state, BFSoIDDFS)
                        elif algoritmo_seleccionado == 'IDDFS':
                            solution_path, ciclos, nodos, mov = solve(initial_state, BFSoIDDFS, 1)
                        metrics = {
                            'algoritmo': algoritmo_seleccionado,
                            'ciclos': ciclos,
                            'nodos': nodos,
                            'movimientos': mov
                        }
                        animando = True  # pasar a modo animación
                        
            # Actualización de hover para botones
            if not animando and event.type == pygame.MOUSEMOTION:
                for btn in buttons:
                    btn['hover'] = btn['rect'].collidepoint(mouse_pos)
                    
        screen.fill(BG_COLOR)
        
        # Dibujar el tablero con el estado actual (si no se está animando, se muestra el estado revuelto)
        draw_board(screen, initial_state, tiles, board_rect)
        
        # Si ya se seleccionó un algoritmo y se terminó la animación, mostrar métricas
        if animando and solution_path:
            animate_solution(screen, board_rect, solution_path, tiles, 0.5, metrics, font, button_area)
            
            pygame.display.update()
            solution_path = None  
            animando = False
        elif not animando:
            # Dibujar los botones para seleccionar algoritmo
            draw_buttons(screen, buttons, font)
        
        pygame.display.update()
        pygame.time.Clock().tick(30)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
