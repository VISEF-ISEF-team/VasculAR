from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import utils

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
        img = utils.ImageReader(image_path)
        pdf_canvas.drawImage(img, 10, 450 - 310*i, width=300, height=300)
        
        for j, (header, content) in enumerate(data.items()):
            p1 = Paragraph(f'''{header}<BR/>{content}''', my_Style)
            p1.wrapOn(pdf_canvas, 200, 20)
            p1.drawOn(pdf_canvas, 350, 700 - 100*j)

    pdf_canvas.save()


# Example usage
# package = {
#     'canvas.png':{
#         'text_1': 'Đây là nội dung của phân tích 1 Đây là nội dung của phân tích 1 Đây là nội dung của phân tích 1',
#         'text_2': 'Đây là nội dung của phân tích 2 Đây là nội dung của phân tích 2 Đây là nội dung của phân tích 2',
#         'text_3': 'Đây là nội dung của phân tích 3 Đây là nội dung của phân tích 3 Đây là nội dung của phân tích 3',
#     },
#     'temp.jpg':{
#         'text_1': 'Đây là nội dung của phân tích 1 Đây là nội dung của phân tích 1 Đây là nội dung của phân tích 1',
#         'text_2': 'Đây là nội dung của phân tích 2 Đây là nội dung của phân tích 2 Đây là nội dung của phân tích 2',
#         'text_3': 'Đây là nội dung của phân tích 3 Đây là nội dung của phân tích 3 Đây là nội dung của phân tích 3',
#     },
#     'canvas.png':{
#         'text_1': 'Đây là nội dung của phân tích 1 Đây là nội dung của phân tích 1 Đây là nội dung của phân tích 1',
#         'text_2': 'Đây là nội dung của phân tích 2 Đây là nội dung của phân tích 2 Đây là nội dung của phân tích 2',
#         'text_3': 'Đây là nội dung của phân tích 3 Đây là nội dung của phân tích 3 Đây là nội dung của phân tích 3',
#     },
#     'temp.jpg':{
#         'text_1': 'Đây là nội dung của phân tích 1 Đây là nội dung của phân tích 1 Đây là nội dung của phân tích 1',
#         'text_2': 'Đây là nội dung của phân tích 2 Đây là nội dung của phân tích 2 Đây là nội dung của phân tích 2',
#         'text_3': 'Đây là nội dung của phân tích 3 Đây là nội dung của phân tích 3 Đây là nội dung của phân tích 3',
#     }
# }
# create_pdf(package=package)