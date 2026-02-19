import os #es como el puente de comunicacion entre python y la computadora, para poder limpiar
import random #para poner en aleatorio cosas, como el queso 

rol = input("Elige Gato (G) o Raton (R): ").upper() #para elegir al personaje antes de jugar// con upper se convierte en mayuscula
tamanho = 8 #la dimension que tendra el mapa
raton_pos = [0, 0] #posicion inicial de R 1ra fila, 1ra columna
gato_pos = [7, 7] #la misma cosa
quesos_comidos = 0 #para saber cuando termina el juego por puntos

# creacion de 5 quesos
quesos = [] #lista vacia para guardar la ubicacion de los quesos
while len(quesos) < 5: #un bucle, cuando no se junte 5 quesos seguimos jugando
    pos = [random.randint(0, 7), random.randint(0, 7)] #para elegir una fila y una columna al azar de 0 a 7
    if pos != raton_pos and pos != gato_pos and pos not in quesos: #para que no coincidan los quesos con la ubi del G/R y otro queso
        quesos.append(pos) #para agregar el queso en la posicion al azar, despues de pasar los filtros

def dibujar_mapa(): #crear una funcion para que se pueda mostrar en pantalla
    os.system('cls' if os.name == 'nt' else 'clear') #limpia ;a pantalla, para que no aparezcan varios turnos impresos, y simule una animacion
    for r in range(tamanho): #bucle para ir creando el mapa recorriendo cada fila de 0 a 7
        fila = "" #un espacio de texto vacio
        for c in range(tamanho): # otro bucle dentro del mismo bucle para recorrer cada columna
            if [r, c] == gato_pos: fila += " G " #compara la posicion del gato, si coincide, pone G
            elif [r, c] == raton_pos: fila += " R " #compara la del raton, si coincide pone R
            elif [r, c] in quesos: fila += " Q " # si coincide con la lista de quesos pone una Q
            else: fila += " . " #si no hay alguno de ellos que ponga un punto (ayuda a dibujar el mapa)
        print(fila) #al terminar de revisar las columnas, imprime la fila completa
    print(f"\nQuesos: {quesos_comidos}/5") #para ir viendo la cantidad de los quesos comidos y disponibles

def mover_manual(pos, nombre): #definir una funcion
    m = input(f"Mover {nombre} (w/a/s/d): ").lower() #para pedir al jugador una direccion a mover
    nf, nc = pos[0], pos[1] # variables temporales, nf es nueva fila y nc es nueva columna
    if m == 'w': nf -= 1 #resta una fila para ir arriba
    elif m == 's': nf += 1 #suma una fila para ir abajo
    elif m == 'a': nc -= 1 #resta una columna para ir a la izq
    elif m == 'd': nc += 1 #suma una columna para ir a la der
    if 0 <= nf < tamanho and 0 <= nc < tamanho: #es para que los jugadores no se salgan de los limites del mapa
        return [nf, nc] # si todo es correcto, le lleva a la nueva posicion
    return pos # si intentas salir del mapa, se queda en el mismo lugar

def evaluar(): #evaluar las posiciones
    # El gato quiere distancia 0 (atrapado). 
    # Si no, devuelve la distancia negativa (mientras más lejos, peor puntaje)
    dist = abs(gato_pos[0] - raton_pos[0]) + abs(gato_pos[1] - raton_pos[1]) #distancia manhattan para medir los pasos 
    return 100 if gato_pos == raton_pos else -dist #si el G atrapa a R el puntaje es 100, si no busca el numero mas alto para estar lo mas cerca del R

def minimax(quien, profundidad): #el algoritmo para las jugadas futuras
    if profundidad == 0 or gato_pos == raton_pos: #detiene a la ia de pensar las jugadas cuando llegue a 0 la profundidad o cuando el G haya ganado
        return evaluar() #entrega un resultado para que pueda elegir el gato
    
    opciones = [[-1, 0], [1, 0], [0, -1], [0, 1]] #las opciones de movimiento, arriba abajo izquierda derecha
    if quien == "G": #el turno del gato
        mejor = -1000 #para comparar el resultado de la posicion del raton y elegir el mejor o mas proximo
        for f, c in opciones: #bucle para probar en las direcciones que estan en opciones
            nf, nc = gato_pos[0] + f, gato_pos[1] + c #para calcular las posibles direcciones
            if 0 <= nf < tamanho and 0 <= nc < tamanho: #Para que solo se mueva dentro del mapa
                orig = list(gato_pos) #lista copia, para guardar la posicion actual antes de moverse
                gato_pos[0], gato_pos[1] = nf, nc #movimiento temporal del G para simular la jugada
                val = minimax("R", profundidad - 1) #para que imagine los posibles movimientos de R
                gato_pos[0], gato_pos[1] = orig #para llevar de cuelta al gato a su posicion donde estaba antes de empezar a pensar
                mejor = max(mejor, val) ## Compara el resultado actual (val) con el mejor que tenía (mejor) y guarda el más alto.
        return mejor #entrega el puntaje mas alto que encontro el gato
    else:
        peor = 1000 #comparar la posicion del gato y elegir el peor o mas lejos
        for f, c in opciones: #bucle para probar las direcciones que estan en opciones
            nf, nc = raton_pos[0] + f, raton_pos[1] + c #calcular las posibles direcciones
            if 0 <= nf < tamanho and 0 <= nc < tamanho: #para que solo se mueva dentro del mapa
                orig = list(raton_pos) #para guardar en la lista la posicion actual antes de moverse
                raton_pos[0], raton_pos[1] = nf, nc #movimiento temporal del R para simular la jugada
                val = minimax("G", profundidad - 1) #para que imagine o piense los posibles movimientos de G
                raton_pos[0], raton_pos[1] = orig #para que vuelva al lugar donde esta antes de simular los movimientos
                peor = min(peor, val) #calcula la mayor distancia negativa , para alejarse mas del gato
        return peor #entrega el puntaje mas bajo que encontro el raton

def mejor_movimiento(quien): #esta es la funcion que toma la decision final para ejecutar el movimiento en el mapa real
    mejor_val = -1000 if quien == "G" else 1000 #Preparamos el puntaje récord inicial dependiendo de quién fue seleccionado
    pos_actual = list(gato_pos if quien == "G" else raton_pos) #mira la pieza que toca mover segun la eleccion R o G
    mejor_pos = list(pos_actual) #guarda las coordenadas del mejor lugar que encontro
    
    for f, c in [[-1, 0], [1, 0], [0, -1], [0, 1]]: #para recorrer las direcciones posibles Arriba Abajo Izq Der
        nf, nc = pos_actual[0] + f, pos_actual[1] + c  # Sumamos el movimiento (f, c) a la posición actual para obtener la nueva coordenada (nf, nc)
        if 0 <= nf < tamanho and 0 <= nc < tamanho: #para calcular la nueva posicion, y asegurarse que este dentro del tablero
            orig = list(gato_pos if quien == "G" else raton_pos) # Guardamos una copia de la posición actual (Gato o Ratón) para poder regresar después de la simulación.
            if quien == "G": gato_pos[0], gato_pos[1] = nf, nc # Movemos al gato a la nueva casilla (nf, nc) para que la IA evalúe qué tan buena es esa posición
            else: raton_pos[0], raton_pos[1] = nf, nc #si no es elegido el gato, que se mueva el raton
            
            val = minimax("R" if quien == "G" else "G", 3) #dependiendo de quien sea seleccionado, simula el movimiento del oponente para saber si es bueno o no, mira 3 turnos por delante
            
            if quien == "G" and val > mejor_val: #si el elegido es el gato, analiza si el resultado de la simulacion es mayor al que tenia guardado
                mejor_val, mejor_pos = val, [nf, nc] #si la simulacion actual es mejor al que teniamos, actualizamos el record y guardamos la ubiacion en esa casilla
            if quien == "R" and val < mejor_val: #si el raton encuentra un movimiento que disminuya el puntaje o sea aleja al  G
                mejor_val, mejor_pos = val, [nf, nc] #guarda el nuevo record o puntaje y la ubicacion 
                
            if quien == "G": gato_pos[0], gato_pos[1] = orig #se encarga de volver a la posicion de origen al personaje despues de moverse en una simulacion
            else: raton_pos[0], raton_pos[1] = orig #si no es el gato elegido, es el raton, vuelve a la posicion de origen despues de moverse en la simulacion
    return mejor_pos #despues de todos los analisis y simulaciones, envia al juego el movimiento real

# --- JUEGO ---
while quesos_comidos < 5 and gato_pos != raton_pos: #continua si la cantidad de quesos comidos es menor a 5 y si el gato esta en diferente posicion del raton
    dibujar_mapa() #mostrar en pantalla los movimientos/coordenadas
    raton_pos = mover_manual(raton_pos, "Raton") if rol == "R" else mejor_movimiento("R") #dependiendo de quien elijamos, lo movemos manualmente, y el que no lo elejimos, lo mueve la ia
    
    if raton_pos in quesos: #si el raton esta en la posicion de Q..
        quesos.remove(raton_pos) #borramos el Q y dejamos a R en esa posicion
        quesos_comidos += 1 #sumamos 1 a la variable de quesos comidos
    
    if gato_pos == raton_pos: break #si ambos estan en la misma posicion se termina el bucle/juego
    
    dibujar_mapa() #mostrar en pantalla los movimientos/coordenadas
    gato_pos = mover_manual(gato_pos, "Gato") if rol == "G" else mejor_movimiento("G")  #si elegimos G, movemos manualmente, sino lo mueve la ia

dibujar_mapa() #dibujar mapa ultima vez para mostrar los resultados
print("¡Victoria!" if quesos_comidos == 5 else "¡Atrapado!") #muestra el resultado si es victoria o derrota dpendiendo de quien se eligio