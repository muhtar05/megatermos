from django import forms
from order.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = (
            'region',
            'city',
            'address',
        )