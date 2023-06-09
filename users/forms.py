from django.contrib.auth.forms import UserCreationForm
from django import forms
# from django.contrib.auth.models import User
from .models import CustomUser as User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'