from tarea import Tarea as T
from rich.console import Console
from rich.text import Text
from rich.table import Table
from datetime import datetime
import json
import os
from enum import Enum

tareas_array = []
console = Console()

class EstadoTarea(Enum):
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En Progreso"
    COMPLETADA = "Completada"

def menu_principal():
    texto = Text("==Bienvenido al gestor de tareas==\n", style="white")
    texto.append(Text("1) ", style="red"))
    texto.append(Text("Agregar tarea\n", style="white"))
    texto.append(Text("2) ", style="red"))
    texto.append(Text("Mostrar tareas\n", style="white"))
    texto.append(Text("3) ", style="red"))
    texto.append(Text("Actualizar estado\n", style="white"))
    texto.append(Text("4) ", style="red"))
    texto.append(Text("Eliminar tarea\n", style="white"))
    texto.append(Text("5) ", style="red"))
    texto.append(Text("Salir\n\n", style="white")) 
    console.print(texto)
    
    while True:
        try:
            opcion = int(input(Text("Selecciona una opcion: ", style="white")))
        except ValueError:
            console.print("Ingrese una opcion valida.", style="red")
        else:
            break
                    
    match opcion:
        case 1:
            AgregarTarea()
        case 2:
            mostrar_tareas()
        case 3:
            actualizar_estado()
        case 4:
            eliminar_tarea()
        case 5:
            return True
        case _:
            console.print("")

def cargar_datos():
    global tareas_array
    if os.path.exists("tareaLista.json"):
        with open("tareaLista.json", "r", encoding="utf-8") as f:
            try:
                tareas_dict = json.load(f)
                tareas_array = [T(**t) for t in tareas_dict]
            except json.JSONDecodeError:
                tareas_array = []
    else:
        tareas_array = []

def AgregarTarea():
    texto = (Text("1) ", style="red"))
    texto.append(Text("Agregar tarea\n", style="white")) 
    console.print(texto)
    tarea_nombre = input("Ingrese el nombre de la nueva tarea: ")
    tarea_descripcion = input("Ingrese la descripcion: ")  
    tarea = T(generar_id(), tarea_nombre, tarea_descripcion, EstadoTarea.PENDIENTE.value, str(datetime.today().strftime('%Y-%m-%d')))
    tareas_array.append(tarea)
    
    with open("tareaLista.json", "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tareas_array], f, indent=4, ensure_ascii=False)

    cargar_datos()
    console.print(Text("Tarea Agregada Correctamente.", style="green"))

def mostrar_tareas():
    table = Table(title="Lista de Tareas")
    table.add_column("ID", style="white")
    table.add_column("Nombre", style="white")
    table.add_column("Estado", style="white")
    table.add_column("Fecha", style="white")

    for tar in tareas_array:
        table.add_row(str(tar.id), tar.nombre, tar.estado, tar.fechaInicio)

    console.print(table)
def generar_id():
    if tareas_array:
        return max(tar.id for tar in tareas_array) + 1
    return 1
        
def actualizar_estado():
    texto = (Text("3) ", style="red"))
    texto.append(Text("Actualizar tarea\n", style="white"))
    console.print(texto)
    while True:
        try:
            t_id = int(input("Ingresa la ID de la tarea que deseas modificar: "))
        except ValueError:
            console.print("Ingrese una opcion valida.", style="red")
        else:
            if any(tar.id == t_id for tar in tareas_array):
                break
            else:
                console.print("Ingrese una opcion valida.", style="red")                
    while True:
        try:
            nuevo_status = int(input("1)Pendiente\n2)En Progreso\n3)Completada\nSeleccione la opcion del nuevo estado: "))
        except ValueError:
            console.print("Ingrese una opcion valida.", style="red")
        else:
            if nuevo_status > 0 and nuevo_status <= 3:
                break
            else:
                console.print("Ingrese una opcion valida.", style="red")       
    
    tarea = next((tar for tar in tareas_array if tar.id == t_id), None) 
    if tarea:
        match nuevo_status:
            case 1:
                tarea.estado = EstadoTarea.PENDIENTE.value
            case 2:
                tarea.estado = EstadoTarea.EN_PROGRESO.value
            case 3:
                tarea.estado = EstadoTarea.COMPLETADA.value
            
    with open("tareaLista.json", "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tareas_array], f, indent=4, ensure_ascii=False)        
    
    console.print("Tarea Actualizada Correctamente.", style="green")
    
def eliminar_tarea():
    while True:
        try:
            t_id = int(input("Ingresa la ID de la tarea que deseas eliminar: "))
        except ValueError:
            console.print("Ingrese una opcion valida.", style="red")
        else:
            if any(tar.id == t_id for tar in tareas_array):
                break
            else:
                console.print("Ingrese una opcion valida.", style="red")   

    tarea = next((tar for tar in tareas_array if tar.id == t_id), None) 
                        
    while True:
        try:
            confirmacion = int(input(f"Seguro que deseas eliminar la tarea '{tarea.nombre}'\n1)Confirmar 2)Cancelar \n"))
        except ValueError:
            console.print("Ingrese una opcion valida.", style="red")
        else:
            if confirmacion in (1, 2):
                break
            else:
                console.print("Ingrese una opcion valida.", style="red")   

    if confirmacion == 1:
        tareas_array.remove(tarea) 
        console.print("Tarea Eliminada.", style="red")
        with open("tareaLista.json", "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tareas_array], f, indent=4, ensure_ascii=False)
    elif confirmacion == 2:
        console.print("Operación cancelada.", style="yellow")   
    
cargar_datos()

while True:        
    if menu_principal():
        console.print("Hasta la proxima.", style="green")
        break
