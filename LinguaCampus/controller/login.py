# controller/login.py
# Logica de negocio para la autenticacion de usuarios.
# Valida los datos antes de consultar el modelo.

from model import login as model_login


def ctrl_login(username, password):
    """
    Valida que los campos no esten vacios y consulta
    la base de datos para verificar las credenciales.
    Retorna el usuario si existe, o None si no coincide.
    """
    # Validacion: los campos son obligatorios
    if not username.strip() or not password.strip():
        raise ValueError("El usuario y la contrasena son obligatorios.")

    return model_login.verificar_usuario(username.strip(), password.strip())
