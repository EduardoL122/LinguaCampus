# view/niveles.py
# Interfaz grafica para el modulo de Niveles.
# Usa Combobox para seleccionar el idioma (llave foranea).

import tkinter as tk
from controller.niveles import (
    ctrl_obtener_niveles,
    ctrl_guardar_nivel,
    ctrl_eliminar_nivel
)
from controller.idiomas import ctrl_obtener_idiomas
from view.utils import (
    crear_ventana, crear_frame_formulario, crear_frame_botones,
    agregar_boton, crear_treeview, llenar_treeview, crear_label,
    crear_combobox, mensaje_ok, mensaje_error, mensaje_advertencia, confirmar
)


def show_niveles(): # Abre la ventana del modulo de niveles.

    ventana = crear_ventana("Gestion de Niveles", ancho=680, alto=500)

    # Variable para guardar el ID del registro seleccionado
    id_seleccionado = [None]

    # ── Titulo
    tk.Label(ventana, text="Modulo de Niveles",
             font=("Arial", 13, "bold")).pack(pady=(10, 2))
    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=10)

    # ── Cargar idiomas para el Combobox (llave foranea idioma_id)
    idiomas = ctrl_obtener_idiomas()
    # Mapa nombre -> id para recuperar el ID al guardar
    mapa_idiomas = {i["nombre_idioma"]: i["id"] for i in idiomas}
    lista_idiomas = ["(Sin idioma)"] + list(mapa_idiomas.keys())

    # ── Formulario
    frame_form = crear_frame_formulario(ventana, " Datos del Nivel ")

    # Combobox para el nombre del nivel (valores estandar MCER)
    crear_label(frame_form, "Nivel:").grid(
        row=0, column=0, sticky="w", pady=6, padx=4)
    cb_nombre = crear_combobox(frame_form, ["A1", "A2", "B1", "B2", "C1", "C2"], width=10)
    cb_nombre.grid(row=0, column=1, pady=6, padx=8, sticky="w")

    # Combobox para el idioma (llave foranea)
    crear_label(frame_form, "Idioma:").grid(
        row=0, column=2, sticky="w", pady=6, padx=4)
    cb_idioma = crear_combobox(frame_form, lista_idiomas, width=22)
    cb_idioma.set("(Sin idioma)")
    cb_idioma.grid(row=0, column=3, pady=6, padx=8)

    # ── Botones
    frame_btn = crear_frame_botones(ventana)

    def limpiar():
        id_seleccionado[0] = None
        cb_nombre.set("")
        cb_idioma.set("(Sin idioma)")
        tv.selection_remove(tv.selection())

    def guardar(): # Obtener el ID del idioma a partir del nombre seleccionado en el Combobox.
        
        sel_idioma = cb_idioma.get()
        idioma_id = mapa_idiomas.get(sel_idioma)  # None si es "(Sin idioma)"
        try:
            ctrl_guardar_nivel(cb_nombre.get(), idioma_id, id_seleccionado[0])
            mensaje_ok("Nivel guardado correctamente.")
            limpiar()
            cargar_tabla()
        except Exception as e:
            mensaje_error(str(e))

    def eliminar():
        if not id_seleccionado[0]:
            mensaje_advertencia("Seleccione un nivel de la tabla primero.")
            return
        if not confirmar("eliminar este nivel"):
            return
        try:
            ctrl_eliminar_nivel(id_seleccionado[0])
            mensaje_ok("Nivel eliminado.")
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
        columnas=["id", "nombre", "idioma"],
        encabezados=["ID", "Nivel", "Idioma"],
        anchos=[60, 120, 280]
    )

    def on_seleccionar(event): # Carga los datos del registro seleccionado en el formulario.
        seleccion = tv.selection()
        if not seleccion:
            return
        fila = tv.item(seleccion[0], "values")
        id_seleccionado[0] = int(fila[0])
        cb_nombre.set(fila[1])
        # Setear el idioma; si es "Sin idioma" usar la opcion por defecto
        cb_idioma.set(fila[2] if fila[2] != "Sin idioma" else "(Sin idioma)")

    tv.bind("<<TreeviewSelect>>", on_seleccionar)

    def cargar_tabla():
        datos = ctrl_obtener_niveles()
        llenar_treeview(tv, datos, ["id", "nombre", "idioma"])

    cargar_tabla()
