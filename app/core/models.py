from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now


class Project(models.Model):
    header_image_url = models.CharField(max_length=355,
                                        default='https://neurohive.io/wp-content/uploads/2019/01/dd-e1547642312239.jpg')
    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateField(default=now())

    def get_samples_done(self):
        return ObjectDetectionSample.objects.filter(
            project=self, is_reviewed=True).count()

    def get_all_samples(self):
        return ObjectDetectionSample.objects.filter(
            project=self).count()

    def get_progress(self):
        all_samples = self.get_all_samples()
        if all_samples == 0:
            return '0'
        samples_done = self.get_samples_done()
        return str(int(samples_done*100/all_samples))


class Sample(models.Model):
    is_reviewed = models.BooleanField(default=False)
    reviewer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True


class ObjectDetectionSample(Sample):
    is_correct = models.BooleanField(default=False)
    is_image_valid = models.BooleanField(default=True)
    target = models.CharField(max_length=255)
    image_url = models.CharField(max_length=355)
