from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload'),
    path('forecast/<int:file_id>/', views.forecast_view, name='forecast'),
]

