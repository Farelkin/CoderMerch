from django import forms
from products.models import Product


class NavBarForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(NavBarForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'col-md-8 col-lg-6 admin-product-sort d-md-flex'
