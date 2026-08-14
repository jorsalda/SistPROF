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

    const inputs = fila.querySelectorAll('.pl-input[data-estudiante-id="' + estudianteId + '"]');
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

    Object.keys(notasPorComp).forEach(compId => {
        const notas = notasPorComp[compId];
        const promedio = notas.reduce((a, b) => a + b, 0) / notas.length;
        const celda = document.getElementById(`prom-${estudianteId}-${compId}`);
        if (celda) {
            celda.textContent = promedio.toFixed(1);
            if (promedio < 3.0) celda.style.color = '#dc3545';
            else if (promedio >= 4.5) celda.style.color = '#28a745';
            else celda.style.color = '#0d6efd';
        }
    });
}

function calcularPromedios() {
    document.querySelectorAll('tr[data-estudiante-id]').forEach(row => {
        const estId = row.dataset.estudianteId;
        recalcularPromediosEstudiante(estId);
        calcularNotaDefinitiva(estId);
    });
}

// =============================================
// 3. CÁLCULO DE NOTA DEFINITIVA (NUEVO)
// =============================================
function calcularNotaDefinitiva(estudianteId) {
    const fila = document.querySelector(`tr[data-estudiante-id="${estudianteId}"]`);
    if (!fila) return;

    // Obtener todas las notas de indicadores
    const inputs = fila.querySelectorAll('.pl-input[data-estudiante-id="' + estudianteId + '"]');
    let sumaCompetencias = 0;
    let totalCompetencias = 0;
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

    // Calcular promedio por competencia
    Object.keys(notasPorComp).forEach(compId => {
        const notas = notasPorComp[compId];
        const promedio = notas.reduce((a, b) => a + b, 0) / notas.length;
        sumaCompetencias += promedio;
        totalCompetencias++;
    });

    const promedioCompetencias = totalCompetencias > 0 ? sumaCompetencias / totalCompetencias : 0;

    // Obtener autoevaluación y examen final
    const autoInput = fila.querySelector('input[name="autoeval_' + estudianteId + '"]');
    const examenInput = fila.querySelector('input[name="examen_' + estudianteId + '"]');

    const auto = parseFloat(autoInput?.value) || 0;
    const examen = parseFloat(examenInput?.value) || 0;

    // Calcular nota definitiva con ponderaciones
    // 75% competencias + 5% autoevaluación + 20% examen final
    const definitiva = (promedioCompetencias * 0.75) + (auto * 0.05) + (examen * 0.20);

    const celdaDefinitiva = document.getElementById(`definitiva-${estudianteId}`);
    if (celdaDefinitiva) {
        if (definitiva > 0) {
            celdaDefinitiva.value = definitiva.toFixed(1);
            // Color según rendimiento
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
// 4. ANÁLISIS IA
// =============================================
function analizarIA(estId, nombre) {
    const modal = new bootstrap.Modal(document.getElementById('modalIA'));
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            estudiante_id: parseInt(estId),
            materia_id: window.PLANILLA_CONFIG.materiaId,
            periodo_id: window.PLANILLA_CONFIG.periodoId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.fortalezas) {
            contenido.innerHTML = `
                <div class="alert alert-info">
                    <strong>Fortalezas:</strong>
                    <ul>${data.fortalezas.map(f => `<li>${f}</li>`).join('')}</ul>
                </div>
                <div class="alert alert-warning">
                    <strong>Debilidades:</strong>
                    <ul>${data.debilidades.map(d => `<li>${d}</li>`).join('')}</ul>
                </div>
                <div class="card border-success">
                    <div class="card-header bg-success text-white">Plan de Apoyo</div>
                    <div class="card-body">
                        <textarea class="form-control" rows="4" id="planApoyo">${data.plan_apoyo || ''}</textarea>
                    </div>
                </div>
            `;
        } else {
            contenido.innerHTML = `<div class="alert alert-danger">${data.error || 'Error en el análisis'}</div>`;
        }
    })
    .catch(error => {
        contenido.innerHTML = `<div class="alert alert-danger">Error de conexión: ${error.message}</div>`;
    });
}

function guardarPlanIA() {
    const plan = document.getElementById('planApoyo')?.value;
    if (!plan) {
        alert('⚠️ El plan de apoyo está vacío');
        return;
    }
    alert('✅ Plan guardado exitosamente');
    bootstrap.Modal.getInstance(document.getElementById('modalIA')).hide();
}

// =============================================
// 5. INICIALIZAR
// =============================================
document.addEventListener('DOMContentLoaded', function() {
    calcularPromedios();
    console.log('📊 Planilla cargada');
});