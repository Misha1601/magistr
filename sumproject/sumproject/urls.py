from django.contrib import admin
from django.urls import path
from sumapp.views import sum_view, result_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sum_view, name='sum'),
    path('result/', result_view, name='result'),
]