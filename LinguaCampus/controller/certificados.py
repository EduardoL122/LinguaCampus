# controller/certificados.py
# Logica de negocio para el modulo de certificados.

from model import certificados as model_certificados


def ctrl_obtener_certificados(): # Retorna todos los certificados con datos relacionados.
    return model_certificados.obtener_todos()


def ctrl_guardar_certificado(estudiante_id, nivel_id, grupo_id, fecha, estado, id_certificado=None):
    """
    Valida los campos del formulario de certificado.
    El modelo verifica que el promedio sea >= 3.5 antes de insertar.
    """
    # Validaciones de campos obligatorios
    if not estudiante_id:
        raise ValueError("Debe seleccionar un estudiante.")
    if not nivel_id:
        raise ValueError("Debe seleccionar un nivel.")
    if not grupo_id:
        raise ValueError("Debe seleccionar un grupo.")
    if not fecha.strip():
        raise ValueError("La fecha es obligatoria.")
    if not estado:
        raise ValueError("Debe seleccionar el estado del certificado.")

    if id_certificado:
        model_certificados.actualizar(id_certificado, estudiante_id, nivel_id,
                                      grupo_id, fecha, estado)
    else:
        # El modelo valida el promedio minimo al insertar
        model_certificados.insertar(estudiante_id, nivel_id, grupo_id, fecha, estado)


def ctrl_eliminar_certificado(id_certificado): # Solicita al modelo eliminar el certificado por su ID.
    if not id_certificado:
        raise ValueError("Seleccione un certificado para eliminar.")
    model_certificados.eliminar(id_certificado)
