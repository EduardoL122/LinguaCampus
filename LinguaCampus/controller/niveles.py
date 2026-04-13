# controller/niveles.py
# Logica de negocio para el modulo de niveles.

from model import niveles as model_niveles


def ctrl_obtener_niveles(): # Retorna todos los niveles con su idioma desde el modelo.
    return model_niveles.obtener_todos()


def ctrl_guardar_nivel(nombre, idioma_id, id_nivel=None):
    """
    Valida el nombre del nivel y llama a insertar o actualizar.
    idioma_id puede ser None si el nivel no tiene idioma asignado.
    """
    # Validacion: el nombre es obligatorio
    if not nombre.strip():
        raise ValueError("El nombre del nivel es obligatorio.")

    if id_nivel:
        model_niveles.actualizar(id_nivel, nombre.strip(), idioma_id)
    else:
        model_niveles.insertar(nombre.strip(), idioma_id)


def ctrl_eliminar_nivel(id_nivel):
    """
    Solicita al modelo eliminar el nivel.
    El modelo verifica si el nivel esta asignado a algun grupo.
    """
    if not id_nivel:
        raise ValueError("Seleccione un nivel para eliminar.")
    model_niveles.eliminar(id_nivel)