import PyPDF2
import docx
import os


def extraer_texto_de_archivo(archivo, tipo_archivo):
    """
    Extrae texto de un archivo PDF o DOCX subido.
    Limpia caracteres inválidos que puedan causar errores de codificación.

    :param archivo: Objeto FileStorage de Flask (request.files['archivo'])
    :param tipo_archivo: Extensión del archivo ('pdf' o 'docx')
    :return: String con el texto extraído y limpio, o None si hay error.
    """
    try:
        if tipo_archivo == 'pdf':
            # Leer PDF
            lector = PyPDF2.PdfReader(archivo)
            texto = ""
            for pagina in lector.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto += texto_pagina + "\n"

            # Limpiar caracteres inválidos
            texto_limpio = limpiar_texto(texto)
            return texto_limpio.strip()

        elif tipo_archivo == 'docx':
            # Leer Word
            doc = docx.Document(archivo)
            texto = "\n".join([parrafo.text for parrafo in doc.paragraphs])

            # Limpiar caracteres inválidos
            texto_limpio = limpiar_texto(texto)
            return texto_limpio.strip()

        else:
            return None

    except Exception as e:
        print(f"Error al extraer texto del documento: {str(e)}")
        return None


def limpiar_texto(texto):
    """
    Elimina caracteres inválidos de UTF-8 (surrogates) que causan errores.
    """
    if not texto:
        return ""

    # Método 1: Codificar y decodificar ignorando errores
    try:
        # Esto elimina automáticamente caracteres inválidos
        texto_limpio = texto.encode('utf-8', errors='ignore').decode('utf-8')
        return texto_limpio
    except:
        pass

    # Método 2: Reemplazar manualmente caracteres surrogate
    try:
        texto_limpio = ""
        for char in texto:
            # Los surrogate pairs están en el rango U+D800 a U+DFFF
            if 0xD800 <= ord(char) <= 0xDFFF:
                continue  # Saltar este caracter
            texto_limpio += char
        return texto_limpio
    except:
        # Si todo falla, devolver string vacío
        return ""