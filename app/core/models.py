from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now


class Project(models.Model):
    header_image_url = models.URLField(default='https://neurohive.io/wp-content/uploads/2019/01/dd-e1547642312239.jpg')
    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateField(default=now())


class Sample(models.Model):
    is_reviewed = models.BooleanField(default=False)
    reviewer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ObjectDetectionSample(Sample):
    is_correct = models.BooleanField()
    target = models.CharField(max_length=255)
    image_url = models.URLField()
