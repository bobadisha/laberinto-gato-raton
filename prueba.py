import os
import random

print("--- 🐱 BIENVENIDO AL DUELO DE EMOJIS 🐭 ---")
rol = input("Elige ser Gato (G) o Raton (R): ").upper()
tamanho = 6
raton_pos = [0, 0]
gato_pos = [3, 3]
quesos = [[1, 2], [2, 1], [3, 0]]
quesos_comidos = 0

def dibujar_mapa():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("  ┌" + "───" * tamanho + "┐")
    for r in range(tamanho):
        fila_texto = "  │"
        for c in range(tamanho):
            if [r, c] == gato_pos and [r, c] == raton_pos:
                fila_texto += "💥 " 
            elif [r, c] == gato_pos:
                fila_texto += "🐱 " 
            elif [r, c] == raton_pos:
                fila_texto += "🐭 " 
            elif [r, c] in quesos:
                fila_texto += "🧀 " 
            else:
                fila_texto += " . " 
        print(fila_texto + "│")
    print("  └" + "───" * tamanho + "┘")
    print(f"  🧀 Quesos: {quesos_comidos}/3 | Jugando como: {rol}")

def mover_manual(posActual, nombre):
    direccion = input(f"\n  Mueve al {nombre} (w/a/s/d): ").lower()
    nf, nc = posActual[0], posActual[1]
    if direccion == 'w': nf -= 1
    elif direccion == 's': nf += 1
    elif direccion == 'a': nc -= 1
    elif direccion == 'd': nc += 1
    
    if 0 <= nf < tamanho and 0 <= nc < tamanho:
        return [nf, nc]
    return posActual

def evaluar():
    # Distancia de Manhattan
    dist = abs(gato_pos[0] - raton_pos[0]) + abs(gato_pos[1] - raton_pos[1])
    if gato_pos == raton_pos:
        return 100
    return -dist

def minimax(quien, profundidad):
    if profundidad == 0 or gato_pos == raton_pos:
        return evaluar()

    opciones = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    
    if quien == "G":
        mejor_val = -1000
        for f, c in opciones:
            nf, nc = gato_pos[0] + f, gato_pos[1] + c
            if 0 <= nf < tamanho and 0 <= nc < tamanho:
                original = list(gato_pos) # Copia real
                gato_pos[0], gato_pos[1] = nf, nc
                val = minimax("R", profundidad - 1)
                gato_pos[0], gato_pos[1] = original[0], original[1]
                mejor_val = max(mejor_val, val)
        return mejor_val
    else:
        peor_val = 1000
        for f, c in opciones:
            nf, nc = raton_pos[0] + f, raton_pos[1] + c
            if 0 <= nf < tamanho and 0 <= nc < tamanho:
                original = list(raton_pos)
                raton_pos[0], raton_pos[1] = nf, nc
                val = minimax("G", profundidad - 1)
                raton_pos[0], raton_pos[1] = original[0], original[1]
                peor_val = min(peor_val, val)
        return peor_val

def mejor_movimiento(quien):
    mejor_val = -1000 if quien == "G" else 1000
    pos_actual = list(gato_pos if quien == "G" else raton_pos)
    mejor_pos = list(pos_actual)
    opciones = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    for f, c in opciones:
        nf, nc = pos_actual[0] + f, pos_actual[1] + c
        if 0 <= nf < tamanho and 0 <= nc < tamanho:
            if quien == "G":
                original = list(gato_pos)
                gato_pos[0], gato_pos[1] = nf, nc
                val = minimax("R", 2)
                gato_pos[0], gato_pos[1] = original[0], original[1]
                if val > mejor_val:
                    mejor_val, mejor_pos = val, [nf, nc]
            else:
                original = list(raton_pos)
                raton_pos[0], raton_pos[1] = nf, nc
                val = minimax("G", 2)
                raton_pos[0], raton_pos[1] = original[0], original[1]
                if val < mejor_val:
                    mejor_val, mejor_pos = val, [nf, nc]
    return mejor_pos

while quesos_comidos < 3:
    dibujar_mapa()
    
    if rol == "R":
        raton_pos = mover_manual(raton_pos, "Ratón")
    else:
        raton_pos = mejor_movimiento("R")
    
    if raton_pos in quesos:
        quesos.remove(raton_pos)
        quesos_comidos += 1
    
    if raton_pos == gato_pos: break

    dibujar_mapa()
    
    if rol == "G":
        gato_pos = mover_manual(gato_pos, "Gato")
    else:
        print("\n  🐱 IA Gato pensando...")
        gato_pos = mejor_movimiento("G")
    
    if gato_pos == raton_pos: break

dibujar_mapa()
if quesos_comidos == 3:
    print("\n  🎉 ¡VICTORIA! El ratón comió todos los quesos.")
else:
    print("\n  💀 ¡GAME OVER! El gato atrapó al ratón.")
