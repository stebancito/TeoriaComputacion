import os
import time

def guardar(lenguaje):
    resp = input("¿Quiere guardar el lenguaje generado en un archivo? (s/n): ").strip().lower()

    if resp == 's':
        try:
            path = input("Ingrese la ruta del archivo: ").strip()

            if not path:
                raise ValueError("La ruta del archivo no puede estar vacía.")

            with open(path, "a", encoding="utf-8") as archivo:
                archivo.write(" ".join(lenguaje))
            
            print(f"Datos guardados correctamente en '{path}'.")

        except FileNotFoundError:
            print("Error: No se encontró el archivo o la ruta es incorrecta.")
        except PermissionError:
            print("Error: No tienes permisos para escribir en este archivo.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
    else:
        print("Operación cancelada.")


class Lenguaje:

    def __init__(self):
        self.lenguajes = []

    def impresion_lenguajes(self):
        print("\n=== Lenguajes Disponibles ===")
        if self.lenguajes:
            for i, leng in enumerate(self.lenguajes, 1):
                print(f"{i}. {leng}")
        else:
            print("No hay lenguajes registrados.")

    def insertar_lenguaje(self):
        path = input("\nIntroduce la ruta del archivo: ")

        try:
            if not path:
                raise ValueError("La ruta del archivo no puede estar vacía.")
            with open(path, 'r') as file:
                leng = (file.read()).split()
                
        except FileNotFoundError:
            print(f"El archivo en la ruta {path} no se encuentra.")
        except IOError:
            print(f"No se pudo abrir el archivo en la ruta {path}.")

        self.lenguajes.append(leng)
        print(f"Lenguaje '{leng}' agregado con éxito.")

    def union_lenguajes(self):
        opciones = input("Escoja los lenguajes que desea unir separados por comas y sin espacios: ").split(",")
        lenguajesUnion = []

        lenguajesUnion = [palabra for op in opciones for palabra in self.lenguajes[int(op)-1]] #podemos usar extend()

        return lenguajesUnion

    def concatenacion_lenguajes(self):
        opciones = input("Escoja los lenguajes que desea concatenar separados por comas y sin espacios: ").split(",")
        resultado = [cadena1 + cadena2 for cadena1 in self.lenguajes[int(opciones[0]) - 1] for cadena2 in self.lenguajes[int(opciones[1]) - 1]]
        return resultado
    
    def potencia_lenguaje(self):
        op =int(input("\nSeleccione el lenguaje que quiere operar: "))
        potencia = int(input("Selecciona la potencia en un rango de -5 a 10: "))
        
        if potencia < -5 or potencia > 10:
            print("Potencia en rango no permitido")

        lenguajePotencia = self.lenguajes[op-1]
                    
        for _ in range(1, abs(potencia)):
            lenguajePotencia = [f"{cadena1}{cadena2}" for cadena1 in lenguajePotencia for cadena2 in self.lenguajes[op-1]]
        
        if potencia < 0:
            lenguajePotenciaInv = []
            for cadena in lenguajePotencia:
                lenguajePotenciaInv.append(cadena[::-1])

            lenguajePotencia = lenguajePotenciaInv
        
        return lenguajePotencia

    def cerradura_positiva(self):
        op = int(input("Seleccione el lenguaje que quiere operar: "))
        lenguajeBase = self.lenguajes[op - 1]
        resultado = lenguajeBase[:]
        
        for _ in range(3):  # Se repite hasta la cuarta potencia
            resultado.extend([s1 + s2 for s1 in resultado for s2 in lenguajeBase])
        
        return resultado

    def cerradura_kleene(self):
        op = int(input("Seleccione el lenguaje que quiere operar: "))
        lenguajeBase = self.lenguajes[op - 1]
        resultado = [""]  # Incluye la cadena vacía para la cerradura de Kleene
        
        for _ in range(4):  # Se repite hasta la cuarta potencia
            resultado.extend([s1 + s2 for s1 in resultado for s2 in lenguajeBase])
        
        return resultado

    def reflexion_lenguaje(self):
        op = input("\nSeleccione el lenguaje que quiere operar: ")

        lenguajereflexion = []
        for cadena in self.lenguajes[int(op) - 1]:
            lenguajereflexion.append(cadena[::-1])

        return lenguajereflexion

    def ejecutar_menu(self):
        opciones = {
            "1": self.insertar_lenguaje,
            "2": self.union_lenguajes,
            "3": self.concatenacion_lenguajes,
            "4": self.potencia_lenguaje,
            "5": self.cerradura_positiva,
            "6": self.cerradura_kleene,
            "7": self.reflexion_lenguaje
        }

        while True:
            self.impresion_lenguajes()
            print("\nMenú de Opciones:")
            print("1. Insertar lenguaje")
            print("2. Unión de lenguajes")
            print("3. Concatenación de lenguajes")
            print("4. Potencia de lenguaje")
            print("5. Cerradura positiva de lenguaje")
            print("6. Cerradura de Kleene")
            print("7. Reflexión de lenguaje")
            print("8. Salir")
            
            opcion = input("Seleccione una opción: ")

            match opcion:
                case "8":
                    print("Saliendo del programa...")
                    break
                case _ if opcion in opciones:
                    resultado = opciones[opcion]()  # Llama a la función correspondiente
                    if opcion != "1":
                        print("Resultado de la operacion: \n", resultado)
                        guardar(resultado)
                    
                    time.sleep(2)
                    os.system('clear') #CAMBIAR A CLS EN WINDOWS  
                case _:
                    print("Opción no válida, intenta de nuevo.")
            
            


lenguaje = Lenguaje()
lenguaje.ejecutar_menu()
