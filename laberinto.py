import random

# =======================
# CONFIGURACIÓN INICIAL
# =======================
ALTO = 5
ANCHO = 5

gato = (0, 0)
raton = (4, 4)
TURNOS = 10

# =======================
# FUNCIONES
# =======================

def mostrar_tablero(gato, raton):
    for fila in range(ALTO):
        for col in range(ANCHO):
            if (fila, col) == gato:
                print("G", end=" ")
            elif (fila, col) == raton:
                print("R", end=" ")
            else:
                print(".", end=" ")
        print()  # nueva línea

def mover_gato(gato, raton):
    fila_g, col_g = gato
    fila_r, col_r = raton

    if fila_g < fila_r:
        fila_g += 1
    if fila_g > fila_r:
        fila_g -= 1
    if col_g < col_r:
        col_g += 1
    if col_g > col_r:
        col_g -= 1

    return (fila_g, col_g)

def minimax_raton(raton, gato):
    fila_r, col_r = raton
    fila_g, col_g = gato

    # Todas las posibles direcciones del ratón
    posibles_movimientos = [
        (fila_r - 1, col_r),     # arriba
        (fila_r + 1, col_r),     # abajo
        (fila_r, col_r - 1),     # izquierda
        (fila_r, col_r + 1),     # derecha
        (fila_r - 1, col_r - 1), # diagonal arriba-izq
        (fila_r - 1, col_r + 1), # diagonal arriba-der
        (fila_r + 1, col_r - 1), # diagonal abajo-izq
        (fila_r + 1, col_r + 1)  # diagonal abajo-der
    ]

    # Filtrar movimientos válidos dentro del tablero
    movimientos_validos = []
    for f, c in posibles_movimientos:
        if 0 <= f < ALTO and 0 <= c < ANCHO:
            movimientos_validos.append((f, c))

    # Evaluar cada movimiento: máxima distancia al gato
    max_distancia = -1
    mejores_movimientos = []

    for f, c in movimientos_validos:
        # Simula cómo se movería el gato después del movimiento del ratón
        fila_g_tmp, col_g_tmp = mover_gato(gato, (f, c))
        distancia = abs(f - fila_g_tmp) + abs(c - col_g_tmp)

        if distancia > max_distancia:
            max_distancia = distancia
            mejores_movimientos = [(f, c)]
        elif distancia == max_distancia:
            mejores_movimientos.append((f, c))

    # Elegir al azar entre los mejores movimientos
    return random.choice(mejores_movimientos)

# =======================
# BUCLE DE TURNOS
# =======================
for turno in range(TURNOS):
    print(f"\n=== Turno {turno + 1} ===")

    # Movimiento del ratón con Minimax + aleatoriedad
    raton = minimax_raton(raton, gato)

    # Movimiento del gato
    gato = mover_gato(gato, raton)

    # Mostrar tablero
    mostrar_tablero(gato, raton)

    # Verificar si el gato atrapó al ratón
    if gato == raton:
        print("🐱 ¡El gato atrapó al ratón!")
        break
