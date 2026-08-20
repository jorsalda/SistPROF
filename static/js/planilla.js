// =============================================
// 1. COLORES CONDICIONALES
// =============================================
function pintarCelda(input) {
    input.classList.remove('nota-baja', 'nota-alta');
    const v = parseFloat(input.value);
    if (isNaN(v)) return;
    if (v < 3.0) input.classList.add('nota-baja');
    else if (v >= 4.5) input.classList.add('nota-alta');
}

document.querySelectorAll('.pl-input:not(.definitiva)').forEach(function(inp) {
    pintarCelda(inp);
    inp.addEventListener('input', function() {
        pintarCelda(this);
        const estId = this.dataset.estudianteId;
        recalcularPromediosEstudiante(estId);
        calcularNotaDefinitiva(estId);
    });
});

// =============================================
// 2. CÁLCULO DE PROMEDIOS POR COMPETENCIA
// =============================================
function recalcularPromediosEstudiante(estudianteId) {
    const fila = document.querySelector(`tr[data-estudiante-id="${estudianteId}"]`);
    if (!fila) return;

    const inputs = fila.querySelectorAll(`.input-nota[data-estudiante-id="${estudianteId}"]`);
    const notasPorComp = {};

    inputs.forEach(input => {
        const compId = input.dataset.competenciaId;
        if (!compId) return;
        const valor = parseFloat(input.value);
        if (!isNaN(valor)) {
            if (!notasPorComp[compId]) notasPorComp[compId] = [];
            notasPorComp[compId].push(valor);
        }
    });

    // Nota: En esta versión, no mostramos celdas Σ separadas,
    // pero la lógica de cálculo permanece para la definitiva.
}

function calcularPromedios() {
    document.querySelectorAll('tr[data-estudiante-id]').forEach(row => {
        const estId = row.dataset.estudianteId;
        recalcularPromediosEstudiante(estId);
        calcularNotaDefinitiva(estId);
    });
}

// =============================================
// 3. CÁLCULO DE NOTA DEFINITIVA (DINÁMICO)
// =============================================
function calcularNotaDefinitiva(estudianteId) {
    const fila = document.querySelector(`tr[data-estudiante-id="${estudianteId}"]`);
    if (!fila) return;

    const config = window.PLANILLA_CONFIG;
    let definitiva = 0;

    // Competencias con su ponderación real
    config.competencias.forEach(comp => {
        const inputs = fila.querySelectorAll(`.input-nota[data-competencia-id="${comp.id}"]`);
        let suma = 0, count = 0;
        inputs.forEach(inp => {
            const v = parseFloat(inp.value);
            if (!isNaN(v)) { suma += v; count++; }
        });
        if (count > 0) {
            const promedio = suma / count;
            definitiva += promedio * (comp.porcentaje / 100);
        }
    });

    // Autoevaluación
    const autoInput = fila.querySelector('input[data-tipo="autoeval"]');
    const auto = parseFloat(autoInput?.value) || 0;
    definitiva += auto * (config.pctAutoeval / 100);

    // Examen final
    const examenInput = fila.querySelector('input[data-tipo="examen"]');
    const examen = parseFloat(examenInput?.value) || 0;
    definitiva += examen * (config.pctExamen / 100);

    // Renderizar
    const celdaDefinitiva = document.getElementById(`definitiva-${estudianteId}`);
    if (celdaDefinitiva) {
        if (definitiva > 0) {
            celdaDefinitiva.value = definitiva.toFixed(1);
            if (definitiva < 3.0) {
                celdaDefinitiva.style.color = '#dc3545';
                celdaDefinitiva.style.background = '#ffcccc';
            } else if (definitiva >= 4.5) {
                celdaDefinitiva.style.color = '#28a745';
                celdaDefinitiva.style.background = '#d9ead3';
            } else {
                celdaDefinitiva.style.color = '#0d6efd';
                celdaDefinitiva.style.background = '#f0f7ff';
            }
        } else {
            celdaDefinitiva.value = '—';
            celdaDefinitiva.style.color = '#0d6efd';
            celdaDefinitiva.style.background = '#f0f7ff';
        }
    }
}

// =============================================
// 4. EDICIÓN INLINE DE PONDERACIONES EN HEADERS
// =============================================
let valoresOriginales = {};

function toggleEdicionPonderaciones(activar) {
    const btnEditar   = document.getElementById('btnEditarPonderaciones');
    const btnAplicar  = document.getElementById('btnAplicarPonderaciones');
    const btnCancelar = document.getElementById('btnCancelarPonderaciones');
    const badgeSuma   = document.getElementById('badgeSumaPonderaciones');

    if (!btnEditar) return;

    if (activar) {
        valoresOriginales = {};

        // Competencias
        document.querySelectorAll('th.h-comp .pct-label').forEach(el => {
            const th = el.closest('th');
            const compId = th.dataset.compId;
            const val = parseFloat(el.textContent) || 0;
            valoresOriginales[`comp-${compId}`] = el.textContent;

            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'pct-input';
            input.value = val;
            input.min = 0;
            input.max = 100;
            input.step = 1;
            input.dataset.tipo = 'competencia';
            input.dataset.id = compId;
            input.addEventListener('input', actualizarSumaEdicion);
            el.replaceWith(input);
        });

        // Autoevaluación
        const autoLabel = document.querySelector('th.h-auto .pct-label');
        if (autoLabel) {
            const val = parseFloat(autoLabel.textContent) || 0;
            valoresOriginales['autoeval'] = autoLabel.textContent;
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'pct-input';
            input.value = val;
            input.min = 0; input.max = 100; input.step = 1;
            input.dataset.tipo = 'autoeval';
            input.addEventListener('input', actualizarSumaEdicion);
            autoLabel.replaceWith(input);
        }

        // Examen
        const examenLabel = document.querySelector('th.h-examen .pct-label');
        if (examenLabel) {
            const val = parseFloat(examenLabel.textContent) || 0;
            valoresOriginales['examen'] = examenLabel.textContent;
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'pct-input';
            input.value = val;
            input.min = 0; input.max = 100; input.step = 1;
            input.dataset.tipo = 'examen';
            input.addEventListener('input', actualizarSumaEdicion);
            examenLabel.replaceWith(input);
        }

        // UI
        btnEditar.classList.add('d-none');
        btnAplicar.classList.remove('d-none');
        btnCancelar.classList.remove('d-none');
        badgeSuma.classList.remove('d-none');
        actualizarSumaEdicion();

    } else {
        // Restaurar valores originales
        document.querySelectorAll('th .pct-input').forEach(input => {
            const tipo = input.dataset.tipo;
            const key = tipo === 'competencia' ? `comp-${input.dataset.id}` : tipo;
            const span = document.createElement('small');
            span.className = 'pct-label';
            span.textContent = valoresOriginales[key] || (input.value + '%');
            input.replaceWith(span);
        });

        btnEditar.classList.remove('d-none');
        btnAplicar.classList.add('d-none');
        btnCancelar.classList.add('d-none');
        badgeSuma.classList.add('d-none');
    }
}

function actualizarSumaEdicion() {
    let suma = 0;
    document.querySelectorAll('th .pct-input').forEach(input => {
        suma += parseFloat(input.value) || 0;
    });

    const badge = document.getElementById('badgeSumaPonderaciones');
    const btnAplicar = document.getElementById('btnAplicarPonderaciones');

    if (badge) {
        badge.textContent = `Total: ${suma}%`;
        badge.className = `badge ms-2 ${suma === 100 ? 'text-bg-success' : 'text-bg-danger'}`;
    }
    if (btnAplicar) {
        btnAplicar.disabled = (suma !== 100);
    }
}

function aplicarPonderaciones() {
    const config = window.PLANILLA_CONFIG;

    // Competencias
    document.querySelectorAll('th .pct-input[data-tipo="competencia"]').forEach(input => {
        const compId = parseInt(input.dataset.id);
        const nuevoPct = parseFloat(input.value) || 0;
        const comp = config.competencias.find(c => c.id === compId);
        if (comp) {
            comp.porcentaje = nuevoPct;
            const th = input.closest('th');
            if (th) th.dataset.porcentaje = nuevoPct;
        }
        const span = document.createElement('small');
        span.className = 'pct-label';
        span.textContent = nuevoPct + '%';
        input.replaceWith(span);
    });

    // Autoeval
    const autoInput = document.querySelector('th .pct-input[data-tipo="autoeval"]');
    if (autoInput) {
        config.pctAutoeval = parseFloat(autoInput.value) || 0;
        const span = document.createElement('small');
        span.className = 'pct-label';
        span.textContent = config.pctAutoeval + '%';
        autoInput.replaceWith(span);
        const th = document.querySelector('th.h-auto');
        if (th) th.dataset.porcentaje = config.pctAutoeval;
    }

    // Examen
    const examenInput = document.querySelector('th .pct-input[data-tipo="examen"]');
    if (examenInput) {
        config.pctExamen = parseFloat(examenInput.value) || 0;
        const span = document.createElement('small');
        span.className = 'pct-label';
        span.textContent = config.pctExamen + '%';
        examenInput.replaceWith(span);
        const th = document.querySelector('th.h-examen');
        if (th) th.dataset.porcentaje = config.pctExamen;
    }

    // Actualizar badge total del toolbar
    const totalPct = config.competencias.reduce((s, c) => s + c.porcentaje, 0) + config.pctAutoeval + config.pctExamen;
    const badgeTotal = document.getElementById('badgeTotalPct');
    const txtTotal = document.getElementById('txtTotalPct');
    if (badgeTotal && txtTotal) {
        txtTotal.textContent = totalPct;
        badgeTotal.className = `badge pl-badge ${totalPct === 100 ? 'text-bg-success' : 'text-bg-warning'}`;
    }

    // UI
    document.getElementById('btnEditarPonderaciones').classList.remove('d-none');
    document.getElementById('btnAplicarPonderaciones').classList.add('d-none');
    document.getElementById('btnCancelarPonderaciones').classList.add('d-none');
    document.getElementById('badgeSumaPonderaciones').classList.add('d-none');

    calcularPromedios();
}

// =============================================
// 5. ANÁLISIS IA
// =============================================
function analizarIA(estId, nombre) {
    const modalEl = document.getElementById('modalIA');
    const modal = new bootstrap.Modal(modalEl);
    const contenido = document.getElementById('contenidoIA');

    contenido.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2">Analizando a ${nombre}...</p>
        </div>
    `;
    modal.show();

    fetch('/docentes/api/ia/analizar-estudiante', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.CSRF_TOKEN || ''
        },
        body: JSON.stringify({
            estudiante_id: parseInt(estId),
            materia_id: window.PLANILLA_CONFIG.materiaId,
            periodo_id: window.PLANILLA_CONFIG.periodoId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.fortalezas && data.fortalezas.length > 0) {
            contenido.innerHTML = `
                <div class="alert alert-info">
                    <strong>Fortalezas:</strong>
                    <ul>${data.fortalezas.map(f => `<li>${f}</li>`).join('')}</ul>
                </div>
                <div class="alert alert-warning">
                    <strong>Debilidades:</strong>
                    <ul>${data.debilidades.map(d => `<li>${d}</li>`).join('')}</ul>
                </div>
                <div class="card border-success mt-3">
                    <div class="card-header bg-success text-white">Plan de Apoyo Sugerido</div>
                    <div class="card-body">
                        <textarea class="form-control" rows="4" id="planApoyo">${data.plan_apoyo || ''}</textarea>
                    </div>
                </div>
            `;
        } else {
            contenido.innerHTML = `<div class="alert alert-danger">${data.error || 'No hay datos suficientes para generar un análisis.'}</div>`;
        }
    })
    .catch(error => {
        contenido.innerHTML = `<div class="alert alert-danger">Error de conexión: ${error.message}</div>`;
    });
}

function guardarPlanIA() {
    const plan = document.getElementById('planApoyo')?.value;
    if (!plan || plan.trim() === '') {
        alert('⚠️ El plan de apoyo está vacío');
        return;
    }
    alert('✅ Plan guardado exitosamente (Simulación)');
    const modalEl = document.getElementById('modalIA');
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();
}

// =============================================
// 6. SINCRONIZACIÓN AUTOMÁTICA DE NIVELES (Tu propuesta pedagógica)
// =============================================

function sincronizarNivelAutomatico(inputNota) {
    console.log(' sincronizarNivelAutomatico llamada', {
        valor: inputNota.value,
        estId: inputNota.dataset.estudianteId,
        compId: inputNota.dataset.competenciaId
    });

    const valor = parseFloat(inputNota.value);
    if (isNaN(valor)) {
        console.warn('⚠️ Valor no es numérico:', inputNota.value);
        return;
    }

    const estId = inputNota.dataset.estudianteId;
    const compId = inputNota.dataset.competenciaId;

    // Buscar la fila del estudiante
    const fila = inputNota.closest('tr');
    if (!fila) {
        console.error('❌ No se encontró la fila del estudiante');
        return;
    }

    // Buscar la celda de nivel específica usando data-comp-id
    const celdaNivel = fila.querySelector(`.td-nivel[data-comp-id="${compId}"]`);
    if (!celdaNivel) {
        console.error(`❌ No se encontró celda de nivel para competencia ${compId}`);
        console.log('Celdas disponibles:', fila.querySelectorAll('.td-nivel'));
        return;
    }

    const containerNivel = celdaNivel.querySelector('.nivel-container');
    const inputNivelOculto = celdaNivel.querySelector(`input[name^="nivel_"]`);

    if (!containerNivel) {
        console.error('❌ No se encontró .nivel-container dentro de la celda');
        return;
    }

    let nivelTexto = '';
    let codigoGenerado = '';

    // Lógica de rangos estándar (ajustable según normativa)
    if (valor >= 4.7) {
        nivelTexto = 'Superior';
        codigoGenerado = `S500`;
    } else if (valor >= 4.0) {
        nivelTexto = 'Alto';
        codigoGenerado = `A400`;
    } else if (valor >= 3.0) {
        nivelTexto = 'Basico';
        codigoGenerado = `B300`;
    } else {
        nivelTexto = 'Bajo';
        codigoGenerado = `b200`; // Para valores < 3.0 (incluye 1.0)
    }

    // Construir código completo: C1-b200, C2-A400, etc.
    const compIndex = Array.from(fila.querySelectorAll('.td-nota')).findIndex(td =>
        td.dataset.compId === compId
    ) + 1;
    const codigoCompleto = `C${compIndex}-${codigoGenerado}`;

    console.log('✅ Generando nivel:', { codigoCompleto, nivelTexto, valor });

    // Actualizar visualización INMEDIATA
    containerNivel.innerHTML = `<span class="badge-nivel" style="font-weight:bold; color:#2c3e50;">${codigoCompleto}</span>`;

    // Actualizar input oculto para persistencia
    if (inputNivelOculto) {
        inputNivelOculto.value = nivelTexto;
        console.log(' Input oculto actualizado:', inputNivelOculto.name, '=', nivelTexto);
    }

    // Recalcular definitivas
    recalcularPromediosEstudiante(estId);
    calcularNotaDefinitiva(estId);
}

// =============================================
// INICIALIZACIÓN: Disparar sincronización al cargar página
// =============================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('📊 Inicializando planilla...');

    // Disparar sincronización para todos los inputs que ya tienen valor
    document.querySelectorAll('.input-nota').forEach(input => {
        if (input.value && input.value !== '') {
            console.log('🔄 Disparando sincronización inicial para input:', input.name, 'valor:', input.value);
            sincronizarNivelAutomatico(input);
        }
    });

    // Calcular promedios iniciales
    calcularPromedios();

    // Vincular botón de guardar
    const btnGuardar = document.getElementById('btn-guardar-notas');
    if (btnGuardar) {
        btnGuardar.addEventListener('click', guardarNotas);
    }
});

// =============================================
// 7. GUARDADO MASIVO DE NOTAS (AJAX) - CORREGIDO PARA NIVELES
// =============================================
async function guardarNotas() {
    const btn = document.getElementById('btn-guardar-notas');
    if (!btn) return;

    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Guardando...';
    btn.disabled = true;

    const payload = {
        notas: {},
        componentes: {},
        ponderaciones: {},
        niveles: {}
    };

    // Recolectar notas por competencia
    document.querySelectorAll('.input-nota[data-competencia-id]').forEach(input => {
        if (input.value !== '' && input.value !== null) {
            const estId = input.dataset.estudianteId;
            const compId = input.dataset.competenciaId;
            if (!payload.notas[estId]) payload.notas[estId] = {};
            payload.notas[estId][compId] = input.value;
        }
    });

    // ✅ NUEVO: Recolectar niveles de las columnas restauradas
    document.querySelectorAll('.td-nivel').forEach(td => {
        const compId = td.dataset.compId;
        const inputOculto = td.querySelector('input[name^="nivel_"]');
        const estId = inputOculto?.name.split('_')[1]; // Extraer ID del nombre del input

        if (estId && compId && inputOculto && inputOculto.value) {
            if (!payload.niveles[estId]) payload.niveles[estId] = {};
            payload.niveles[estId][compId] = inputOculto.value;
        }
    });

    // Recolectar componentes (Autoeval / Examen)
    document.querySelectorAll('.pl-input[data-tipo]').forEach(input => {
        if (input.value !== '' && input.value !== null) {
            const estId = input.dataset.estudianteId;
            const tipo = input.dataset.tipo;
            const key = tipo === 'autoeval' ? 'autoevaluacion' : 'examen_final';

            if (!payload.componentes[estId]) payload.componentes[estId] = {};
            payload.componentes[estId][key] = input.value;
        }
    });

    // Enviar al backend
    try {
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.CSRF_TOKEN || ''
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (result.success) {
            alert('✅ ' + result.message);
            window.location.reload();
        } else {
            alert('❌ Error: ' + (result.error || 'Error desconocido'));
        }
    } catch (err) {
        alert('Error de conexión: ' + err.message);
    } finally {
        btn.innerHTML = originalHTML;
        btn.disabled = false;
    }
}

// =============================================
// 8. INICIALIZACIÓN Y EVENT LISTENERS
// =============================================
document.addEventListener('DOMContentLoaded', function() {
    // Calcular promedios iniciales al cargar
    calcularPromedios();

    // Vincular botón de guardar
    const btnGuardar = document.getElementById('btn-guardar-notas');
    if (btnGuardar) {
        btnGuardar.addEventListener('click', guardarNotas);
    }

    console.log('📊 Planilla inicializada correctamente');
});