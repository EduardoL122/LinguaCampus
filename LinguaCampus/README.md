# LinguaCampus — Sistema de Gestion de Escuela de Idiomas

Proyecto 12 — SENA  
Desarrollado en Python con Tkinter y MySQL. Arquitectura MVC con funciones.

---

## Estructura del Proyecto

```
LinguaCampus/
├── main.py                      # Punto de entrada
├── config/
│   └── db.py                    # Configuracion de conexion MySQL
├── model/
│   ├── login.py                 # Consultas de autenticacion
│   ├── idiomas.py               # CRUD idiomas
│   ├── niveles.py               # CRUD niveles
│   ├── docentes.py              # CRUD docentes
│   ├── estudiantes.py           # CRUD estudiantes
│   ├── grupos.py                # CRUD grupos
│   ├── inscripciones.py         # CRUD inscripciones
│   ├── evaluaciones.py          # CRUD evaluaciones
│   ├── certificados.py          # CRUD certificados
│   └── reportes.py              # Consultas con JOIN para reportes
├── controller/
│   ├── login.py                 # Logica de autenticacion
│   ├── idiomas.py               # Logica de idiomas
│   ├── niveles.py               # Logica de niveles
│   ├── docentes.py              # Logica de docentes
│   ├── estudiantes.py           # Logica de estudiantes
│   ├── grupos.py                # Logica de grupos
│   ├── inscripciones.py         # Logica de inscripciones
│   ├── evaluaciones.py          # Logica de evaluaciones
│   ├── certificados.py          # Logica de certificados
│   └── reportes.py              # Logica de reportes
├── view/
│   ├── utils.py                 # Funciones auxiliares compartidas
│   ├── login.py                 # Ventana de inicio de sesion
│   ├── menu.py                  # Menu principal de navegacion
│   ├── idiomas.py               # Modulo de idiomas
│   ├── niveles.py               # Modulo de niveles
│   ├── docentes.py              # Modulo de docentes
│   ├── estudiantes.py           # Modulo de estudiantes
│   ├── grupos.py                # Modulo de grupos
│   ├── inscripciones.py         # Modulo de inscripciones
│   ├── evaluaciones.py          # Modulo de evaluaciones
│   ├── certificados.py          # Modulo de certificados
│   └── reportes.py              # Modulo de reportes y filtros
└── Dump20260406.sql             # Script SQL de la base de datos
```

---

## Modulos del Sistema

| Modulo        | Descripcion                                          |
| ------------- | ---------------------------------------------------- |
| Login         | Autenticacion con usuario y contrasena               |
| Estudiantes   | CRUD con nombre, email y estado                      |
| Docentes      | CRUD con idioma, nivel certificado y estado          |
| Idiomas       | CRUD de idiomas disponibles                          |
| Niveles       | CRUD de niveles A1 a C2 por idioma                   |
| Grupos        | CRUD con idioma, nivel, docente, horario y cupo      |
| Inscripciones | Registro de estudiantes en grupos (muchos a muchos)  |
| Evaluaciones  | Notas por modulo dentro de cada grupo                |
| Certificados  | Emision validando promedio >= 3.5                    |
| Reportes      | Aptos para certificacion, reporte completo y filtros |

---

## Reglas de Negocio

- No se puede inscribir un estudiante si el grupo ya alcanzo el cupo maximo.
- Un docente no puede tener dos grupos con el mismo horario.
- El certificado solo se emite si el promedio del estudiante en el grupo es >= 3.5.
- No se puede eliminar un idioma que tenga grupos o niveles asociados.

---

## Herramientas

- Python 3.8+
- Tkinter (interfaz grafica)
- MySQL 8.0 (base de datos)
- mysql-connector-python (conector)

---

## Instalacion

```bash
# 1. Instalar dependencia
pip install mysql-connector-python

# 2. Importar la base de datos
mysql -u root -p < Dump20260406.sql

# 3. Ajustar credenciales en config/db.py

# 4. Ejecutar
python main.py
```

Credenciales por defecto: usuario `admin`, contraseña `1234`

---

## Autor

Nombre: [Eduardo Lara Padilla]  
Ficha: [3300632]  
SENA — 2026
