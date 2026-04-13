# view/estudiantes.py
# Interfaz grafica para el modulo de Estudiantes.
# Usa Combobox para el campo estado.

import tkinter as tk
from controller.estudiantes import (
    ctrl_obtener_estudiantes,
    ctrl_guardar_estudiante,
    ctrl_eliminar_estudiante
)
from view.utils import (
    crear_ventana, crear_frame_formulario, crear_frame_botones,
    agregar_boton, crear_treeview, llenar_treeview, crear_label,
    crear_entry, crear_combobox, mensaje_ok, mensaje_error,
    mensaje_advertencia, confirmar
)


def show_estudiantes(): # Abre la ventana del modulo de estudiantes.

    ventana = crear_ventana("Gestion de Estudiantes", ancho=800, alto=520)

    # Variable para guardar el ID del registro seleccionado
    id_seleccionado = [None]

    # ── Titulo
    tk.Label(ventana, text="Modulo de Estudiantes",
             font=("Arial", 13, "bold")).pack(pady=(10, 2))
    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=10)

    # ── Formulario
    frame_form = crear_frame_formulario(ventana, " Datos del Estudiante ")

    # Fila 0: nombre y email
    crear_label(frame_form, "Nombre:").grid(
        row=0, column=0, sticky="w", pady=5, padx=4)
    ent_nombre = crear_entry(frame_form, width=28)
    ent_nombre.grid(row=0, column=1, pady=5, padx=8)

    crear_label(frame_form, "Email:").grid(
        row=0, column=2, sticky="w", pady=5, padx=4)
    ent_email = crear_entry(frame_form, width=28)
    ent_email.grid(row=0, column=3, pady=5, padx=8)

    # Fila 1: estado
    crear_label(frame_form, "Estado:").grid(
        row=1, column=0, sticky="w", pady=5, padx=4)
    # Combobox estado
    cb_estado = crear_combobox(frame_form, ["activo", "inactivo"], width=15)
    cb_estado.set("activo")
    cb_estado.grid(row=1, column=1, pady=5, padx=8, sticky="w")

    # ── Botones
    frame_btn = crear_frame_botones(ventana)

    def limpiar():
        id_seleccionado[0] = None
        ent_nombre.delete(0, "end")
        ent_email.delete(0, "end")
        cb_estado.set("activo")
        tv.selection_remove(tv.selection())

    def guardar():
        try:
            ctrl_guardar_estudiante(
                ent_nombre.get(),
                ent_email.get(),
                cb_estado.get(),
                id_seleccionado[0]
            )
            mensaje_ok("Estudiante guardado correctamente.")
            limpiar()
            cargar_tabla()
        except Exception as e:
            mensaje_error(str(e))

    def eliminar():
        if not id_seleccionado[0]:
            mensaje_advertencia("Seleccione un estudiante de la tabla primero.")
            return
        if not confirmar("eliminar este estudiante"):
            return
        try:
            ctrl_eliminar_estudiante(id_seleccionado[0])
            mensaje_ok("Estudiante eliminado.")
            limpiar()
            cargar_tabla()
        except Exception as e:
            mensaje_error(str(e))

    agregar_boton(frame_btn, "Nuevo",    limpiar)
    agregar_boton(frame_btn, "Guardar",  guardar)
    agregar_boton(frame_btn, "Eliminar", eliminar)

    # ── Treeview
    tv = crear_treeview(
        ventana,
        columnas=["id", "nombre", "email", "estado"],
        encabezados=["ID", "Nombre", "Email", "Estado"],
        anchos=[50, 210, 250, 90]
    )

    def on_seleccionar(event): # Carga los datos del esrudiante seleccionado en el formulario.
        seleccion = tv.selection()
        if not seleccion:
            return
        fila = tv.item(seleccion[0], "values")
        id_seleccionado[0] = int(fila[0])
        ent_nombre.delete(0, "end")
        ent_nombre.insert(0, fila[1])
        ent_email.delete(0, "end")
        ent_email.insert(0, fila[2])
        cb_estado.set(fila[3])

    tv.bind("<<TreeviewSelect>>", on_seleccionar)

    def cargar_tabla():
        datos = ctrl_obtener_estudiantes()
        llenar_treeview(tv, datos, ["id", "nombre", "email", "estado"])

    cargar_tabla()
