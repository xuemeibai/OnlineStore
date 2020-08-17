from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from onlinestore.models import *
from django.forms.widgets import FileInput
from django.forms import ModelForm, FileInput
MAX_UPLOAD_SIZE = 2500000


class LoginForm(forms.Form):
	username = forms.CharField(max_length = 20)
	password = forms.CharField(max_length = 200, widget = forms.PasswordInput())

	# Customizes form validation for properties that apply to more
	# than one field.  Overrides the forms.Form.clean function.
	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super().clean()

		# Confirms that the two password fields match
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user:
			raise forms.ValidationError("Invalid username/password")

		# We must return the cleaned data we got from our parent.
		return cleaned_data

class RegistrationForm(forms.Form):
	username   = forms.CharField(max_length = 20)
	password  = forms.CharField(max_length = 200,
								 label='Password',
								 widget = forms.PasswordInput())
	confirm_password  = forms.CharField(max_length = 200,
								 label='Confirm password',
								 widget = forms.PasswordInput())

	email      = forms.CharField(max_length=50,
								 widget = forms.EmailInput())
	first_name = forms.CharField(max_length=20)
	last_name  = forms.CharField(max_length=20)

	# Customizes form validation for properties that apply to more
	# than one field.  Overrides the forms.Form.clean function.
	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super().clean()

		# Confirms that the two password fields match
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		if password and confirm_password and password != confirm_password:
			raise forms.ValidationError("Passwords did not match.")

		# We must return the cleaned data we got from our parent.
		return cleaned_data


	# Customizes form validation for the username field.
	def clean_username(self):
		# Confirms that the username is not already present in the
		# User model database.
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")

		# We must return the cleaned data we got from the cleaned_data
		# dictionary
		return username
class ItemPostForm(forms.ModelForm):

	class Meta:
		model = Item
		fields = ('lat','lng','name','picture','description','price','original_price')

	def __init__(self, *args, **kwargs):
		super(ItemPostForm, self).__init__(*args, **kwargs)
		self.fields['original_price'].required = False	

	def clean_picture(self):
		picture = self.cleaned_data['picture']
		if not picture:
			print('You must upload a picture')
			raise forms.ValidationError('You must upload a picture')
		if not picture.content_type or not picture.content_type.startswith('image'):
			print('File type is not image')
			raise forms.ValidationError('File type is not image')
		if picture.size > MAX_UPLOAD_SIZE:
			print('file too big')
			raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
		return picture
# class ConditionForm(forms.Form):
# 	CONDITION = (
#                 ('Brand New', 'BrandNew'),
#                 ('80% New', '80'),
#                 ('60% New', '60'),
#                 ('40% New', '40'),
#                 ('Old', 'Old'),
#         )
#     condition_value = forms.CharField(max_length=20,widget=forms.widgets.Select(choices=CONDITION))
# class CategoryForm(forms.Form):
# 	TYPE=(
#                 ('Furniture', 'Furniture'),
#                 ('Electronics', 'Electronics'),
#                 ('Others', 'Others'),
#         )
#     type_value = forms.CharField(max_length=20,widget=forms.widgets.Select(choices=TYPE))


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('profile_picture',)

	def clean_picture(self):
		picture = self.cleaned_data['profile_picture']
		if not picture:
			raise forms.ValidationError('You must upload a picture')
		if not picture.content_type or not picture.content_type.startswith('image'):
			raise forms.ValidationError('File type is not image')
		if picture.size > MAX_UPLOAD_SIZE:
			raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
		return picture
