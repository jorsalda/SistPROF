class ClsEstudiante {
    constructor() {
        this.preguntas = [];
        this.preguntaActual = 0;
        this.respuestasCorrectas = 0;
        this.respuestasIncorrectas = 0;
        this.numPreguntasJuego = 0;  // Se setea al cargar el examen
        this.respuestaResaltada = false;
        this.temporizadorDetenido = false;
        this.segundoClic = false;
        this.countdownInterval = null;
        this.explicacionVisible = false;
        this.examenId = null;  // 🔥 NUEVO: almacena el ID del examen seleccionado
        this.tiempoPorPregunta = 30;  // 🔥 NUEVO: se setea desde el tipo_examen
    }

    // 🔥 NUEVO: Cargar lista de exámenes disponibles al iniciar
    init() {
        $(document).ready(() => {
            this.cargarListaExamenes();

            // Manejador para el botón de siguiente pregunta
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

            // Manejador para el botón de ver explicación
            $("#explanationButton").click(() => {
                this.mostrarExplicacion();
            });

            // Manejador para seleccionar opciones
            $(document).on("click", "#options label", function() {
                $("#options label").removeClass('selected');
                $(this).addClass('selected');
            });
        });
    }

    // 🔥 NUEVO: Cargar lista de exámenes desde el backend
    cargarListaExamenes() {
        fetch('/api/examen/disponibles')
            .then(response => response.json())
            .then(examenes => {
                this.mostrarListaExamenes(examenes);
            })
            .catch(error => {
                console.error('Error al cargar exámenes:', error);
                $("#result").html('<p class="error">Error al cargar los exámenes disponibles</p>').show();
            });
    }

    // 🔥 NUEVO: Mostrar lista de exámenes para que el estudiante elija
    mostrarListaExamenes(examenes) {
        if (examenes.length === 0) {
            $("#question").html('<p>No hay exámenes disponibles en este momento.</p>');
            return;
        }

        let html = '<div class="lista-examenes"><h3>Seleccione un examen:</h3><ul>';
        examenes.forEach(ex => {
            html += `<li class="examen-item" data-id="${ex.id}">
                        <strong>${ex.nombre}</strong><br>
                        <span class="descripcion">${ex.descripcion || ''}</span><br>
                        <span class="tiempo">Tiempo: ${ex.tiempo_limite_minutos} minutos</span>
                        <span class="tipo">Tipo: ${ex.tipo_examen || 'Estándar'}</span>
                        <button class="btn-seleccionar">Seleccionar este examen</button>
                    </li>`;
        });
        html += '</ul></div>';

        $("#question").html(html);
        $("#options").hide();
        $("#countdown").hide();
        $("#nextButton").hide();

        // Eventos para los botones de selección
        $(".btn-seleccionar").click((e) => {
            const item = $(e.target).closest('.examen-item');
            const examenId = item.data('id');
            this.seleccionarExamen(examenId);
        });
    }

    // 🔥 NUEVO: Seleccionar un examen y cargar sus preguntas
    seleccionarExamen(examenId) {
        this.examenId = examenId;
        this.cargarPreguntasDesdeAPI(examenId);
    }

    // 🔥 NUEVO: Cargar preguntas desde el backend (reemplaza cargarPreguntasDesdeArchivo)
    cargarPreguntasDesdeAPI(examenId) {
        fetch(`/api/examen/${examenId}/json`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al cargar el examen');
                }
                return response.json();
            })
            .then(data => {
                this.preguntas = data.preguntas;
                this.numPreguntasJuego = this.preguntas.length;
                this.preguntaActual = 0;
                this.respuestasCorrectas = 0;
                this.respuestasIncorrectas = 0;
                this.respuestaResaltada = false;

                // Mezclar preguntas
                this.shuffleArray(this.preguntas);

                // Mostrar interfaz de examen
                $("#options").show();
                $("#nextButton").show();
                this.mostrarPregunta();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('No se pudo cargar el examen. Intente de nuevo.');
            });
    }

    // Mostrar pregunta (adaptado)
    mostrarPregunta() {
        if (this.preguntaActual < this.numPreguntasJuego && this.preguntaActual < this.preguntas.length) {
            var pregunta = this.preguntas[this.preguntaActual];

            // Mostrar el contexto
            if (pregunta.contexto) {
                $("#contexto").html(`<b>Contexto:</b> ${pregunta.contexto}`).show();
            } else {
                $("#contexto").hide();
            }

            // Mostrar la pregunta
            $("#question").html(`<b>Pregunta ${this.preguntaActual + 1}:</b> ${pregunta.pregunta}`);

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
            this.iniciarContador();

            $("#selectedNumQuestions").text(`${this.numPreguntasJuego}`);
        } else {
            this.mostrarResultado();
        }
    }

    // Mostrar resultado (adaptado para enviar al backend)
    mostrarResultado() {
        $("#question").empty();
        $("#options").empty();
        $("#contexto").empty();

        const totalPreguntas = this.numPreguntasJuego;
        const porcentaje = (this.respuestasCorrectas / totalPreguntas) * 100;
        const calificacionDecimal = (porcentaje / 20).toFixed(2);
        let calificacionLetra = '';

        if (porcentaje >= 100) {
            calificacionLetra = 'S';
        } else if (porcentaje >= 80) {
            calificacionLetra = 'A';
        } else if (porcentaje >= 60) {
            calificacionLetra = 'B';
        } else if (porcentaje >= 40) {
            calificacionLetra = 'b';
        } else if (porcentaje >= 20) {
            calificacionLetra = 'I';
        }

        $("#result").html(`
            <table>
                <tr>
                    <th>Correctas</th>
                    <th>Incorrectas</th>
                    <th>Porcentaje</th>
                    <th>Literal</th>
                    <th>Numérica</th>
                </tr>
                <tr>
                    <td>${this.respuestasCorrectas}</td>
                    <td>${this.respuestasIncorrectas}</td>
                    <td>${porcentaje.toFixed(2)}%</td>
                    <td>${calificacionLetra}</td>
                    <td>${calificacionDecimal}</td>
                </tr>
            </table>
            <button id="playAgain">Nuevo Examen</button>
        `).show();

        // 🔥 NUEVO: Guardar resultado en el backend
        this.guardarResultado(porcentaje, calificacionDecimal, calificacionLetra);

        $("#nextButton").hide();
        $("#countdown").hide();
    }

    // 🔥 NUEVO: Guardar resultado en la base de datos
    guardarResultado(porcentaje, notaNumerica, literal) {
        if (!this.examenId) return;

        fetch('/api/examen/guardar-resultado', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                examen_id: this.examenId,
                respuestas_correctas: this.respuestasCorrectas,
                respuestas_incorrectas: this.respuestasIncorrectas,
                porcentaje: porcentaje,
                nota_numerica: parseFloat(notaNumerica),
                literal: literal
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Resultado guardado:', data);
        })
        .catch(error => {
            console.error('Error al guardar resultado:', error);
        });
    }

    // Resetear estado del juego
    resetGameState() {
        this.preguntaActual = 0;
        this.respuestasCorrectas = 0;
        this.respuestasIncorrectas = 0;
        this.respuestaResaltada = false;
        this.temporizadorDetenido = false;
        this.segundoClic = false;
        this.explicacionVisible = false;
        clearInterval(this.countdownInterval);
        this.countdownInterval = null;
    }

    iniciarNuevoJuego() {
        this.resetGameState();
        this.cargarListaExamenes();  // 🔥 Volver a la lista
        $("#result").empty().hide();
        $("#nextButton").hide();
        $("#options").hide();
    }

    // Iniciar contador (30 segundos por defecto)
    iniciarContador() {
        var tiempoRestante = this.tiempoPorPregunta;
        $("#countdown").text(`Tiempo restante: ${tiempoRestante} segundos`);
        this.countdownInterval = setInterval(() => {
            tiempoRestante--;
            if (tiempoRestante >= 0) {
                $("#countdown").text(`Tiempo restante: ${tiempoRestante} segundos`);
            } else {
                this.detenerContador();
                alert("¡Se acabó el tiempo!");
                this.avanzarAPreguntaSiguiente();
            }
        }, 1000);
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
            alert("Seleccione una opción antes de continuar.");
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
            $("#explanation-column").html(`<b>Explicación:</b> ${explicacion}`).show().css('color', 'blue');
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
        if (respuestaSeleccionada !== undefined) {
            var pregunta = this.preguntas[this.preguntaActual];
            if (respuestaSeleccionada === pregunta.respuesta) {
                this.respuestasCorrectas++;
            } else {
                this.respuestasIncorrectas++;
            }
        } else {
            var pregunta = this.preguntas[this.preguntaActual];
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
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
}

// Instanciar y ejecutar
const clsEstudiante = new ClsEstudiante();
clsEstudiante.init();