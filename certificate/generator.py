from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import cm
from PyPDF2 import PdfReader, PdfWriter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.conf import settings
from django.http import HttpResponse
import os
import subprocess

from string import Template

def generate(**kwargs):
    test_date = kwargs['test_date']
    certificate_pass =  kwargs['certificate_pass']
    student = kwargs['tstudent']
    foss = kwargs['foss']
    score = kwargs['score']
    institute = kwargs['institute']
    certificate_path = "/beta_st/beta_spoken-tutorial_in/spoken-landing-website/certificates/"   
    file_name = '{0}'.format(certificate_pass)
    _type = 'P'
        
    error = False
    err = None
    try:
        download_file_name = 'certificate.pdf'
        template = 'template'
        template_file = open('{0}{1}'.format(certificate_path, template), 'r')
        content = Template(template_file.read())
        template_file.close()

        content_tex = content.safe_substitute(name=student.title(),
                cpass=certificate_pass, institute=institute, date=test_date, grade=score, foss=foss)
        create_tex = open('{0}{1}.tex'.format(certificate_path, file_name), 'w')
        create_tex.write(content_tex)
        create_tex.close()
        return_value, err = _make_certificate_certificate(certificate_path,
                _type, file_name)
        if return_value == 0:
            pdf = open('{0}{1}.pdf'.format(certificate_path, file_name) , 'rb')
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; \
                    filename=%s' % (download_file_name)
            response.write(pdf.read())
            _clean_certificate_certificate(certificate_path, file_name)
            return [response, False]
        else:
            error = True
    except Exception as e:
        error = True
        print(e)
        err = e
    return [err, error] 
            

def _make_certificate_certificate(path, type, file_name):
    command = 'participant_cert'
    if type == 'P':
        command = 'participant_cert'
    elif type == 'A':
        command = 'paper_cert'
    elif type == 'W':
        command = 'workshop_cert'
    elif type == 'T':
        command = 'workshop_cert'
    process = subprocess.Popen('timeout 15 make -C {0} {1} file_name={2}'.format(path, command, file_name),
                               stderr=subprocess.PIPE, shell=True)
    err = process.communicate()[1]
    return process.returncode, err


def _clean_certificate_certificate(path, file_name):
    clean_process = subprocess.Popen('make -C {0} clean file_name={1}'.format(path, file_name),
                                     shell=True)
    clean_process.wait()
