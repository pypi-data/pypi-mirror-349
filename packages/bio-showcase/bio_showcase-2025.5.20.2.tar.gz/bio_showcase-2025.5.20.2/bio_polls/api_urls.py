from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.QuestionListAPIView.as_view(), name='question-list-api'),
    path(
        'questions/<int:pk>/',
        views.QuestionDetailAPIView.as_view(),
        name='question-detail-api',
    ),
    path('choices/', views.ChoiceListCreateAPIView.as_view(), name='choice-list-api'),
    path(
        'choices/<int:pk>/',
        views.ChoiceDetailAPIView.as_view(),
        name='choice-detail-api',
    ),
]
