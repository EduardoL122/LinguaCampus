# view/docentes.py
# Interfaz grafica para el modulo de Docentes.
# Usa Combobox para idioma (llave foranea), nivel certificado y estado.

import tkinter as tk
from controller.docentes import (
    ctrl_obtener_docentes,
    ctrl_guardar_docente,
    ctrl_eliminar_docente
)
from controller.idiomas import ctrl_obtener_idiomas
from view.utils import (
    crear_ventana, crear_frame_formulario, crear_frame_botones,
    agregar_boton, crear_treeview, llenar_treeview, crear_label,
    crear_entry, crear_combobox, mensaje_ok, mensaje_error,
    mensaje_advertencia, confirmar
)


def show_docentes(): # Abre la ventana del modulo de Docentes.

    ventana = crear_ventana("Gestion de Docentes", ancho=850, alto=530)

    # Variable para guardar el ID del registro seleccionado
    id_seleccionado = [None]

    # ── Titulo
    tk.Label(ventana, text="Modulo de Docentes",
             font=("Arial", 13, "bold")).pack(pady=(10, 2))
    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=10)

    # ── Cargar idiomas para el Combobox (llave foranea idioma_id)
    idiomas = ctrl_obtener_idiomas()
    mapa_idiomas = {i["nombre_idioma"]: i["id"] for i in idiomas}
    lista_idiomas = list(mapa_idiomas.keys())

    # ── Formulario
    frame_form = crear_frame_formulario(ventana, " Datos del Docente ")

    # Fila 0: nombre e idioma
    crear_label(frame_form, "Nombre:").grid(
        row=0, column=0, sticky="w", pady=5, padx=4)
    ent_nombre = crear_entry(frame_form, width=28)
    ent_nombre.grid(row=0, column=1, pady=5, padx=8)

    crear_label(frame_form, "Idioma Principal:").grid(
        row=0, column=2, sticky="w", pady=5, padx=4)
    # Combobox idioma: llave foranea idioma_id
    cb_idioma = crear_combobox(frame_form, lista_idiomas, width=20)
    cb_idioma.grid(row=0, column=3, pady=5, padx=8)

    # Fila 1: nivel certificado y estado
    crear_label(frame_form, "Nivel Certificado:").grid(
        row=1, column=0, sticky="w", pady=5, padx=4)
    # Combobox nivel certificado (valores MCER)
    cb_nivel_cert = crear_combobox(frame_form, ["A1", "A2", "B1", "B2", "C1", "C2"], width=10)
    cb_nivel_cert.grid(row=1, column=1, pady=5, padx=8, sticky="w")

    crear_label(frame_form, "Estado:").grid(
        row=1, column=2, sticky="w", pady=5, padx=4)
    # Combobox estado
    cb_estado = crear_combobox(frame_form, ["activo", "inactivo"], width=14)
    cb_estado.set("activo")
    cb_estado.grid(row=1, column=3, pady=5, padx=8, sticky="w")

    # ── Botones
    frame_btn = crear_frame_botones(ventana)

    def limpiar():
        id_seleccionado[0] = None
        ent_nombre.delete(0, "end")
        cb_idioma.set("")
        cb_nivel_cert.set("")
        cb_estado.set("activo")
        tv.selection_remove(tv.selection())

    def guardar(): # Resolver el ID del idioma desde el nombre seleccionado en el combobox y llamar al controlador para guardar al docente.
        idioma_id = mapa_idiomas.get(cb_idioma.get())
        try:
            ctrl_guardar_docente(
                ent_nombre.get(),
                idioma_id,
                cb_nivel_cert.get(),
                cb_estado.get(),
                id_seleccionado[0]
            )
            mensaje_ok("Docente guardado correctamente.")
            limpiar()
            cargar_tabla()
        except Exception as e:
            mensaje_error(str(e))

    def eliminar():
        if not id_seleccionado[0]:
            mensaje_advertencia("Seleccione un docente de la tabla primero.")
            return
        if not confirmar("eliminar este docente"):
            return
        try:
            ctrl_eliminar_docente(id_seleccionado[0])
            mensaje_ok("Docente eliminado.")
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
        columnas=["id", "nombre", "idioma", "nivel_certificado", "estado"],
        encabezados=["ID", "Nombre", "Idioma", "Nivel Cert.", "Estado"],
        anchos=[50, 220, 130, 110, 90]
    )

    def on_seleccionar(event): # Carga los datos del docente seleccionado en el formulario.
        seleccion = tv.selection()
        if not seleccion:
            return
        fila = tv.item(seleccion[0], "values")
        # Buscar el registro completo para obtener el idioma_id original
        datos = ctrl_obtener_docentes()
        registro = next((d for d in datos if d["id"] == int(fila[0])), None)
        if not registro:
            return
        id_seleccionado[0] = registro["id"]
        ent_nombre.delete(0, "end")
        ent_nombre.insert(0, registro["nombre"])
        cb_idioma.set(registro["idioma"] if registro["idioma"] != "Sin idioma" else "")
        cb_nivel_cert.set(registro["nivel_certificado"])
        cb_estado.set(registro["estado"])

    tv.bind("<<TreeviewSelect>>", on_seleccionar)

    def cargar_tabla():
        datos = ctrl_obtener_docentes()
        llenar_treeview(tv, datos, ["id", "nombre", "idioma", "nivel_certificado", "estado"])

    cargar_tabla()
