from django import forms

from .models import Student, Student_Foss
GEEKS_CHOICES =(
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
)
class RaiseTestRequestForm(forms.Form):
    foss = forms.ChoiceField(choices=GEEKS_CHOICES)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        student = Student.objects.get(user=user)
        student_foss = Student_Foss.objects.filter(student=student)
        data = [(x.csc_foss.spoken_foss.id,x.csc_foss.spoken_foss) for x in student_foss]
        super(RaiseTestRequestForm,self).__init__(*args, **kwargs)
        self.fields['foss'].choices = data

