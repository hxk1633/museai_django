from django.db import models
from ffmpy import FFmpeg
import os
import sys
import zipfile

STATUS_CHOICES = [
    ('t','todo'),
    ('p', 'Processing'),
    ('c', 'Created'),
]

CATEGORIES = [
    ("ART","art"),
]

def zip_folder(folder_path, output_path):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    parent_folder = os.path.dirname(folder_path)
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path)
    try:
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '\\',
                                                      '')
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '\\',
                                                      '')
                zip_file.write(absolute_path, relative_path)
    except IOError as message:
        print(message)
        sys.exit(1)
    except OSError as message:
        print(message)
        sys.exit(1)
    except zipfile.BadZipfile as message:
        print(message)
        sys.exit(1)
    finally:
        zip_file.close()

def convertVideo(video):
    os.mkdir('media/albums/' + video.getFileName())
    convert = FFmpeg(inputs={video.getFilePath(): None}, outputs={"media/videos/" + video.getFileName() + ".mp4": None})
    ff = FFmpeg(inputs={"media/videos/" + video.getFileName() + ".mp4": None}, outputs={"media/albums/" + video.getFileName() + "/" + video.getFileName() + "%d.png": ['-vf', 'fps=10']})
    convert.run()
    ff.run()
    zip_folder("media/albums/"+video.getFileName(), "media/albums/"+video.getFileName()+".zip")

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='videos/')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='t')

    def getFilePath(self):
        print(self.file.path)
        return self.file.path

    def getFileName(self):
        return self.file.name.split("/")[1].split(".")[0]

    def getAlbum(self):
        name = getFileName()
        return "media/albums/" + name + ".zip"

    def save(self, *args, **kwargs):
        print("Converting video")
        super(Video, self).save(*args, **kwargs)
        convertVideo(self)
        print("Conversion successful")

    def __str__(self):
        return self.title

class Album(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, primary_key=True)
    category = models.CharField(max_length = 50, choices=CATEGORIES)

    def __str__(self):
        return self.video.title
