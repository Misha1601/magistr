from django import forms

COUNTRIES = [
    ('usa', 'США'),
    ('russia', 'Россия'),
    ('china', 'Китай'),
    ('germany', 'Германия'),
]

MODELS = [
    ('Bass1', 'Bass111111'),
    ('Bass2', 'Bass2222'),
    ('Bass3', 'Bass3333'),
    ('Logic1', 'Logic1'),
    ('Logic2', 'Logic2'),
    ('Logic3', 'Logic3'),
    ('Gompertz1', 'Gompertz1'),
    ('Gompertz2', 'Gompertz2'),
    ('Gompertz3', 'Gompertz3'),
]

PREDICTIONS = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, 'Other'),
]

class WindForm(forms.Form):
    country = forms.ChoiceField(
        choices=COUNTRIES,
        label="Страна",
        widget=forms.Select
    )
    models = forms.MultipleChoiceField(
        choices=MODELS,
        label="Модели",
        widget=forms.CheckboxSelectMultiple
    )
    prediction = forms.ChoiceField(
        choices=PREDICTIONS,
        label="Предсказание",
        widget=forms.RadioSelect
    )
    custom_prediction = forms.IntegerField(
        min_value=6,
        max_value=50,
        required=False,
        label="Свое значение (6-50)"
    )