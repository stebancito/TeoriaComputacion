import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, PhotoImage
import re, urllib.request

class Urls:
    def __init__(self, urls = ()):
        if len(urls) != 3:
            raise ValueError("Debes proporcionar exactamente 3 URLs.")
        self.urls = urls
        self.htmls = {}

    def guardarEnArchivo(self, elementos, url, archivo):
        with open(archivo, "a") as file:
            file.write(f"\nRecuperado de {url}\n")
            for elemento in elementos:
                file.write(f"{elemento}\n") 

    def extraerHTML(self):
        for url in self.urls:
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    self.htmls[url] = response.read().decode("utf-8", errors="ignore")
            except Exception as e:
                print(f" Error al acceder a la URL: {e}")
                self.htmls[url] = None

    def obtenerCorreos(self):
        archivo = input('Nombre del archivo a guardar: ').strip()
        archivo = archivo+'.txt'

        self.extraerHTML()
        # por cada url buscar correos
        for url in self.htmls:
            html = self.htmls[url]
            if html:
                patron_correo = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                correos = set(re.findall(patron_correo, html))
                if correos:
                    self.guardarEnArchivo(correos, url, archivo)
                else:
                    print("\nNo se encontraron correos electrónicos.")
            else:
                print("No esta definido el html")

    def obtenerLinks(self):
        if not self.htmls:
            self.extraerHTML()

        archivo = input('Nombra al archivo resultante: ').strip()
        archivo = archivo + '.txt'
        # por cada url buscar links
        for url in self.htmls:
            html = self.htmls[url]
            if html:
                patron_enlace = r'href=["\'](https?://[^\s"\']+)["\']'
                links = set(re.findall(patron_enlace, html))
                if links:
                    self.guardarEnArchivo(links, url, archivo)
                else:
                    print("\nNo se encontraron correos electrónicos.")
            else:
                print("No esta definido el html")



if __name__ == "__main__":


    url = input("Introduce la URL: ") 
    url2 = input("introduce otra url: ")
    url3 = input("introduce otra url: ")
    urls = (url, url2, url3)

    urls1 = Urls(urls)
    urls1.obtenerCorreos()
    urls1.obtenerLinks()

