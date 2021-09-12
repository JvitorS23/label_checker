from django.contrib import admin
from .models import Project, ObjectDetectionSample
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class ProjectForm(forms.ModelForm):
    samples_file = forms.FileField(required=False,
                                   help_text='Arquivo txt onde cada linha é '
                                             'uma amostra da base de dados.')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        super_users = User.objects.filter(is_superuser=True).all()
        self.fields['owner'].queryset = super_users

    class Meta:
        model = Project
        exclude = []

    def clean(self):
        data = self.cleaned_data
        file = data.get('samples_file', None)
        if not file:
            return super().clean()

        if file.size == 0:
            raise ValidationError("Arquivo de amostras vazio!")

        try:
            file.seek(0)
            lines = file.read().decode("utf-8").split('\n')
            for line in lines:
                line = line.strip().split(',')
                if len(line) == 3:
                    image_url, title, target_str = line[0], line[1], line[2]
        except:
            raise ValidationError("Arquivo de amostras inválido!")

        return super().clean()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'get_progress', 'is_done',
                    'get_invalid_samples')

    def get_progress(self, obj):
        return f'{obj.get_progress()}%'

    def is_done(self, obj) -> bool:
        return int(obj.get_progress()) == 100

    is_done.boolean = True
    is_done.short_description = 'Done?'
    get_progress.short_description = 'Progress'

    def get_invalid_samples(self, obj):
        url = reverse("invalids_csv", kwargs={'project_id': obj.id})
        return mark_safe(f'<a target="_BLANK" href="{url}">Get invalid Samples</a>')

    get_invalid_samples.short_description = 'Get invalid samples'
    get_invalid_samples.allow_tags = True

    form = ProjectForm

    def save_model(self, request, obj, form, change):
        data = form.cleaned_data
        file = data.pop('samples_file', None)
        project = Project(**data)
        project.save()
        project.refresh_from_db()

        if file:
            file.seek(0)
            lines = file.read().decode("utf-8").split('\n')
            for line in lines:
                line = line.strip().split(',')
                if len(line) == 3:
                    image_url, title, target_str = line[0], line[1], line[2]
                    ObjectDetectionSample.objects.create(
                        project=project, target=target_str,
                        image_url=image_url, title=title, is_correct=False,

                    )


@admin.register(ObjectDetectionSample)
class ObjectDetectionSampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_reviewed', 'is_correct', 'is_image_valid',
                    'reviewer')
    list_filter = ('is_correct', 'is_image_valid', 'project__title')
