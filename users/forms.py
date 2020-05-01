from django import forms
from users.models import User


class UserForm(forms.ModelForm):
    phone = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
        )
