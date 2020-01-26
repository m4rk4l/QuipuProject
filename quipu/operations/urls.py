from django.urls import path
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view

from . import views

app_name = 'operations'

urlpatterns = [
    path('addition/', views.AdditionView.as_view()),
    path('multiplication/', views.MultiplicationView.as_view()),
    path('simple-calculator/', views.SimpleCalculatorView.as_view()),


    path('openapi/', get_schema_view(
        title="Quipu Operations",
        description="API for simple mathematical operations.",
        version="0.0.1"
    ), name='openapi-schema'),

    path('swagger-ui/', TemplateView.as_view(
        template_name='operations/swagger-ui.html',
        extra_context={'schema_url': 'operations:openapi-schema'}
    ), name='swagger-ui'),
]
