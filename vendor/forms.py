from django import forms
from .models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('name', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control my-3'