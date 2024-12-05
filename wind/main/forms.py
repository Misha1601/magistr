from django import forms
from modules.Models_diffusion_innovations import execute_sql_query

# Получаем уникальные регионы и страны
select_all_region_country = f'SELECT DISTINCT "Region", "Country" FROM Wind WHERE "Region" != "-" AND "Country" NOT LIKE "%Total%"'
region = {}
COUNTRIES = execute_sql_query(select_all_region_country)

# COUNTRIES = [
#     ('usa', 'США'),
#     ('russia', 'Россия'),
#     ('china', 'Китай'),
#     ('germany', 'Германия'),
# ]

MODELS = [
    ('Bass1', 'Bass1'),
    ('Bass2', 'Bass2'),
    ('Bass3', 'Bass3'),
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