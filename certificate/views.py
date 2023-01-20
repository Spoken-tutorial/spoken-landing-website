from django.shortcuts import render
from django.template import RequestContext

from .models import *
from csc.models import CSCTestAtttendance

# Create your views here.
def key_verification(serial):
    context = {}
    try:
        cert_log = Log.objects.get(key=serial)
        print("&&&&&&&&&&&&&&&&&&&&&&&&",cert_log.test_attendance_id)

        certificate = CSCTestAtttendance.objects.get(id=cert_log.test_attendance_id)


        name = certificate.student.user.first_name+ " "+certificate.student.user.last_name
        grade = certificate.mdlgrade
        foss = certificate.test.foss.foss
        tdate = certificate.test.tdate

        detail = {}
        detail['Participant Name'] = name
        detail['Foss'] = foss
        detail['Test Date'] = tdate.strftime('%Y-%m-%d')
        detail['Grade'] = "{:.2f} %".format(grade)
        detail['CSC'] = f"CSC Academy Centre, {certificate.test.vle.csc.state} , CSC ID - {certificate.test.vle.csc.csc_id}"
        
        context['certificate'] = certificate
        context['detail'] = detail
        context['serial_no'] = True
        
    except Log.DoesNotExist:
        context["invalidserial"] = 1
    return context


def verify_test_certificate(request):
	context = {}
	ci = RequestContext(request)
	if request.method == 'POST':
		serial_no = request.POST.get('serial_no').strip()
		context = key_verification(serial_no)
		context['serial_no_val'] = serial_no
        
		return render(request, 'verify_test_certificate.html', context)
	return render(request, 'verify_test_certificate.html', {})

