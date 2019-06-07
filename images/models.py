from django.db import models

STATUS_CHOICES = [
    ('t','todo'),
    ('p', 'Processing'),
    ('c', 'Created'),
]

CATEGORIES = [
    ("ART","art"),
]

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='videos/')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='t')

    def getFilePath(self):
        return self.file.path

    def getFileName(self):
        return self.file.name.split("/")[1].split(".")[0]

    def __str__(self):
        return self.title

class Album(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, primary_key=True)
    category = models.CharField(max_length = 50, choices=CATEGORIES)

    def __str__(self):
        return self.video.title
