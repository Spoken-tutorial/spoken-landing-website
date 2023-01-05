from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import cm
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

import os


def generate(**kwargs):
       test_date = kwargs['test_date']
       certificate_pass =  kwargs['certificate_pass']

       student = kwargs['tstudent']
       foss = kwargs['foss']
       institute = kwargs['institute']
       bg_file ="cert-comp.pdf" 
 
       imgTemp = BytesIO()
       imgDoc = canvas.Canvas(imgTemp)

       imgDoc.setFont('Helvetica', 16, leading=None)
       imgDoc.drawCentredString(180, 155, test_date)

       imgDoc.setFillColorRGB(0, 0, 0)
       imgDoc.setFont('Helvetica', 12, leading=None)
       imgDoc.drawString(207, 127, certificate_pass)


       centered = ParagraphStyle(name = 'centered',
          fontSize = 15,
          leading = 24,
          alignment = 0,
          spaceAfter = 20)

       text = "This certificate is awarded to <br/> " + student + "<br /> from <br />" + institute + "<br /> for successfully completing <b>"+ foss + "</b> <br /> "
       centered = ParagraphStyle(name = 'centered',
          fontSize = 21,
          leading = 25,
          alignment = 1,
          spaceAfter = 15)

       p = Paragraph(text, centered)
       p.wrapOn(imgDoc, 500, 100)
       p.drawOn(imgDoc, 6 * cm, 13 * cm)


       data = [['Score'], [], ['89%'], []]
       t=Table(data)
       t.setStyle(TableStyle([('BACKGROUND',(0,0),(3,3),colors.lightgrey),
           ('FONTSIZE', (0,0), (3,3), 22), ]))

       t.wrapOn(imgDoc, 500, 200)
       t.drawOn(imgDoc, 13 * cm, 10 * cm)


       imgDoc.save()

       page = PdfFileReader(open("cert-comp.pdf", "rb")).getPage(0)
       overlay = PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0)
       page.mergePage(overlay)

       output = PdfFileWriter()
       output.addPage(page)

       if not os.path.exists('./certificates'):
           os.makedirs('./certificates')
       pdf_out = open(bg_file, 'wb')
       output.write(pdf_out)
       pdf_out.close()

       return output
