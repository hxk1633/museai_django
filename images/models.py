from django.db import models

STATUS_CHOICES = [
    ('t','todo'),
    ('p', 'Processing'),
    ('c', 'Created'),
]

# Create your models here.
class Album(models.Model):
    title = models.TextField()
    file = models.FileField(upload_to='videos/')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='t')

    def getFilePath(self):
        return self.file.path

    def getFileName(self):
        return self.file.name.split("/")[1].split(".")[0]

    def __str__(self):
        return self.title
