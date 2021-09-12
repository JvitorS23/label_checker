from django.contrib import admin
from .models import Project, ObjectDetectionSample
from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model


User = get_user_model()


class ProjectForm(forms.ModelForm):

    samples_file = forms.FileField(required=False,
                                   help_text='Arquivo txt onde cada linha é '
                                             'uma amostra da base de dados. '
                                             'O formato esperado é '
                                             '<url_imagem>,<target>')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        super_users = User.objects.filter(is_superuser=True).all()
        self.fields['owner'].queryset = super_users

    class Meta:
        model = Project
        exclude = []

    def clean(self):
        data = self.cleaned_data
        file = data.pop('samples_file', None)
        if not file:
            return super().clean()

        if file.size == 0:
            raise ValidationError("Arquivo de amostras vazio!")

        try:
            file = data.pop('samples_file')
            file.seek(0)
            lines = file.read().decode("utf-8").split('\n')
            for line in lines:
                image_url, target_str = line.split(',')
        except Exception:
            raise ValidationError("Arquivo de amostras inválido!")

        return super().clean()

    def save(self, commit=True):
        data = self.cleaned_data

        file = data.pop('samples_file', None)
        project = Project(**data)
        project.save()
        project.refresh_from_db()

        if file:
            file = data.pop('samples_file')
            file.seek(0)
            lines = file.read().decode("utf-8").split('\n')
            for line in lines:
                image_url, target_str = line.split(',')
                sample = ObjectDetectionSample()
                sample.project = project
                sample.target = target_str
                sample.image_url = image_url

        return super().save(commit=commit)


@admin.register(Project)
class AuthorAdmin(admin.ModelAdmin):
    form = ProjectForm


admin.site.register(ObjectDetectionSample)
