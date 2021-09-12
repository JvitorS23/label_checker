from django.urls import path
from core.views import RootView, ProjectDetailView, send_review, invalid_csv
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', RootView.as_view()),
    path('project/<project_id>', login_required(ProjectDetailView.as_view()),
         name='detail'),

    path('project/invalid_csv/<project_id>', login_required(invalid_csv),
         name='invalids_csv'),

    path('project/<project_id>/review/<sample_id>',
         login_required(send_review), name='eval'),
]
