import flet as ft
import json
from visual_automata.fa.dfa import VisualDFA
import base64

transiciones_dfa = {}

# FUNCIONES LOGICAS AUTOMATA
def convertir_transiciones(lista_transiciones):

    if not lista_transiciones:
        print("No se han cargado datos del autómata.")
        return False
    
    transiciones_dfa = {}
    for trans in lista_transiciones:
        origen = trans["origen"]
        simbolo = trans["simbolo"]
        destino = trans["destino"]

        if origen not in transiciones_dfa:
            transiciones_dfa[origen] = {}
        transiciones_dfa[origen][simbolo] = destino

    print(transiciones_dfa)
    return transiciones_dfa

def procesar_cadena(datos, transiciones, cadena):
    
    estado_actual = datos['e_inicial']
    recorrido = [estado_actual]

    for simbolo in cadena:
        print(f"Procesando símbolo: {simbolo}")
        if simbolo not in datos['alfabeto']:
            print(f"Símbolo '{simbolo}' no pertenece al alfabeto.")
            return (False, "Simbolo no pertenece al alfabeto")

        transiciones_estado = transiciones.get(estado_actual)
        estado_actual = transiciones_estado.get(simbolo, estado_actual)

        recorrido.append(estado_actual)

    if estado_actual in datos['e_finales']:
        print("Cadena aceptada")
        return (True, recorrido)
    else:
        print("Cadena no aceptada")
        return (False, "Se llego a un estado no final")



#FUNCIONES DE INTERFAZ

def render_diagrama(dfa):
    graph = dfa.show_diagram(view=False)
    output_path = "dfa_diagrama"
    graph.format = "png"
    rendered_path = graph.render(filename=output_path, cleanup=True)
    return rendered_path


def crear_dfa(datos):
    transiciones = convertir_transiciones(datos["trancisiones"])
    dfa = VisualDFA(
        states=set(datos['estados']),
        input_symbols=set(datos['alfabeto']),
        transitions=transiciones,
        initial_state=datos['e_inicial'],
        final_states=set(datos['e_finales']),
    )
    return dfa


def crear_encabezado():
    return ft.Row(
        controls=[ft.Image(src="logoESCOM.png", width=200)],
        alignment=ft.MainAxisAlignment.CENTER
    )

def crar_resultado(valor):
    resultado = ft.Container(
        content=ft.Text(size=22, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD), 
        alignment=ft.alignment.center,
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREY_500),
        border_radius=8)
    
    if valor[0] == True:
        resultado.content.value = f"Cadena aceptada\nRecorrido: {' → '.join(valor[1])}"
        resultado.content.color = ft.Colors.GREEN_800
        
    else:   
        resultado.content.value = f"Cadena no aceptada\n{valor[1]}"
        resultado.content.color = ft.Colors.RED_800

    return resultado

def crear_alerta():
    return ft.Container(
        content=ft.Text("Nota: El archivo debe estar en formato JSON y contener los campos 'alfabeto', 'e_inicial', 'e_finales' y 'trancisiones'\n datos escenciales que representan al autómata.", size=16, color=ft.Colors.GREEN_ACCENT_700, italic=True),
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.1, ft.colors.GREEN),
        border_radius=8,
        alignment=ft.alignment.center
    )

#FUNCION MAIN

def main(page: ft.Page):
    page.bgcolor = "#F3F4F5"
    page.title = "Autómatas deterministas"

    imagen_dfa_container = ft.AnimatedSwitcher(
        content=ft.Container(),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=1000,
        switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
    )
    file_path = ft.Text(color=ft.Colors.RED)
    resultado_container = ft.Column()
    datos = None

    def actualizar_diagrama(datos):
        dfa = crear_dfa(datos)
        imagen_path = render_diagrama(dfa)

        # Convertir la imagen en base64
        with open(imagen_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        imagen = ft.Image(src_base64=img_base64, width=500)

        imagen_contenedor = ft.Container(
            content=imagen,
            bgcolor="#ffffff",
            padding=10,
            border_radius=30,
            alignment=ft.alignment.center,
        )

        imagen_dfa_container.content = imagen_contenedor
        page.update()

    def leerArchivo(path: str):

        nonlocal datos
        try:
            with open(path, 'r') as file:
                print("Archivo leido")
                datos = json.load(file)
                actualizar_diagrama(datos)
        except FileNotFoundError:
            print("El archivo no existe")

    def on_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path.value = e.files[0].name
            leerArchivo(e.files[0].path)
            page.update()
    
    cadena_input = ft.TextField(label="Cadena", autofocus=True, width=300, focus_color="BLACK", color="BLACK", border_color="BLACK", focused_border_color="BLACK", label_style=ft.TextStyle(color="BLACK"))

    def procesar():
        if datos:
            trans = convertir_transiciones(datos["trancisiones"])

            resultado = procesar_cadena(datos, trans, cadena_input.value)
            resultado_container.controls.clear()
            resultado_container.controls.append(crar_resultado(resultado))
            page.update()
        
        else:
            resultado_container.controls.clear()
            aux = ft.Container(
                content=ft.Text(size=22, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                padding=10,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_200),
                border_radius=8)
            aux.content.value = "No se han cargado datos del autómata."
            aux.content.color = ft.Colors.ORANGE
            resultado_container.controls.append(aux)
            page.update()
            
    file_picker = ft.FilePicker(on_result=on_result)
    page.overlay.append(file_picker)

    boton_seleccionar = ft.Row(
        controls=[
            ft.FilledButton("Seleccionar archivo", on_click=lambda _: file_picker.pick_files(allow_multiple=False),style=ft.ButtonStyle(bgcolor="#006BBB",color="white",overlay_color=ft.Colors.with_opacity(0.1, "BLACK"),animation_duration=300,elevation={"hovered": 30, "pressed": 0})),
            file_path
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    def limpiar_todo():
        cadena_input.value = ""
        resultado_container.controls.clear()
        imagen_dfa_container.content = ft.Container()
        file_path.value = ""
        nonlocal datos
        datos = None
        page.update()

    
    page.add(
        ft.Column(
            controls=[
                crear_encabezado(),
                ft.Container(
                    content=ft.Text("Autómatas deterministas", size=40, color="#006BBB", weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.center,
                ),
                # participantes(),
                ft.Text("Seleccione un archivo que contenga la descripción del autómata.", size=22, color="#006BBB"),
                crear_alerta(),
                boton_seleccionar,
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Cadena a procesar:", size=22, color=ft.Colors.BLACK),
                                cadena_input,
                                ft.Row(
                                    controls=[
                                        ft.Button(text="Procesar", on_click=lambda e: procesar(),style=ft.ButtonStyle(bgcolor="#006BBB",color="WHITE",overlay_color=ft.Colors.with_opacity(0.1, "BLACK"),animation_duration=300,elevation={"hovered": 30, "pressed": 0})),
                                        ft.Button(text="Limpiar todo", on_click=lambda e: limpiar_todo(), style=ft.ButtonStyle(bgcolor="RED", color="WHITE", overlay_color=ft.Colors.with_opacity(0.1, "BLACK"), animation_duration=300, elevation={"hovered": 30, "pressed": 0}))
                                    ],
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Text("Resultado:", size=22, color=ft.Colors.BLACK),
                                resultado_container,
                                imagen_dfa_container
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            scroll=ft.ScrollMode.ALWAYS,
            height=800
        )
    )

# def participantes():
#     return ft.Container(
#         content=ft.Column(
#             controls=[
#                 ft.Text("Participantes:", size=16, weight=ft.FontWeight.BOLD, color="white"),
#                 ft.Text("• Juan Esteban Rios Gomez", size=14, color="white"),
#                 ft.Text("• Pierre Augusto Pérez Pérez", size=14, color="white"),
#             ],
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             spacing=5
#         ),
#         padding=20,
#         alignment=ft.alignment.center
#     )


ft.app(target=main)

