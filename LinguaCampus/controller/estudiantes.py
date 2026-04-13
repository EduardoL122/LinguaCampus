# controller/estudiantes.py
# Logica de negocio para el modulo de estudiantes.

from model import estudiantes as model_estudiantes


def ctrl_obtener_estudiantes(): # Retorna todos los estudiantes desde el modelo.
    return model_estudiantes.obtener_todos()


def ctrl_guardar_estudiante(nombre, email, estado, id_estudiante=None):
    """
    Valida nombre, email y estado antes de guardar.
    Llama a insertar si es nuevo o actualizar si tiene ID.
    """
    # Validacion de campos obligatorios
    if not nombre.strip():
        raise ValueError("El nombre del estudiante es obligatorio.")
    if not email.strip():
        raise ValueError("El email es obligatorio.")
    if "@" not in email or "." not in email:
        raise ValueError("El email no tiene un formato valido.")
    if not estado:
        raise ValueError("Debe seleccionar el estado del estudiante.")

    if id_estudiante:
        model_estudiantes.actualizar(id_estudiante, nombre.strip(), email.strip(), estado)
    else:
        model_estudiantes.insertar(nombre.strip(), email.strip(), estado)


def ctrl_eliminar_estudiante(id_estudiante):
    """
    Solicita al modelo eliminar el estudiante.
    El modelo verifica si tiene inscripciones antes de eliminar.
    """
    if not id_estudiante:
        raise ValueError("Seleccione un estudiante para eliminar.")
    model_estudiantes.eliminar(id_estudiante)
