# controller/reportes.py
# Logica de negocio para el modulo de reportes.
# Prepara los parametros de filtro y llama al modelo.

from model import reportes as model_reportes


def ctrl_reporte_aptos():
    """
    Retorna los estudiantes aptos para certificacion
    (promedio >= 3.5 en su grupo).
    """
    return model_reportes.reporte_aptos_certificacion()


def ctrl_reporte_completo():
    """
    Retorna la vista completa: estudiante, grupo, idioma,
    nivel, docente y calificaciones por modulo.
    """
    return model_reportes.reporte_completo()


def ctrl_filtrar_estudiantes(idioma_id=None, nivel_id=None, estado_ins=None):
    """
    Filtra estudiantes segun los parametros recibidos.
    Los valores None significan 'sin filtro' para ese campo.
    """
    return model_reportes.filtrar_estudiantes(idioma_id, nivel_id, estado_ins)
