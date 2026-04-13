# main.py
# Punto de entrada de la aplicacion LinguaCampus.

import tkinter as tk
from view.login import show_login


def main():
    """
    Crea la ventana raiz de Tkinter y lanza la ventana de login.
    La ventana raiz se oculta despues del login exitoso y
    se destruye cuando el usuario cierra el menu principal.
    """
    root = tk.Tk()
    show_login(root)
    root.mainloop()


if __name__ == "__main__":
    main()