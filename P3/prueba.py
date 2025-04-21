import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import re, urllib.request

class Urls:
    def __init__(self, urls = ()):
        if len(urls) != 3:
            raise ValueError("Debes proporcionar exactamente 3 URLs.")
        self.urls = urls
        self.htmls = {}

    def guardarEnArchivo(self, elementos, url, archivo):
        try:
            with open(archivo, "a") as file:
                file.write(f"\nRecuperado de {url}\n")
                for elemento in elementos:
                    file.write(f"{elemento}\n") 
        except Exception as e:
            print(f"Error al guardar en el archivo: {e}")

    def extraerHTML(self):
        for url in self.urls:
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    self.htmls[url] = response.read().decode("utf-8", errors="ignore")
            except Exception as e:
                print(f" Error al acceder a la URL {url}: {e}")
                self.htmls[url] = None

    def obtenerCorreos(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
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
                    print(f"\nNo se encontraron correos electrónicos en {url}.")
            else:
                print(f"No se pudo obtener HTML de {url}.")

    def obtenerLinks(self):
        if not self.htmls:
            self.extraerHTML()
        
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not archivo:
            return
        
        for url, html in self.htmls.items():
            if html:
                re_enlace = r'href=["\'](https?://[^\s"\']+)["\']'
                links = set(re.findall(re_enlace, html))
                if links:
                    self.guardarEnArchivo(links, url, archivo)
                else:
                    print(f"\nNo se encontraron enlaces en {url}.")
            else:
                print(f"No se pudo obtener HTML de {url}.")

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de Correos y Links")
        self.root.geometry("500x300")

        self.url_entry1 = tk.Entry(root, width=40)
        self.url_entry1.pack(pady=5)
        self.url_entry1.insert(0, "Introduce la URL 1")

        self.url_entry2 = tk.Entry(root, width=40)
        self.url_entry2.pack(pady=5)
        self.url_entry2.insert(0, "Introduce la URL 2")

        self.url_entry3 = tk.Entry(root, width=40)
        self.url_entry3.pack(pady=5)
        self.url_entry3.insert(0, "Introduce la URL 3")

        self.button = tk.Button(root, text="Ejecutar", command=self.ejecutar)
        self.button.pack(pady=20)

    def ejecutar(self):
        urls = (self.url_entry1.get(), self.url_entry2.get(), self.url_entry3.get())
        urls_obj = Urls(urls)

        urls_obj.obtenerCorreos()
        urls_obj.obtenerLinks()
        messagebox.showinfo("Éxito", "Proceso completado")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
