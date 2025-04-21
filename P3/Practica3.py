import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import re, urllib.request, urllib.error

class Urls:
    def __init__(self, urls):
        if len(urls) != 3 or any(not url.strip() for url in urls):
            raise ValueError("Debes proporcionar exactamente 3 URLs válidas.")
        self.urls = urls
        self.htmls = {}

    def guardarEnArchivo(self, elementos, url, archivo):
        try:
            with open(archivo, "a", encoding="utf-8") as file:
                file.write(f"\nRecuperado de {url}\n")
                for elemento in elementos:
                    file.write(f"{elemento}\n") 
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar en el archivo: {e}")

    def extraerHTML(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        for url in self.urls:
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    self.htmls[url] = response.read().decode("utf-8", errors="ignore")
            except urllib.error.HTTPError as e:
                messagebox.showwarning("Advertencia", f"Error HTTP {e.code} en {url}")
                self.htmls[url] = None
            except urllib.error.URLError as e:
                messagebox.showwarning("Advertencia", f"No se pudo acceder a {url}: {e.reason}")
                self.htmls[url] = None
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado en {url}: {e}")
                self.htmls[url] = None

    def obtenerCorreos(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if not archivo:
            return
        self.extraerHTML()
        
        for url, html in self.htmls.items():
            if html:
                re_correo = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                correos = set(re.findall(re_correo, html))
                if correos:
                    self.guardarEnArchivo(correos, url, archivo)
                else:
                    messagebox.showinfo("Información", f"No se encontraron correos en {url}.")

    def obtenerLinks(self):
        if not self.htmls:
            self.extraerHTML()
        
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if not archivo:
            return
        
        for url, html in self.htmls.items():
            if html:
                re_enlace = r'href=["\'](https?://[^\s"\']+)["\']'
                links = set(re.findall(re_enlace, html))
                if links:
                    self.guardarEnArchivo(links, url, archivo)
                else:
                    messagebox.showinfo("Información", f"No se encontraron enlaces en {url}.")

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de Correos y Links")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        tk.Label(root, text="Introduce 3 URLs en los campos", font=("Arial", 12)).pack(pady=10)

        self.url_entries = []
        for i in range(3):
            entry = tk.Entry(root, width=50)
            entry.pack(pady=5)
            self.url_entries.append(entry)
        
        tk.Label(root, text="Espere 10 segundos después de dar ejecutar y guardar archivo!", font=("Arial", 12), fg="#216c07").pack(pady=5)

        self.boton_ejecutar = tk.Button(root, text="Ejecutar", command=self.ejecutar, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.boton_ejecutar.pack(pady=20)
        self.boton_salir = tk.Button(root, text="Salir", command=quit, bg="#EB3913", fg="white", font=("Arial", 10, "bold"))
        self.boton_salir.pack()
        

    def ejecutar(self):
        urls = tuple(entry.get().strip() for entry in self.url_entries)
        
        if any(not url for url in urls):
            messagebox.showerror("Error", "Todas las URLs deben estar completas.")
            return
        
        try:
            urls_obj = Urls(urls)
            urls_obj.obtenerCorreos()
            urls_obj.obtenerLinks()
            messagebox.showinfo("Éxito", "Proceso completado con éxito.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

if __name__ == "__main__":
    root = tk.Tk()

    imagen_fondo = PhotoImage(file="logoESCOM2x.png").subsample(2)

    fondo = tk.Label(root, image=imagen_fondo)
    fondo.pack(side="top")

    tk.Label(root, text="© Todos los derechos reservados.", font=("Arial", 9)).pack(side="bottom", pady=3)
    tk.Label(root, text="Rios Gomez Juan Esteban", font=("Arial", 10)).pack(side="bottom")
    tk.Label(root, text="Pérez Pérez Pierre", font=("Arial", 10)).pack(side="bottom")

    app = Interfaz(root)
    root.mainloop()
