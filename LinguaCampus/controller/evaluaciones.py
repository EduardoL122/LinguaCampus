# controller/evaluaciones.py
# Logica de negocio para el modulo de evaluaciones.

from model import evaluaciones as model_evaluaciones


def ctrl_obtener_evaluaciones(): # Retorna todas las evaluaciones con datos relacionados desde el modelo.
    return model_evaluaciones.obtener_todas()


def ctrl_guardar_evaluacion(estudiante_id, grupo_id, modulo, nota, id_evaluacion=None):
    """
    Valida los campos del formulario de evaluacion.
    La nota debe ser un numero decimal entre 0.0 y 5.0.
    """
    # Validaciones de campos obligatorios
    if not estudiante_id:
        raise ValueError("Debe seleccionar un estudiante.")
    if not grupo_id:
        raise ValueError("Debe seleccionar un grupo.")
    if not modulo.strip():
        raise ValueError("El modulo es obligatorio.")

    # Validar que la nota sea un numero en rango valido
    try:
        nota_float = float(nota)
        if not (0.0 <= nota_float <= 5.0):
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("La nota debe ser un numero entre 0.0 y 5.0.")

    if id_evaluacion:
        model_evaluaciones.actualizar(id_evaluacion, estudiante_id, grupo_id,
                                      modulo.strip(), nota_float)
    else:
        model_evaluaciones.insertar(estudiante_id, grupo_id, modulo.strip(), nota_float)


def ctrl_eliminar_evaluacion(id_evaluacion): # Solicita al modelo eliminar la evaluacion por su ID.
    if not id_evaluacion:
        raise ValueError("Seleccione una evaluacion para eliminar.")
    model_evaluaciones.eliminar(id_evaluacion)
