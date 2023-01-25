import fitz

def convert_file(path: str):
    pdf_doc = fitz.open(f"temp/upload/{path}.pdf")
    images = []
    for page_num in range(pdf_doc.page_count):
        page = pdf_doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(2,2))
        images.append(pix.tobytes())
        
    output_pdf = fitz.open()

    for image in images:
        pdf_page = output_pdf.new_page()
        pdf_page.insert_image(pdf_page.rect, stream=image, xref=0)

    output_pdf.save(f"temp/download/{path}.pdf")

    return f"temp/download/{path}.pdf"
