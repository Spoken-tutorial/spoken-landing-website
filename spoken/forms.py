from .models import ContactMsg
from django.forms import ModelForm, Textarea, TextInput
from django import forms

class ContactForm(forms.ModelForm):

	class Meta:
		model = ContactMsg
		fields = '__all__'
		widgets={
		'name' : TextInput(attrs={'placeholder':'Your name','cols':40,'rows':20}),
		'email' : TextInput(attrs={'placeholder':'Your Email'}),
		'subject' : TextInput(attrs={'placeholder':'Subject'}),
		'message' : TextInput(attrs={'placeholder':'Message'}),
		}
		labels ={
		'name' :'',
		'email':'',
		'subject':'',
		'message':'',
		}