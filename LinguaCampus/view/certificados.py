# view/certificados.py
# Interfaz grafica para el modulo de Certificados.
# Uso de Combobox para estudiante, nivel y grupo (llaves foraneas).

import tkinter as tk
from datetime import date
from controller.certificados import (
    ctrl_obtener_certificados,
    ctrl_guardar_certificado,
    ctrl_eliminar_certificado
)
from controller.estudiantes import ctrl_obtener_estudiantes
from controller.niveles     import ctrl_obtener_niveles
from controller.grupos      import ctrl_obtener_grupos
from view.utils import (
    crear_ventana, crear_frame_formulario, crear_frame_botones,
    agregar_boton, crear_treeview, llenar_treeview, crear_label,
    crear_entry, crear_combobox, mensaje_ok, mensaje_error,
    mensaje_advertencia, confirmar
)


def show_certificados(): # Abre la ventana del modulo de certificados.

    ventana = crear_ventana("Gestion de Certificados", ancho=960, alto=560)

    # Variable para guardar el ID del registro seleccionado
    id_seleccionado = [None]

    # ── Titulo
    tk.Label(ventana, text="Modulo de Certificados",
             font=("Arial", 13, "bold")).pack(pady=(10, 2))
    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=10)

    # ── Cargar datos para los Combobox (llaves foraneas)
    estudiantes = ctrl_obtener_estudiantes()
    niveles     = ctrl_obtener_niveles()
    grupos      = ctrl_obtener_grupos()

    mapa_estudiantes = {e["nombre"]: e["id"] for e in estudiantes}
    mapa_niveles     = {n['nombre']: n["id"] for n in niveles}
    mapa_grupos      = {g["nombre_grupo"]: g["id"] for g in grupos}

    # ── Formulario
    frame_form = crear_frame_formulario(ventana, " Datos del Certificado ")

    # Fila 0: estudiante y nivel (llaves foraneas)
    crear_label(frame_form, "Estudiante:").grid(
        row=0, column=0, sticky="w", pady=5, padx=4)
    # Combobox estudiante: llave foranea estudiante_id
    cb_estudiante = crear_combobox(frame_form, list(mapa_estudiantes.keys()), width=26)
    cb_estudiante.grid(row=0, column=1, pady=5, padx=8)

    crear_label(frame_form, "Nivel:").grid(
        row=0, column=2, sticky="w", pady=5, padx=4)
    # Combobox nivel: llave foranea nivel_id
    cb_nivel = crear_combobox(frame_form, list(mapa_niveles.keys()), width=26)
    cb_nivel.grid(row=0, column=3, pady=5, padx=8)

    # Fila 1: grupo, fecha y estado
    crear_label(frame_form, "Grupo:").grid(
        row=1, column=0, sticky="w", pady=5, padx=4)
    # Combobox grupo: llave foranea grupo_id
    cb_grupo = crear_combobox(frame_form, list(mapa_grupos.keys()), width=26)
    cb_grupo.grid(row=1, column=1, pady=5, padx=8)

    crear_label(frame_form, "Fecha (YYYY-MM-DD):").grid(
        row=1, column=2, sticky="w", pady=5, padx=4)
    ent_fecha = crear_entry(frame_form, width=16)
    ent_fecha.insert(0, str(date.today()))
    ent_fecha.grid(row=1, column=3, pady=5, padx=8, sticky="w")

    crear_label(frame_form, "Estado:").grid(
        row=2, column=0, sticky="w", pady=5, padx=4)
    cb_estado = crear_combobox(frame_form, ["emitido", "pendiente", "anulado"], width=16)
    cb_estado.set("emitido")
    cb_estado.grid(row=2, column=1, pady=5, padx=8, sticky="w")

    # ── Botones
    frame_btn = crear_frame_botones(ventana)

    def limpiar():
        id_seleccionado[0] = None
        cb_estudiante.set("")
        cb_nivel.set("")
        cb_grupo.set("")
        ent_fecha.delete(0, "end")
        ent_fecha.insert(0, str(date.today()))
        cb_estado.set("emitido")
        tv.selection_remove(tv.selection())

    def guardar(): # Resolver IDs a partir de los nombres del Comboboxes y llamar al contralador para guardar el certificado.
        est_id = mapa_estudiantes.get(cb_estudiante.get())
        niv_id = mapa_niveles.get(cb_nivel.get())
        grp_id = mapa_grupos.get(cb_grupo.get())
        try:
            ctrl_guardar_certificado(
                est_id, niv_id, grp_id,
                ent_fecha.get(), cb_estado.get(),
                id_seleccionado[0]
            )
            mensaje_ok("Certificado guardado correctamente.")
            limpiar()
            cargar_tabla()
        except Exception as e:
            mensaje_error(str(e))

    def eliminar():
        if not id_seleccionado[0]:
            mensaje_advertencia("Seleccione un certificado de la tabla primero.")
            return
        if not confirmar("eliminar este certificado"):
            return
        try:
            ctrl_eliminar_certificado(id_seleccionado[0])
            mensaje_ok("Certificado eliminado.")
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
        columnas=["id", "estudiante", "nivel", "grupo", "fecha", "estado"],
        encabezados=["ID", "Estudiante", "Nivel", "Grupo", "Fecha", "Estado"],
        anchos=[50, 190, 120, 190, 110, 90]
    )

    def on_seleccionar(event): # Carga los datos del certificado seleccionado en el formulario.
        seleccion = tv.selection()
        if not seleccion:
            return
        fila = tv.item(seleccion[0], "values")
        datos = ctrl_obtener_certificados()
        registro = next((r for r in datos if r["id"] == int(fila[0])), None)
        if not registro:
            return
        id_seleccionado[0] = registro["id"]
        cb_estudiante.set(registro["estudiante"])
        cb_grupo.set(registro["grupo"])
        ent_fecha.delete(0, "end")
        ent_fecha.insert(0, str(registro["fecha"]))
        cb_estado.set(registro["estado"])
        # Buscar la clave del nivel en el mapa
        clave_nivel = next(
            (k for k, v in mapa_niveles.items() if v == registro["nivel_id"]), ""
        )
        cb_nivel.set(clave_nivel)

    tv.bind("<<TreeviewSelect>>", on_seleccionar)

    def cargar_tabla():
        datos = ctrl_obtener_certificados()
        llenar_treeview(tv, datos,
                        ["id", "estudiante", "nivel", "grupo", "fecha", "estado"])

    cargar_tabla()
