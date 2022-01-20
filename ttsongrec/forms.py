from django import forms


class LinkForm(forms.Form):
    link = forms.URLField(max_length=500)

