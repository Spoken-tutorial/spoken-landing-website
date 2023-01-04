from django.db.models import Count,Q,F
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from csc.models import CertifiateCategories, Student,Student_Foss,FossCategory, CSC, VLE, CategoryCourses

TEST_VLE_COUNT=int(getattr(settings, "TEST_VLE_COUNT", 2))
TEST_STUDENT_COUNT=int(getattr(settings, "TEST_STUDENT_COUNT", 1))
TEST_VLE_EMAIL=getattr(settings, "TEST_VLE_EMAIL", ['ankitamk@gmail.com','roliimpex@gmail.com'])
TEST_STUDENT_EMAIL=getattr(settings, "TEST_STUDENT_EMAIL", ['kirti3192@gmail.com'])
TEST_CSC_ID=getattr(settings, "TEST_CSC_ID", [1,2])

qs_students = Student.objects.exclude(Q(user__email__in=TEST_STUDENT_EMAIL))
qs_student_foss = Student_Foss.objects.exclude(Q(student__user__email__in=TEST_STUDENT_EMAIL))
qs_csc = CSC.objects.exclude(Q(id__in=TEST_CSC_ID))
qs_vle = VLE.objects.exclude(Q(user__email__in=TEST_VLE_EMAIL))


    

def get_student_gender_stats():
    return qs_students.values('gender').annotate(count=Count('gender')).order_by('-count')


def get_student_category_stats():
    return qs_students.values('category').annotate(count=Count('category')).order_by('-count')

def get_student_occupation_stats():
    return qs_students.values('occupation').annotate(count=Count('occupation')).order_by('-count')

def get_student_certi_stats():
    return qs_student_foss.values('cert_category__code').annotate(count=Count('cert_category'),title=F('cert_category__title')).order_by('-count')

def get_student_state_stats():
    return qs_csc.values('state').annotate(count=Count('state')).order_by('state')

def get_student_foss_stats(start=0,end=len(qs_student_foss),type=''):
    t = FossCategory.objects.filter(available_for_jio=1).order_by('foss')
    indi = CertifiateCategories.objects.get(code='INDI')
    if type:
        q = [x['csc_foss__foss'] for x in qs_student_foss.filter(csc_foss__in=t,cert_category=indi).values('csc_foss__foss').annotate(count=Count('csc_foss__foss')).order_by('-count')]
    else:
        q = [x['csc_foss__foss'] for x in qs_student_foss.filter(csc_foss__in=t).values('csc_foss__foss').annotate(count=Count('csc_foss__foss')).order_by('-count')]
    temp = []
    for x in range(start, end, 1):
        try:
            temp.append(q[x])
        except Exception as e:
            # print(e)
            pass
    if type:
        return qs_student_foss.filter(csc_foss__foss__in=temp,cert_category=indi).values('csc_foss__foss').annotate(count=Count('csc_foss__foss')).order_by('-count')
    else:
        return qs_student_foss.filter(csc_foss__foss__in=temp).values('csc_foss__foss').annotate(count=Count('csc_foss__foss')).order_by('-count')
    
def get_page(resource, page=1, limit=40):
    paginator = Paginator(resource, limit)
    try:
        resource = paginator.page(page)
    except PageNotAnInteger:
        resource = paginator.page(1)
    except EmptyPage:
        resource = paginator.page(paginator.num_pages)
    return resource
    
def get_test_stats():
    f = [x.foss.id for x in CategoryCourses.objects.filter(certificate_category__code='IT07')]
    return FossCategory.objects.filter(id__in=f).annotate(tests=Count('test'))