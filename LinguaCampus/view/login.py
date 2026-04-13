# view/login.py
# Ventana de inicio de sesion del sistema LinguaCampus.
# Es la primera ventana que ve el usuario al ejecutar el programa.

import tkinter as tk
from tkinter import messagebox
from controller.login import ctrl_login


def show_login(root):
    """
    Construye y muestra la ventana de login.
    Recibe la ventana raiz (root) para poder ocultarla
    cuando el usuario ingrese correctamente.
    """

    # Configurar la ventana raiz como ventana de login
    root.title("LinguaCampus - Iniciar Sesion")
    root.geometry("380x320")
    root.resizable(False, False)

    # ── Titulo de la aplicacion
    tk.Label(root, text="LinguaCampus",
             font=("Arial", 18, "bold")).pack(pady=(30, 2))
    tk.Label(root, text="Sistema de Gestion de Escuela de Idiomas",
             font=("Arial", 9)).pack(pady=(0, 20))

    # ── Frame del formulario
    frame = tk.Frame(root, padx=30, pady=10)
    frame.pack()

    # Campo usuario
    tk.Label(frame, text="Usuario:", font=("Arial", 10),
             anchor="w").grid(row=0, column=0, sticky="w", pady=4)
    ent_usuario = tk.Entry(frame, font=("Arial", 10), width=25)
    ent_usuario.grid(row=0, column=1, pady=4, padx=6)

    # Campo contrasena
    tk.Label(frame, text="Contrasena:", font=("Arial", 10),
             anchor="w").grid(row=1, column=0, sticky="w", pady=4)
    ent_password = tk.Entry(frame, font=("Arial", 10), width=25, show="*")
    ent_password.grid(row=1, column=1, pady=4, padx=6)

    # Label para mostrar mensajes de error
    lbl_mensaje = tk.Label(root, text="", font=("Arial", 9), fg="red")
    lbl_mensaje.pack()

    def do_login(event=None):
        """
        Llama al controlador con las credenciales ingresadas.
        Si son correctas oculta el login y abre el menu principal.
        """
        usuario = ent_usuario.get()
        password = ent_password.get()
        try:
            resultado = ctrl_login(usuario, password)
            if resultado:
                # Login exitoso: ocultar ventana de login y abrir menu
                root.withdraw()
                abrir_menu(root)
            else:
                lbl_mensaje.config(text="Usuario o contrasena incorrectos.")
        except ValueError as e:
            lbl_mensaje.config(text=str(e))
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))

    # Boton ingresar y atajo con Enter
    tk.Button(root, text="Ingresar", font=("Arial", 10, "bold"),
              width=20, pady=4, command=do_login).pack(pady=10)
    ent_password.bind("<Return>", do_login)

    # Poner el foco en el campo usuario al abrir
    ent_usuario.bind("<Return>", lambda e: ent_password.focus())
    ent_password.bind("<Return>", lambda e: do_login())
    ent_usuario.focus()


def abrir_menu(root):
    """
    Importa y abre el menu principal luego del login exitoso.
    La importacion se hace aqui para evitar importaciones circulares.
    """
    from view.menu import show_menu
    show_menu(root)
