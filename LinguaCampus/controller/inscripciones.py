# controller/inscripciones.py
# Logica de negocio para el modulo de inscripciones.

from model import inscripciones as model_inscripciones


def ctrl_obtener_inscripciones(): # Retorna todas las inscripciones con datos relacionados desde el modelo.
    return model_inscripciones.obtener_todas()


def ctrl_guardar_inscripcion(estudiante_id, grupo_id, fecha, estado, id_inscripcion=None):
    """
    Valida los campos del formulario de inscripcion.
    El modelo se encarga de verificar el cupo y duplicados.
    """
    # Validaciones de campos obligatorios
    if not estudiante_id:
        raise ValueError("Debe seleccionar un estudiante.")
    if not grupo_id:
        raise ValueError("Debe seleccionar un grupo.")
    if not fecha.strip():
        raise ValueError("La fecha de inscripcion es obligatoria.")
    if not estado:
        raise ValueError("Debe seleccionar el estado.")

    if id_inscripcion:
        model_inscripciones.actualizar(id_inscripcion, estudiante_id, grupo_id, fecha, estado)
    else:
        model_inscripciones.insertar(estudiante_id, grupo_id, fecha, estado)


def ctrl_eliminar_inscripcion(id_inscripcion): # Solicita al modelo eliminar la inscripcion por su ID.
    if not id_inscripcion:
        raise ValueError("Seleccione una inscripcion para eliminar.")
    model_inscripciones.eliminar(id_inscripcion)
