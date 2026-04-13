# view/evaluaciones.py
# Interfaz grafica para el modulo de Evaluaciones.
# Usa Combobox para estudiante, grupo y modulo.

import tkinter as tk
from controller.evaluaciones import (
    ctrl_obtener_evaluaciones,
    ctrl_guardar_evaluacion,
    ctrl_eliminar_evaluacion
)
from controller.estudiantes import ctrl_obtener_estudiantes
from controller.grupos      import ctrl_obtener_grupos
from view.utils import (
    crear_ventana, crear_frame_formulario, crear_frame_botones,
    agregar_boton, crear_treeview, llenar_treeview, crear_label,
    crear_entry, crear_combobox, mensaje_ok, mensaje_error,
    mensaje_advertencia, confirmar
)


def show_evaluaciones(): # Abre la ventana del modulo de evaluaciones.

    ventana = crear_ventana("Gestion de Evaluaciones", ancho=880, alto=530)

    # Variable para guardar el ID del registro seleccionado
    id_seleccionado = [None]

    # ── Titulo
    tk.Label(ventana, text="Modulo de Evaluaciones",
             font=("Arial", 13, "bold")).pack(pady=(10, 2))
    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=10)

    # ── Cargar datos para los Combobox (llaves foraneas)
    estudiantes = ctrl_obtener_estudiantes()
    grupos      = ctrl_obtener_grupos()

    mapa_estudiantes = {e["nombre"]: e["id"] for e in estudiantes}
    mapa_grupos      = {g["nombre_grupo"]: g["id"] for g in grupos}

    # ── Formulario
    frame_form = crear_frame_formulario(ventana, " Datos de la Evaluacion ")

    # Fila 0: estudiante y grupo (llaves foraneas)
    crear_label(frame_form, "Estudiante:").grid(
        row=0, column=0, sticky="w", pady=5, padx=4)
    # Combobox estudiante: llave foranea estudiante_id
    cb_estudiante = crear_combobox(frame_form, list(mapa_estudiantes.keys()), width=26)
    cb_estudiante.grid(row=0, column=1, pady=5, padx=8)

    crear_label(frame_form, "Grupo:").grid(
        row=0, column=2, sticky="w", pady=5, padx=4)
    # Combobox grupo: llave foranea grupo_id
    cb_grupo = crear_combobox(frame_form, list(mapa_grupos.keys()), width=26)
    cb_grupo.grid(row=0, column=3, pady=5, padx=8)

    # Fila 1: modulo y nota
    crear_label(frame_form, "Modulo:").grid(
        row=1, column=0, sticky="w", pady=5, padx=4)
    # Combobox modulo (opciones predefinidas)
    cb_modulo = crear_combobox(
        frame_form,
        ["Modulo 1", "Modulo 2", "Modulo 3", "Modulo 4"],
        width=16
    )
    cb_modulo.grid(row=1, column=1, pady=5, padx=8, sticky="w")

    crear_label(frame_form, "Nota (0.0 - 5.0):").grid(
        row=1, column=2, sticky="w", pady=5, padx=4)
    ent_nota = crear_entry(frame_form, width=10)
    ent_nota.grid(row=1, column=3, pady=5, padx=8, sticky="w")

    # ── Botones
    frame_btn = crear_frame_botones(ventana)

    def limpiar():
        id_seleccionado[0] = None
        cb_estudiante.set("")
        cb_grupo.set("")
        cb_modulo.set("")
        ent_nota.delete(0, "end")
        tv.selection_remove(tv.selection())

    def guardar(): # Resolver IDs a partir de los nombres del Combobox.
        est_id = mapa_estudiantes.get(cb_estudiante.get())
        grp_id = mapa_grupos.get(cb_grupo.get())
        try:
            ctrl_guardar_evaluacion(
                est_id, grp_id,
                cb_modulo.get(), ent_nota.get(),
                id_seleccionado[0]
            )
            mensaje_ok("Evaluacion guardada correctamente.")
            limpiar()
            cargar_tabla()
        except Exception as e:
            mensaje_error(str(e))

    def eliminar():
        if not id_seleccionado[0]:
            mensaje_advertencia("Seleccione una evaluacion de la tabla primero.")
            return
        if not confirmar("eliminar esta evaluacion"):
            return
        try:
            ctrl_eliminar_evaluacion(id_seleccionado[0])
            mensaje_ok("Evaluacion eliminada.")
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
        columnas=["id", "estudiante", "grupo", "modulo", "nota"],
        encabezados=["ID", "Estudiante", "Grupo", "Modulo", "Nota"],
        anchos=[50, 220, 220, 120, 80]
    )

    def on_seleccionar(event): # Carga los datos de la evaluacion seleccionada en el formulario.
        seleccion = tv.selection()
        if not seleccion:
            return
        fila = tv.item(seleccion[0], "values")
        datos = ctrl_obtener_evaluaciones()
        registro = next((r for r in datos if r["id"] == int(fila[0])), None)
        if not registro:
            return
        id_seleccionado[0] = registro["id"]
        cb_estudiante.set(registro["estudiante"])
        cb_grupo.set(registro["grupo"])
        cb_modulo.set(registro["modulo"])
        ent_nota.delete(0, "end")
        ent_nota.insert(0, str(registro["nota"]))

    tv.bind("<<TreeviewSelect>>", on_seleccionar)

    def cargar_tabla():
        datos = ctrl_obtener_evaluaciones()
        llenar_treeview(tv, datos, ["id", "estudiante", "grupo", "modulo", "nota"])

    cargar_tabla()
