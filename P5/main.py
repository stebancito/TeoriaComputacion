import json
from typing import List, Dict, Set

import xml.etree.ElementTree as ET
import math


def convertirTransiciones(datos):
    # representara las transiciones de forma simple en un diccionoario con una tupla como clave y lista como valor (origen, simbolo) : [destinos]
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
    #print(f"Transiciones ep: {transiciones_ep}")
    mover = mover_A(simbolo, conjunto, transiciones)
    #print(f"Mover : {mover}")
    for estado in mover:
        resultado.update(cerraduraEpsilon(estado, transiciones_ep))
    
    return resultado
    
def obtenerEstadosFinalesDfa(estados_dfa, finales_nfa):
    finales_dfa = []
    for estado_dfa in estados_dfa:
        # vemos si algun elemento del conjunto de estados del dfa tiene un estado final del nfa
        if any(estado in finales_nfa for estado in estado_dfa):
            finales_dfa.append(frozenset(estado_dfa))
    return finales_dfa

def convertir(datos):
    alfabeto = datos["alfabeto"]
    e_inicial = datos["e_inicial"]
    finales_nfa = datos["e_finales"]
    transiciones = convertirTransiciones(datos)
    
    transiciones_epsilon = transicionesEpsilon(transiciones)
    cerradura_inicial = cerraduraEpsilon(e_inicial, transiciones_epsilon)
    print(transiciones_epsilon)
    
    print(f"\n\033[95mCerradura epsilon inicial: {cerradura_inicial} \033[0m\n")
    
    # lista para ir guardando los conjutnos nuevos
    estados_dfa = [cerradura_inicial]
    transiciones_dfa = {}
    
    i = 0
    while i < len(estados_dfa):
        
        estado_actual = estados_dfa[i]
        transiciones_dfa[frozenset(estado_actual)] = {}
        
        for simbolo in alfabeto:

            conjunto_siguiente = ir_A(simbolo, estado_actual, transiciones)
            if conjunto_siguiente:
                print(f"Operacion ir_A con simbolo {simbolo} y conjunto {estado_actual}: {conjunto_siguiente}")

            # si el conjunto es diferente a los anteriores lo guardamos como nuevo
            if not any(set(conjunto_siguiente) == set(e) for e in estados_dfa):
                estados_dfa.append(conjunto_siguiente)

            # agregamos la transicion
            # usamos frozenset para que el conjunto {edos nfa} pueda ser clave para el diccionario donde clave: (simbolo, {edos nfa}), valor {resultado ir_A}
            transiciones_dfa[frozenset(estado_actual)][simbolo] = frozenset(conjunto_siguiente)
        i += 1

    finales_dfa = obtenerEstadosFinalesDfa(estados_dfa, finales_nfa)

    estado_inicial_dfa = frozenset(cerradura_inicial)
    
    dfa = {
        "estado_inicial": estado_inicial_dfa,
        "estados": [frozenset(e) for e in estados_dfa],
        "transiciones": transiciones_dfa,
        "estados_finales": finales_dfa
    }
    return dfa

def leerArchivo(path: str):
    try:
        with open(path, 'r') as file:
            
            print("Archivo leido")
            datos = json.load(file)
            return datos
    except FileNotFoundError:
        raise FileNotFoundError("El archivo no existe")

# pasa del conjunto {} a nombres para los estados
def mapearEstados(estados):
    mapeo = {}
    contador = 0
    for estado in estados:
        if not estado:
            continue
        nombre = f"S{contador}"
        mapeo[frozenset(estado)] = nombre
        contador += 1
    return mapeo

def exportar_a_jflap(dfa, nombre_archivo="dfa.jff"):
    estados = dfa["estados"]
    transiciones = dfa["transiciones"]
    estado_inicial = dfa["estado_inicial"]
    finales = dfa["estados_finales"]

    mapeo = mapearEstados(estados)
    estados_mapeados = list(mapeo.keys())

    # coordenadas circulares para poner los estados
    def posiciones_circulares(n, radio=200, cx=300, cy=300):
        return [
            (cx + radio * math.cos(2 * math.pi * i / n),
             cy + radio * math.sin(2 * math.pi * i / n))
            for i in range(n)
        ]

    posiciones = posiciones_circulares(len(estados_mapeados))

    # estructura base del XML es decir el jff
    estructura = ET.Element("structure")
    tipo = ET.SubElement(estructura, "type")
    tipo.text = "fa"
    automata = ET.SubElement(estructura, "automaton")

    # crear estados
    for i, estado in enumerate(estados_mapeados):
        nombre = mapeo[estado]
        state = ET.SubElement(automata, "state", id=str(i), name=nombre)
        x, y = posiciones[i]
        ET.SubElement(state, "x").text = str(x)
        ET.SubElement(state, "y").text = str(y)

        if estado == frozenset(estado_inicial):
            ET.SubElement(state, "initial")
        if estado in finales:
            ET.SubElement(state, "final")

    # Crear transiciones
    for origen, trans in transiciones.items():
        if not origen:
            continue
        for simbolo, destino in trans.items():
            if not destino:
                continue
            t = ET.SubElement(automata, "transition")
            ET.SubElement(t, "from").text = str(estados_mapeados.index(frozenset(origen)))
            ET.SubElement(t, "to").text = str(estados_mapeados.index(frozenset(destino)))
            ET.SubElement(t, "read").text = simbolo

    # Guardar archivo
    tree = ET.ElementTree(estructura)
    tree.write(nombre_archivo, encoding="utf-8", xml_declaration=True)

    print(f"\n\033[92mDFA exportado como {nombre_archivo}\033[0m")


if __name__ == "__main__":
        
    print("####### Bienvenido ########")
    while 1:

        path = input("\n\033[94mIngresa el archivo de AFN: \033[0m")
        print(path)
        datos = None

        try:
            datos = leerArchivo(path)
        except FileNotFoundError as e:
            print(f"\033[91m{e}\033[0m\n")
            continue

        transiciones = convertirTransiciones(datos)
        
        for trans in datos["transiciones"]:
            simbolo = trans["simbolo"]
            origen = trans["origen"]
            destinos = trans["destino"]
            print(f"{origen} --{simbolo or 'ε'}--> {destinos}")

        dfa = convertir(datos)
        mapeo = mapearEstados(dfa["estados"])
        

        print("\033[95m\nEstado inicial: \033[0m")
        if dfa["estado_inicial"]:
            print(mapeo[dfa["estado_inicial"]])
        else:
            print("Estado inicial no definido o vacío.")

        
        print("\033[95mEstados: \033[0m")
        for estado in dfa["estados"]:
            if not estado:
                continue
            print(mapeo[estado])

        finales_legibles = [mapeo[e] for e in dfa["estados_finales"] if e and e in mapeo]
        print("\033[95mEstados finales: \033[0m", finales_legibles)


        print("\033[95mTransiciones: \033[0m")
        for origen, trans in dfa["transiciones"].items():
            if not origen:
                continue
            for simbolo, destino in trans.items():
                if not destino:
                    continue
                print(f"{mapeo[origen]} --{simbolo}--> {mapeo[destino]}")


        exportar_a_jflap(dfa, "dfa_convertido.jff")




