"""Catalogo de claves de permisos finos.

Cada clave representa un permiso configurable por el admin del colegio.
Las claves estan agrupadas por area funcional.
"""

# ─────────────────────────────────────────────────────────────
# SECRETARIA — Acceso a modulos del sidebar
# ─────────────────────────────────────────────────────────────

SECRETARIA_VER_DOCENTES = 'secretaria.ver_docentes'
SECRETARIA_VER_ESTUDIANTES = 'secretaria.ver_estudiantes'
SECRETARIA_VER_ACUDIENTES = 'secretaria.ver_acudientes'
SECRETARIA_VER_COORDINADORES = 'secretaria.ver_coordinadores'
SECRETARIA_VER_PORTEROS = 'secretaria.ver_porteros'


# ─────────────────────────────────────────────────────────────
# CATALOGO COMPLETO (para UI y validaciones)
# ─────────────────────────────────────────────────────────────

CATALOGO = {
    SECRETARIA_VER_DOCENTES: {
        'titulo': 'Ver Docentes',
        'descripcion': 'Acceso al listado y gestion de docentes.',
        'grupo': 'Secretaria',
    },
    SECRETARIA_VER_ESTUDIANTES: {
        'titulo': 'Ver Estudiantes',
        'descripcion': 'Acceso al listado y gestion de estudiantes.',
        'grupo': 'Secretaria',
    },
    SECRETARIA_VER_ACUDIENTES: {
        'titulo': 'Ver Acudientes',
        'descripcion': 'Acceso al listado y gestion de acudientes.',
        'grupo': 'Secretaria',
    },
    SECRETARIA_VER_COORDINADORES: {
        'titulo': 'Ver Coordinadores',
        'descripcion': 'Acceso al listado y gestion de coordinadores.',
        'grupo': 'Secretaria',
    },
    SECRETARIA_VER_PORTEROS: {
        'titulo': 'Ver Porteros',
        'descripcion': 'Acceso al listado y gestion de porteros.',
        'grupo': 'Secretaria',
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
