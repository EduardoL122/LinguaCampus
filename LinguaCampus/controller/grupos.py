# controller/grupos.py
# Logica de negocio para el modulo de grupos.

from model import grupos as model_grupos


def ctrl_obtener_grupos(): # Retorna todos los grupos con sus datos relacionados desde el modelo.
    return model_grupos.obtener_todos()


def ctrl_guardar_grupo(idioma_id, nivel_id, docente_id, nombre_grupo, horario, cupo_maximo, id_grupo=None):
    """
    Valida todos los campos del formulario de grupos.
    El cupo debe ser un numero entero positivo.
    El modelo se encarga de verificar conflictos de horario.
    """
    # Validaciones de campos obligatorios
    if not nombre_grupo.strip():
        raise ValueError("El nombre del grupo es obligatorio.")
    if not horario.strip():
        raise ValueError("El horario es obligatorio.")
    if not idioma_id:
        raise ValueError("Debe seleccionar un idioma.")
    if not nivel_id:
        raise ValueError("Debe seleccionar un nivel.")
    if not docente_id:
        raise ValueError("Debe seleccionar un docente.")

    # Validar que el cupo sea un numero entero positivo
    try:
        cupo = int(cupo_maximo)
        if cupo <= 0:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("El cupo maximo debe ser un numero entero positivo.")

    if id_grupo:
        model_grupos.actualizar(id_grupo, idioma_id, nivel_id, docente_id,
                                nombre_grupo.strip(), horario.strip(), cupo)
    else:
        model_grupos.insertar(idioma_id, nivel_id, docente_id,
                              nombre_grupo.strip(), horario.strip(), cupo)


def ctrl_eliminar_grupo(id_grupo):
    """
    Solicita al modelo eliminar el grupo.
    El modelo verifica si tiene inscripciones antes de eliminar.
    """
    if not id_grupo:
        raise ValueError("Seleccione un grupo para eliminar.")
    model_grupos.eliminar(id_grupo)
