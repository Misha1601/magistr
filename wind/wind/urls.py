from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('process/', views.process_form, name='process_form'),
    path('plots/', views.plot_view, name='plot_view'),
    path('export_excel/', views.export_excel, name='export_excel'),
]