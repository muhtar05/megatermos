from django import forms
from catalog.models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = (
            'first_name',
            'email',
            'advantages',
            'disadvantages',
        )