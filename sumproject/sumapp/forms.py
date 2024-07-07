from django import forms

class SumForm(forms.Form):
    num1 = forms.FloatField(label='Число 1')
    num2 = forms.FloatField(label='Число 2')
    num3 = forms.FloatField(label='Число 3')
    num4 = forms.FloatField(label='Число 4')