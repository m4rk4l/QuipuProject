from django.urls import path

from . import views

app_name = 'operations'

urlpatterns = [
    path('addition/', views.AdditionView.as_view(), name='addition')
]
