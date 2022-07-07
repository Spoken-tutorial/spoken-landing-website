from django.forms import ModelForm, Textarea, TextInput
from django import forms

from csc.models import *
from spokenlogin.models import *


class FossForm(forms.ModelForm):
	programme_type = forms.ChoiceField(required=True)
	spoken_foss = forms.ModelMultipleChoiceField(queryset=SpokenFoss.objects.filter(available_for_jio=True))

	class Meta(object):
		model = Vle_csc_foss
		exclude = ['created','updated']

	def __init__(self, *args, **kwargs):
		print(kwargs,"***")
		programme_type = kwargs.get('programme_type')

		super(FossForm, self).__init__(*args, **kwargs)
		print(programme_type,"@@@@@@@@@@@@@@@@@@")

		self.fields['programme_type'].choices = programme_type

		if kwargs and 'data' in kwargs:  
			if kwargs['data']['programme_type'] != '':
				programme_type = kwargs['data']['programme_type']

			if programme_type == 'dca':
				fosses = SpokenFoss.objects.filter(csc_dca_programme=True, available_for_jio=True).order_by('foss')
			else:
				fosses = SpokenFoss.objects.filter(csc_dca_programme=False, available_for_jio=True).order_by('foss')

			self.fields['spoken_foss'].queryset = fosses
			self.fields['spoken_foss'].initial =  kwargs['data']['spoken_foss']
