class CslTIngenios {
    constructor() {
        this.preguntas = [];
        this.preguntaActual = 0;
        this.respuestasCorrectas = 0;
        this.respuestasIncorrectas = 0;
        this.numPreguntasJuego = 1;
        this.respuestaResaltada = false;
        this.countdownInterval = null;
        this.explicacionVisible = false;
        this.modoRevision = false;
        this.password = "jes1";
        this.intentosRestantes = 3;
    }

    cargarPreguntasDesdeArchivo(file) {
        const reader = new FileReader();

        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);
                this.preguntas = data.preguntas || [];

                this.preguntas.forEach((p) => {
                    p.opcionesOrdenadas = this.shuffleArray(
                        [...p.opciones]
                    );
                });

                $("#loadedQuestionsCount").html(
                    "<b>El archivo tiene:</b> " +
                    this.preguntas.length +
                    " preguntas"
                );

                this.mostrarPregunta();

                $("#loadQuestions").hide();
                $("#fileInput").hide();
                $("#updateQuestions").hide();
                $("#numQuestions").hide();

                $("#nextButton").show();

            } catch (error) {
                console.error(error);
                alert("Error al cargar JSON");
            }
        };

        reader.readAsText(file);
    }

    init() {
        $("#loadQuestions").click(() => {
            const file = $("#fileInput")[0].files[0];

            if (!file) {
                alert("Seleccione un archivo JSON");
                return;
            }

            this.cargarPreguntasDesdeArchivo(file);
        });

        $("#updateQuestions").click(() => {
            this.numPreguntasJuego =
                parseInt($("#numQuestions").val()) || 1;

            $("#selectedNumQuestions").html(
                "<b>Preguntas seleccionadas:</b> " +
                this.numPreguntasJuego
            );
        });

        $("#nextButton").click(() => {
            if (!this.respuestaResaltada) {
                this.detenerContador();
                this.mostrarResultadoRespuesta();
            } else {
                this.avanzarAPreguntaSiguiente();
            }
        });

        $("#explanationButton").click(() => {
            this.mostrarExplicacion();
        });

        $(document).on("click", "#playAgain", () => {
            this.preguntaActual = 0;
            this.modoRevision = true;
            this.respuestaResaltada = false;

            $("#result").hide();
            $("#nextButton").show();

            this.mostrarPregunta();
        });

        $(document).on("click", "#options label", function () {
            $("#options label").removeClass("selected");
            $(this).addClass("selected");
        });
    }

    renderContexto(contexto) {
        if (!contexto) {
            $("#contexto").empty();
            return;
        }

        let html = "";

        if (contexto.tipo === "texto") {
            html += `<p>${contexto.contenido}</p>`;
        }

        if (contexto.tipo === "imagen") {
            html += `<img src="${contexto.src}" class="img-fluid">`;
        }

        if (contexto.tipo === "video") {
            html += `
                <video controls width="100%">
                    <source src="${contexto.src}" type="video/mp4">
                </video>
            `;
        }

        $("#contexto").html(html);
    }

    mostrarPregunta() {
        if (
            this.preguntaActual >= this.numPreguntasJuego ||
            this.preguntaActual >= this.preguntas.length
        ) {
            this.mostrarResultado();
            return;
        }

        const pregunta = this.preguntas[this.preguntaActual];

        this.renderContexto(pregunta.contexto);

        $("#question").html(
            `<b>Pregunta ${this.preguntaActual + 1}:</b> ${pregunta.pregunta}`
        );

        $("#options").empty();

        const letras = ["A)", "B)", "C)", "D)"];

        pregunta.opcionesOrdenadas.forEach((opcion, index) => {
            $("#options").append(`
                <label class="d-block mb-2">
                    <input type="radio" name="opcion" value="${opcion}">
                    ${letras[index]} ${opcion}
                </label>
            `);
        });

        $("#explanationButton").hide();

        if (!this.modoRevision) {
            $("#countdown").show();
            this.iniciarContador();
        }
    }

    mostrarResultadoRespuesta() {
        const pregunta = this.preguntas[this.preguntaActual];

        const seleccion = $("input[name='opcion']:checked").val();

        if (!seleccion) {
            alert("Seleccione una opción");
            return;
        }

        if (seleccion === pregunta.respuesta) {
            this.respuestasCorrectas++;
        } else {
            this.respuestasIncorrectas++;
        }

        this.respuestaResaltada = true;
        $("#explanationButton").show();
    }

    mostrarExplicacion() {
        const pregunta = this.preguntas[this.preguntaActual];

        $("#explanation-column").html(
            `<p>${pregunta.explicacion}</p>`
        );
    }

    avanzarAPreguntaSiguiente() {
        $("#explanation-column").empty();

        this.preguntaActual++;
        this.respuestaResaltada = false;

        this.mostrarPregunta();
    }

    mostrarResultado() {
        $("#question").empty();
        $("#options").empty();

        $("#result")
            .html(`
                <h4>Resultado final</h4>
                <p>Correctas: ${this.respuestasCorrectas}</p>
                <p>Incorrectas: ${this.respuestasIncorrectas}</p>
                <button id="playAgain" class="btn btn-primary">
                    Revisar examen
                </button>
            `)
            .show();

        $("#nextButton").hide();
        $("#countdown").hide();
    }

    iniciarContador() {
        let tiempo = 90;

        $("#countdown").text(
            "Tiempo restante: " + tiempo
        );

        this.countdownInterval = setInterval(() => {
            tiempo--;

            $("#countdown").text(
                "Tiempo restante: " + tiempo
            );

            if (tiempo <= 0) {
                this.detenerContador();
                this.avanzarAPreguntaSiguiente();
            }
        }, 1000);
    }

    detenerContador() {
        clearInterval(this.countdownInterval);
    }

    shuffleArray(array) {
        for (
            let i = array.length - 1;
            i > 0;
            i--
        ) {
            const j = Math.floor(
                Math.random() * (i + 1)
            );

            [array[i], array[j]] =
                [array[j], array[i]];
        }

        return array;
    }
}