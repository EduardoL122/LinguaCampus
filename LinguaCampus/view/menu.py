# view/menu.py
# Ventana principal del sistema con el menu de navegacion.
# Se muestra luego de un login exitoso.

import tkinter as tk


def show_menu(root):
    """
    Construye la ventana principal con botones para cada modulo.
    Recibe root para poder cerrarlo al salir del sistema.
    """
    ventana = tk.Toplevel()
    ventana.title("LinguaCampus - Menu Principal")
    ventana.geometry("500x480")
    ventana.resizable(False, False)

    # Al cerrar el menu, cerrar toda la aplicacion
    ventana.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

    # ── Encabezado
    tk.Label(ventana, text="LinguaCampus",
             font=("Arial", 16, "bold")).pack(pady=(20, 2))
    tk.Label(ventana, text="Seleccione un modulo",
             font=("Arial", 10)).pack(pady=(0, 16))

    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=20)

    # ── Frame para la grilla de botones
    frame_botones = tk.Frame(ventana, padx=30, pady=20)
    frame_botones.pack()

    # Definicion de los modulos: (texto, funcion_vista)
    # Las importaciones se hacen aqui para evitar importaciones circulares
    def abrir_estudiantes():
        from view.estudiantes import show_estudiantes
        show_estudiantes()

    def abrir_docentes():
        from view.docentes import show_docentes
        show_docentes()

    def abrir_idiomas():
        from view.idiomas import show_idiomas
        show_idiomas()

    def abrir_niveles():
        from view.niveles import show_niveles
        show_niveles()

    def abrir_grupos():
        from view.grupos import show_grupos
        show_grupos()

    def abrir_inscripciones():
        from view.inscripciones import show_inscripciones
        show_inscripciones()

    def abrir_evaluaciones():
        from view.evaluaciones import show_evaluaciones
        show_evaluaciones()

    def abrir_certificados():
        from view.certificados import show_certificados
        show_certificados()

    def abrir_reportes():
        from view.reportes import show_reportes
        show_reportes()

    # Lista de modulos con su texto y funcion
    modulos = [
        ("Estudiantes",    abrir_estudiantes),
        ("Docentes",       abrir_docentes),
        ("Idiomas",        abrir_idiomas),
        ("Niveles",        abrir_niveles),
        ("Grupos",         abrir_grupos),
        ("Inscripciones",  abrir_inscripciones),
        ("Evaluaciones",   abrir_evaluaciones),
        ("Certificados",   abrir_certificados),
        ("Reportes",       abrir_reportes),
    ]

    # Organizar los botones en 3 columnas
    for i, (texto, comando) in enumerate(modulos):
        fila = i // 3
        columna = i % 3
        tk.Button(
            frame_botones,
            text=texto,
            command=comando,
            font=("Arial", 10),
            width=16,
            pady=8
        ).grid(row=fila, column=columna, padx=8, pady=6)

    # Boton de salir al final
    tk.Frame(ventana, height=1, bg="gray").pack(fill="x", padx=20, pady=(4, 0))
    tk.Button(ventana, text="Cerrar sesion / Salir",
              command=root.destroy,
              font=("Arial", 9), pady=4).pack(pady=12)
