# view/utils.py
# Funciones auxiliares compartidas por todos los modulos de vista.
# Contiene helpers para crear widgets, tablas y mensajes.

import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# FUNCIONES DE MENSAJES
# ============================================================

def mensaje_ok(texto): # Muestra un cuadro de dialogo de exito.
    messagebox.showinfo("Exito", texto)


def mensaje_error(texto): # Muestra un cuadro de dialogo de error.
    messagebox.showerror("Error", texto)


def mensaje_advertencia(texto): # Muestra un cuadro de dialogo de advertencia.
    messagebox.showwarning("Advertencia", texto)


def confirmar(accion="eliminar este registro"):
    """
    Muestra un cuadro de confirmacion antes de una accion critica.
    Retorna True si el usuario confirma, False si cancela.
    """
    return messagebox.askyesno("Confirmar", f"Esta seguro de {accion}?")


# ============================================================
# FUNCIONES DE WIDGETS
# ============================================================

def crear_entry(parent, width=30): # Crea y retorna un campo de texto Entry estandar.
    entry = tk.Entry(parent, width=width, font=("Arial", 10))
    return entry


def crear_combobox(parent, valores, width=27):
    """
    Crea y retorna un Combobox de solo lectura con los valores dados.
    Se usa para todas las llaves foraneas del sistema.
    """
    combo = ttk.Combobox(parent, values=valores, width=width,
                         font=("Arial", 10), state="readonly")
    return combo


def crear_label(parent, texto): # Crea y retorna un Label estandar.
    return tk.Label(parent, text=texto, font=("Arial", 10), anchor="w")


# ============================================================
# TREEVIEW
# ============================================================

def crear_treeview(parent, columnas, encabezados, anchos=None):
    """
    Crea un Treeview con scrollbar vertical y horizontal.
    - columnas: lista de nombres internos de columnas
    - encabezados: lista de textos visibles en la cabecera
    - anchos: lista opcional de anchos por columna (en pixeles)
    Retorna el widget Treeview listo para usar.
    """
    # Frame contenedor para el treeview y los scrollbars
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Scrollbars
    scroll_y = ttk.Scrollbar(frame, orient="vertical")
    scroll_x = ttk.Scrollbar(frame, orient="horizontal")

    # Crear el Treeview
    tv = ttk.Treeview(
        frame,
        columns=columnas,
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
        selectmode="browse"
    )

    # Configurar scrollbars
    scroll_y.config(command=tv.yview)
    scroll_x.config(command=tv.xview)

    # Colocar widgets en la grilla del frame
    tv.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Configurar columnas y encabezados
    for i, (col, enc) in enumerate(zip(columnas, encabezados)):
        tv.heading(col, text=enc, anchor="center")
        ancho = anchos[i] if anchos else 120
        tv.column(col, width=ancho, anchor="center")

    return tv


def llenar_treeview(tv, filas, claves):
    """
    Limpia el Treeview y lo rellena con las filas dadas.
    - filas: lista de diccionarios (resultado de la BD)
    - claves: lista de keys del diccionario a mostrar en cada columna
    """
    # Limpiar registros anteriores
    tv.delete(*tv.get_children())

    # Insertar cada fila
    for fila in filas:
        valores = [fila.get(clave, "") for clave in claves]
        tv.insert("", "end", values=valores)


# ============================================================
# VENTANA DE MODULO
# ============================================================

def crear_ventana(titulo, ancho=950, alto=620):
    """
    Crea y retorna una ventana Toplevel con titulo y tamano dados.
    Usa grab_set para bloquear la ventana principal mientras esta abierta.
    """
    ventana = tk.Toplevel()
    ventana.title(titulo)
    ventana.geometry(f"{ancho}x{alto}")
    ventana.grab_set()
    return ventana


def crear_frame_formulario(parent, titulo):
    """
    Crea un LabelFrame que agrupa los campos del formulario.
    Retorna el frame listo para agregar widgets.
    """
    frame = tk.LabelFrame(parent, text=titulo, font=("Arial", 10, "bold"),
                          padx=10, pady=8)
    frame.pack(fill="x", padx=10, pady=(10, 4))
    return frame


def crear_frame_botones(parent):
    """
    Crea un Frame horizontal para los botones de accion (Nuevo, Guardar, Eliminar).
    Retorna el frame listo para agregar botones.
    """
    frame = tk.Frame(parent)
    frame.pack(pady=6)
    return frame


def agregar_boton(frame, texto, comando):
    """Crea y empaqueta un boton estandar dentro de un frame."""
    btn = tk.Button(frame, text=texto, command=comando,
                    font=("Arial", 10), width=14, pady=4)
    btn.pack(side="left", padx=6)
    return btn
