class CslTIngenios {
    constructor() {
        this.preguntas = [];
        this.preguntaActual = 0;
        this.respuestasCorrectas = 0;
        this.respuestasIncorrectas = 0;
        this.numPreguntasJuego = 1;
        this.respuestaResaltada = false;
        this.temporizadorDetenido = false;
        this.segundoClic = false;
        this.countdownInterval = null;
        this.explicacionVisible = false;
        this.password = "jes1";
        this.intentosRestantes = 3;
        
        // 🔹 NUEVO: Historial de respuestas para enviar al backend
        this.historialRespuestas = [];
    }

    cargarPreguntasDesdeArchivo(file) {
        var reader = new FileReader();
        reader.onload = (e) => {
            try {
                this.preguntas = JSON.parse(e.target.result).preguntas;
                var cantidadPreguntas = this.preguntas.length;
                $("#loadedQuestionsCount").html(`<b>El archivo tiene:</b> ${cantidadPreguntas}`);
                this.shuffleArray(this.preguntas);
                this.mostrarPregunta();

                $("#loadQuestions").hide();
                $("#fileInput").hide();
                $("#updateQuestions").hide();
                $("#numQuestions").hide();
                $("#nextButton").show();
            } catch (error) {
                alert("Error al cargar el archivo JSON.");
            }
        };
        reader.readAsText(file);
    }

    init() {
        $(document).ready(() => {
            // Manejador para el botón de enviar contraseña
            $("#submitButton").click(() => {
                var enteredPassword = $("#passwordInput").val();
                if (enteredPassword === this.password) {
                    $("#passwordContainer").hide();
                    $("#errorMessage").hide();
                    this.iniciarNuevoJuego();
                } else {
                    this.intentosRestantes--;
                    if (this.intentosRestantes > 0) {
                        $("#errorMessage").text(`Contraseña incorrecta. Intentos restantes: ${this.intentosRestantes}`).show();
                    } else {
                        $("#errorMessage").text("Se agotaron los intentos. Actualice la página para volver a intentarlo.").show();
                        $("#submitButton").prop("disabled", true);
                    }
                }
            });

            // Manejador para el botón de cargar preguntas
            $("#loadQuestions").click(() => {
                var file = $("#fileInput")[0].files[0];
                if (file) {
                    this.cargarPreguntasDesdeArchivo(file);
                } else {
                    alert("Por favor seleccione un archivo JSON.");
                }
            });

            // Manejador para el botón de actualizar preguntas
            $("#updateQuestions").click(() => {
                this.numPreguntasJuego = parseInt($("#numQuestions").val());
                this.preguntaActual = 0;
                if (this.preguntaActual < this.numPreguntasJuego) {
                    this.mostrarPregunta();
                }
                $("#updateQuestions").hide();
                $("#numQuestions").hide();
            });

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

            // Manejador para el botón de jugar de nuevo
            $(document).on("click", "#playAgain", () => {
                this.resetGameState();
                $("#passwordContainer").show();
                $("#passwordInput").val("");
                $("#errorMessage").hide();
            });

            // Manejador para seleccionar opciones
            $(document).on("click", "#options label", function () {
                $("#options label").removeClass('selected');
                $(this).addClass('selected');
            });

            $("#passwordInput").keypress((event) => {
                if (event.which === 13) {
                    $("#submitButton").click();
                }
            });
        });
    }

    resetGameState() {
        this.preguntaActual = 0;
        this.respuestasCorrectas = 0;
        this.respuestasIncorrectas = 0;
        this.respuestaResaltada = false;
        this.temporizadorDetenido = false;
        this.segundoClic = false;
        this.explicacionVisible = false;
        this.historialRespuestas = []; // 🔹 Limpiar historial
        
        clearInterval(this.countdownInterval);
        this.countdownInterval = null;
    }

    iniciarNuevoJuego() {
        this.resetGameState();
        this.shuffleArray(this.preguntas);
        this.mostrarPregunta();
        $("#result").empty().hide();
        $("#nextButton").show();
    }

    mostrarPregunta() {
        if (this.preguntaActual < this.numPreguntasJuego && this.preguntaActual < this.preguntas.length) {
            var pregunta = this.preguntas[this.preguntaActual];
            
            // Mostrar el contexto antes de la pregunta
            $("#contexto").html(`<b>Contexto:</b> ${pregunta.contexto || ''}`).show();
            
            // Mostrar la pregunta
            $("#question").html(`<b>Pregunta ${this.preguntaActual + 1}:</b> ${pregunta.pregunta}`);

            $("#options").empty();
            var opciones = this.shuffleArray(pregunta.opciones.slice());
            var letrasOpciones = ['A)', 'B)', 'C)', 'D)'];

            opciones.forEach((opcion, index) => {
                var id = "opcion" + index;
                var label = $("<label>").attr("for", id).html(`<input type="radio" name="opcion" id="${id}" value="${opcion}">${letrasOpciones[index]} ${opcion}`);
                $("#options").append(label);
            });

            $("#countdown").show();
            this.iniciarContador();
            $("#selectedNumQuestions").text(`${this.numPreguntasJuego}`);
        } else {
            if (this.preguntaActual >= this.numPreguntasJuego) {
                this.mostrarResultado();
            }
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
        // 🔹 GUARDAR RESPUESTA EN EL HISTORIAL
        var pregunta = this.preguntas[this.preguntaActual];
        var respuestaSeleccionada = $("input[name='opcion']:checked").val();
        
        this.historialRespuestas.push({
            texto_pregunta: pregunta.pregunta,
            respuesta_seleccionada: respuestaSeleccionada || "Sin responder",
            respuesta_correcta: pregunta.respuesta,
            es_correcta: (respuestaSeleccionada === pregunta.respuesta),
            tiempo_respuesta_seg: null
        });

        if (this.segundoClic) {
            $("#feedback").empty().hide();
            this.explicacionVisible = false;
            $("#explanation-column").empty().hide();
        }
        
        if (!this.temporizadorDetenido) {
            this.detenerContador();
        }
        
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

    mostrarResultado() {
        $("#question").empty();
        $("#options").empty();
        
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

        $("#nextButton").hide();
        $("#countdown").hide();

        // 🔹 ENVIAR RESULTADOS AL BACKEND
        this.enviarResultados();
    }

    // 🔹 NUEVO: Método para enviar resultados al backend Flask
    enviarResultados() {
        // Obtener IDs desde variables globales inyectadas por Flask
        const examenId = window.DATOS_EXAMEN ? window.DATOS_EXAMEN.id : 1;
        const materiaId = window.DATOS_EXAMEN ? window.DATOS_EXAMEN.materia_id : 1;

        const payload = {
            examen_id: examenId,
            materia_id: materiaId,
            respuestas: this.historialRespuestas
        };

        console.log("📤 Enviando resultados al backend:", payload);

        fetch('/api/examen/guardar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.log("✅ Examen guardado exitosamente:", data);
            } else {
                console.error("❌ Error al guardar:", data.error);
            }
        })
        .catch(error => {
            console.error("❌ Error de red:", error);
        });
    }

    iniciarContador() {
        var tiempoRestante = 30;
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

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
}

const cslTIngenios = new CslTIngenios();
cslTIngenios.init();