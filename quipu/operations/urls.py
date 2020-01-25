from django.urls import path

from . import views

app_name = 'operations'

urlpatterns = [
    path('addition/', views.OperationView.as_view(operation_type="addition")),
    path('multiplication/', views.OperationView.as_view(operation_type="multiplication"))
]
