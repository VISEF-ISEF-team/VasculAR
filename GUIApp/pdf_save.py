from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib import utils
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_pdf(package, output_pdf="output.pdf"):
    font_path = "C:/Windows/Fonts/Arial.ttf" 
    pdfmetrics.registerFont(TTFont("ArialUnicode", font_path))

    my_Style = ParagraphStyle(
        'My Para style',
        fontName='ArialUnicode',  # Use the registered font
        backColor='#F1F1F1',
        fontSize=9,
        borderColor='#3b3b3b',
        borderWidth=2,
        borderPadding=(5, 5, 5),
        leading=20,
        alignment=0
    )

    pdf_canvas = canvas.Canvas(output_pdf, pagesize=A4)

    for i, (image_path, data) in enumerate(package.items()):
        if image_path == 'number': 
            continue
        if i > 1:
            pdf_canvas.showPage()  # Start a new page after each iteration

        img = utils.ImageReader(image_path)
        pdf_canvas.drawImage(img, 10, 420, width=300, height=300)

        for j, (header, content) in enumerate(data.items()):
            p1 = Paragraph(f'''{header}<BR/>{content}''', my_Style)
            p1.wrapOn(pdf_canvas, 200, 20)
            p1.drawOn(pdf_canvas, 350, 650 - 100*j)

    pdf_canvas.save()


