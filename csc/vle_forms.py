from django.forms import Form, ModelForm, Textarea, TextInput
from django import forms

from csc.models import *
from spokenlogin.models import *


class FossForm(forms.Form):
	programme_type = forms.ChoiceField(required=True, choices=PROGRAMME_TYPE_CHOICES)
	spoken_foss = forms.ModelMultipleChoiceField(queryset=SpokenFoss.objects.filter(available_for_jio=True))

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
