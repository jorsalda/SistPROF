from datetime import datetime


class ExamenService:
    """
    Servicio para manejar la lógica de negocio de exámenes
    """

    @staticmethod
    def calcular_literal(porcentaje):
        """
        Calcula el literal según la escala de EstudianteJS
        S: 100%
        A: 80-99%
        B: 60-79%
        b: 40-59%
        I: 0-39%
        """
        if porcentaje >= 100:
            return 'S'
        elif porcentaje >= 80:
            return 'A'
        elif porcentaje >= 60:
            return 'B'
        elif porcentaje >= 40:
            return 'b'
        else:
            return 'I'

    @staticmethod
    def calcular_nota_decimal(porcentaje):
        """
        Convierte porcentaje a escala 0.0 - 5.0
        Fórmula: (porcentaje / 20)
        """
        return round(porcentaje / 20, 2)

    @staticmethod
    def validar_respuestas(respuestas):
        """
        Valida y calcula métricas de las respuestas
        Returns: dict con total, correctas, incorrectas, porcentaje
        """
        if not respuestas or len(respuestas) == 0:
            return {
                'total': 0,
                'correctas': 0,
                'incorrectas': 0,
                'porcentaje': 0.0
            }

        total = len(respuestas)
        correctas = sum(1 for r in respuestas if r.get('es_correcta', False))
        incorrectas = total - correctas
        porcentaje = (correctas / total * 100) if total > 0 else 0

        return {
            'total': total,
            'correctas': correctas,
            'incorrectas': incorrectas,
            'porcentaje': round(porcentaje, 2)
        }