"""Catalogo de claves de permisos finos.

Cada clave representa un permiso configurable por el admin del colegio.
Las claves estan agrupadas por area funcional y entidad.
"""

# ─────────────────────────────────────────────────────────────
# SECRETARIA — Docentes
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_DOCENTES = 'secretaria.ver_docentes'
SECRETARIA_CREAR_DOCENTES = 'secretaria.crear_docentes'
SECRETARIA_EDITAR_DOCENTES = 'secretaria.editar_docentes'
SECRETARIA_ELIMINAR_DOCENTES = 'secretaria.eliminar_docentes'


# ─────────────────────────────────────────────────────────────
# SECRETARIA — Estudiantes
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_ESTUDIANTES = 'secretaria.ver_estudiantes'
SECRETARIA_CREAR_ESTUDIANTES = 'secretaria.crear_estudiantes'
SECRETARIA_EDITAR_ESTUDIANTES = 'secretaria.editar_estudiantes'
SECRETARIA_ELIMINAR_ESTUDIANTES = 'secretaria.eliminar_estudiantes'


# ─────────────────────────────────────────────────────────────
# SECRETARIA — Acudientes
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_ACUDIENTES = 'secretaria.ver_acudientes'
SECRETARIA_CREAR_ACUDIENTES = 'secretaria.crear_acudientes'
SECRETARIA_EDITAR_ACUDIENTES = 'secretaria.editar_acudientes'
SECRETARIA_ELIMINAR_ACUDIENTES = 'secretaria.eliminar_acudientes'


# ─────────────────────────────────────────────────────────────
# SECRETARIA — Coordinadores
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_COORDINADORES = 'secretaria.ver_coordinadores'
SECRETARIA_CREAR_COORDINADORES = 'secretaria.crear_coordinadores'
SECRETARIA_EDITAR_COORDINADORES = 'secretaria.editar_coordinadores'
SECRETARIA_ELIMINAR_COORDINADORES = 'secretaria.eliminar_coordinadores'


# ─────────────────────────────────────────────────────────────
# SECRETARIA — Porteros
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_PORTEROS = 'secretaria.ver_porteros'
SECRETARIA_CREAR_PORTEROS = 'secretaria.crear_porteros'
SECRETARIA_EDITAR_PORTEROS = 'secretaria.editar_porteros'
SECRETARIA_ELIMINAR_PORTEROS = 'secretaria.eliminar_porteros'


# ─────────────────────────────────────────────────────────────
# SECRETARIA — Profesionales PIAR
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_PROFESIONAL_PIAR = 'secretaria.ver_profesional_piar'
SECRETARIA_CREAR_PROFESIONAL_PIAR = 'secretaria.crear_profesional_piar'
SECRETARIA_EDITAR_PROFESIONAL_PIAR = 'secretaria.editar_profesional_piar'
SECRETARIA_ELIMINAR_PROFESIONAL_PIAR = 'secretaria.eliminar_profesional_piar'


# ─────────────────────────────────────────────────────────────
# SECRETARIA — Psicólogos
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_PSICOLOGOS = 'secretaria.ver_psicologos'
SECRETARIA_CREAR_PSICOLOGOS = 'secretaria.crear_psicologos'
SECRETARIA_EDITAR_PSICOLOGOS = 'secretaria.editar_psicologos'
SECRETARIA_ELIMINAR_PSICOLOGOS = 'secretaria.eliminar_psicologos'



# ─────────────────────────────────────────────────────────────
# SECRETARIA — Sedes
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_SEDES = 'secretaria.ver_sedes'
SECRETARIA_CREAR_SEDES = 'secretaria.crear_sedes'
SECRETARIA_EDITAR_SEDES = 'secretaria.editar_sedes'


# ─────────────────────────────────────────────────────────────
# SECRETARIA — Jornadas
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_JORNADAS = 'secretaria.ver_jornadas'
SECRETARIA_CREAR_JORNADAS = 'secretaria.crear_jornadas'
SECRETARIA_EDITAR_JORNADAS = 'secretaria.editar_jornadas'


# ─────────────────────────────────────────────────────────────
# SECRETARIA — Grupos
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_GRUPOS = 'secretaria.ver_grupos'
SECRETARIA_CREAR_GRUPOS = 'secretaria.crear_grupos'
SECRETARIA_EDITAR_GRUPOS = 'secretaria.editar_grupos'
SECRETARIA_ELIMINAR_GRUPOS = 'secretaria.eliminar_grupos'

# ─────────────────────────────────────────────────────────────
# CATALOGO COMPLETO (para UI y validaciones)
# ─────────────────────────────────────────────────────────────

CATALOGO = {
    # Docentes
    SECRETARIA_VER_DOCENTES: {
        'titulo': 'Ver Docentes',
        'descripcion': 'Acceso al listado de docentes.',
        'grupo': 'Secretaría · Docentes',
    },
    SECRETARIA_CREAR_DOCENTES: {
        'titulo': 'Crear Docentes',
        'descripcion': 'Permite crear nuevos docentes.',
        'grupo': 'Secretaría · Docentes',
    },
    SECRETARIA_EDITAR_DOCENTES: {
        'titulo': 'Editar Docentes',
        'descripcion': 'Permite editar docentes existentes.',
        'grupo': 'Secretaría · Docentes',
    },
    SECRETARIA_ELIMINAR_DOCENTES: {
        'titulo': 'Eliminar Docentes',
        'descripcion': 'Permite eliminar docentes.',
        'grupo': 'Secretaría · Docentes',
    },

    # Estudiantes
    SECRETARIA_VER_ESTUDIANTES: {
        'titulo': 'Ver Estudiantes',
        'descripcion': 'Acceso al listado de estudiantes.',
        'grupo': 'Secretaría · Estudiantes',
    },
    SECRETARIA_CREAR_ESTUDIANTES: {
        'titulo': 'Crear Estudiantes',
        'descripcion': 'Permite crear nuevos estudiantes.',
        'grupo': 'Secretaría · Estudiantes',
    },
    SECRETARIA_EDITAR_ESTUDIANTES: {
        'titulo': 'Editar Estudiantes',
        'descripcion': 'Permite editar estudiantes existentes.',
        'grupo': 'Secretaría · Estudiantes',
    },
    SECRETARIA_ELIMINAR_ESTUDIANTES: {
        'titulo': 'Eliminar Estudiantes',
        'descripcion': 'Permite eliminar estudiantes.',
        'grupo': 'Secretaría · Estudiantes',
    },

    # Acudientes
    SECRETARIA_VER_ACUDIENTES: {
        'titulo': 'Ver Acudientes',
        'descripcion': 'Acceso al listado de acudientes.',
        'grupo': 'Secretaría · Acudientes',
    },
    SECRETARIA_CREAR_ACUDIENTES: {
        'titulo': 'Crear Acudientes',
        'descripcion': 'Permite crear nuevos acudientes.',
        'grupo': 'Secretaría · Acudientes',
    },
    SECRETARIA_EDITAR_ACUDIENTES: {
        'titulo': 'Editar Acudientes',
        'descripcion': 'Permite editar acudientes existentes.',
        'grupo': 'Secretaría · Acudientes',
    },
    SECRETARIA_ELIMINAR_ACUDIENTES: {
        'titulo': 'Eliminar Acudientes',
        'descripcion': 'Permite eliminar acudientes.',
        'grupo': 'Secretaría · Acudientes',
    },

    # Coordinadores
    SECRETARIA_VER_COORDINADORES: {
        'titulo': 'Ver Coordinadores',
        'descripcion': 'Acceso al listado de coordinadores.',
        'grupo': 'Secretaría · Coordinadores',
    },
    SECRETARIA_CREAR_COORDINADORES: {
        'titulo': 'Crear Coordinadores',
        'descripcion': 'Permite crear nuevos coordinadores.',
        'grupo': 'Secretaría · Coordinadores',
    },
    SECRETARIA_EDITAR_COORDINADORES: {
        'titulo': 'Editar Coordinadores',
        'descripcion': 'Permite editar coordinadores existentes.',
        'grupo': 'Secretaría · Coordinadores',
    },
    SECRETARIA_ELIMINAR_COORDINADORES: {
        'titulo': 'Eliminar Coordinadores',
        'descripcion': 'Permite eliminar coordinadores.',
        'grupo': 'Secretaría · Coordinadores',
    },

    # Porteros
    SECRETARIA_VER_PORTEROS: {
        'titulo': 'Ver Porteros',
        'descripcion': 'Acceso al listado de porteros.',
        'grupo': 'Secretaría · Porteros',
    },
    SECRETARIA_CREAR_PORTEROS: {
        'titulo': 'Crear Porteros',
        'descripcion': 'Permite crear nuevos porteros.',
        'grupo': 'Secretaría · Porteros',
    },
    SECRETARIA_EDITAR_PORTEROS: {
        'titulo': 'Editar Porteros',
        'descripcion': 'Permite editar porteros existentes.',
        'grupo': 'Secretaría · Porteros',
    },
    SECRETARIA_ELIMINAR_PORTEROS: {
        'titulo': 'Eliminar Porteros',
        'descripcion': 'Permite eliminar porteros.',
        'grupo': 'Secretaría · Porteros',
    },

    # Profesionales PIAR
    SECRETARIA_VER_PROFESIONAL_PIAR: {
        'titulo': 'Ver Profesionales PIAR',
        'descripcion': 'Acceso al listado de profesionales PIAR.',
        'grupo': 'Secretaría · Profesionales PIAR',
    },
    SECRETARIA_CREAR_PROFESIONAL_PIAR: {
        'titulo': 'Crear Profesionales PIAR',
        'descripcion': 'Permite crear nuevos profesionales PIAR.',
        'grupo': 'Secretaría · Profesionales PIAR',
    },
    SECRETARIA_EDITAR_PROFESIONAL_PIAR: {
        'titulo': 'Editar Profesionales PIAR',
        'descripcion': 'Permite editar profesionales PIAR existentes.',
        'grupo': 'Secretaría · Profesionales PIAR',
    },
    SECRETARIA_ELIMINAR_PROFESIONAL_PIAR: {
        'titulo': 'Eliminar Profesionales PIAR',
        'descripcion': 'Permite eliminar profesionales PIAR.',
        'grupo': 'Secretaría · Profesionales PIAR',
    },

    # Psicólogos
    SECRETARIA_VER_PSICOLOGOS: {
        'titulo': 'Ver Psicólogos',
        'descripcion': 'Acceso al listado de psicólogos.',
        'grupo': 'Secretaría · Psicólogos',
    },
    SECRETARIA_CREAR_PSICOLOGOS: {
        'titulo': 'Crear Psicólogos',
        'descripcion': 'Permite crear nuevos psicólogos.',
        'grupo': 'Secretaría · Psicólogos',
    },
    SECRETARIA_EDITAR_PSICOLOGOS: {
        'titulo': 'Editar Psicólogos',
        'descripcion': 'Permite editar psicólogos existentes.',
        'grupo': 'Secretaría · Psicólogos',
    },
    SECRETARIA_ELIMINAR_PSICOLOGOS: {
        'titulo': 'Eliminar Psicólogos',
        'descripcion': 'Permite eliminar psicólogos.',
        'grupo': 'Secretaría · Psicólogos',
    },

    SECRETARIA_ELIMINAR_PSICOLOGOS: {
        'titulo': 'Eliminar Psicólogos',
        'descripcion': 'Permite eliminar psicólogos.',
        'grupo': 'Secretaría · Psicólogos',
    },

    # Sedes
    SECRETARIA_VER_SEDES: {
        'titulo': 'Ver Sedes',
        'descripcion': 'Acceso al listado de sedes.',
        'grupo': 'Secretaría · Sedes',
    },
    SECRETARIA_CREAR_SEDES: {
        'titulo': 'Crear Sedes',
        'descripcion': 'Permite crear nuevas sedes.',
        'grupo': 'Secretaría · Sedes',
    },
    SECRETARIA_EDITAR_SEDES: {
        'titulo': 'Editar Sedes',
        'descripcion': 'Permite editar sedes existentes.',
        'grupo': 'Secretaría · Sedes',
    },

    # Jornadas
    SECRETARIA_VER_JORNADAS: {
        'titulo': 'Ver Jornadas',
        'descripcion': 'Acceso al listado de jornadas.',
        'grupo': 'Secretaría · Jornadas',
    },
    SECRETARIA_CREAR_JORNADAS: {
        'titulo': 'Crear Jornadas',
        'descripcion': 'Permite crear nuevas jornadas.',
        'grupo': 'Secretaría · Jornadas',
    },
    SECRETARIA_EDITAR_JORNADAS: {
        'titulo': 'Editar Jornadas',
        'descripcion': 'Permite editar jornadas existentes.',
        'grupo': 'Secretaría · Jornadas',
    },

    # Grupos
    SECRETARIA_VER_GRUPOS: {
        'titulo': 'Ver Grupos',
        'descripcion': 'Acceso al listado de grupos.',
        'grupo': 'Secretaría · Grupos',
    },
    SECRETARIA_CREAR_GRUPOS: {
        'titulo': 'Crear Grupos',
        'descripcion': 'Permite crear nuevos grupos.',
        'grupo': 'Secretaría · Grupos',
    },
    SECRETARIA_EDITAR_GRUPOS: {
        'titulo': 'Editar Grupos',
        'descripcion': 'Permite editar grupos existentes.',
        'grupo': 'Secretaría · Grupos',
    },
    SECRETARIA_ELIMINAR_GRUPOS: {
        'titulo': 'Eliminar Grupos',
        'descripcion': 'Permite eliminar grupos.',
        'grupo': 'Secretaría · Grupos',
    },
}


def claves_validas():
    """Devuelve la lista de todas las claves validas."""
    return list(CATALOGO.keys())


def clave_existe(clave):
    """Verifica si una clave existe en el catalogo."""
    return clave in CATALOGO


def catalogo_por_grupo():
    """Devuelve el catalogo agrupado por 'grupo'.

    Util para la UI del admin.
    """
    agrupado = {}
    for clave, datos in CATALOGO.items():
        grupo = datos['grupo']
        if grupo not in agrupado:
            agrupado[grupo] = []
        agrupado[grupo].append({
            'clave': clave,
            'titulo': datos['titulo'],
            'descripcion': datos['descripcion'],
        })
    return agrupado