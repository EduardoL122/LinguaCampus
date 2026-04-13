# view/grupos.py
# Interfaz grafica para el modulo de Grupos.
# Usa Combobox para idioma, nivel y docente (llaves foraneas).

import tkinter as tk
from controller.grupos import (
    ctrl_obtener_grupos,
    ctrl_guardar_grupo,
    ctrl_eliminar_grupo
)
from controller.idiomas  import ctrl_obtener_idiomas
from controller.niveles  import ctrl_obtener_niveles
from controller.docentes import ctrl_obtener_docentes
from view.utils import (
    crear_ventana, crear_frame_formulario, crear_frame_botones,
    agregar_boton, crear_treeview, llenar_treeview, crear_label,
    crear_entry, crear_combobox, mensaje_ok, mensaje_error,
    mensaje_advertencia, confirmar
)


def show_grupos(): # Abre la ventana del modulo de grupos.

    ventana = crear_ventana("Gestion de Grupos", ancho=960, alto=580)

    # Variable para guardar el ID del registro seleccionado
    id_seleccionado = [None]

    # ── Titulo
    tk.Label(ventana, text="Modulo de Grupos",
             font=("Arial", 13, "bold")).pack(pady=(10, 2))
    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=10)

    # ── Cargar datos para los Combobox (llaves foraneas)
    idiomas  = ctrl_obtener_idiomas()
    niveles  = ctrl_obtener_niveles()
    docentes = ctrl_obtener_docentes()

    # Mapas nombre -> id para recuperar el ID al guardar
    mapa_idiomas  = {i["nombre_idioma"]: i["id"] for i in idiomas}
    mapa_niveles  = {n['nombre']: n["id"] for n in niveles}
    mapa_docentes = {d["nombre"]: d["id"] for d in docentes}

    # ── Formulario
    frame_form = crear_frame_formulario(ventana, " Datos del Grupo ")

    # Fila 0: nombre del grupo, horario, cupo
    crear_label(frame_form, "Nombre Grupo:").grid(
        row=0, column=0, sticky="w", pady=5, padx=4)
    ent_nombre = crear_entry(frame_form, width=24)
    ent_nombre.grid(row=0, column=1, pady=5, padx=6)

    crear_label(frame_form, "Horario:").grid(
        row=0, column=2, sticky="w", pady=5, padx=4)
    ent_horario = crear_entry(frame_form, width=20)
    ent_horario.grid(row=0, column=3, pady=5, padx=6)

    crear_label(frame_form, "Cupo Maximo:").grid(
        row=0, column=4, sticky="w", pady=5, padx=4)
    ent_cupo = crear_entry(frame_form, width=6)
    ent_cupo.grid(row=0, column=5, pady=5, padx=6)

    # Fila 1: idioma, nivel, docente (todos son llaves foraneas con Combobox)
    crear_label(frame_form, "Idioma:").grid(
        row=1, column=0, sticky="w", pady=5, padx=4)
    cb_idioma = crear_combobox(frame_form, list(mapa_idiomas.keys()), width=16)
    cb_idioma.grid(row=1, column=1, pady=5, padx=6)

    crear_label(frame_form, "Nivel:").grid(
        row=1, column=2, sticky="w", pady=5, padx=4)
    # El nivel muestra "A1 - Frances" para mayor claridad
    cb_nivel = crear_combobox(frame_form, list(mapa_niveles.keys()), width=22)
    cb_nivel.grid(row=1, column=3, pady=5, padx=6)

    crear_label(frame_form, "Docente:").grid(
        row=1, column=4, sticky="w", pady=5, padx=4)
    cb_docente = crear_combobox(frame_form, list(mapa_docentes.keys()), width=20)
    cb_docente.grid(row=1, column=5, pady=5, padx=6)

    # ── Botones
    frame_btn = crear_frame_botones(ventana)

    def limpiar():
        id_seleccionado[0] = None
        ent_nombre.delete(0, "end")
        ent_horario.delete(0, "end")
        ent_cupo.delete(0, "end")
        cb_idioma.set("")
        cb_nivel.set("")
        cb_docente.set("")
        tv.selection_remove(tv.selection())

    def guardar(): # Resolver IDs desde los nombres seleccionados en los Combobox.
        idioma_id  = mapa_idiomas.get(cb_idioma.get())
        nivel_id   = mapa_niveles.get(cb_nivel.get())
        docente_id = mapa_docentes.get(cb_docente.get())
        try:
            ctrl_guardar_grupo(
                idioma_id, nivel_id, docente_id,
                ent_nombre.get(), ent_horario.get(), ent_cupo.get(),
                id_seleccionado[0]
            )
            mensaje_ok("Grupo guardado correctamente.")
            limpiar()
            cargar_tabla()
        except Exception as e:
            mensaje_error(str(e))

    def eliminar():
        if not id_seleccionado[0]:
            mensaje_advertencia("Seleccione un grupo de la tabla primero.")
            return
        if not confirmar("eliminar este grupo"):
            return
        try:
            ctrl_eliminar_grupo(id_seleccionado[0])
            mensaje_ok("Grupo eliminado.")
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
        columnas=["id", "nombre_grupo", "horario", "cupo_maximo", "idioma", "nivel", "docente"],
        encabezados=["ID", "Grupo", "Horario", "Cupo", "Idioma", "Nivel", "Docente"],
        anchos=[40, 180, 150, 55, 100, 80, 160]
    )

    def on_seleccionar(event): # Carga los datos del grupo seleccionado en el formulario.
        seleccion = tv.selection()
        if not seleccion:
            return
        fila = tv.item(seleccion[0], "values")
        datos = ctrl_obtener_grupos()
        registro = next((g for g in datos if g["id"] == int(fila[0])), None)
        if not registro:
            return
        id_seleccionado[0] = registro["id"]
        ent_nombre.delete(0, "end");  ent_nombre.insert(0, registro["nombre_grupo"])
        ent_horario.delete(0, "end"); ent_horario.insert(0, registro["horario"])
        ent_cupo.delete(0, "end");    ent_cupo.insert(0, registro["cupo_maximo"])
        cb_idioma.set(registro["idioma"])
        cb_docente.set(registro["docente"])
        # Buscar la clave del nivel en el mapa (formato "A1 - Frances")
        clave_nivel = next(
            (k for k, v in mapa_niveles.items() if v == registro["nivel_id"]), ""
        )
        cb_nivel.set(clave_nivel)

    tv.bind("<<TreeviewSelect>>", on_seleccionar)

    def cargar_tabla():
        datos = ctrl_obtener_grupos()
        llenar_treeview(tv, datos,
                        ["id", "nombre_grupo", "horario", "cupo_maximo",
                         "idioma", "nivel", "docente"])

    cargar_tabla()
