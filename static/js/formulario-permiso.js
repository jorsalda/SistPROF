// ============================================
// FORMULARIO DE PERMISOS - LÓGICA PROFESIONAL
// ============================================

class HistorialPermisos {
    constructor() {
        this.container = document.getElementById('historial-permisos');
        this.selectDocente = document.getElementById('docente_id');
        this.init();
    }

    init() {
        if (!this.selectDocente) {
            console.warn('Select de docente no encontrado');
            return;
        }

        // Evento al cambiar docente
        this.selectDocente.addEventListener('change', (e) => {
            this.cargarHistorial(e.target.value);
        });

        // Cargar automáticamente si hay docente en URL
        this.cargarDesdeURL();

        // Inicializar fechas
        this.inicializarFechas();
    }

    async cargarHistorial(docenteId) {
        if (!docenteId) {
            this.limpiarHistorial();
            return;
        }

        this.mostrarCargando();

        try {
            const response = await fetch(`/permisos/api/permisos-docente/${docenteId}`);

            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                this.mostrarHistorial(data);
            } else {
                this.mostrarError(data.error || 'Error desconocido');
            }

        } catch (error) {
            console.error('Error cargando historial:', error);
            this.mostrarError('Error de conexión con el servidor');
        }
    }

    mostrarCargando() {
        this.container.innerHTML = `
            <div class="historial-loading">
                <div>
                    <span class="loading-spinner"></span>
                    <span class="loading-text">Cargando historial de permisos...</span>
                </div>
            </div>
        `;
    }

    mostrarHistorial(data) {
        if (data.total === 0) {
            this.container.innerHTML = `
                <div class="alert alert-info">
                    <strong>📋 ${data.docente}</strong><br>
                    Este docente no tiene permisos registrados.
                </div>
            `;
            return;
        }

        const html = this.generarTablaHTML(data);
        this.container.innerHTML = html;
    }

    generarTablaHTML(data) {
        // Mapeo de tipos a clases CSS
        const tipoClases = {
            'Vacaciones': 'tipo-vacaciones',
            'Enfermedad': 'tipo-enfermedad',
            'Capacitación': 'tipo-capacitacion',
            'Permiso Personal': 'tipo-personal',
            'Licencia': 'tipo-licencia',
            'Otro': 'tipo-otro'
        };

        let filas = '';
        data.permisos.forEach(permiso => {
            const clase = tipoClases[permiso.tipo] || 'tipo-otro';

            filas += `
                <tr>
                    <td>
                        <span class="tipo-badge ${clase}">
                            ${permiso.tipo}
                        </span>
                    </td>
                    <td>${permiso.fecha_inicio}</td>
                    <td>${permiso.fecha_fin}</td>
                    <td class="text-center fw-bold">${permiso.dias}</td>
                    <td class="text-muted small">
                        ${permiso.observacion || '<em>Sin observación</em>'}
                    </td>
                </tr>
            `;
        });

        return `
            <div class="historial-container">
                <div class="historial-header">
                    <span>📋 Historial de permisos: ${data.docente}</span>
                    <span class="historial-badge">${data.total} permiso(s)</span>
                </div>

                <div class="historial-table-container">
                    <table class="historial-table">
                        <thead>
                            <tr>
                                <th>Tipo</th>
                                <th>Inicio</th>
                                <th>Fin</th>
                                <th>Días</th>
                                <th>Observación</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${filas}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    mostrarError(mensaje) {
        this.container.innerHTML = `
            <div class="alert alert-danger">
                <strong>❌ Error</strong><br>
                ${mensaje}
            </div>
        `;
    }

    limpiarHistorial() {
        this.container.innerHTML = '';
    }

    cargarDesdeURL() {
        const urlParams = new URLSearchParams(window.location.search);
        const docenteId = urlParams.get('docente_id');

        if (docenteId && this.selectDocente) {
            this.selectDocente.value = docenteId;
            // Pequeño delay para asegurar que el DOM esté listo
            setTimeout(() => this.cargarHistorial(docenteId), 100);
        }
    }

    inicializarFechas() {
        const hoy = new Date().toISOString().split('T')[0];
        const fechaInicio = document.getElementById('fecha_inicio');
        const fechaFin = document.getElementById('fecha_fin');

        if (fechaInicio && !fechaInicio.value) {
            fechaInicio.value = hoy;
        }
        if (fechaFin && !fechaFin.value) {
            fechaFin.value = hoy;
        }

        // Validación de fechas
        const form = document.getElementById('permiso-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                const inicio = fechaInicio.value;
                const fin = fechaFin.value;

                if (inicio && fin && new Date(fin) < new Date(inicio)) {
                    e.preventDefault();
                    alert('❌ Error: La fecha fin no puede ser anterior a la fecha inicio');
                    fechaFin.focus();
                }
            });
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new HistorialPermisos();
});