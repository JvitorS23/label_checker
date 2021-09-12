from django.views.generic import TemplateView
from .models import Project, ObjectDetectionSample
import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import csv
from django.db.models import Q
from random import randint


class RootView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.filter(
            is_public=True, is_active=True)
        valid_projects = []
        for project in projects:
            if project.get_all_samples() > 0:
                valid_projects.append(project)
        context['projects'] = valid_projects
        return context


class ProjectDetailView(TemplateView):
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = int(kwargs.get('project_id'))
        project = Project.objects.get(pk=project_id)
        context['project'] = project
        samples = ObjectDetectionSample.objects.filter(
            project=project, is_reviewed=False)
        num_samples = samples.count()
        if num_samples > 0:
            random_index = randint(0, num_samples - 1)
            sample = samples.all()[random_index]
            if sample:
                context['sample'] = sample

        return context


def send_review(request, *args, **kwargs):
    project_id = int(kwargs.get('project_id'))
    sample_id = int(kwargs.get('sample_id'))
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        review = json.loads(body_unicode)

        project = Project.objects.get(pk=project_id)
        sample = ObjectDetectionSample.objects.filter(
                project=project, id=sample_id).first()
        sample.is_reviewed = True
        sample.is_correct = bool(int(review['label_is_correct']))
        sample.is_image_valid = bool(int(review['image_is_valid']))
        if request.user:
            sample.reviewer = request.user
        sample.save()

        if int(project.get_progress()) == 100:
            project.is_public = False
            project.save()
            return JsonResponse({'status': 'completed'})

        return JsonResponse({'status': 'success'})


def invalid_csv(request, *args, **kwargs):
    project_id = int(kwargs.get('project_id'))
    project = Project.objects.get(pk=project_id)

    data_headings = ['title', 'is_correct', 'is_image_valid',
                    'reviewer']
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response[
        'Content-Disposition'] = 'attachment;filename=' +\
                                 f'invalids_project_{project_id}.csv'
    writer = csv.writer(response)
    writer.writerow(data_headings)

    data = ObjectDetectionSample.objects.filter(
            project=project, is_reviewed=True)\
        .filter(Q(is_correct=False) | Q(is_image_valid=False))

    for reg in data:
        writer.writerow(
            [reg.title, reg.is_correct, reg.is_image_valid,
             reg.reviewer])

    return response
