# view/inscripciones.py
# Interfaz grafica para el modulo de Inscripciones.
# Uso de Combobox para estudiante y grupo (llaves foraneas).

import tkinter as tk
from datetime import date
from controller.inscripciones import (
    ctrl_obtener_inscripciones,
    ctrl_guardar_inscripcion,
    ctrl_eliminar_inscripcion
)
from controller.estudiantes import ctrl_obtener_estudiantes
from controller.grupos      import ctrl_obtener_grupos
from view.utils import (
    crear_ventana, crear_frame_formulario, crear_frame_botones,
    agregar_boton, crear_treeview, llenar_treeview, crear_label,
    crear_entry, crear_combobox, mensaje_ok, mensaje_error,
    mensaje_advertencia, confirmar
)


def show_inscripciones(): # Abre la ventana del modulo de inscripciones.

    ventana = crear_ventana("Gestion de Inscripciones", ancho=960, alto=560)

    # Variable para guardar el ID del registro seleccionado
    id_seleccionado = [None]

    # ── Titulo
    tk.Label(ventana, text="Modulo de Inscripciones",
             font=("Arial", 13, "bold")).pack(pady=(10, 2))
    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=10)

    # ── Cargar datos para los Combobox (llaves foraneas)
    estudiantes = ctrl_obtener_estudiantes()
    grupos      = ctrl_obtener_grupos()

    mapa_estudiantes = {e["nombre"]: e["id"] for e in estudiantes}
    mapa_grupos      = {g["nombre_grupo"]: g["id"] for g in grupos}

    # ── Formulario
    frame_form = crear_frame_formulario(ventana, " Datos de la Inscripcion ")

    # Fila 0: estudiante y grupo (ambos son llaves foraneas)
    crear_label(frame_form, "Estudiante:").grid(
        row=0, column=0, sticky="w", pady=5, padx=4)
    # Combobox estudiante: llave foranea estudiante_id
    cb_estudiante = crear_combobox(frame_form, list(mapa_estudiantes.keys()), width=28)
    cb_estudiante.grid(row=0, column=1, pady=5, padx=8)

    crear_label(frame_form, "Grupo:").grid(
        row=0, column=2, sticky="w", pady=5, padx=4)
    # Combobox grupo: llave foranea grupo_id
    cb_grupo = crear_combobox(frame_form, list(mapa_grupos.keys()), width=28)
    cb_grupo.grid(row=0, column=3, pady=5, padx=8)

    # Fila 1: fecha y estado
    crear_label(frame_form, "Fecha (YYYY-MM-DD):").grid(
        row=1, column=0, sticky="w", pady=5, padx=4)
    ent_fecha = crear_entry(frame_form, width=16)
    ent_fecha.insert(0, str(date.today()))  # Fecha de hoy por defecto
    ent_fecha.grid(row=1, column=1, pady=5, padx=8, sticky="w")

    crear_label(frame_form, "Estado:").grid(
        row=1, column=2, sticky="w", pady=5, padx=4)
    cb_estado = crear_combobox(frame_form, ["activo", "inactivo", "retirado"], width=16)
    cb_estado.set("activo")
    cb_estado.grid(row=1, column=3, pady=5, padx=8, sticky="w")

    # ── Botones
    frame_btn = crear_frame_botones(ventana)

    def limpiar(): # Limpia el formulario y deselecciona la tabla.
        id_seleccionado[0] = None
        cb_estudiante.set("")
        cb_grupo.set("")
        ent_fecha.delete(0, "end")
        ent_fecha.insert(0, str(date.today()))
        cb_estado.set("activo")
        tv.selection_remove(tv.selection())

    def guardar(): # Valida los datos del formulario y guarda (insertar o actualizar) la inscripcion.
        est_id = mapa_estudiantes.get(cb_estudiante.get())
        grp_id = mapa_grupos.get(cb_grupo.get())
        try:
            ctrl_guardar_inscripcion(
                est_id, grp_id,
                ent_fecha.get(), cb_estado.get(),
                id_seleccionado[0]
            )
            mensaje_ok("Inscripcion guardada correctamente.")
            limpiar()
            cargar_tabla()
        except Exception as e:
            mensaje_error(str(e))

    def eliminar():
        if not id_seleccionado[0]:
            mensaje_advertencia("Seleccione una inscripcion de la tabla primero.")
            return
        if not confirmar("eliminar esta inscripcion"):
            return
        try:
            ctrl_eliminar_inscripcion(id_seleccionado[0])
            mensaje_ok("Inscripcion eliminada.")
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
        columnas=["id", "estudiante", "grupo", "idioma", "nivel",
                  "fecha_inscripcion", "estado"],
        encabezados=["ID", "Estudiante", "Grupo", "Idioma", "Nivel",
                     "Fecha", "Estado"],
        anchos=[40, 170, 170, 100, 70, 110, 80]
    )

    def on_seleccionar(event): # Carga los datos de la inscripcion seleccionada en el formulario.
        seleccion = tv.selection()
        if not seleccion:
            return
        fila = tv.item(seleccion[0], "values")
        datos = ctrl_obtener_inscripciones()
        registro = next((r for r in datos if r["id"] == int(fila[0])), None)
        if not registro:
            return
        id_seleccionado[0] = registro["id"]
        cb_estudiante.set(registro["estudiante"])
        cb_grupo.set(registro["grupo"])
        ent_fecha.delete(0, "end")
        ent_fecha.insert(0, str(registro["fecha_inscripcion"]))
        cb_estado.set(registro["estado"])

    tv.bind("<<TreeviewSelect>>", on_seleccionar)

    def cargar_tabla():
        datos = ctrl_obtener_inscripciones()
        llenar_treeview(tv, datos,
                        ["id", "estudiante", "grupo", "idioma", "nivel",
                         "fecha_inscripcion", "estado"])

    cargar_tabla()
