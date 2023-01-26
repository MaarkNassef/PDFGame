import fitz

def convert(content):
    pdf_document = fitz.open(stream = content, filetype = 'pdf')
    img_pdf = fitz.open()
    images = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(2,2))
        images.append(pix.tobytes())
        
    for image in images:
        pdf_page = img_pdf.new_page()
        pdf_page.insert_image(pdf_page.rect, stream=image, xref=0)
    return img_pdf