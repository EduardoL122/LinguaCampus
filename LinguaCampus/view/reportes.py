# view/reportes.py
# Interfaz grafica para el modulo de Reportes y Consultas.
# Contiene tres pestanas: aptos, reporte completo y filtros.

import tkinter as tk
from tkinter import ttk
from controller.reportes    import ctrl_reporte_aptos, ctrl_reporte_completo, ctrl_filtrar_estudiantes
from controller.idiomas     import ctrl_obtener_idiomas
from controller.niveles     import ctrl_obtener_niveles
from view.utils import (
    crear_ventana, crear_treeview, llenar_treeview,
    crear_label, crear_combobox, crear_frame_formulario,
    mensaje_error
)


def show_reportes(): # Abre la ventana de modulo de reportes con tres pestañas.

    ventana = crear_ventana("Reportes y Consultas", ancho=980, alto=580)

    # ── Titulo
    tk.Label(ventana, text="Modulo de Reportes",
             font=("Arial", 13, "bold")).pack(pady=(10, 2))
    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=10)

    # ── Notebook con las tres pestanas
    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True, padx=10, pady=8)

    # ===========================================================
    # PESTAÑA 1: Estudiantes aptos para certificacion
    # ===========================================================

    tab_aptos = tk.Frame(notebook)
    notebook.add(tab_aptos, text="  Aptos para Certificacion  ")

    tk.Label(tab_aptos,
             text="Estudiantes con promedio >= 3.5 en su grupo",
             font=("Arial", 10)).pack(pady=(8, 4))

    # Treeview de aptos
    tv_aptos = crear_treeview(
        tab_aptos,
        columnas=["estudiante", "grupo", "idioma", "nivel", "promedio"],
        encabezados=["Estudiante", "Grupo", "Idioma", "Nivel", "Promedio"],
        anchos=[200, 200, 120, 80, 90]
    )

    def cargar_aptos(): # Consulta el controlador y actualiza el Treeview de aptos.
        try:
            datos = ctrl_reporte_aptos()
            llenar_treeview(tv_aptos, datos,
                            ["estudiante", "grupo", "idioma", "nivel", "promedio"])
        except Exception as e:
            mensaje_error(str(e))

    tk.Button(tab_aptos, text="Actualizar",
              command=cargar_aptos,
              font=("Arial", 10), pady=4).pack(pady=4)
    cargar_aptos()

    # ===========================================================
    # PESTAÑA 2: Reporte completo con JOIN
    # ===========================================================
    tab_completo = tk.Frame(notebook)
    notebook.add(tab_completo, text="  Reporte Completo  ")

    tk.Label(tab_completo,
             text="Vista general: estudiante, grupo, idioma, nivel, docente y notas",
             font=("Arial", 10)).pack(pady=(8, 4))

    # Treeview del reporte completo
    tv_completo = crear_treeview(
        tab_completo,
        columnas=["estudiante", "email", "grupo", "idioma", "nivel", "docente", "modulo", "nota"],
        encabezados=["Estudiante", "Email", "Grupo", "Idioma", "Nivel", "Docente", "Modulo", "Nota"],
        anchos=[150, 170, 160, 90, 70, 140, 90, 60]
    )

    def cargar_completo(): # Consulta el contrador y actualiza el Treeview del reporte completo.
        try:
            datos = ctrl_reporte_completo()
            llenar_treeview(tv_completo, datos,
                            ["estudiante", "email", "grupo", "idioma",
                             "nivel", "docente", "modulo", "nota"])
        except Exception as e:
            mensaje_error(str(e))

    tk.Button(tab_completo, text="Actualizar",
              command=cargar_completo,
              font=("Arial", 10), pady=4).pack(pady=4)
    cargar_completo()

    # ===========================================================
    # PESTAÑA 3: Filtro de estudiantes
    # ===========================================================
    tab_filtro = tk.Frame(notebook)
    notebook.add(tab_filtro, text="  Filtrar Estudiantes  ")

    tk.Label(tab_filtro,
             text="Filtre estudiantes por idioma, nivel o estado de inscripcion",
             font=("Arial", 10)).pack(pady=(8, 4))

    # Cargar datos para los Combobox de filtro
    idiomas = ctrl_obtener_idiomas()
    niveles = ctrl_obtener_niveles()

    # Mapa con opcion "Todos" incluida al inicio
    mapa_idiomas_f = {"(Todos)": None, **{i["nombre_idioma"]: i["id"] for i in idiomas}}
    mapa_niveles_f = {"(Todos)": None, **{n["nombre"]: n["id"] for n in niveles}}

    # Frame de filtros
    frame_filtros = crear_frame_formulario(tab_filtro, " Filtros ")

    crear_label(frame_filtros, "Idioma:").grid(
        row=0, column=0, sticky="w", padx=6, pady=4)
    cb_f_idioma = crear_combobox(frame_filtros, list(mapa_idiomas_f.keys()), width=18)
    cb_f_idioma.set("(Todos)")
    cb_f_idioma.grid(row=0, column=1, padx=8, pady=4)

    crear_label(frame_filtros, "Nivel:").grid(
        row=0, column=2, sticky="w", padx=6, pady=4)
    cb_f_nivel = crear_combobox(frame_filtros, list(mapa_niveles_f.keys()), width=14)
    cb_f_nivel.set("(Todos)")
    cb_f_nivel.grid(row=0, column=3, padx=8, pady=4)

    crear_label(frame_filtros, "Estado Inscripcion:").grid(
        row=0, column=4, sticky="w", padx=6, pady=4)
    cb_f_estado = crear_combobox(
        frame_filtros,
        ["(Todos)", "activo", "inactivo", "retirado"],
        width=14
    )
    cb_f_estado.set("(Todos)")
    cb_f_estado.grid(row=0, column=5, padx=8, pady=4)

    # Treeview del filtro
    tv_filtro = crear_treeview(
        tab_filtro,
        columnas=["nombre", "email", "estado", "idioma", "nivel", "estado_inscripcion"],
        encabezados=["Nombre", "Email", "Estado", "Idioma", "Nivel", "Estado Ins."],
        anchos=[180, 200, 80, 110, 80, 100]
    )

    def aplicar_filtro():
        """
        Lee los valores de los Combobox de filtro,
        obtiene los IDs correspondientes y llama al controlador.
        """
        try:
            idioma_id = mapa_idiomas_f.get(cb_f_idioma.get())
            nivel_id  = mapa_niveles_f.get(cb_f_nivel.get())
            estado    = cb_f_estado.get() if cb_f_estado.get() != "(Todos)" else None
            datos = ctrl_filtrar_estudiantes(idioma_id, nivel_id, estado)
            llenar_treeview(tv_filtro, datos,
                            ["nombre", "email", "estado", "idioma",
                             "nivel", "estado_inscripcion"])
        except Exception as e:
            mensaje_error(str(e))

    tk.Button(tab_filtro, text="Aplicar Filtro",
              command=aplicar_filtro,
              font=("Arial", 10), pady=4).pack(pady=4)
    aplicar_filtro()
