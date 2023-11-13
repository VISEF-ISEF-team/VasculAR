from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import utils


def create_pdf(package, output_pdf="output.pdf", font_path="C:/Windows/Fonts/Times.ttf"):
    # Register custom font
    pdfmetrics.registerFont(TTFont("CustomFont", font_path))

    # Create a PDF document
    width, height = letter
    pdf_canvas = canvas.Canvas(output_pdf, pagesize=letter)
    pdf_canvas.setFont("CustomFont", 12)

    # Add images to the PDF
    for i, (image_path, data) in enumerate(package.items()): 
        img = utils.ImageReader(image_path)
        pdf_canvas.drawImage(img, 10, 450 - 310*i, width=300, height=300)
        
        for j, (header, content) in enumerate(data.items()):
            pdf_canvas.drawString(350, 720 - 100*j, header)
            pdf_canvas.drawString(350, 700 - 100*j, content)
            
        print(data)
        
    pdf_canvas.save()

# Example usage
package = {
    'canvas.png':{
        'text_1': 'Đây là nội dung của phân tích 1',
        'text_2': 'Đây là nội dung của phân tích 2',
        'text_3': 'Đây là nội dung của phân tích 3',
    },
    'temp.jpg':{
        'text_1': 'Đây là nội dung của phân tích 1',
        'text_2': 'Đây là nội dung của phân tích 2',
        'text_3': 'Đây là nội dung của phân tích 3',
    },
    'canvas.png':{
        'text_1': 'Đây là nội dung của phân tích 1',
        'text_2': 'Đây là nội dung của phân tích 2',
        'text_3': 'Đây là nội dung của phân tích 3',
    },
    'temp.jpg':{
        'text_1': 'Đây là nội dung của phân tích 1',
        'text_2': 'Đây là nội dung của phân tích 2',
        'text_3': 'Đây là nội dung của phân tích 3',
    }
}
create_pdf(package=package)
