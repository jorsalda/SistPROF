// ===== FUNCIONALIDAD PARA FORMULARIO DE PERMISOS =====

document.addEventListener('DOMContentLoaded', function() {
    const docenteSelect = document.getElementById('docente_id');
    const tipoSelect = document.getElementById('tipo');
    const fechaInicioInput = document.getElementById('fecha_inicio');
    const fechaFinInput = document.getElementById('fecha_fin');
    const formulario = document.querySelector('form');

    if (!docenteSelect) return;

    // Elementos del contenedor de permisos
    const permisosContainer = document.getElementById('permisos-docente-container');
    const permisosContent = document.getElementById('permisos-content');
    const permisosEmpty = document.getElementById('permisos-empty');
    const permisosLoading = document.getElementById('permisos-loading');

    // Inicializar fechas con hoy
    const hoy = new Date().toISOString().split('T')[0];
    if (fechaInicioInput && !fechaInicioInput.value) {
        fechaInicioInput.value = hoy;
    }
    if (fechaFinInput && !fechaFinInput.value) {
        fechaFinInput.value = hoy;
    }

    // Cargar permisos del docente
    async function cargarPermisosDocente(docenteId) {
        if (!docenteId || !docenteId.trim()) {
            ocultarPermisos();
            return;
        }

        mostrarLoadingPermisos();

        try {
            const data = await apiRequest(`/permisos/api/permisos-docente/${docenteId}`);

            if (data.success && data.permisos && data.permisos.length > 0) {
                mostrarPermisos(data);
            } else {
                mostrarSinPermisos(data.docente);
            }
        } catch (error) {
            mostrarErrorPermisos();
        }
    }

    function mostrarPermisos(data) {
        permisosLoading.style.display = 'none';
        permisosEmpty.style.display = 'none';
        permisosContainer.style.display = 'block';

        let html = `
            <div class="permiso-mini-card">
                <div class="permiso-mini-header">
                    <span class="permiso-mini-type">📋 Resumen</span>
                    <span class="badge badge-info">${data.total} permiso(s)</span>
                </div>
                <div style="font-size: 12px; color: #666; margin-top: 5px;">
                    Docente: <strong>${data.docente}</strong>
                </div>
            </div>
        `;

        data.permisos.forEach(permiso => {
            const esLargo = permiso.dias > 10;
            const esReciente = esPermisoReciente(permiso.fecha_fin);

            html += `
                <div class="permiso-mini-card ${esLargo ? 'warning' : ''} ${esReciente ? 'danger' : ''}">
                    <div class="permiso-mini-header">
                        <span class="permiso-mini-type">${getIconoTipo(permiso.tipo)} ${permiso.tipo}</span>
                        <span class="permiso-mini-days">${permiso.dias}d</span>
                    </div>
                    <div class="permiso-mini-dates">
                        ${permiso.fecha_inicio} → ${permiso.fecha_fin}
                    </div>
                    ${permiso.observacion ? `
                    <div style="margin-top: 5px; font-size: 11px; color: #666;">
                        📝 ${permiso.observacion}
                    </div>
                    ` : ''}
                </div>
            `;
        });

        permisosContent.innerHTML = html;
    }

    function mostrarSinPermisos(nombreDocente) {
        permisosLoading.style.display = 'none';
        permisosContent.innerHTML = '';
        permisosEmpty.style.display = 'block';
        permisosContainer.style.display = 'block';

        permisosEmpty.innerHTML = `
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 24px; margin-bottom: 10px;">✅</div>
                <div><strong>${nombreDocente}</strong></div>
                <div style="color: #666; font-size: 14px; margin-top: 5px;">
                    No tiene permisos registrados
                </div>
            </div>
        `;
    }

    function mostrarErrorPermisos() {
        permisosLoading.style.display = 'none';
        permisosContent.innerHTML = '';
        permisosEmpty.style.display = 'block';
        permisosContainer.style.display = 'block';

        permisosEmpty.innerHTML = `
            <div style="text-align: center; padding: 20px; color: var(--danger-color);">
                <div style="font-size: 24px; margin-bottom: 10px;">❌</div>
                <div>Error al cargar permisos</div>
            </div>
        `;
    }

    function mostrarLoadingPermisos() {
        permisosLoading.style.display = 'block';
        permisosEmpty.style.display = 'none';
        permisosContent.innerHTML = '';
        permisosContainer.style.display = 'block';
    }

    function ocultarPermisos() {
        permisosContainer.style.display = 'none';
    }

    // Helper functions
    function getIconoTipo(tipo) {
        const iconos = {
            'Vacaciones': '🏖️',
            'Enfermedad': '🤒',
            'Capacitación': '📚',
            'Permiso Personal': '👤',
            'Licencia': '📄',
            'Otro': '❓'
        };
        return iconos[tipo] || '📋';
    }

    function esPermisoReciente(fechaFin) {
        const fecha = new Date(fechaFin.split('/').reverse().join('-'));
        const hoy = new Date();
        const diffTime = hoy - fecha;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays <= 7; // Últimos 7 días
    }

    // Event Listeners
    if (docenteSelect) {
        docenteSelect.addEventListener('change', function() {
            cargarPermisosDocente(this.value);
        });

        // Cargar permisos si ya hay un docente seleccionado
        const urlParams = new URLSearchParams(window.location.search);
        const docenteIdFromUrl = urlParams.get('docente_id');
        if (docenteIdFromUrl) {
            docenteSelect.value = docenteIdFromUrl;
            setTimeout(() => cargarPermisosDocente(docenteIdFromUrl), 100);
        }
    }

    // Validación de fechas
    if (formulario) {
        formulario.addEventListener('submit', function(e) {
            if (!validarFechas()) {
                e.preventDefault();
            }
        });
    }

    function validarFechas() {
        if (!fechaInicioInput || !fechaFinInput) return true;

        const inicio = new Date(fechaInicioInput.value);
        const fin = new Date(fechaFinInput.value);

        if (fin < inicio) {
            alert('❌ Error: La fecha fin no puede ser anterior a la fecha inicio');
            fechaFinInput.focus();
            fechaFinInput.style.borderColor = 'var(--danger-color)';
            return false;
        }

        // Validar que no sea muy largo (más de 30 días)
        const diffTime = fin - inicio;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;

        if (diffDays > 30) {
            if (!confirm(`⚠️ Este permiso es de ${diffDays} días (más de 30 días). ¿Estás seguro?`)) {
                fechaFinInput.focus();
                return false;
            }
        }

        return true;
    }

    // Resetear estilos al cambiar
    [fechaInicioInput, fechaFinInput].forEach(input => {
        if (input) {
            input.addEventListener('input', function() {
                this.style.borderColor = '';
            });
        }
    });
});