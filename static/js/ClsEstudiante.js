class ClsEstudiante {
    constructor() {
        this.preguntas = [];
        this.preguntaActual = 0;
        this.respuestasCorrectas = 0;
        this.respuestasIncorrectas = 0;
        this.numPreguntasJuego = 0;
        this.respuestaResaltada = false;
        this.temporizadorDetenido = false;
        this.segundoClic = false;
        this.countdownInterval = null;
        this.totalTimeInterval = null;
        this.explicacionVisible = false;
        this.examenId = null;
        this.materiaId = null;
        this.tiempoPorPregunta = 30;
        this.tiempoTotalExamen = 0;
        this.tiempoRestanteTotal = 0;
        this.todasLasRespuestas = [];
        this.examenFinalizado = false;
    }

    init() {
        $(document).ready(() => {
            this.cargarListaExamenes();

            $("#updateQuestions").click(() => {
                const cantidad = parseInt($("#numQuestions").val());
                const tiempoPorPreguntaMin = parseInt($("#timePerQuestion").val());

                if (cantidad > 0 && this.examenId) {
                    this.tiempoPorPregunta = tiempoPorPreguntaMin * 60;
                    this.tiempoTotalExamen = cantidad * this.tiempoPorPregunta;
                    this.tiempoRestanteTotal = this.tiempoTotalExamen;

                    console.log(`>>>>> Configuración: ${cantidad} preguntas, ${tiempoPorPreguntaMin} min por pregunta`);

                    $("#examInfo").text(`${cantidad} preguntas | ${tiempoPorPreguntaMin} min/pregunta | Total: ${this.formatTime(this.tiempoTotalExamen)}`).show();

                    this.finalizarExamen(false);
                    this.cargarPreguntasDesdeAPI(this.examenId, cantidad);
                } else if (!this.examenId) {
                    alert('Primero debe seleccionar un examen');
                }
            });

            $("#nextButton").click(() => {
                if (!this.respuestaResaltada) {
                    this.detenerContador();
                    this.temporizadorDetenido = true;
                    this.mostrarResultadoRespuesta();
                    this.segundoClic = true;
                } else {
                    this.avanzarAPreguntaSiguiente();
                }
            });

            $("#explanationButton").click(() => {
                this.mostrarExplicacion();
            });

            $(document).on("click", "#options label", function () {
                $("#options label").removeClass('selected');
                $(this).addClass('selected');
            });
        });
    }

    cargarListaExamenes() {
        fetch('/api/examen/disponibles')
            .then(response => response.json())
            .then(examenes => {
                this.mostrarListaExamenes(examenes);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    mostrarListaExamenes(examenes) {
        const contenedor = document.getElementById('lista-examenes');
        if (!contenedor) return;

        if (examenes.length === 0) {
            contenedor.innerHTML = '<p class="text-muted">No hay exámenes disponibles.</p>';
            return;
        }

        let html = '<ul class="list-group">';
        examenes.forEach(ex => {
            html += `<li class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${ex.nombre}</strong><br>
                            <small class="text-muted">${ex.descripcion || ''}</small><br>
                            <small>Tiempo: ${ex.tiempo_limite_minutos} min</small>
                        </div>
                        <a href="/api/examen/estudiante?id=${ex.id}" class="btn btn-primary btn-sm">
                            Presentar
                        </a>
                    </li>`;
        });
        html += '</ul>';
        contenedor.innerHTML = html;
    }

    seleccionarExamen(examenId, materiaId) {
        console.log('>>>>> seleccionarExamen:', examenId);
        this.examenId = examenId;
        this.materiaId = materiaId;

        const cantidad = parseInt($("#numQuestions").val()) || 10;
        const tiempoPorPreguntaMin = parseInt($("#timePerQuestion").val()) || 2;

        this.tiempoPorPregunta = tiempoPorPreguntaMin * 60;
        this.tiempoTotalExamen = cantidad * this.tiempoPorPregunta;
        this.tiempoRestanteTotal = this.tiempoTotalExamen;

        $("#examInfo").text(`${cantidad} preguntas | ${tiempoPorPreguntaMin} min/pregunta | Total: ${this.formatTime(this.tiempoTotalExamen)}`).show();

        this.cargarPreguntasDesdeAPI(examenId, cantidad);
    }

    cargarPreguntasDesdeAPI(examenId, cantidadSolicitada) {
        console.log('>>>>> Cargando', cantidadSolicitada, 'preguntas del examen', examenId);

        fetch(`/api/examen/${examenId}/json?cantidad=${cantidadSolicitada}`)
            .then(response => {
                if (!response.ok) throw new Error('Error al cargar');
                return response.json();
            })
            .then(data => {
                console.log('>>>>> Preguntas recibidas del backend:', data.preguntas ? data.preguntas.length : 0);

                // 🔥 CORRECCIÓN: Limitar estrictamente a la cantidad solicitada
                if (data.preguntas && data.preguntas.length > cantidadSolicitada) {
                    console.log(`>>>>> Backend devolvió ${data.preguntas.length} preguntas, limitando a ${cantidadSolicitada}`);
                    this.preguntas = data.preguntas.slice(0, cantidadSolicitada);
                } else {
                    this.preguntas = data.preguntas;
                }

                // 🔥 CORRECCIÓN: Forzar que numPreguntasJuego sea exactamente la cantidad solicitada
                this.numPreguntasJuego = cantidadSolicitada;

                this.preguntaActual = 0;
                this.respuestasCorrectas = 0;
                this.respuestasIncorrectas = 0;
                this.respuestaResaltada = false;
                this.todasLasRespuestas = [];
                this.examenFinalizado = false;

                console.log(`>>>>> numPreguntasJuego establecido a: ${this.numPreguntasJuego}`);
                console.log(`>>>>> Total de preguntas en array: ${this.preguntas.length}`);

                $("#options").show();
                $("#nextButton").show();
                $("#loadedQuestionsCount").html(`<b>Preguntas cargadas:</b> ${this.numPreguntasJuego}`);

                this.iniciarContadorTotal();
                this.mostrarPregunta();
            })
            .catch(error => {
                console.error('❌ Error:', error);
                $('#question').html(`<div class="alert alert-danger">Error: ${error.message}</div>`);
            });
    }


    iniciarContadorTotal() {
        $("#timers-container").show();
        this.actualizarDisplayTiempoTotal();

        this.totalTimeInterval = setInterval(() => {
            this.tiempoRestanteTotal--;
            this.actualizarDisplayTiempoTotal();

            if (this.tiempoRestanteTotal <= 0) {
                console.log('>>>>> ¡Tiempo total terminado!');
                this.finalizarExamenAutomaticamente();
            }
        }, 1000);
    }

    actualizarDisplayTiempoTotal() {
        const examTimer = $("#exam-timer");
        const examTimeSpan = $("#exam-time");

        examTimeSpan.text(this.formatTime(this.tiempoRestanteTotal));

        if (this.tiempoRestanteTotal <= 60) {
            examTimer.addClass('warning-critical');
        } else {
            examTimer.removeClass('warning-critical');
        }
    }

    iniciarContadorPregunta() {
        var tiempoRestante = this.tiempoPorPregunta;

        const questionTimer = $("#question-timer");
        const questionTimeSpan = $("#question-time");

        questionTimeSpan.text(this.formatTime(tiempoRestante));
        $("#timers-container").show();

        this.countdownInterval = setInterval(() => {
            tiempoRestante--;
            questionTimeSpan.text(this.formatTime(tiempoRestante));

            if (tiempoRestante <= 10 && tiempoRestante > 0) {
                questionTimer.addClass('warning-critical');
            } else {
                questionTimer.removeClass('warning-critical');
            }

            if (tiempoRestante < 0) {
                this.detenerContador();
                this.avanzarAPreguntaSiguiente();
            }
        }, 1000);
    }

    finalizarExamen(mostrarResultado = true) {
        this.examenFinalizado = true;

        this.detenerContador();
        if (this.totalTimeInterval) {
            clearInterval(this.totalTimeInterval);
            this.totalTimeInterval = null;
        }

        // Ocultar contadores
        $("#timers-container").hide();

        if (mostrarResultado) {
            this.mostrarResultado();
        }
    }

    formatTime(segundos) {
        const mins = Math.floor(segundos / 60);
        const secs = segundos % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    mostrarPregunta() {
        // 🔥 VERIFICACIÓN ESTRICTA
        if (this.preguntaActual < this.numPreguntasJuego && this.preguntaActual < this.preguntas.length) {
            var pregunta = this.preguntas[this.preguntaActual];

            if (pregunta.contexto) {
                let contextoHtml = '<b>Contexto:</b>';

                if (pregunta.contexto.tipo === 'imagen') {
                    contextoHtml += `<p>${pregunta.contexto.texto || ''}</p>`;
                    contextoHtml += `<img src="${pregunta.contexto.src}" class="imagen-contexto">`;
                } else if (pregunta.contexto.tipo === 'video') {
                    contextoHtml += `<p>${pregunta.contexto.texto || ''}</p>`;
                    contextoHtml += `<video controls class="video-contexto"><source src="${pregunta.contexto.src}" type="video/mp4"></video>`;
                } else {
                    contextoHtml += `<p>${pregunta.contexto}</p>`;
                }

                $("#contexto").html(contextoHtml).show();
            } else {
                $("#contexto").empty().hide();
            }

            // 🔥 Mostrar número correcto de pregunta
            $("#question").html(`<b>Pregunta ${this.preguntaActual + 1} de ${this.numPreguntasJuego}:</b> ${pregunta.pregunta}`);

            $("#options").empty();
            var opciones = this.shuffleArray(pregunta.opciones.slice());
            var letrasOpciones = ['A)', 'B)', 'C)', 'D)'];
            opciones.forEach((opcion, index) => {
                var id = "opcion" + index;
                var label = $(`<label for="${id}">${letrasOpciones[index]} ${opcion}</label>`);
                var input = $(`<input type="radio" name="opcion" id="${id}" value="${opcion}">`);
                label.prepend(input);
                $("#options").append(label);
            });

            $("#countdown").show();
            this.iniciarContadorPregunta();
            $("#nextButton").show();
            $("#explanationButton").hide();
            $("#feedback").hide();
            $("#explanation-column").empty();
            this.explicacionVisible = false;

            $("#selectedNumQuestions").text(`Pregunta ${this.preguntaActual + 1} de ${this.numPreguntasJuego}`);
        } else {
            console.log(`>>>>> Terminó el examen. Preguntas respondidas: ${this.preguntaActual}, Total configurado: ${this.numPreguntasJuego}`);
            this.finalizarExamen(true);
        }
    }

    iniciarContadorPregunta() {
        var tiempoRestante = this.tiempoPorPregunta;
        $("#countdown").text(`Tiempo restante: ${this.formatTime(tiempoRestante)}`);

        this.countdownInterval = setInterval(() => {
            tiempoRestante--;
            $("#countdown").text(`Tiempo restante: ${this.formatTime(tiempoRestante)}`);

            if (tiempoRestante < 0) {
                this.detenerContador();
                this.avanzarAPreguntaSiguiente();
            }
        }, 1000);
    }

    finalizarExamenAutomaticamente() {
        if (!this.examenFinalizado) {
            console.log('>>>>> Finalizando automáticamente');
            this.finalizarExamen(true);
        }
    }

    finalizarExamen(mostrarResultado = true) {
        this.examenFinalizado = true;

        this.detenerContador();
        if (this.totalTimeInterval) {
            clearInterval(this.totalTimeInterval);
            this.totalTimeInterval = null;
        }

        if (mostrarResultado) {
            this.mostrarResultado();
        }
    }

    mostrarResultado() {
        // 🔥 OCULTAR TODO EL EXAMEN (header, columnas, contadores)
        $("#exam-wrapper").hide();
        $("#timers-container").hide();

        const totalPreguntas = this.numPreguntasJuego;
        const porcentaje = totalPreguntas > 0 ? (this.respuestasCorrectas / totalPreguntas) * 100 : 0;
        const calificacionDecimal = (porcentaje / 20).toFixed(2);

        let calificacionLetra = '';
        if (porcentaje >= 100) calificacionLetra = 'S';
        else if (porcentaje >= 80) calificacionLetra = 'A';
        else if (porcentaje >= 60) calificacionLetra = 'B';
        else if (porcentaje >= 40) calificacionLetra = 'b';
        else calificacionLetra = 'I';

        // ✅ AGREGADO: Estado inicial de guardado automático
        let estadoGuardado = '<div class="alert alert-warning mt-3 py-2"><i class="bi bi-hourglass-split me-2"></i>Guardando resultados...</div>';

        $("#result").html(`
        <div class="result-container">
            <h2 class="result-title">Resultado del Examen</h2>
            
            <table class="result-table">
                <thead>
                    <tr>
                        <th>Correctas</th>
                        <th>Incorrectas</th>
                        <th>Total</th>
                        <th>Porcentaje</th>
                        <th>Literal</th>
                        <th>Nota (0-5)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="text-success"><strong>${this.respuestasCorrectas}</strong></td>
                        <td class="text-danger"><strong>${this.respuestasIncorrectas}</strong></td>
                        <td><strong>${totalPreguntas}</strong></td>
                        <td><strong>${porcentaje.toFixed(2)}%</strong></td>
                        <td><strong>${calificacionLetra}</strong></td>
                        <td><strong>${calificacionDecimal}</strong></td>
                    </tr>
                </tbody>
            </table>
            
            <div class="result-message">${this.getResultMessage(porcentaje)}</div>
            
            <!-- ✅ CONTENEDOR DE ESTADO DE GUARDADO -->
            <div id="estadoGuardado">${estadoGuardado}</div>
            
            <button id="playAgain" class="btn-play-again mt-3">Presentar Nuevo Examen</button>
        </div>
    `).show();

        // ✅ LLAMADA AUTOMÁTICA AL GUARDADO CON FEEDBACK
        this.guardarResultadoAutomatico(porcentaje, calificacionDecimal, calificacionLetra);

        $(document).off("click", "#playAgain").on("click", "#playAgain", () => {
            location.reload();
        });
    }

    getResultMessage(porcentaje) {
        if (porcentaje >= 90) return '<div class="alert alert-success">¡Excelente trabajo!</div>';
        else if (porcentaje >= 70) return '<div class="alert alert-info">Buen trabajo</div>';
        else if (porcentaje >= 60) return '<div class="alert alert-warning">Aprobado, pero puede mejorar</div>';
        else return '<div class="alert alert-danger">Necesitas reforzar</div>';
    }

    // ✅ NUEVA FUNCIÓN: Guardado automático robusto

    guardarResultadoAutomatico(porcentaje, notaNumerica, literal) {
    if (!this.examenId) {
        console.error("ERROR: No hay examenId definido");
        $("#estadoGuardado").html('<div class="alert alert-danger mt-3 py-2"><i class="bi bi-x-circle me-2"></i>Error: No se pudo identificar el examen.</div>');
        return;
    }

    const payload = {
        examen_id: this.examenId,
        materia_id: this.materiaId || null,
        respuestas: this.todasLasRespuestas
    };

    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || '';

    console.log("📦 Payload a enviar:", JSON.stringify(payload, null, 2));

    fetch('/api/examen/guardar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin',
        body: JSON.stringify(payload)
    })
    .then(async response => {
        const contentType = response.headers.get('content-type');

        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            console.error("❌ El servidor devolvió HTML:", text.substring(0, 500));
            throw new Error(`HTML recibido (Status ${response.status})`);
        }

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP ${response.status}`);
        }

        return response.json();
    })
    .then(data => {
        console.log("✅ Resultado guardado:", data);
        $("#estadoGuardado").html('<div class="alert alert-success mt-3 py-2"><i class="bi bi-check-circle-fill me-2"></i>✅ ¡Examen guardado exitosamente!</div>');
    })
    .catch(error => {
        console.error("❌ Error:", error);
        $("#estadoGuardado").html(`<div class="alert alert-danger mt-3 py-2"><i class="bi bi-exclamation-triangle-fill me-2"></i>Error: ${error.message}</div>`);
    });
}

    detenerContador() {
        if (this.countdownInterval) {
            clearInterval(this.countdownInterval);
            this.countdownInterval = null;
        }
    }

    mostrarResultadoRespuesta() {
        var respuestaSeleccionada = $("input[name='opcion']:checked").val();
        if (respuestaSeleccionada !== undefined) {
            var pregunta = this.preguntas[this.preguntaActual];
            if (respuestaSeleccionada === pregunta.respuesta) {
                $("#feedback").html(`<b>Respuesta correcta</b>`).show().css('color', 'green');
            } else {
                $("#feedback").html(`<b>Respuesta incorrecta</b>`).show().css('color', 'red');
            }
            var respuestaCorrecta = pregunta.respuesta;
            var seleccionUsuario = $("input[name='opcion']:checked");
            $("#options label").removeClass('selected');
            seleccionUsuario.parent().addClass('selected');
            $("input[value='" + respuestaCorrecta + "']").parent().addClass('correct-answer');
            this.respuestaResaltada = true;
            setTimeout(() => {
                seleccionUsuario.prop('checked', true);
            }, 100);
            $("#explanationButton").show();
        } else {
            alert("Seleccione una opción");
        }
    }

    mostrarExplicacion() {
        var pregunta = this.preguntas[this.preguntaActual];
        var explicacion = pregunta.explicacion;
        if (this.explicacionVisible) {
            $("#explanation-column").empty().hide();
            this.explicacionVisible = false;
            $("#explanationButton").show();
        } else {
            $("#explanation-column").html(`<b>Explicación:</b> ${explicacion}`).show();
            this.explicacionVisible = true;
            $("#explanationButton").hide();
        }
    }

    avanzarAPreguntaSiguiente() {
        if (this.segundoClic) {
            $("#feedback").empty().hide();
            this.explicacionVisible = false;
            $("#explanation-column").empty().hide();
        }

        if (!this.temporizadorDetenido) {
            this.detenerContador();
        }

        var respuestaSeleccionada = $("input[name='opcion']:checked").val();
        var pregunta = this.preguntas[this.preguntaActual];

        // ✅ AGREGADO: indicador_logro_id para vinculación con competencias
        let respuestaData = {
            texto_pregunta: pregunta.pregunta,
            respuesta_seleccionada: respuestaSeleccionada || '',
            respuesta_correcta: pregunta.respuesta,
            es_correcta: (respuestaSeleccionada === pregunta.respuesta),
            tiempo_respuesta_seg: this.tiempoPorPregunta,
            indicador_logro_id: pregunta.indicador_logro_id || null
        };
        this.todasLasRespuestas.push(respuestaData);

        if (respuestaSeleccionada !== undefined) {
            if (respuestaSeleccionada === pregunta.respuesta) {
                this.respuestasCorrectas++;
            } else {
                this.respuestasIncorrectas++;
            }
        } else {
            var opciones = pregunta.opciones;
            var respuestaCorrecta = pregunta.respuesta;
            var respuestaIncorrecta = opciones.find(opcion => opcion !== respuestaCorrecta);
            $("input[value='" + respuestaIncorrecta + "']").prop("checked", true);
            this.respuestasIncorrectas++;
        }

        this.preguntaActual++;
        this.mostrarPregunta();
        this.respuestaResaltada = false;
        this.temporizadorDetenido = false;
        this.segundoClic = false;
        $("#explanationButton").hide();
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            // ✅ CORRECCIÓN DEFINITIVA: Era 'arrayarray', ahora es 'array'
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
}

const clsEstudiante = new ClsEstudiante();
clsEstudiante.init();