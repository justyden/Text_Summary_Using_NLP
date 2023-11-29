from django import forms

class TextInputForm(forms.Form):
    form_name = "Insert the text here"
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

