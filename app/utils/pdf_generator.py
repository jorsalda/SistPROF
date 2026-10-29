from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io


def generar_pdf_permiso(permiso):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    margen_x = 40
    ancho_util = width - (margen_x * 2)

    # ==========================================
    # 1. ENCABEZADO
    # ==========================================
    y_header_top = height - 40
    alto_header = 60
    y_header_bottom = y_header_top - alto_header

    c.rect(margen_x, y_header_bottom, ancho_util * 0.20, alto_header)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(margen_x + (ancho_util * 0.10), y_header_bottom + 25, "ESCUDO")

    c.rect(margen_x + (ancho_util * 0.20), y_header_bottom, ancho_util * 0.55, alto_header)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(margen_x + (ancho_util * 0.20) + (ancho_util * 0.275), y_header_bottom + 35,
                        "INSTITUCIÓN EDUCATIVA")
    c.drawCentredString(margen_x + (ancho_util * 0.20) + (ancho_util * 0.275), y_header_bottom + 20,
                        "JUAN DE DIOS CARVAJAL")

    c.rect(margen_x + (ancho_util * 0.75), y_header_bottom, ancho_util * 0.25, alto_header)
    c.setFont("Helvetica", 8)
    c.drawString(margen_x + (ancho_util * 0.75) + 5, y_header_bottom + 40, "Código: FD-21")
    c.drawString(margen_x + (ancho_util * 0.75) + 5, y_header_bottom + 25, "Fecha: 13-05-2015")

    # ==========================================
    # 2. TÍTULO PRINCIPAL
    # ==========================================
    y_titulo = y_header_bottom - 30
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, y_titulo, "SOLICITUD DE PERMISO")


    # ==========================================
    # 3. DATOS DEL SOLICITANTE
    # ==========================================
    y_seccion = y_titulo - 30
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margen_x, y_seccion, "1. DATOS DEL SOLICITANTE")

    y_fila = y_seccion - 35
    alto_fila = 35

    # ✅ LÓGICA SIMPLE Y DIRECTA (Para que no falle)
    # 1. Tomamos el nombre tal cual de la BD
    p_nombre = permiso.docente.nombre if permiso.docente.nombre else ""

    # 2. Tomamos el apellido tal cual de la BD. Si está vacío, tomamos la última palabra del nombre
    if permiso.docente.apellido:
        p_apellido = permiso.docente.apellido
    else:
        partes = str(p_nombre).split()
        if len(partes) > 1:
            p_nombre = " ".join(partes[:-1])  # Todo menos la última palabra
            p_apellido = partes[-1]  # La última palabra
        else:
            p_apellido = ""

    # 3. Para el segundo apellido, lo dejamos vacío
    s_apellido = ""

    w_nombres = ancho_util / 4

    def draw_caja_campo(x, y, w, h, etiqueta, valor):
        c.rect(x, y, w, h)
        # Título ARRIBA
        c.setFont("Helvetica", 6)
        c.drawCentredString(x + w / 2, y + h - 10, etiqueta)
        # Dato ABAJO
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + w / 2, y + 8, str(valor))

    # Dibujar las 4 cajas
    draw_caja_campo(margen_x, y_fila, w_nombres, alto_fila, "PRIMER NOMBRE", p_nombre)
    draw_caja_campo(margen_x + w_nombres, y_fila, w_nombres, alto_fila, "PRIMER APELLIDO", p_apellido)
    draw_caja_campo(margen_x + (w_nombres * 2), y_fila, w_nombres, alto_fila, "SEGUNDO APELLIDO", s_apellido)
    draw_caja_campo(margen_x + (w_nombres * 3), y_fila, w_nombres, alto_fila, "C.C. N°",
                    permiso.docente.documento or "")

    y_fila2 = y_fila

    # ==========================================
    # 4. MOTIVO DE LA SOLICITUD
    # ==========================================
    y_motivo = y_fila2 - 40
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margen_x, y_motivo + 5, "2. MOTIVO DE LA SOLICITUD")

    c.rect(margen_x, y_motivo - 20, ancho_util, 20)
    c.setFont("Helvetica", 9)
    c.drawString(margen_x + 5, y_motivo - 13, permiso.observacion or "Sin observación")

    # ==========================================
    # 5. FECHA DEL PERMISO
    # ==========================================
    y_fecha = y_motivo - 45
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margen_x, y_fecha + 5, "3. FECHA DEL PERMISO")

    c.rect(margen_x, y_fecha - 20, ancho_util / 2, 20)
    c.setFont("Helvetica", 9)
    c.drawString(margen_x + 5, y_fecha - 13, "Fecha Inicio:")
    c.drawString(margen_x + 60, y_fecha - 13, permiso.fecha_inicio.strftime("%d/%m/%Y"))

    c.rect(margen_x + (ancho_util / 2), y_fecha - 20, ancho_util / 2, 20)
    c.drawString(margen_x + (ancho_util / 2) + 5, y_fecha - 13, "Fecha Fin:")
    c.drawString(margen_x + (ancho_util / 2) + 55, y_fecha - 13, permiso.fecha_fin.strftime("%d/%m/%Y"))

    # ==========================================
    # 6. DESCRIPCIÓN DE LA RESPUESTA
    # ==========================================
    y_resp = y_fecha - 45
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margen_x, y_resp + 5, "4. DESCRIPCIÓN DE LA RESPUESTA")

    c.rect(margen_x, y_resp - 20, ancho_util, 20)
    c.setFont("Helvetica", 9)
    c.drawString(margen_x + 5, y_resp - 13, "SE CONCEDIÓ:")

    es_aprobado = permiso.estado == 'autorizado'

    c.rect(margen_x + 90, y_resp - 15, 10, 10)
    if es_aprobado:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x + 92, y_resp - 14, "X")
    c.setFont("Helvetica", 9)
    c.drawString(margen_x + 105, y_resp - 13, "SI")

    c.rect(margen_x + 135, y_resp - 15, 10, 10)
    if not es_aprobado:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x + 137, y_resp - 14, "X")
    c.setFont("Helvetica", 9)
    c.drawString(margen_x + 150, y_resp - 13, "NO")

    # ==========================================
    # 7. FIRMAS Y OBSERVACIONES
    # ==========================================
    y_firmas = y_resp - 80

    c.line(margen_x, y_firmas, margen_x + 200, y_firmas)
    c.setFont("Helvetica", 8)
    c.drawCentredString(margen_x + 100, y_firmas - 10, "Firma del Solicitante")

    c.line(width - margen_x - 200, y_firmas, width - margen_x, y_firmas)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width - margen_x - 100, y_firmas - 10, "Firma Rector (A)")

    y_obs = y_firmas - 40
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margen_x, y_obs + 5, "5. OBSERVACIONES")
    c.rect(margen_x, y_obs - 30, ancho_util, 30)
    c.setFont("Helvetica", 8)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


if __name__ == "__main__":
    import sys

    sys.path.insert(0, '.')
    from app import create_app
    from app.models.permiso import Permiso

    app = create_app()
    with app.app_context():
        p = Permiso.query.first()
        if p:
            pdf = generar_pdf_permiso(p)
            with open('prueba_permiso.pdf', 'wb') as f:
                f.write(pdf.getvalue())
            print("✅ PDF generado exitosamente en la raíz del proyecto.")
        else:
            print("❌ No hay permisos en la base de datos.")