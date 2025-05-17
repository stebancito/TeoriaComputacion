import json
from typing import List, Dict, Set

def convertirTransiciones(datos):
    #representara las transiciones de forma simple en un diccionoario con una tupla como clave y lista como valor (origen, simbolo) : [destinos]
    dic_simplificado = {}

    for tran in datos["transiciones"]:
        clave = (tran["origen"], tran["simbolo"])
        if clave not in dic_simplificado:
            dic_simplificado[clave] = []
        dic_simplificado[clave].extend(tran["destino"])

    return dic_simplificado

def transicionesEpsilon(transiciones: Dict[tuple, List[str]]) -> Dict[str, List[str]]:

    # transiciones que se hacen mediante cadena vacia, epsilon pues
    transiciones_ep = {}

    # items() devuelve una tupla donde tiene la clave y valor del dict (clave, valor)
    for (origen, simbolo), destinos in transiciones.items(): #(origen, destino) = (origen, destino) del dict, y destinos = [] del dict, es decir recorremos las transiciones simplificadas
        if simbolo == "":
            if origen not in transiciones_ep:
                transiciones_ep[origen] = []
            #agregamos los destinos de esa clave (origen)
            transiciones_ep[origen].extend(destinos)
    return transiciones_ep


def cerraduraEpsilon(estado: str, transiciones_eps: Dict[str, List[str]]) -> Set[str]:

    cerradura = set()
    pila = [estado] #pila de apoyo para verificar todos los estados y no olvidarnos de alguno que pueda tener destinos con epsilon
    cerradura.add(estado)

    while pila:
        estado_actual = pila.pop()
        # recorremos cada destino de cada estado si es que esta en las transiciones epsilon
        for destino in transiciones_eps.get(estado_actual, []):
            if destino not in cerradura:
                cerradura.add(destino)
                pila.append(destino)
    return cerradura


def mover_A(simbolo: str, conjunto: Set[str], transiciones: Dict[tuple, List[str]]) -> Set[str]:
    resultado = set()

    for estado in conjunto:
        # (estado, simbolo) es la clave del diccionario indice, devuelve [] si no encontro
        resultado.update(transiciones.get((estado, simbolo), []))
    return resultado

def ir_A(simbolo: str, conjunto: Set[str], transiciones: Dict[tuple, List[str]]) -> Set[str]:
    resultado = set()
    transiciones_ep = transicionesEpsilon(transiciones)
    print(f"Transiciones ep: {transiciones_ep}")
    mover = mover_A(simbolo, conjunto, transiciones)
    print(f"Mover : {mover}")
    for estado in mover:
        print(estado)
        resultado.update(cerraduraEpsilon(estado, transiciones_ep))
    
    return resultado


def leerArchivo(path: str):
    try:
        with open(path, 'r') as file:
            
            print("Archivo leido")
            datos = json.load(file)
            return datos
    except FileNotFoundError:
        print("El archivo no existe")


if __name__ == "__main__":
    print("Bienvenido")

    path = input("Ingresa el archivo de AFN: ")
    print(path)

    datos = leerArchivo(path)
    transiciones = convertirTransiciones(datos)
    
    for trans in datos["transiciones"]:
        simbolo = trans["simbolo"]
        origen = trans["origen"]
        destinos = trans["destino"]
        print(f"{origen} --{simbolo or 'ε'}--> {destinos}")

    print(f"Transiciones simplificadas {transiciones}")

    transiciones_epsilon = transicionesEpsilon(transiciones)
    print(f"Transiciones epsilon {transiciones_epsilon}")

    cerradura_epsilon = cerraduraEpsilon(datos["e_inicial"], transiciones_epsilon)
    print(f"De la cerradura epsilon resulta: {cerradura_epsilon}")


    ira = ir_A(datos["alfabeto"][0], cerradura_epsilon, transiciones)
    print(f"De la operacion ir_a resulta con simbolo {datos["alfabeto"][0]}: {ira}")



