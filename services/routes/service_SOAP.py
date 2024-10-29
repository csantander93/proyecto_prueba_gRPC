from fpdf import FPDF

def generar_pdf_catalogo(catalogo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Catálogo: {catalogo.titulo}", ln=True, align="C")
    for producto in catalogo.productos:
        pdf.cell(200, 10, txt=f"Producto: {producto.nombre}, Color: {producto.color}, Talle: {producto.talle}", ln=True)
    # Guardar PDF temporal y devolver a servicio SOAP
    pdf_path = f"/tmp/catalogo_{catalogo.id_catalogo}.pdf"
    pdf.output(pdf_path)
    return pdf_path
