# controller/docentes.py
# Logica de negocio para el modulo de docentes.

from model import docentes as model_docentes


def ctrl_obtener_docentes(): # Retorna todos lo sdocentes con su idioma desde el modelo.
    return model_docentes.obtener_todos()


def ctrl_guardar_docente(nombre, idioma_id, nivel_certificado, estado, id_docente=None):
    """
    Valida los campos obligatorios del formulario de docentes
    y llama a insertar o actualizar segun corresponda.
    """
    # Validaciones de campos obligatorios
    if not nombre.strip():
        raise ValueError("El nombre del docente es obligatorio.")
    if not nivel_certificado:
        raise ValueError("Debe seleccionar el nivel certificado.")
    if not estado:
        raise ValueError("Debe seleccionar el estado del docente.")

    if id_docente:
        model_docentes.actualizar(id_docente, nombre.strip(), idioma_id, nivel_certificado, estado)
    else:
        model_docentes.insertar(nombre.strip(), idioma_id, nivel_certificado, estado)


def ctrl_eliminar_docente(id_docente):
    """
    Solicita al modelo eliminar el docente.
    El modelo verifica si tiene grupos asignados antes de eliminar.
    """
    if not id_docente:
        raise ValueError("Seleccione un docente para eliminar.")
    model_docentes.eliminar(id_docente)
