from .models import Student, Student_Foss
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import VLE,Vle_csc_foss,Student_Foss,TestRequest, CSC,StudentTest, Test

@csrf_exempt
def get_foss_from_csc(request):
    student = Student.objects.get(user = request.user)
    
    csc = request.POST['csc']
    vle = VLE.objects.get(csc_id = csc)
    print(csc)
    vle_csc_foss = Vle_csc_foss.objects.filter(vle=vle)
    sf = Student_Foss.objects.filter(student=student,csc_foss__in = vle_csc_foss) 

    # fosses = [(x.csc_foss.spoken_foss.foss,x.csc_foss.spoken_foss.id) for x in sf]
    fosses = [x.csc_foss.spoken_foss for x in sf]
    applied = [x.foss for x in TestRequest.objects.filter(student=student)]
    print(f'fosses : {fosses}')
    print(f'applied : {applied}')
    available_foss = [] 
    for foss in fosses:
        if not foss in applied:
            available_foss.append((foss.foss,foss.id))
    # data = {}
    # for foss in fosses:
    #     data[foss[1]] = fos
    print(f'available_foss : {available_foss}')
    print(fosses)
    return JsonResponse({'fosses' : available_foss}) 
    

@csrf_exempt
def raise_test_request(request):
    student = Student.objects.get(user = request.user)
    csc = request.POST['csc']
    foss = request.POST['foss']
    foss_id = request.POST['foss_id']
    vle = VLE.objects.get(csc_id = csc)
    
    try:
        TestRequest.objects.get(student=student,vle=vle,foss_id=foss_id)
        csc_obj = CSC.objects.get(id=csc)
        msg = f'Test request already submitted for {foss} in csc center - {csc_obj.city} [id: {csc_obj.csc_id}].'

        return JsonResponse({'msg' : msg}) 
    except TestRequest.DoesNotExist:
        TestRequest.objects.create(student=student,vle=vle,foss_id=foss_id,status=0)
        msg = f"Test request raised for {foss} !"
        return JsonResponse({'msg' : msg}) 
@csrf_exempt
def apply_for_test(request):
    context = {}
    test_id = request.POST.get('test_id')
    student = Student.objects.get(user=request.user)

    try:
        StudentTest.objects.create(student=student,test_id=test_id,status=0)
        print("Ceated succesfully ")
        msg = f"appied !"
    except Exception as e:
        msg = f"faied !"
    
    
    return JsonResponse({'msg' : msg}) 

@csrf_exempt
def ajax_mark_attendance(request):
    data = {}
    print(request.POST)
    test_id = request.POST.get('test_id')
    students = request.POST.getlist('students[]')
    st = StudentTest.objects.filter(test_id=test_id,student_id__in=students)
    for item in st:
        item.test_status = 1
        item.save()
    # StudentTest.objects.bulk_update(st,'test_status')
    st = [x.student for x in StudentTest.objects.filter(test_id=test_id)]
    total_enrolled = len(st)
    attending = StudentTest.objects.filter(test_status=1).count()
    pending = total_enrolled - attending
    data['total_enrolled'] = total_enrolled
    data['attending'] = attending
    data['pending'] = pending
    return JsonResponse(data)