from django.forms import Form, ModelForm, Textarea, TextInput
from django import forms

from csc.models import *
from spokenlogin.models import *


class FossForm(forms.Form):
	programme_type = forms.ChoiceField(required=True, choices=PROGRAMME_TYPE_CHOICES)
	spoken_foss = forms.ModelMultipleChoiceField(queryset=FossCategory.objects.filter(available_for_jio=True))

	# class Meta(object):
	# 	model = Vle_csc_foss
	# 	exclude = ['created','updated']

	def __init__(self, *args, **kwargs):
		initial = ''
		if 'instance' in kwargs:
			initial = kwargs["instance"]

		if 'user' in kwargs:
			user = kwargs["user"]
			del kwargs["user"]		


		super(FossForm, self).__init__(*args, **kwargs)

		self.fields['programme_type'].choices = PROGRAMME_TYPE_CHOICES

		if kwargs and 'data' in kwargs:  
			if kwargs['data']['programme_type'] != '':
				programme_type = kwargs['data']['programme_type']

			if programme_type == 'dca':
				fosses = SpokenFoss.objects.filter(csc_dca_programme=True, available_for_jio=True).order_by('foss')
			else:
				fosses = SpokenFoss.objects.filter(csc_dca_programme=False, available_for_jio=True).order_by('foss')

			# self.fields['spoken_foss'].queryset = fosses
			self.fields['spoken_foss'].initial =  kwargs['data']['spoken_foss']


class StudentForm(forms.ModelForm):
	GENDER = (('f','female'),('m','male'))
	fname = forms.CharField(max_length=120,label='First Name')
	lname = forms.CharField(max_length=120,label='Last Name')
	gender = forms.ChoiceField(choices = GENDER)

	class Meta:
		model = Student
		fields = ['gender','dob','phone','edu_qualification','state','city','district','pincode','address']
		labels = {
			'fname' :'First Nameing'
		}


class InvigilatorForm(forms.Form):
	email = forms.EmailField()
	fname = forms.CharField(max_length=120,label='First Name')
	lname = forms.CharField(max_length=120,label='Last Name')
	phone = forms.CharField(max_length=32,label='Contact Number')
	

class InvigilationRequestForm(forms.Form):
	
	test = forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={'disabled':'disabled'}))
	invigilators = forms.ModelMultipleChoiceField(queryset=None)

	def __init__(self, *args, **kwargs):		
		vle_id = kwargs.pop('vle_id')
		test_id = kwargs.pop('test_id')

		
		super(InvigilationRequestForm,self).__init__(*args, **kwargs)
		vle = VLE.objects.get(id=vle_id)
		self.fields['test'].queryset = Test.objects.filter(vle=vle)
		self.fields['test'].initial = test_id
		self.fields['invigilators'].queryset = Invigilator.objects.filter(vle=vle)
		l = InvigilationRequest.objects.filter(test_id=test_id).values('invigilator')
		l = [x['invigilator'] for x in l]
		self.fields['invigilators'].initial = l



