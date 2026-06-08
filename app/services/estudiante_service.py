from app.extensions import db
from models.estudiante import Estudiante, EstudianteAcudiente
from models.acudiente import Acudiente
from models.grupo import Grupo
from datetime import datetime
from sqlalchemy import or_, func


class EstudianteService:

    @staticmethod
    def get_all_by_colegio(colegio_id, page=1, per_page=10, search=None,
                           grado=None, grupo_id=None, activo=True):
        """
        Obtener estudiantes de un colegio con paginación y filtros

        Args:
            colegio_id: ID del colegio
            page: Página actual
            per_page: Registros por página
            search: Término de búsqueda (nombre)
            grado: Filtrar por grado
            grupo_id: Filtrar por grupo específico
            activo: Solo activos o todos

        Returns:
            dict: Estudiantes paginados y metadata
        """
        query = Estudiante.query.filter_by(colegio_id=colegio_id)

        if activo is not None:
            query = query.filter_by(activo=activo)

        # Búsqueda por nombre
        if search:
            search_term = f'%{search}%'
            query = query.filter(Estudiante.nombre.ilike(search_term))

        # Filtro por grado
        if grado:
            query = query.filter_by(grado=grado)

        # Filtro por grupo específico
        if grupo_id:
            query = query.filter_by(grupo_id=grupo_id)

        # Ordenar por nombre
        query = query.order_by(Estudiante.nombre.asc())

        # Paginación
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return {
            'estudiantes': pagination.items,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }

    @staticmethod
    def get_by_id(estudiante_id, colegio_id):
        """
        Obtener estudiante por ID validando que pertenezca al colegio

        Args:
            estudiante_id: ID del estudiante
            colegio_id: ID del colegio (para validación de seguridad)

        Returns:
            Estudiante o None
        """
        return Estudiante.query.filter_by(
            id=estudiante_id,
            colegio_id=colegio_id,
            activo=True
        ).first()

    @staticmethod
    def create(data, colegio_id):
        """
        Crear un nuevo estudiante

        Args:
            data: Diccionario con los datos del estudiante
            colegio_id: ID del colegio

        Returns:
            tuple: (estudiante, error) - estudiante creado o None, error o None
        """
        try:
            # Validar que el acudiente principal exista y pertenezca al colegio
            acudiente = Acudiente.query.filter_by(
                id=data['acudiente_principal_id'],
                colegio_id=colegio_id
            ).first()

            if not acudiente:
                return None, 'El acudiente principal no existe o no pertenece al colegio'

            # Validar que el teléfono no esté duplicado en el mismo colegio
            existing_phone = Estudiante.query.filter_by(
                telefono=data['telefono'],
                colegio_id=colegio_id,
                activo=True
            ).first()

            if existing_phone:
                return None, 'Ya existe un estudiante con ese teléfono en el colegio'

            # Crear estudiante
            estudiante = Estudiante(
                nombre=data['nombre'].upper().strip(),
                direccion=data['direccion'].strip(),
                telefono=data['telefono'].strip(),
                colegio_id=colegio_id,
                acudiente_principal_id=data['acudiente_principal_id'],
                activo=True
            )

            # Si se proporciona grupo_id, actualizar datos automáticamente
            if data.get('grupo_id'):
                grupo = Grupo.query.get(data['grupo_id'])
                if grupo:
                    estudiante.grupo_id = grupo.id
                    estudiante.actualizar_datos_grupo()

            # Si se proporciona docente_id (opcional)
            if data.get('docente_id'):
                estudiante.docente_id = data['docente_id']

            # Generar QR token automáticamente
            estudiante.generar_qr_token()

            # Guardar en base de datos
            db.session.add(estudiante)
            db.session.flush()  # Para obtener el ID

            # Agregar acudientes adicionales si existen
            if data.get('acudientes_adicionales'):
                for acudiente_id in data['acudientes_adicionales']:
                    # Validar que no sea el mismo que el principal
                    if acudiente_id != data['acudiente_principal_id']:
                        relacion = EstudianteAcudiente(
                            estudiante_id=estudiante.id,
                            acudiente_id=acudiente_id
                        )
                        db.session.add(relacion)

            db.session.commit()
            return estudiante, None

        except Exception as e:
            db.session.rollback()
            return None, f'Error al crear estudiante: {str(e)}'

    @staticmethod
    def update(estudiante_id, data, colegio_id):
        """
        Actualizar un estudiante existente

        Args:
            estudiante_id: ID del estudiante
            data: Diccionario con los datos a actualizar
            colegio_id: ID del colegio (para validación)

        Returns:
            tuple: (estudiante, error)
        """
        estudiante = EstudianteService.get_by_id(estudiante_id, colegio_id)

        if not estudiante:
            return None, 'Estudiante no encontrado'

        try:
            # Validar acudiente principal si se cambia
            if data.get('acudiente_principal_id'):
                acudiente = Acudiente.query.filter_by(
                    id=data['acudiente_principal_id'],
                    colegio_id=colegio_id
                ).first()

                if not acudiente:
                    return None, 'El acudiente principal no existe o no pertenece al colegio'

                estudiante.acudiente_principal_id = data['acudiente_principal_id']

            # Validar teléfono único si se cambia
            if data.get('telefono') and data['telefono'] != estudiante.telefono:
                existing_phone = Estudiante.query.filter(
                    Estudiante.telefono == data['telefono'],
                    Estudiante.colegio_id == colegio_id,
                    Estudiante.id != estudiante_id,
                    Estudiante.activo == True
                ).first()

                if existing_phone:
                    return None, 'Ya existe un estudiante con ese teléfono en el colegio'

                estudiante.telefono = data['telefono'].strip()

            # Actualizar campos básicos
            if data.get('nombre'):
                estudiante.nombre = data['nombre'].upper().strip()

            if data.get('direccion'):
                estudiante.direccion = data['direccion'].strip()

            # Actualizar grupo y datos relacionados
            if data.get('grupo_id'):
                grupo = Grupo.query.get(data['grupo_id'])
                if grupo:
                    estudiante.grupo_id = grupo.id
                    estudiante.actualizar_datos_grupo()

            # Actualizar docente (puede ser NULL)
            if 'docente_id' in data:
                estudiante.docente_id = data['docente_id']

            # Actualizar acudientes adicionales
            if 'acudientes_adicionales' in data:
                # Eliminar relaciones actuales
                EstudianteAcudiente.query.filter_by(
                    estudiante_id=estudiante.id
                ).delete()

                # Agregar nuevas relaciones
                for acudiente_id in data['acudientes_adicionales']:
                    if acudiente_id != estudiante.acudiente_principal_id:
                        relacion = EstudianteAcudiente(
                            estudiante_id=estudiante.id,
                            acudiente_id=acudiente_id
                        )
                        db.session.add(relacion)

            db.session.commit()
            return estudiante, None

        except Exception as e:
            db.session.rollback()
            return None, f'Error al actualizar estudiante: {str(e)}'

    @staticmethod
    def delete(estudiante_id, colegio_id):
        """
        Eliminar lógicamente un estudiante (marcar como inactivo)

        Args:
            estudiante_id: ID del estudiante
            colegio_id: ID del colegio

        Returns:
            tuple: (success, error)
        """
        estudiante = EstudianteService.get_by_id(estudiante_id, colegio_id)

        if not estudiante:
            return False, 'Estudiante no encontrado'

        try:
            estudiante.activo = False
            db.session.commit()
            return True, None

        except Exception as e:
            db.session.rollback()
            return False, f'Error al eliminar estudiante: {str(e)}'

    @staticmethod
    def get_acudientes_by_estudiante(estudiante_id, colegio_id):
        """
        Obtener todos los acudientes de un estudiante (principal + adicionales)

        Args:
            estudiante_id: ID del estudiante
            colegio_id: ID del colegio

        Returns:
            list: Lista de acudientes
        """
        estudiante = EstudianteService.get_by_id(estudiante_id, colegio_id)

        if not estudiante:
            return []

        # Obtener acudiente principal
        acudientes = [estudiante.acudiente_principal]

        # Obtener acudientes adicionales
        relaciones = EstudianteAcudiente.query.filter_by(
            estudiante_id=estudiante.id
        ).all()

        for relacion in relaciones:
            acudiente = Acudiente.query.get(relacion.acudiente_id)
            if acudiente and acudiente.id != estudiante.acudiente_principal_id:
                acudientes.append(acudiente)

        return acudientes

    @staticmethod
    def get_estadisticas(colegio_id):
        """
        Obtener estadísticas de estudiantes del colegio

        Args:
            colegio_id: ID del colegio

        Returns:
            dict: Estadísticas
        """
        # Total de estudiantes activos
        total = Estudiante.query.filter_by(
            colegio_id=colegio_id,
            activo=True
        ).count()

        # Por grado
        grados = db.session.query(
            Estudiante.grado,
            func.count(Estudiante.id)
        ).filter_by(
            colegio_id=colegio_id,
            activo=True
        ).group_by(Estudiante.grado).all()

        # Por grupo
        grupos = db.session.query(
            Estudiante.grupo,
            func.count(Estudiante.id)
        ).filter_by(
            colegio_id=colegio_id,
            activo=True
        ).group_by(Estudiante.grupo).all()

        return {
            'total': total,
            'por_grado': {g: c for g, c in grados if g},
            'por_grupo': {g: c for g, c in grupos if g}
        }

    @staticmethod
    def verificar_pertenencia(estudiante_id, colegio_id):
        """
        Verificar que un estudiante pertenezca al colegio especificado

        Args:
            estudiante_id: ID del estudiante
            colegio_id: ID del colegio

        Returns:
            bool: True si pertenece, False si no
        """
        estudiante = Estudiante.query.filter_by(
            id=estudiante_id,
            colegio_id=colegio_id,
            activo=True
        ).first()

        return estudiante is not None