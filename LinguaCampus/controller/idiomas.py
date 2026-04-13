# controller/idiomas.py
# Logica de negocio para el modulo de idiomas.
# Valida los datos del formulario antes de llamar al modelo.

from model import idiomas as model_idiomas


def ctrl_obtener_idiomas(): # Retorna la lista de todos los idiomas desde el modelo.
    return model_idiomas.obtener_todos()


def ctrl_guardar_idioma(nombre, id_idioma=None):
    """
    Valida el nombre y llama a insertar o actualizar segun
    si se recibe un ID (edicion) o no (nuevo registro).
    """
    # Validacion: el nombre no puede estar vacio
    if not nombre.strip():
        raise ValueError("El nombre del idioma es obligatorio.")

    if id_idioma:
        # Actualizar idioma existente
        model_idiomas.actualizar(id_idioma, nombre.strip())
    else:
        # Insertar nuevo idioma
        model_idiomas.insertar(nombre.strip())


def ctrl_eliminar_idioma(id_idioma):
    """
    Llama al modelo para eliminar el idioma.
    El modelo verifica si hay dependencias antes de eliminar.
    """
    if not id_idioma:
        raise ValueError("Seleccione un idioma para eliminar.")
    model_idiomas.eliminar(id_idioma)
