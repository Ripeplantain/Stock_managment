from django import forms
from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'image', 'quantity')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'



class CreateOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'


class UpdateOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('product', 'number', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'