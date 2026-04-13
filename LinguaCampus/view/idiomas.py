# view/idiomas.py
# Interfaz grafica para el modulo de Idiomas, permite crear, editar y eliminar idiomas del sistema.

import tkinter as tk
from controller.idiomas import (
    ctrl_obtener_idiomas,
    ctrl_guardar_idioma,
    ctrl_eliminar_idioma
)
from view.utils import (
    crear_ventana, crear_frame_formulario, crear_frame_botones,
    agregar_boton, crear_treeview, llenar_treeview, crear_label,
    crear_entry, mensaje_ok, mensaje_error, mensaje_advertencia, confirmar
)


def show_idiomas(): # Abre la ventana del modulo de Idiomas.

    ventana = crear_ventana("Gestion de Idiomas", ancho=550, alto=480)

    # Variable para guardar el ID del registro seleccionado
    id_seleccionado = [None]

    # ── Titulo
    tk.Label(ventana, text="Modulo de Idiomas",
             font=("Arial", 13, "bold")).pack(pady=(10, 2))
    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=10)

    # ── Formulario
    frame_form = crear_frame_formulario(ventana, " Datos del Idioma ")

    crear_label(frame_form, "Nombre del Idioma:").grid(
        row=0, column=0, sticky="w", pady=6, padx=4)
    ent_nombre = crear_entry(frame_form, width=30)
    ent_nombre.grid(row=0, column=1, pady=6, padx=8)

    # ── Botones de accion
    frame_btn = crear_frame_botones(ventana)

    def limpiar(): # Limpia el formulario y deselecciona la tabla.
        id_seleccionado[0] = None
        ent_nombre.delete(0, "end")
        tv.selection_remove(tv.selection())

    def guardar(): # Valida y guarda (insertar o actualizar) el idioma.
        try:
            ctrl_guardar_idioma(ent_nombre.get(), id_seleccionado[0])
            mensaje_ok("Idioma guardado correctamente.")
            limpiar()
            cargar_tabla()
        except Exception as e:
            mensaje_error(str(e))

    def eliminar(): # Solicita confirmacion y elimina el dioma seleccionado.
        if not id_seleccionado[0]:
            mensaje_advertencia("Seleccione un idioma de la tabla primero.")
            return
        if not confirmar("eliminar este idioma"):
            return
        try:
            ctrl_eliminar_idioma(id_seleccionado[0])
            mensaje_ok("Idioma eliminado.")
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
        columnas=["id", "nombre"],
        encabezados=["ID", "Nombre del Idioma"],
        anchos=[60, 350]
    )

    def on_seleccionar(event): # Carga los datos del registro seleccionado en el formulario.
        seleccion = tv.selection()
        if not seleccion:
            return
        fila = tv.item(seleccion[0], "values")
        id_seleccionado[0] = int(fila[0])
        ent_nombre.delete(0, "end")
        ent_nombre.insert(0, fila[1])

    tv.bind("<<TreeviewSelect>>", on_seleccionar)

    def cargar_tabla(): # Consulta el contralador y actualiza el Treeview.
        datos = ctrl_obtener_idiomas()
        llenar_treeview(tv, datos, ["id", "nombre_idioma"])

    cargar_tabla()
