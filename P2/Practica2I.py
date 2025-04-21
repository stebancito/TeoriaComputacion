
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, PhotoImage

class LenguajeInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Operaciones con Lenguajes")
        self.root.geometry("400x610")
        self.lenguajes = []

        tk.Label(root, text="Menú de Opciones", font=("Ghotam", 14)).pack(pady=10)
        
        opciones = [
            ("Insertar Lenguaje", self.insertar_lenguaje),
            ("Unión de Lenguajes", self.union_lenguajes),
            ("Concatenación", self.concatenacion_lenguajes),
            ("Potencia", self.potencia_lenguaje),
            ("Cerradura Positiva", self.cerradura_positiva),
            ("Cerradura de Kleene", self.cerradura_kleene),
            ("Reflexión", self.reflexion_lenguaje),
            ("Ver Lenguajes", self.abrir_ventana_lenguajes)
        ]

        # genera botones depende de la opcion
        for texto, comando in opciones:
            tk.Button(root, text=texto, command=comando, width=30).pack(pady=5)

        tk.Button(root, text="Salir", width=10, command=quit, fg="red").pack(pady=10)

    def mostrar_resultado(self, resultado):
        #generamos nueva ventana
        ventana = tk.Toplevel(self.root)
        ventana.title("Resultado")
        ventana.geometry("1000x500")
        
        text_area = scrolledtext.ScrolledText(ventana, width=120, height=20, state='disabled')
        text_area.pack(pady=10)
        text_area.configure(state='normal')
        text_area.insert(tk.END, ", ".join(resultado))
        text_area.configure(state='disabled')
        
        def guardar():
            # generamos dialogo de archivo
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if path:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(" ".join(resultado))
                messagebox.showinfo("Éxito", f"Datos guardados en {path}")
        
        tk.Button(ventana, text="Guardar", command=guardar, fg="green").pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(ventana, text="Regresar", command=ventana.destroy).pack(side=tk.RIGHT, padx=20, pady=10)
    
    def seleccionar_lenguajes(self):
        if not self.lenguajes:
            messagebox.showwarning("Advertencia", "No hay lenguajes cargados.")
            return []
        seleccion = simpledialog.askstring("Seleccionar Lenguajes", "Escriba los números de los lenguajes separados por comas:\n")
        if seleccion:
            try:
                # convierte los numeros que ingresan en una lista de indices, separando por comas, quitando posibles espacios y conviertiendo cada elemento a numero
                indices = [int(i.strip()) - 1 for i in seleccion.split(",")]
                return [self.lenguajes[i] for i in indices] # devuelve una lista de los lenguajes 
            except:
                messagebox.showerror("Error", "Selección inválida.")
        return []
    
    def abrir_ventana_lenguajes(self):
        ventana_lenguajes = tk.Toplevel(self.root)
        ventana_lenguajes.title("Lenguajes Disponibles")
        ventana_lenguajes.geometry("800x800")
        
        frame = tk.Frame(ventana_lenguajes)
        frame.pack(pady=10)
        
        textbox = tk.Text(frame, height=90, width=90)
        scrollbar = tk.Scrollbar(frame, command=textbox.yview)
        textbox.config(yscrollcommand=scrollbar.set)
        
        textbox.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if not self.lenguajes:
            textbox.insert(tk.END, "No hay lenguajes cargados.\n")
        else:
            for i, l in enumerate(self.lenguajes):
                textbox.insert(tk.END, f"{i+1}. {', '.join(l)}\n")
        
        textbox.config(state=tk.DISABLED)

    def insertar_lenguaje(self):
        # abrir dialogo de archivos
        path = filedialog.askopenfilename()
        if path:
            try:
                with open(path, 'r') as file:
                    leng = file.read().split() # convierte cada cadena separada por espacio en un elemento de una lista
                self.lenguajes.append(leng)
                self.mostrar_resultado(leng)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def union_lenguajes(self):
        seleccionados = self.seleccionar_lenguajes()
        if seleccionados:
            # convertimos a conjunto para usar metodo union
            resultado = list(set().union(*seleccionados)) # * hace que loa que esta en las listas se vuelvan argumentos de la lista principal
            self.mostrar_resultado(resultado)

    def concatenacion_lenguajes(self):
        seleccionados = self.seleccionar_lenguajes()
        if len(seleccionados) == 2:
            resultado = [c1 + c2 for c1 in seleccionados[0] for c2 in seleccionados[1]]
            self.mostrar_resultado(resultado)

    def potencia_lenguaje(self):
        seleccionados = self.seleccionar_lenguajes()
        if seleccionados:
            lenguaje_base = set(seleccionados[0])
            
            potencia = simpledialog.askinteger("Potencia", "Ingrese la potencia (-5 a 10):", minvalue=-5, maxvalue=10)
            if potencia is None:
                return

            if potencia == 0:
                resultado = [""]
            elif potencia < 0:
                lenguaje_base = {palabra[::-1] for palabra in lenguaje_base}  # invertimos cadenas
                potencia = abs(potencia)
                resultado = list(lenguaje_base) if potencia == 1 else self.calcular_potencia(lenguaje_base, potencia)
            else:
                resultado = list(lenguaje_base) if potencia == 1 else self.calcular_potencia(lenguaje_base, potencia)

            self.mostrar_resultado(sorted(resultado))

    def calcular_potencia(self, lenguaje_base, potencia):
        resultado = lenguaje_base
        for _ in range(potencia - 1):  
            resultado = {c1 + c2 for c1 in resultado for c2 in lenguaje_base}
        return resultado


    def cerradura_positiva(self):
        seleccionados = self.seleccionar_lenguajes()
        if seleccionados:
            lenguaje_base = set(seleccionados[0])
            resultado = lenguaje_base.copy()

            for _ in range(3): 
                nuevo = set(c1 + c2 for c1 in resultado for c2 in lenguaje_base)
                resultado.update(nuevo) 

            self.mostrar_resultado(sorted(resultado))

    def cerradura_kleene(self):
        seleccionados = self.seleccionar_lenguajes()
        if seleccionados:
            lenguaje_base = set(seleccionados[0])
            resultado = {""} | lenguaje_base
            
            for _ in range(3): 
                nuevo = set(c1 + c2 for c1 in resultado for c2 in lenguaje_base)
                resultado.update(nuevo)

            self.mostrar_resultado(sorted(resultado))

    
    def reflexion_lenguaje(self):
        seleccionados = self.seleccionar_lenguajes()
        if seleccionados:
            resultado = [x[::-1] for x in seleccionados[0]]
            self.mostrar_resultado(resultado)

if __name__ == "__main__":
    root = tk.Tk()

    imagen_fondo = PhotoImage(file="logoESCOM2x.png").subsample(2)

    fondo = tk.Label(root, image=imagen_fondo)
    fondo.pack(side="top")

    tk.Label(root, text="© Todos los derechos reservados.", font=("Arial", 9)).pack(side="bottom", pady=3)
    tk.Label(root, text="Pérez Pérez Pierre", font=("Arial", 10)).pack(side="bottom")
    tk.Label(root, text="Rios Gomez Juan Esteban", font=("Arial", 10)).pack(side="bottom")
    inteerfaz = LenguajeInterfaz(root)
    root.mainloop()
