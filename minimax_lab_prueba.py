import random  # Necesario para elegir movimientos al azar

alto = 8 # Tamaño del mapa/laberinto
ancho = 8
# Posiciones iniciales del gato y del ratón
pos_gato = (0, 0)      # esquina superior izquierda
pos_raton = (7, 7)     # esquina inferior derecha (inicial)

#elmapa vacío
mapa = []  # lista que representará el tablero


for i in range(alto):       # bucle para crear cada fila
    fila = []                # lista vacía que será la fila
    for j in range(ancho):   # bucle para crear cada columna
        fila.append(".")     # agregar punto que representa espacio vacío
    mapa.append(fila)        # agregar fila al mapa

paredes = [ # Agregar paredes al mapa
    (3, 3), (3, 4), (3, 5),
    (4, 3),
    (5, 3)
]
for f, c in paredes:
    mapa[f][c] = "#"

# Colocar al gato y al ratón en el mapa
mapa[pos_gato[0]][pos_gato[1]] = "G"       # G = gato
mapa[pos_raton[0]][pos_raton[1]] = "R"     # R = ratón

def es_valido(pos):
    fila, col = pos
    return 0 <= fila < alto and 0 <= col < ancho and mapa[fila][col] != "#"

# Función para calcular distancia Manhattan entre dos posiciones
def distancia(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

print("Mapa inicial:") # Imprimir mapa inicial
for fila in mapa:
    print(" ".join(fila))  # join para mostrar los elementos de la fila separados por espacio

movimientos_totales = 20 # Número máximo de turnos

for turno in range(movimientos_totales): # Bucle principal del juego

    movimientos_posibles = [ # Lista de movimientos posibles del ratón (solo 4 direcciones)
        (pos_raton[0]-1, pos_raton[1]),  # Arriba
        (pos_raton[0]+1, pos_raton[1]),  # Abajo
        (pos_raton[0], pos_raton[1]-1),  # Izquierda
        (pos_raton[0], pos_raton[1]+1)   # Derecha
    ]
 # Filtrar movimientos válidos del ratón
    movimientos_validos = []  # lista donde guardaremos los movimientos posibles
    for pos in movimientos_posibles:
        if es_valido(pos) and pos != pos_gato:  # dentro del tablero, no pared, y no pisar al gato
         movimientos_validos.append(pos)

    # Movimiento del ratón con Minimax profundidad 2
    if movimientos_validos:
        mapa[pos_raton[0]][pos_raton[1]] = "."

        mejor_movimiento = None
        mejor_valor = -9999  # porque queremos maximizar

        # Probar cada movimiento posible del ratón
        for movimiento_raton in movimientos_validos:

            nueva_pos_raton = movimiento_raton

            # Simular posibles movimientos del gato
            movimientos_gato_simulados = [
                (pos_gato[0]-1, pos_gato[1]),
                (pos_gato[0]+1, pos_gato[1]),
                (pos_gato[0], pos_gato[1]-1),
                (pos_gato[0], pos_gato[1]+1)
            ]

            movimientos_validos_gato_sim = []
            for f, c in movimientos_gato_simulados:
                if 0 <= f < alto and 0 <= c < ancho and mapa[f][c] != "#":
                    movimientos_validos_gato_sim.append((f, c))

            # El gato responde minimizando la distancia al ratón simulado
            if movimientos_validos_gato_sim:
                mejor_mov_gato = min(
                    movimientos_validos_gato_sim,
                    key=lambda pos: distancia(pos, nueva_pos_raton)
                )
            else:
                mejor_mov_gato = pos_gato

            # Evaluar la posición final después de ambos movimientos
            valor = distancia(mejor_mov_gato, nueva_pos_raton)

            # El ratón quiere maximizar esa distancia
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = nueva_pos_raton

        # Aplicar el mejor movimiento encontrado
        pos_raton = mejor_movimiento
        mapa[pos_raton[0]][pos_raton[1]] = "R"

    # Lista de movimientos posibles del gato (solo 4 direcciones)
    movimientos_gato = [
        (pos_gato[0]-1, pos_gato[1]),  # Arriba
        (pos_gato[0]+1, pos_gato[1]),  # Abajo
        (pos_gato[0], pos_gato[1]-1),  # Izquierda
        (pos_gato[0], pos_gato[1]+1)   # Derecha
    ]
    # Filtrar movimientos válidos del gato
    movimientos_validos_gato = []
    for pos in movimientos_gato:
        if es_valido(pos) and pos != pos_raton:  # dentro del tablero, no pared, y no pisar al ratón
         movimientos_validos_gato.append(pos)

   
    # Elegir movimiento que minimice la distancia al ratón
    if movimientos_validos_gato:  # solo si hay movimientos posibles
        mapa[pos_gato[0]][pos_gato[1]] = "."  # borrar gato de posición anterior
        pos_gato = min(movimientos_validos_gato, key=lambda pos: distancia(pos, pos_raton))
  # moverse al más cercano
        mapa[pos_gato[0]][pos_gato[1]] = "G"  # colocar gato en nueva posición

    # Comprobar si el gato atrapó al ratón
    if pos_gato == pos_raton:  # si coinciden las posiciones
        print(f"\nEl gato atrapó al ratón en el turno {turno + 1}!")
        break  # termina el bucle y el juego
    # Imprimir mapa después del turno
    print(f"\nTurno {turno + 1}:")
    for fila in mapa:
        print(" ".join(fila))