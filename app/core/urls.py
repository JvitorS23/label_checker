from django.urls import path
from core.views import RootView, ProjectDetailView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', RootView.as_view()),
    path('project/<project_id>', login_required(ProjectDetailView.as_view()),
         name='detail'),
]
