from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('delete_city/<str:city>/', views.DeleteCityView.as_view(), name='delete_city')
]
