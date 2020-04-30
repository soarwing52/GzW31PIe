from django.urls import path

from . import views
from .views import Customer_View, Calculate_Csv
app_name = 'django_cvb'
urlpatterns = [
    path('', Customer_View.as_view(), name='index'),
    path('calculate_csv/',Calculate_Csv.as_view()),
    ]