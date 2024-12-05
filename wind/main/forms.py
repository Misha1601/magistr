from django import forms
from modules.Models_diffusion_innovations import execute_sql_query

# Получаем уникальные регионы и страны
select_all_region_country = f'SELECT DISTINCT "Region", "Country" FROM Wind WHERE "Region" != "-" AND "Country" NOT LIKE "%Total%"'
COUNTRIES_DATA = execute_sql_query(select_all_region_country)

# Создаем словарь регионов и стран
REGIONS_COUNTRIES = {}
for region, country in COUNTRIES_DATA:
    if region not in REGIONS_COUNTRIES:
        REGIONS_COUNTRIES[region] = []
    REGIONS_COUNTRIES[region].append(country)

# Создаем список регионов для выбора
REGIONS = [(region, region) for region in REGIONS_COUNTRIES.keys()]
# Создаем полный список стран для начального состояния
ALL_COUNTRIES = [(country, country) for _, country in COUNTRIES_DATA]

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
    region = forms.ChoiceField(
        choices=REGIONS,
        label="Регион",
        widget=forms.Select(attrs={'class': 'region-select'})
    )
    country = forms.ChoiceField(
        choices=ALL_COUNTRIES,
        label="Страна",
        widget=forms.Select(attrs={'class': 'country-select'})
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