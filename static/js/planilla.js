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
// 2. CÁLCULO DE PROMEDIOS
// =============================================
function recalcularPromediosEstudiante(estudianteId) {
    const fila = document.querySelector(`tr[data-estudiante-id="${estudianteId}"]`);
    if (!fila) return;
}

function calcularPromedios() {
    document.querySelectorAll('tr[data-estudiante-id]').forEach(row => {
        const estId = row.dataset.estudianteId;
        recalcularPromediosEstudiante(estId);
        calcularNotaDefinitiva(estId);
    });
}

// =============================================
// 3. CÁLCULO DE NOTA DEFINITIVA
// =============================================
function calcularNotaDefinitiva(estudianteId) {
    const fila = document.querySelector(`tr[data-estudiante-id="${estudianteId}"]`);
    if (!fila) return;

    const config = window.PLANILLA_CONFIG;
    let definitiva = 0;

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

    const autoInput = fila.querySelector('input[data-tipo="autoeval"]');
    const auto = parseFloat(autoInput?.value) || 0;
    definitiva += auto * (config.pctAutoeval / 100);

    const examenInput = fila.querySelector('input[data-tipo="examen"]');
    const examen = parseFloat(examenInput?.value) || 0;
    definitiva += examen * (config.pctExamen / 100);

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
// 4. PONDERACIONES
// =============================================
function toggleEdicionPonderaciones(activar) {
    const btnEditar = document.getElementById('btnEditarPonderaciones');
    const btnAplicar = document.getElementById('btnAplicarPonderaciones');
    const btnCancelar = document.getElementById('btnCancelarPonderaciones');
    const badgeSuma = document.getElementById('badgeSumaPonderaciones');

    if (!btnEditar) return;

    if (activar) {
        btnEditar.classList.add('d-none');
        btnAplicar.classList.remove('d-none');
        btnCancelar.classList.remove('d-none');
        badgeSuma.classList.remove('d-none');
    } else {
        btnEditar.classList.remove('d-none');
        btnAplicar.classList.add('d-none');
        btnCancelar.classList.add('d-none');
        badgeSuma.classList.add('d-none');
    }
}

function aplicarPonderaciones() {
    alert('Función de ponderaciones en construcción.');
    toggleEdicionPonderaciones(false);
}

// =============================================
// 5. IA
// =============================================
function analizarIA(estId, nombre) {
    alert(`Análisis IA para ${nombre} (ID: ${estId}) en construcción.`);
}

function guardarPlanIA() {
    alert('Guardar plan IA en construcción.');
}

// =============================================
// 6. SINCRONIZACIÓN DE NIVELES (CON TOOLTIP)
// =============================================
function sincronizarNivelAutomatico(inputNota) {
    const valor = parseFloat(inputNota.value);
    if (isNaN(valor)) return;

    const estId = inputNota.dataset.estudianteId;
    const compId = inputNota.dataset.competenciaId;

    const fila = inputNota.closest('tr');
    if (!fila) return;

    const celdaNivel = fila.querySelector(`.td-nivel[data-comp-id="${compId}"]`);
    if (!celdaNivel) return;

    const containerNivel = celdaNivel.querySelector('.nivel-container');
    const inputNivelOculto = celdaNivel.querySelector(`input[name^="nivel_"]`);

    if (!containerNivel) return;

    let nivelTexto, codigoGenerado;
    if (valor >= 4.7) { nivelTexto = 'Superior'; codigoGenerado = 'S500'; }
    else if (valor >= 4.0) { nivelTexto = 'Alto'; codigoGenerado = 'A400'; }
    else if (valor >= 3.0) { nivelTexto = 'Basico'; codigoGenerado = 'B300'; }
    else { nivelTexto = 'Bajo'; codigoGenerado = 'b200'; }

    const compIndex = Array.from(fila.querySelectorAll('.td-nota')).findIndex(td => td.dataset.compId === compId) + 1;
    const codigoCompleto = `C${compIndex}-${codigoGenerado}`;

    // ✅ LEER LA DESCRIPCIÓN DEL ATRIBUTO DEL TD
    const descripcion = celdaNivel.getAttribute('data-descripcion-indicador') || 'Sin descripción';

    // ✅ CREAR EL BADGE CON EL TOOLTIP
    containerNivel.innerHTML = `<span class="badge-nivel" style="font-weight:bold; color:#2c3e50;" data-bs-toggle="tooltip" title="${codigoCompleto}: ${descripcion}">${codigoCompleto}</span>`;

    // ✅ ACTIVAR EL TOOLTIP
    var tooltipTrigger = containerNivel.querySelector('.badge-nivel');
    if (tooltipTrigger) {
        new bootstrap.Tooltip(tooltipTrigger);
    }

    if (inputNivelOculto) inputNivelOculto.value = nivelTexto;

    recalcularPromediosEstudiante(estId);
    calcularNotaDefinitiva(estId);
}

// =============================================
// 7. GUARDADO MASIVO
// =============================================
async function guardarNotas() {
    const btn = document.getElementById('btn-guardar-notas');
    if (!btn) return;

    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Guardando...';
    btn.disabled = true;

    const payload = { notas: {}, componentes: {}, niveles: {} };

    document.querySelectorAll('.input-nota[data-competencia-id]').forEach(input => {
        if (input.value !== '' && input.value !== null) {
            const estId = input.dataset.estudianteId;
            const compId = input.dataset.competenciaId;
            if (!payload.notas[estId]) payload.notas[estId] = {};
            payload.notas[estId][compId] = input.value;
        }
    });

    document.querySelectorAll('.pl-input[data-tipo]').forEach(input => {
        if (input.value !== '' && input.value !== null) {
            const estId = input.dataset.estudianteId;
            const tipo = input.dataset.tipo;
            const key = tipo === 'autoeval' ? 'autoevaluacion' : 'examen_final';
            if (!payload.componentes[estId]) payload.componentes[estId] = {};
            payload.componentes[estId][key] = input.value;
        }
    });

    try {
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': window.CSRF_TOKEN || '' },
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
// 8. INICIALIZACIÓN
// =============================================
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.input-nota').forEach(input => {
        if (input.value && input.value !== '') {
            sincronizarNivelAutomatico(input);
        }
    });

    calcularPromedios();

    const btnGuardar = document.getElementById('btn-guardar-notas');
    if (btnGuardar) {
        btnGuardar.addEventListener('click', guardarNotas);
    }
});