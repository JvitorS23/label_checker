from django.views.generic import TemplateView
from .models import Project


class RootView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(is_public=True,
                                                     is_active=True)
        return context


class ProjectDetailView(TemplateView):
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = int(kwargs.get('project_id'))

        context['project'] = Project.objects.get(pk=project_id)
        return context
